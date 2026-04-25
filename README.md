# Sebastian's Weather Tracker 

    A Python application that fetches real-time weather data and stores it in a database.  Built for [CSIS 1230 - Programming for Everyone II].

## Features 
    - Fetches real-time weather data from the Open-Meteo API
    - Stores weather observations in a PostgreSQL database
    - Displays all weather obsevations in a table 
    - View detailed weather info for individual cities
    - Add new cities via the Open-Meteo API
    - Manually edit existing weather records
    - Delete weather records
    - Enviorment variables used to securely store databse credentials 

## Technologies used 
    - Python
    - Flask 
    - PostgreSQL
    - psycopg2
    - Open-Meteo API
    - python-dotenv
    - Jinja2

## Installation 
1. Clone this repository: 
    ```bash 
    git clone https://github.com/yourusername/local_weather_tracker_CSIS-1230_finalProject.git
    cd local_weather_tracker_CSIS-1230_finalProject
    ```

2. Install dependencies: 
    pip install -r requirements.txt

3. Create a `.env` file in the project root with your database credentials: 

    DB_NAME = your_databse_name
    DB_USER = your_postgres_username
    DB_PASSWORD = your_password
    DB_HOST = localhost
    DB_PORT = 5432

4. Set up your PostgreSQL databse and create the obsevations table: 
    ```sql 
        CREATE TABLE observations ( 
            id serial PRIMARY KEY, 
            city VARCHAR(50) NOT NULL, 
            country VARCHAR(50) NOT NULL,
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            temperature NUMERIC(5, 2),
            elevation NUMERIC(8, 2),
            windspeed NUMERIC(6, 2),
            observation_time TIMESTAMP DEFAULT NOW()
        );
    ```

5. Run the application: 
    ```bash
        python main.py
    ```

6. Open your browser and navigate to: 
    https://localhost:8080

## Usage
    - **Home page** - click "View Weather observations" to see the table 
    - **Add a city** - click "Add City" and enter a city name and country code (e.g. US, GB, JP) 
    - **Edit a record** - click "Edit" on any row to manually update values
    - **Delete a record** - click "Delete" on any row to remove it 
    - **View Details** - click any city name to see its full weather report 






