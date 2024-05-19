from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from nltk.corpus import wordnet
import time
from PIL import Image
import math
from rembg import remove
import random

model_url = "https://kaggle.com/models/google/universal-sentence-encoder/TensorFlow1/universal-sentence-encoder/1"
embed = hub.load(model_url)
finscore = 1000
input_history = []
leaderboard = []
def format_image(input_path, new_size):

    # Open the image
    with Image.open(input_path) as img:
        resized_img = img.resize(new_size)
        resized_img = remove(resized_img)
        newimg = resized_img.load()
        a,b = resized_img.size
        for i in range(a):
            for j in range(b):
                if newimg[i,j][3]!=0:
                    resized_img.putpixel((i,j),(0,0,0))
        resized_img.save("static/cur.png")
    
def pick_random_word():
    words = ['airpods', 'apple', 'baguette', 'bottle', 'cabbage', 'calculator', 'can', 'car', 'cat', 'cheese', 
             'cheetah', 'cleat', 'dog', 'drum', 'eagle', 'elephant', 'flowers', 'gorilla', 'guitar', 
             'hammer', 'hoodie', 'iron', 'knife', 'lamp', 'laptop', 'lion', 'marker', 'monitor', 'monkey', 
             'mouse', 'mug', 'orange', 'pizza', 'plane', 'plantain', 'rhino', 'rooster', 'shark', 'skyscraper', 
             'sofa', 'speaker', 'spoon', 'suitcase', 'truck', 'turtle', 'watermelon', 'whale','wolf', 'zebra']
    return words[np.random.randint(0,len(words))]

curword = pick_random_word()
format_image("static/"+curword+".png", (300,300))

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms

def difference(a, b):
    vec1 = a[0]
    vec2 = b[0]
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def get_diff(word1, word2):
    input_sentences = [
        f"Another synonym for {word1} is: " + ", ".join(get_synonyms(word1)),
        f"Another synonym for {word2} is: " + ", ".join(get_synonyms(word2))
    ]

    signature = embed.signatures["default"]

    embeddings = []

    for sentence in input_sentences:
        sentence_embedding = signature(tf.constant([sentence]))["default"]
        embeddings.append(sentence_embedding.numpy())

    embeddings_array = np.array(embeddings)

    embedding_quick_context = embeddings_array[0]
    embedding_lazy_context = embeddings_array[1]
    k = min(max(difference(embedding_quick_context, embedding_lazy_context),-1),1)
    return int(math.acos(k)*180/math.pi)


@app.route('/')
def index():
    return render_template('homepage.html', history=input_history)

@app.route('/gamepage.html', methods = ['GET', 'POST'])
def gamepage():
    global leaderboard
    global input_history
    global finscore
    global curword
    if request.method == 'POST':
        if 'resetInput' in request.form and request.form['resetInput'] == 'clicked':
            input_history = []
            print("cleared")
            return render_template('gamepage.html', history=input_history,leaderboard=leaderboard,score=finscore)
        if 'revealPixelButton' in request.form and request.form['revealPixelButton']=='clicked':
            finscore-=20
            finscore = max(0,finscore)
            tmp = Image.open("static/cur.png")
            newtmp = tmp.load()
            og = Image.open("static/"+curword+".png").resize((300,300))
            rand = random.randint(0,289)
            for i in range(rand,rand+10):
                for j in range(300):
                    if newtmp[i,j][3]!=0:
                        tmp.putpixel((i,j),og.getpixel((i,j)))
            tmp.save("static/cur.png")
            return render_template('gamepage.html', history=input_history,leaderboard=leaderboard,score=finscore)
        else:
            text_input = request.form['playerInput']
            score_off=get_diff(text_input, curword)
            if text_input.lower()!=curword and finscore>0 and text_input!="":
                input_history = [text_input + " - " + str(score_off)] + input_history
                finscore-=score_off 
                finscore = max(0,finscore)
                return render_template('gamepage.html', history=input_history,leaderboard=leaderboard,score=finscore)
            elif text_input=="":
                return render_template('gamepage.html', history=input_history,leaderboard=leaderboard,score=finscore)
            else:
                leaderboard.append(finscore)
                leaderboard.sort(reverse=True)
                leaderboard = leaderboard[:min(len(leaderboard),5)]
                curword = pick_random_word()
                finscore=1000
                format_image("static/"+curword+".png", (300,300))
                return render_template('gamepage.html', history=input_history,leaderboard=leaderboard,score=finscore)
    return render_template('gamepage.html', history=input_history,leaderboard=leaderboard,score=finscore)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
