from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, sha256
from models import db, users, activities

app = Flask(__name__)
CORS(app)

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
              'token': create_jwt(identity=1),
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

@app.route('/activities', methods=['GET'])
def handle_activities():

    if request.method == 'GET':
        allActivities = activities.query.all()

        if not allActivities:
            return jsonify({'msg':'Activities not found'}), 404

        return jsonify( [x.serialize() for x in allActivities] ), 200

    return "Invalid Method", 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)