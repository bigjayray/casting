import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors
from authy import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  cors = CORS(app, resources={r"/casting/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        
    return response
  
  # ROUTES
  
  # Home
  @app.route('/')
  def home():
    return jsonify('Welcome')
  
  # GET /casting/movies
  
  @app.route('/casting/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    try:
      selection = Movies.query.order_by(Movies.id).all()
      movies = [movie.format() for movie in selection]
      
      return jsonify({
        'success': True,
        'movies': movies
        })

    except Exception as e:
      print(e)
      abort(404)

  # GET /casting/actors
  
  @app.route('/casting/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
    try:
      selection = Actors.query.order_by(Actors.id).all()
      actors = [actor.format() for actor in selection]
      
      return jsonify({
        'success': True,
        'actors': actors
        })

    except Exception as e:
      print(e)
      abort(404)
  
  # POST /casting/movies
  
  @app.route('/casting/movies', methods=['POST'])
  @requires_auth('post:movies')
  def new_movie(payload):
    body = request.get_json()
    
    # if no form data
    if body is None:
      abort(404)
      
    title = body.get('title', None)
    release_date = body.get('release_date', None)
    
    try:
      movie = Movies(title=title, release_date=release_date)
      movie.insert()
      
      return jsonify({
        'success': True,
        'movie': movie.format(),
        }), 200
      
    except Exception as e:
      print(e)
      abort(422)


  # POST /casting/actors
  
  @app.route('/casting/actors', methods=['POST'])
  @requires_auth('post:actors')
  def new_actor(payload):
    body = request.get_json()
    
    # if no form data
    if body is None:
      abort(404)
      
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    
    try:
      actor = Actors(name=name, age=age, gender=gender)
      actor.insert()
      
      return jsonify({
        'success': True,
        'actor': actor.format(),
        }), 200
      
    except Exception as e:
      print(e)
      abort(422)

  # DELETE /casting/movies/<int:movie_id>

  @app.route('/casting/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
    try:
      movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

      if movie is None:
        abort(404)
            
      movie.delete()

      return jsonify({
        'success': True,
        'deleted': movie_id
      })
    except:
      abort(422)


  # DELETE /casting/actors/<int:actor_id>

  @app.route('/casting/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    try:
      actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

      if actor is None:
        abort(404)
            
      actor.delete()

      return jsonify({
        'success': True,
        'deleted': actor_id
      })
    except:
      abort(422)

  # PATCH /casting/movies/<int:movie_id>

  @app.route('/casting/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, movie_id):
    body = request.get_json()
    
    # if no form data
    if body is None:
      abort(404)

    try:
      movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
      
      if movie is None:
        abort(404)

      title = body.get('title', movie.title)
      release_date = body.get('release_date', movie.title)
      
      movie.title = title
      movie.release_date = release_date
      
      movie.update()
      
      return jsonify({
        'success': True,
        'movie': movie.format()
        }), 200
      
    except Exception as e:
      print(e)
      abort(422)


  # PATCH /casting/actors/<int:movie_id>

  @app.route('/casting/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, actor_id):
    body = request.get_json()
    
    # if no form data
    if body is None:
      abort(404)

    try:
      actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
      
      if actor is None:
        abort(404)

      name = body.get('name', actor.name)
      age = body.get('age', actor.age)
      gender = body.get('gender', actor.gender)
      
      actor.name = name
      actor.age = age
      actor.gender = gender
      
      actor.update()
      
      return jsonify({
        'success': True,
        'actor': actor.format()
        }), 200
      
    except Exception as e:
      print(e)
      abort(422)

  # Error Handling
  
  @app.errorhandler(500)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal server error'
  }), 500
    
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessible'
  }), 422

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  return app

APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)