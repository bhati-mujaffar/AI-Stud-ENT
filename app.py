from flask import Flask
from flask import render_template, request
from flask import redirect, flash 
import json
with open("config.json","r") as c:
    params=json.load(c)["params"]

app = Flask(__name__)

@app.route("/")
def textchat():
    return render_template('index.html',params=params)

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html',params=params)

@app.route("/chatbot")
def chatbot():
    return render_template('chatbot.html',params=params)



app.run(debug=True)