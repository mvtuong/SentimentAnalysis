import requests, json
response = requests.post("http://127.0.0.1:5000/predict/", data='terrible')
if response.status_code == 200:
    response = json.loads(response.text)
    if response["message"] == "success":
        print(response["value"])
#http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
#http://cssdeck.com/labs/percentage-bar
#with open("predict_logs.txt", "a") as logfile:
            #logfile.write("data: " + str(request.data))
from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    if request.method == 'POST':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            #Always use get on request.POST. Correct way of querying a QueryDict.
            email = request.POST.get('email           password = request.POST.get('password           data = {"email":email , "password" : password}
            #Returning same data back to browser.It is not possible with Normal submit
            return JsonResponse(data)
    #Get goes here
    return render(request,'base.html')


$.ajax({
         url : window.location.href, // the endpoint,commonly same url
         type : "POST", // http method
         data : { csrfmiddlewaretoken : csrftoken, 
         email : email,
         password : password
 }, // data sent with the post request

 // handle a successful response
 success : function(json) {
      console.log(json); // another sanity check
      //On success show the data posted to server as a message
      alert('Hi '+json['email'] +'!.' + ' You have entered password:'+      json['password']);
 },

 // handle a non-successful response
 error : function(xhr,errmsg,err) {
 console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
 }
 });
});
