from flask import Flask, jsonify
import json
import datetime
import db_access.db_question as db_access_layer

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/get/question/<int:task_id>', methods=['GET'])
def get_question(task_id):
    try:
        result = None
        dbconnect = db_access_layer.database_access()
        result = dbconnect.get_by_id(1)
        dbconnect.close_connection()
        return result.get_jsonified()
    except Exception as ex:
        return "you passed in "+str(task_id)+ " exception give: "+str(ex)

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