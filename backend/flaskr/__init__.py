import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})


    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response


    '''
    Create an endpoint to handle GET requests
    for all available categories.
    '''


    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query().all()
        if len(categories) == 0:
            abort(404)
        return jsonify({
          'success': True,
          'categories': [category.type for category in categories]
        })


    '''
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen.
    Clicking on the page numbers should update the questions.
    '''


    def fitler_questions(request=request, category=None, search=None):
        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)
        if len(current_questions) == 0:
            abort(404)
        if category is not None:
            category = Question.query.filter(Question.category == category)
        if search is not None:
            questions = Question.query.filter(Question.question.ilike(search))
            questions = questions.order_by(Question.difficulty).all()
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        if len(questions) < start:
            abort(404)
        return jsonify({
          'success': True,
          'status': 200,
          'questions': current_questions,
          'total_questions': len(questions),
          'current_category': category,
          'categories': [category.type for category in Category.query.all()]
        })


    @app.route('/questions')
    def retrieve_questions():
        return fitler_questions(request)


    '''
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.filter_by(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'status': 200,
                'deleted_id': question_id,
                'questions': current_questions,
                'total_questions': len(questions),
            })
        except:
            abort(422)

    '''
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''

    '''
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''


    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        # searchTerm case
        search = body.get('searchTerm', None)
        if search is not None:
            try:
                return fitler_questions(search=search)
            except:
                abort(422)
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty ', None)
        try:
            new_question = Question(question=question, answe=answer, category=category, difficulty=difficulty)
            new_question.insert()
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'created': Question.id,
                'questions': current_questions,
                'total_questions': len(questions)
            })
        except:
            abort(422)


    '''
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''


    @app.route('/categories/<int:category_id>/questions')
    def retrieve_questions_by_categoty(category_id):
        return fitler_questions(category=category_id)

    '''
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''


    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            quiz_category_id = None
            quiz_category_type = None

            if quiz_category is not None:
                quiz_category_id = quiz_category.get("id", None)
                quiz_category_type = quiz_category.get("type", None)
            category = Category.query.filter(Category.type == quiz_category_type).one_or_none()
            if category is not None:
                questions = Question.query.filter(Question.category == category.id)
            none_previous_questions = questions.query.filter(~Question.id.in_(previous_questions)).all()
            if len(none_previous_questions) == 0 or len(previous_questions) >= 5:
                return jsonify({})
            random_id = random.randint(0, len(none_previous_questions)-1)
            return jsonify({
                'success': True,
                'question': questions[random_id].format()
            })
        except:
            abort(422)

    '''
    Create error handlers for all expected errors
    including 404 and 422.
    '''


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        })


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        })


    return app
