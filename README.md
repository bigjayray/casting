# CASTING API Backend

This is a backend system to simplify and steamline the process of creating movies, managing and assigning actors to those movies for a casting agency.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, create a database in terminal run:

```bash
createdb casting --o postgres
```

## Running the server

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Testing

To run the tests, run

```bash
createdb casting_test
python test_flaskr.py
```

Test endpoints with [Postman](https://getpostman.com):

- I have created collection with bearer tokens for different roles generated using auth0
- Import the postman collection `udacity-capstone-casting.postman_collection.json`
- Run the collection.

# API Reference

## Getting Started

- Base URL: The backend app is hosted at the default <http://localhost:5000/>, which is set as a proxy in the front configuration.
- Authentication: This version of the application does not require authentication or API keys.

## Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "error": 405,
    "message": "method not allowed",
    "success": false
}
```

The API will return five error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processible
- 500: Internal Server Error

## Endpoints

### GET /casting/movies

- General:
  - Returns a list of movie objects and success value
- Sample: `curl http://localhost:5000/casting/movies`

```json
{
  "movies": [
    {
      "id": 2,
      "release_date": "Tue, 14 Jul 2020 00:00:00 GMT",
      "title": "End of the wicked"
    }
  ],
  "success": true
}
```

### GET /casting/actors

- General:
  - Returns a list of actor objects and success value
- Sample: `curl http://localhost:5000/casting/actors`

```json
{
  "actors": [
    {
      "age": 14,
      "gender": "Male",
      "id": 3,
      "name": "John Doe"
    }
  ],
  "success": true
}
```

### POST /casting/movies

- General:
  - Creates a new movie using the submitted movie. Raturns the id of the created movie, success value and movie object.

  - Sample: `curl http://127.0.0.1:5000/casting/movies -X POST -H "Content-Type: application/json" -d '{"title":"End of the wicked", "release_date":"2020-07-14"}'`

 ```json
{
  "movie": {
    "id": 2,
    "release_date": "Tue, 14 Jul 2020 00:00:00 GMT",
    "title": "End of the wicked"
  },
  "success": true
}
```

### POST /casting/actors

- General:
  - Creates a new actor using the submitted actor. Raturns the id of the created actor, success value and actor object.

  - Sample: `curl http://127.0.0.1:5000/casting/actors -X POST -H "Content-Type: application/json" -d '{"name":"John Doe", "age":"14", "gender": "Male"}'`

 ```json
{
  "actor": {
    "age": 14,
    "gender": "Male",
    "id": 3,
    "name": "John Doe"
  },
  "success": true
}
```

### PATCH /casting/movies

- General:
  - Updates existing movie using the submitted movie. Raturns the id of the updated movie, success value and movie object.

  - Sample: `curl http://127.0.0.1:5000/casting/movies -X PATCH -H "Content-Type: application/json" -d '{"title":"I'll go anywhere with you", "release_date":"2020-07-15"}'`

 ```json
{
  "movie": {
    "id": 2,
    "release_date": "Wed, 15 Jul 2020 00:00:00 GMT",
    "title": "I'll go anywhere with you"
  },
  "success": true
}
```

### PATCH /casting/actors

- General:
  - Updates existing actor using the submitted actor. Raturns the id of the updated actor, success value and movie object.

  - Sample: `curl http://127.0.0.1:5000/casting/actors -X PATCH -H "Content-Type: application/json" -d '{"name":"Jane Doe", "age":"24", "Female"}'`

 ```json
{
  "actor": {
    "age": 24,
    "gender": "Female",
    "id": 3,
    "name": "Jane Doe"
  },
  "success": true
}
```

### DELETE /casting/movies/{movie_id}

- General:
  - Deletes the question object of the given ID if it exists. Returns the id of the deleted question and success value.
- Sample: `curl -X DELETE http://127.0.0.1:5000/casting/movies/2`

```json
{
  "deleted": 2,
  "success": true
}
```

### DELETE /casting/actors/{actor_id}

- General:
  - Deletes the question object of the given ID if it exists. Returns the id of the deleted question and success value.
- Sample: `curl -X DELETE http://127.0.0.1:5000/casting/actors/3`

```json
{
  "deleted": 3,
  "success": true
}
```
