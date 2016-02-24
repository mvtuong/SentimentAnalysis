from flask import Blueprint
main = Blueprint('main', __name__)
import json
from engine import SentimentAnalysis 
from flask import Flask, request

@main.route("/", methods = ['GET'])
def hello():
    return "Hello World!"
 
@main.route('/predict/', methods = ['POST'])
def get_predict():
    if request.method == 'POST':
        
        if 0 < len(request.data) < 50000:
            text = str(request.data)            
            rating = sa.get_predict_ratings(text)[0]
            r = [int(round(i, 2)*100) for i in rating]
            response = {"message": "success", "value": {"x1": r[0], "x2": r[1], "x3": r[2], "x4": r[3], "x5": r[4]}}
            return json.dumps(response)
        else:
            response = {"message": "error", "value": "something's wrong with the input text"}
            return json.dumps(response)
 
def create_app():
    global sa
    sa = SentimentAnalysis()
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
 
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=8888)
