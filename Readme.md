# **Weather Dashboard with S3 Integration**

## **Overview**
This Python-based Weather Dashboard fetches weather data for multiple cities using the OpenWeatherMap API and stores the weather reports in an AWS S3 bucket. The weather reports are saved in plain text format and include temperature, humidity, weather conditions, and timestamps for easy access.

## **Features**
- Fetch weather data for multiple cities dynamically entered by the user.
- Save weather reports to AWS S3 in plain text format.
- Automatic creation of the S3 bucket if it doesn’t exist.
- Clear and readable weather reports for each city.
- Error handling for API requests and S3 operations.

## **Requirements**
### **Python Packages**
- `boto3` - For AWS S3 integration.
- `requests` - For making HTTP requests to the OpenWeatherMap API.
- `python-dotenv` - For securely managing API keys and environment variables.


# **Setup Instructions**

#### 1. Clone the Repository:
```bash
git clone https://github.com/your-repository/weather-dashboard.git

cd weather-dashboard
```
#### 2. Create a `.env` File: Add your API keys and bucket name to the `.env` file:
```bash
OPENWEATHER_API_KEY=your_openweather_api_key
AWS_BUCKET_NAME=your_s3_bucket_name
```
### 3. Install required Python packages:
```bash
run: pip install -r requirements.txt
```
### 4. Run the Script:
```bash
python src\weather_dashboard.py
```
### File Structure
```bash

weather-dashboard/

├── assests
    ├── images
          ├── Output.png
├── Data
├── src
    ├── init.py     
    ├── weather_dashboard.py  # Main script
├── .env                  # Environment variables
├── .gitignore            # To ignore the files unnecessary to project
├── requirements.txt      # Package dependencies
├── README.md             # Project documentation

```


## Configuration
1. Set up your AWS credentials and configure your S3 bucket.
2. Obtain an API key from OpenWeatherMap and set it in your environment variables.

# **Output**
![Result](https://github.com/rshammad/weather-dashboard/blob/master/assets/images/Output.png?raw=true)

## Acknowledgements
- [OpenWeatherMap](https://openweathermap.org/) for providing the weather data API.
