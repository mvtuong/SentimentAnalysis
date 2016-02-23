from flask import Blueprint
main = Blueprint('main', __name__)
import json
from engine import SentimentAnalysis 
from flask import Flask, request

@main.route("/", methods = ['GET'])
def hello():
    return "Hello World 1!"
 
@main.route('/predict/', methods = ['POST'])
def get_predict():
    if request.method == 'POST':
        with open("log.txt", "w") as text_file:
            text_file.write("data: " + str(request.data))
        if 0 < len(request.data) < 5000:
            text = str(request.data)
            
            rating = sa.get_predict_ratings(text)
            
            response = {"message": "success", "value": rating[0]}
            return json.dumps(response)
        else:
            response = {"message": "error", "value": "something wrong with the input"}
            return json.dumps(response)
 
def create_app():
    global sa
    sa = SentimentAnalysis()
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
 
if __name__ == "__main__":
    app = create_app()
    app.run()
