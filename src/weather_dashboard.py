import os
import json
import boto3
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto3.client('s3')

    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logging.info(f"Bucket {self.bucket_name} already exists.")
        except self.s3_client.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                logging.info(f"Bucket {self.bucket_name} not found. Creating bucket...")
                try:
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                    logging.info(f"Successfully created bucket {self.bucket_name}.")
                except Exception as e:
                    logging.error(f"Error creating bucket: {e}")
                    raise
            else:
                logging.error(f"Error checking bucket: {e}")
                raise

    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            logging.info(f"Successfully fetched weather data for {city}.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching weather data for {city}: {e}")
            return None

    def format_weather_data(self, weather_data, city):
        """Format weather data into plain text."""
        try:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            formatted_data = (
                f"Weather Report for {city}\n"
                f"--------------------------------\n"
                f"Timestamp: {timestamp}\n"
                f"Temperature: {temp}°F\n"
                f"Feels Like: {feels_like}°F\n"
                f"Humidity: {humidity}%\n"
                f"Conditions: {description.capitalize()}\n"
            )
            return formatted_data
        except KeyError as e:
            logging.error(f"Error formatting weather data: Missing key {e}")
            return None        

    def save_to_s3(self, weather_data, city):
        """Save formatted weather data to S3 bucket as a plain text file."""
        if not weather_data:
            return False

        formatted_data = self.format_weather_data(weather_data, city)
        if not formatted_data:
            logging.error(f"Could not format weather data for {city}.")
            return False

        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.txt"

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=formatted_data,
                ContentType='text/plain'
            )
            logging.info(f"Successfully saved data for {city} to S3 as plain text.")
            return True
        except Exception as e:
            logging.error(f"Error saving to S3: {e}")
            return False

def main():
    dashboard = WeatherDashboard()

    # Create bucket if needed
    try:
        dashboard.create_bucket_if_not_exists()
    except Exception as e:
        logging.error("Failed to initialize S3 bucket. Exiting...")
        return

    # Get cities dynamically from user input
    cities_input = input("Enter city names (comma-separated): ").strip()
    cities = [city.strip() for city in cities_input.split(",") if city.strip()]

    if not cities:
        logging.warning("No cities provided. Exiting...")
        return

    for city in cities:
        logging.info(f"\nFetching weather for {city}...")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']

            # Save to S3
            success = dashboard.save_to_s3(weather_data, city)
            if success:
                logging.info(f"Weather data for {city} successfully saved to S3.")
            else:
                logging.error(f"Failed to save weather data for {city} to S3.")
        else:
            logging.error(f"Failed to fetch weather data for {city}.")

if __name__ == "__main__":
    main()
