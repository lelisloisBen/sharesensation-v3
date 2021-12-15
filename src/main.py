from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, sha256
from models import db, users, activities, saletaxes
# from flask_jwt_simple import JWTManager, jwt_required, create_jwt
import os

app = Flask(__name__)
app.config.from_object("config")
db.init_app(app)
CORS(app)
# app.config['JWT_SECRET_KEY'] = 'dfsh3289349yhoelqwru9g'
# jwt = JWTManager(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def hello_world():
    return "<div style='text-align: center; background-color: orange'><h1>Backend running...</h1><br/><h3>Welcome back samir</h3><img src='https://media.gettyimages.com/photos/woman-sitting-by-washing-machine-picture-id117852649?s=2048x2048' width='80%' /></div>"

@app.route('/login', methods=['POST'])
def handle_login():

    body = request.get_json()

    user = users.query.filter_by(email=body['email'], password=sha256(body['password'])).first()

    if not user:
        return 'User not found', 404

    return jsonify({
            #   'token': create_jwt(identity=1),
              'id': user.id,
              'email': user.email,
              'firstname': user.firstname,
              'lastname': user.lastname,
              'avatar': user.avatar,
              'wallet': user.wallet,
              'birthdate': user.birthdate,
              'gender': user.gender,
              'address': user.address,
              'city': user.city,
              'state': user.state,
              'zipCode': user.zipCode,
              'phone': user.phone,
              'admin': user.admin
              })

@app.route('/register', methods=['POST'])
def handle_register():

    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'firstname' not in body and 'lastname' not in body:
        raise APIException("You need to specify the first name and last name", status_code=400)
    if 'password' not in body and 'email' not in body:
        raise APIException("You need to specify the password and email", status_code=400)
    if 'firstname' not in body:
        raise APIException('You need to specify the first name', status_code=400)
    if 'lastname' not in body:
        raise APIException('You need to specify the last name', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)

    db.session.add(users(
        email = body['email'],
        firstname = body['firstname'],
        lastname = body['lastname'],
        password = sha256(body['password']),
        admin = 0
    ))
    db.session.commit()

    return jsonify({
        'register': 'success',
        'msg': 'Successfully Registered'
    })


@app.route('/activities', methods=['GET'])
def handle_activities():

    if request.method == 'GET':
        allActivities = activities.query.all()

        if not allActivities:
            return jsonify({'msg':'Activities not found'}), 404

        return jsonify( [x.serialize() for x in allActivities] ), 200

    return "Invalid Method", 404

@app.route('/activitiesbycategory', methods=['POST'])
def handle_activities_by_category():
    body = request.get_json()

    if request.method == 'POST':
        GetAllActivitiesByCategory = activities.query.filter_by(cat=body['category']).all()

        if not GetAllActivitiesByCategory:
            return jsonify({'msg':'Activities not found'}), 404

        return jsonify( [x.serialize() for x in GetAllActivitiesByCategory] ), 200

    return "Invalid Method", 404

@app.route('/saletaxes', methods=['GET'])
def handle_saletaxes():

    if request.method == 'GET':
        allSaletaxes = saletaxes.query.all()

        if not allSaletaxes:
            return jsonify({'msg':'Sale Taxes not found'}), 404

        return jsonify( [x.serialize() for x in allSaletaxes] ), 200

    return "Invalid Method", 404

@app.route('/saletaxesbystate', methods=['POST'])
def handle_saletaxes_by_state():
    body = request.get_json()
    
    if request.method == 'POST':
        GetTaxByState = saletaxes.query.filter_by(state=body['state']).first()

        if not GetTaxByState:
            return jsonify({'msg':'Sale Taxes not found for this state'}), 404

        # return jsonify( [x.serialize() for x in GetTaxByState] ), 200
        return jsonify( GetTaxByState.rate ), 200

    return "Invalid Method", 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)