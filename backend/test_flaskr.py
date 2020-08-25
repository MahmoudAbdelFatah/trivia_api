import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_password = ''
        self.database_path = "postgresql://{}:{}@{}/{}"
        .format('postgres', database_password, 'localhost:5432', database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'A new question',
            'answer': 'New answer',
            'category': 1,
            'difficulty': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        questions = Question.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['total_questions']), questions)
        self.assertEqual(data['current_category'], '')

    def test_get_pagination_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']), 10)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_search_question(self):
        res = self.client().post(
            '/questions', json={'searchTerm': 'question1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(len(data['questions']), 10)

    def test_search_not_found_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'xxx'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertEqual(data['questions'][0]['category'], 1)

    def test_get_questions_not_exist_category(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data.get('questions', False))

    def test_get_questions_by_category_page(self):
        res = self.client().get('/categories/1/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertEqual(data['questions'][0]['category'], 1)

    def test_get_questions_by_category_page(self):
        res = self.client().get('/categories/1/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_add_question(self):
        total_questions = len(Question.query.all())
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        new_total_questions = len(Question.query.all())
        self.assertEqual(total_questions + 1, new_total_questions)

    def test_422_unproccessable_add_question(self):
        self.new_question['category'] = 10
        total_questions = len(Question.query.all())

        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

        new_total_question = len(Question.query.all())
        self.assertEqual(total_questions, new_total_question)

    def test_delete_question(self):
        questions = Question.query.all()
        total_questions = len(questions)

        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1).one_or_none()
        new_total_questions = len(data['questions'])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_id'], 1)
        self.assertEqual(total_questions - 1, new_total_questions)

    def test_404_delete_question(self):
        total_questions = len(Question.query.all())

        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)

        new_total_questions = len(Question.query.all())

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(total_questions, new_total_questions)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        categories = Category.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), len(categories))

    def test_get_quizzes_no_json(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)


if __name__ == "__main__":
    unittest.main()
