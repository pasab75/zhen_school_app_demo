from flask import Flask, jsonify, request, abort
import json
import datetime
import db_access.db_question as db_access_layer

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/get/question', methods=['POST'])
def get_question():
    try:
        incoming_request = request
        print (incoming_request)
        print(incoming_request.data)
        task_id = incoming_request.data[0]
        result = None
        dbconnect = db_access_layer.database_access()
        result = dbconnect.get_by_id(task_id)
        dbconnect.close_connection()
        return result.get_jsonified()
    except Exception as ex:
        print(ex)
        abort(500, "Unable to find id or no id given")

#TODO: enable CORS so that app can talk to API
#need to research this to make sure it's safe to use like this

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

if __name__ == '__main__':
    app.run(debug=True)