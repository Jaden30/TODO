from flask import Flask, render_template, jsonify, request
from pusher import Pusher
import json 

from file import app_id, key, secret, cluster

# create an object of the flask 
app = Flask(__name__)

# configure pusher object 

pusher = Pusher(
    app_id= app_id,
    key= key, 
    secret= secret, 
    cluster= cluster,
    ssl=True 
)



# index route, shows the view of index.html view 

@app.route('/')
def index():
    return render_template("index.html")

# creating an endpoint and a method for  todoitem using the method POST 

@app.route("/add-item", methods=["POST"])
def create():
    data = json.loads(request.data)  # this loads a json data from request 
    pusher.trigger("todo", "item-added", data) # this adds to-do item to the list 
    return jsonify(data)


# creating an endpoint to remove a method for todo item 
@app.route("/remove/<item_id>", methods=["DELETE"])
def delete(item_id):
    data = {"id" : item_id}
    pusher.trigger("todo", "item_removed", data )
    return jsonify(data)


# creating an endpoint to update an added item 
@app.route("/update/<item_id>", methods=["POST"])
def update(item_id):
    data = {
        "id" : item_id, 
        "completed" : json.loads(request.data).get("completed", 0)
    }

    pusher.trigger("todo", "item_updated", data)
    return jsonify(data)
      

 # run Flask app in debug mode
    app.run(debug=True)