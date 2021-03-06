from flask import Blueprint, jsonify, abort, request
from flask_cors import cross_origin

from pymongo.errors import WriteError

import src.controllers.usercontroller as controller

# instantiate the flask blueprint
user_blueprint = Blueprint('user_blueprint', __name__)

# create a new user
@user_blueprint.route('/create', methods=['POST'])
@cross_origin()
def create_user():
    data = request.form.to_dict()
    user = None
    try:
        user = controller.create_user(data)
        return jsonify(user)
    except WriteError as e:
        abort(400, 'Invalid input data')
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

# obtain one user by id (and optionally update him)
@user_blueprint.route('/<id>', methods=['GET', 'PUT'])
@cross_origin()
def get_user(id):
    try:
        # get a specific user
        if request.method == 'GET':
            user = controller.get_user(id)
            return jsonify(user), 200
        # update the user
        elif request.method == 'PUT':
            data = request.form
            update_result = controller.update_user(id, data)
            user = controller.get_user(id)
            return jsonify(user), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

# obtain one user by id (and optionally update him)
@user_blueprint.route('/bymail/<email>', methods=['GET'])
@cross_origin()
def get_user_by_mail(email):
    try:
        user = controller.get_user_by_email(email)
        return jsonify(user), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

# obtain all users and return them
@user_blueprint.route('/all', methods=['GET'])
@cross_origin()
def get_users():
    try:
        users = controller.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')