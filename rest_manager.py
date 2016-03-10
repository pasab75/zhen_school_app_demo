from flask import Flask, jsonify, request, abort
import json
import datetime
import db_access.db_question as db_access_layer

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/get/random/MC', methods=['POST'])

@app.route('/get/random/FR', methods=['POST'])

@app.route('/get/random/DEF', methods=['POST'])

@app.route('/get/WORD', methods=['POST'])

@app.route('/get/DEF', methods=['POST'])

@app.route('/get/FR', methods=['POST'])

#TODO:make these routes available

@app.route('/get/MC', methods=['POST'])
def get_question():
    try:
        incoming_request = request
        print(incoming_request)
        task_id=(request.json['id'])
        result = None
        dbconnect = db_access_layer.database_access()
        result = dbconnect.get_by_id(task_id)
        dbconnect.close_connection()
        return result.get_jsonified()
    except Exception as ex:
        print(ex)
        abort(500, "Unable to find id or no id given")

#TODO: check to see if this CORS implementation is safe
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

if __name__ == '__main__':
        app.debug = True
        #be careful with this apparently it's a security hazard

        app.run(host='0.0.0.0')
        #this allows the API to use the public IP
