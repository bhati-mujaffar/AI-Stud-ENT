from flask import Flask
from flask import render_template, request
from flask import redirect, flash 
import imghdr
import json
with open("config.json","r") as c:
    params=json.load(c)["params"]

app = Flask(__name__)

# @app.route("/",methods=["POST"])
# def textchat():
#     
#     return render_template('index.html',params=params)

@app.route('/', methods=['GET', 'POST'])
def textchat():
    if request.method == 'POST':
        img = request.files['images']
        link = "temp."+imghdr.what(img)
        img.save(link)
        print(img)
        print("lol")
    return render_template('index.html',params=params)



@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html',params=params)

@app.route("/chatbot")
def chatbot():
    return render_template('chatbot.html',params=params)



app.run(debug=True)