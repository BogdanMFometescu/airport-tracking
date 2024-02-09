# airport-tracking


## Description

Airport Tracking  is a Dash-FastAPI based web application which allows users to check different airports information.
It features various sections like Airplanes, Airports and Schedules along with graphs and a map.
Requests for information are made to an external API using airlabs API. 
## Installation


### Prerequisites

- Python 3.12
- Poetry for Python dependency management
- Postgres database
- Virtual environment (optional but recommended)
- AIRLAB API KEY (which is has a free tier with 1000 request / month) :https://airlabs.co/

### Steps

1. Clone the repository or download the source code.
2. (Optional) Create a virtual environment:

  ```bash
    python -m venv venv
    venv\Scripts\activate
  ```

3.Install dependencies using Poetry:

  ```bash
    poetry install
  ```

4.Set up your environment variables in the .env file ,
including the Postgres database settings.

- DB_NAME
- DB_USERNAME
- DB_PASSWORD
- DB_HOST (this is set to 'db' in docker-compose file)
- DB_PORT
- AIRLAB_API_KEY

5.Create fastapi image from Dockerfile:

  ```bash
   docker build -t fastapi02 .
   ```

6.Create dash image from Dockerfile:

  ```bash
  docker build -f dashboard/Dockerfile -t dash02 .
  ```  
7.Start the app :
```bash
 docker compose up --build

```

### Usage

After installation, access the web application at http://localhost:8050.
Each user search for an airport or schedule are auto-saved in the database based on the specific API call.


### Features

- Search for airports based on standard IATA_CODES
- Search for airports schedules 
- Visualize graphs for airports, schedules and airplanes 
- Visualize airports locations on a map 


### Technologies 

- Dash 
- FastAPI
- SQLAlchemy
- Postgres as the database backend
- Poetry for dependency management


### Contributing

Contributions to airport-tracking are welcome. 
Please follow the coding standards and contribute to tests for new features.

### Licence

This project is licensed under the MIT License - see the LICENSE file for details.