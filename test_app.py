import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors

class CastingTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_movie = {
            'title': 'End of the wicked',
            'release_date': '2020-07-14',
        }
        
        self.new_actor = {
            'name': 'John Doe',
            'age': '24',
            'gender': 'Male',
        }
        
        self.token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVQb3RLSFVoTHRvM2RMWWFFRWVJUyJ9.eyJpc3MiOiJodHRwczovL2pvaS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwZDg1NTc3MTQ2OGMwMDEzMDAyOTJlIiwiYXVkIjoiQ2FzdGluZyIsImlhdCI6MTU5NDcyMzE3OSwiZXhwIjoxNTk0ODA5NTc5LCJhenAiOiJicEJIbGpDODBQQ2h0NnNnbDRxMkFJTXRQWlhUZ01yeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.CF1aica2viMwrbPpkOfpCltxd4m09dL_SJyeBWaAaAav-QUcEVhTAQBc2U5r3Gg5FNbS-PUOvpKWePKbvM3YhsKjeUd2W8lgNI2RbjvVv9bY3BWXtQuZymvf-RBFc9hgJtWc8JwVlUf-Bs_H9TooIsK8_HtiToq34c0ClcNCgfxSZMKOZ5IO-IlUegaNiB1BFWjN5kBzNeJrWDD-VrdQG_wWGj_PJCKhp0ji5cUmUD4oYTwKhSGABy4GlJNm_l5pLSnQX9e2dhslAnVN0y_K5whej_O0GH8acQHqG8p-UTZyZKmqc4XkKcUBBd8qbup-vexMUd4zvaEEeqh8lWOcRQ'

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Tests
    def test_create_new_movie(self):
        res = self.client().post('/casting/movies', headers={'Authorization': 'Bearer {}'.format(self.token)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
    
    def test_create_new_actor(self):
        res = self.client().post('/casting/actors', headers={'Authorization': 'Bearer {}'.format(self.token)}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_get_movies(self):
        res = self.client().get('/casting/movies', headers={'Authorization': 'Bearer {}'.format(self.token)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors(self):
        res = self.client().get('/casting/actors', headers={'Authorization': 'Bearer {}'.format(self.token)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies(self):
        res = self.client().delete('/casting/movies/1', headers={'Authorization': 'Bearer {}'.format(self.token)})
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
    
    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/casting/movies/100', headers={'Authorization': 'Bearer {}'.format(self.token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessible')

    def test_delete_actors(self):
        res = self.client().delete('/casting/actors/1', headers={'Authorization': 'Bearer {}'.format(self.token)})
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/casting/actors/100', headers={'Authorization': 'Bearer {}'.format(self.token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessible')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()