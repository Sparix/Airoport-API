# Airport-API

The Airport API service, built on Django REST, is specifically crafted to 
monitor flights originating from airports globally. Providing comprehensive 
details on airports, planes, flights, routes, and beyond, this API functions 
as a powerful tool for effectively managing and analyzing data associated 
with air travel.


## Installing using GitHub

Before you begin, ensure you have met the following requirements:
 - Install PostgresSQL and create db
 - Python3 must be already installed. 

## Run the project locally without Docker

## Installed

1. Clone the repository:
```shell
git clone https://github.com/Sparix/Airport-API
```
2. Go to the project directory:
```shell
cd Airport_API
```
3. Create a virtual Python engine and activate it:
```shell
python -m venv venv 
source venv/bin/activate(on macOS)
venv\Scripts\activate(on Windows)
```
4. Set the project assignments:
```shell
pip install -r requirements.txt
```
## Configuration Environment Variables:
  - Create a file named .env, using .env.sample as an example.
  - Make sure you have replaced all the dummy keys with your actual data.

```shell
set SECRET_KEY=< secret_key >
set POSTGRES_HOST=< db_host_name >
set POSTGRES_DB=< db_name >
set POSTGRES_USER=< db_username >
set POSTGRES_PASSWORD=< password_db >
```

## Starting the server
1. Create database migrations:
```shell
python maange.py makemigrations
python manage.py migrate
```

2. Load data to db:
```shell
python manage.py loaddata data_base.json
```

3. Start the development server:
```shell
python manage.py runserver
```

The API should now be accessible at http://localhost:8000/

## RUN with Docker

Docker should bу installed

```shell
docker-compose build
```
```shell
docker-compose up
```

# Getting access
 - create user api/user/register/
 - get access token api/user/token/

 - To authenticate, include the obtained token in your request headers with the format:
```shell
 - Authorization: Bearer <your-token>
```

## API Documentation

- The API is documented using the OpenAPI standard.
- Access the API documentation by running the server and navigating to http://localhost:8000/api/doc/swagger/
  or http://localhost:8000/api/doc/redoc/.

## Features of the project:

- **Information Restriction**:
Communication between administrators and regular users is limited, ensuring users access only entitled information.

- **Airport Details**:
Retrieve comprehensive data on global airports, including names, airport codes, and proximity to major cities and countries.

- **Route Insights**:
Access details about different routes, encompassing departure and destination airport names along with the distance between them.

- **Airplane Details**:
Retrieve information about airplane, such as their names, types, passenger row counts, and seat numbers per row.
The system includes a built-in function for downloading and storing airplane images.

- **Flight Overview**:
Obtain detailed flight information, including route specifics, departure and arrival times, aircraft details, and seat availability.
Filter the flight list by departure and arrival dates for added convenience.

- **Order Status**:
Authenticated users can review their order information.

- **Ticket Details**:
Facilitates the addition of flight tickets, allowing users to specify row and seat numbers for the order.

- **Authentication Mechanism**:
Users can create profiles by providing an email address and password.
The API employs JWT (JSON Web Tokens) authentication to safeguard sensitive flight data.