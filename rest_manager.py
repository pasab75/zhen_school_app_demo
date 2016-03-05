from flask import Flask, jsonify
import datetime
import db_access.database_access as db_access_layer

app = Flask(__name__)


#this should probably be replaced at some point... yay
@app.route('/')
def index():
    return "Hello, World!"

@app.route('/get/question/<int:task_id>', methods=['GET'])
def get_question(task_id):
    try:
        dbconnect = db_access_layer.database_access()
        result = dbconnect.get_question(1)
        dbconnect.close_connection()
        return "made a connection, getting read to check for id="+str(result)
    except Exception as ex:
        return "you passed in "+str(task_id)+ " exception give: "+str(ex)



if __name__ == '__main__':
    app.run(debug=True)