# Airport API
Api service for airport work and management written on DRF 
## Installing using GitHub 
```
1. git clone https://github.com/xborismenx/airport_service.git
2. cd airport_service
3. python -m venv .venv
4. source .venv/bin/activate
5. pip install -r requirements.txt
6. set all variables in env.sample for work with postgres 
7. python manage.py migrate
8. python manage.py runserver
```
## Run with Docker
1. Docker should be installed
2. create a .env file based on .env.sample and fill it with the necessary data to connect to the database.
3. docker-compose build
4. docker-compose up
## Getting access
create user via user/register/

recieve access token via api/token/

# Features
- JWT Authenticated
- Admin panel /admin/
- Documentation is located at /api/schema/swagger-ui/
- adding permissions for staff, common and admin users
- Managing Order and Tickets
- Adding Airplanes and his types
- Creating Crew for airplane
