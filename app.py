from flask import Flask
from flask import render_template, request
from flask import redirect, flash 
import imghdr
import json
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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
        image = Image.open(link)
        text2 = pytesseract.image_to_string(image, lang='eng')
        print(text2)
        with open("notebook.txt","r+") as f:
            f.write(text2)
        with open("notebook.txt", "r") as f:
            lines = f.readlines()
        # Remove any blank lines or extra whitespace
        lines = [line.strip() for line in lines if line.strip()]
        with open("notebook.txt", "w") as f:
            f.write("\n".join(lines))
        with open("notebook.txt","r+") as f:
            data=f.read()    
            params["dataset"]=data
    return render_template('index.html',params=params)



@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        if "content" in request.form:
            with open("notebook.txt", "w") as f:
                f.write(request.form["content"])
            with open("notebook.txt", "r") as f:
                data = f.read()
                params["dataset"] = data
            return render_template("dashboard.html", params=params)
        else:
            return render_template("dashboard.html", params=params)
    else:
        with open("notebook.txt", "r") as f:
            data = f.read().strip()
            params["dataset"] = data
        return render_template("dashboard.html", params=params)

@app.route("/chatbot")
def chatbot():
    return render_template('chatbot.html',params=params)



app.run(debug=True)