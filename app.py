from flask import Flask
from flask import render_template, request
from flask import redirect, flash 
import imghdr
import json
import pytesseract

from PIL import Image
import torch
import pickle
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"




#loading the files 
open_file = open("chatmodel.pickle", "rb")
model= pickle.load(open_file)
open_file.close()

open_file = open("chattokenizer.pickle", "rb")
tokenizer= pickle.load(open_file)
open_file.close()

with open("config.json","r") as c:
    params=json.load(c)["params"]


#chatbot function to be used 

def question_answer(question, text):
    #tokenizes the question and the text given as a pair
    input_ids = tokenizer.encode(question, text)
    #converted to string inn the form of cls and sep
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    #segment IDs of the inputs
    #when was sep token first used in the list of the tokenized version
    sep_idx = input_ids.index(tokenizer.sep_token_id)
    #no of tokens in Question
    num_seg_a = sep_idx+1
    #no of tokens in text given
    num_seg_b = len(input_ids) - num_seg_a
    
    #list of 0s and 1s for segment embeddings
    #1 for tokens that are not masked,0 for tokens that are masked.
    #Bert masks 15% percent of the sentence randomly hence....
    segment_ids = [0]*num_seg_a + [1]*num_seg_b
    assert len(segment_ids) == len(input_ids)
    
    #model output using input_ids and segment_ids, token type ids define the first or second portion of the input 
    output = model(torch.tensor([input_ids]),
                   token_type_ids=torch.tensor([segment_ids]))
    
    #reconstructing the answer with start and end logits
    #start logits are span start scores, ends are vice versa
    answer_start_index = output.start_logits.argmax()
    answer_end_index = output.end_logits.argmax()
    
    #forming of the answers
    if answer_end_index >= answer_start_index:
        answer = tokens[answer_start_index]
        for i in range(answer_start_index+1, answer_end_index+1):
            if tokens[i][0:2] == "##": # here ## stands as a subword for example if the word is tokenization --> token and ##ization
                answer += tokens[i][2:]
            else:
                answer += " " + tokens[i]
                
    # if answer starts with cls.....
    else:
        answer = "Unable to find the answer to your question."
    return answer.capitalize()



app = Flask(__name__)

# @app.route("/",methods=["POST"])
# def textchat():
#     
#     return render_template('index.html',params=params)

def chatbot_response(usertext):
    with open("notebook.txt","r") as f:
        dataset=f.read()
    s=question_answer(usertext,dataset)
    return s.capitalize()+"."

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
@app.route("/chatbot/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)



app.run(debug=True)