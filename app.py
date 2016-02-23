import json
from engine import SentimentAnalysis 
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
 
@app.route("/predict/", methods = ["POST"])
def get_predict():
    if request.method == 'POST':
        if 0 < len(request.data) < 5000:
            text = str(request.data)
            rating = sa.get_predict_ratings(text)
            response = {"message": "success", "value": rating}
            return json.dumps(response)
        else:
            response = {"message": "error", "value": "something wrong with the input"}
            return json.dumps(response)
 
 
if __name__ == "__main__":
    global sa
    sa = SentimentAnalysis()    
    
    #app.debug = True
    app.run( host="127.0.0.1", port=int("8888") )
