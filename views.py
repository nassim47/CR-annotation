import os
from termcolor import colored
import xml.dom.minidom
import json
from flask import json
from os.path import basename
from lxml import etree
import re


import xmltodict

import xml.etree.ElementTree as ET
from xml.dom.minidom import parse




from flask import Flask, render_template, request, redirect, flash, url_for, send_file, safe_join
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = '/Users/nassim/Desktop/Stage'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'log', 'xml', 'json'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"



@app.route('/')
def index():
    data = {
        'title': 'AppTool',
    }
    return render_template('index.html', data=data)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/chargement/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash(u'No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filenam
        if file.filename == '':
            flash(u'No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(filename)
            return redirect(url_for('annotation',
                                    filename=filename))
    return render_template('chargement.html')





@app.route('/afficher/')
def afficher():
    data = {
        'title': 'afficher',
    }



    #with open('/Users/nassim/Desktop/Stage/' + filename, 'rt') as myfile:
     # contents = myfile.read()
      #espace = contents.split()
      #saut = contents.split('\n')





    return render_template('afficher.html', data=data)





@app.route('/annotation/<filename>')
def annotation(filename):
    data = {
        'title': 'Annotation',
    }
    tree = ET.parse("/Users/nassim/Desktop/Stage/"+filename)
    root = tree.getroot()

    liste = []
    start_end = []



    for medical_event in root.findall('sentences/sentence/medical_event'):
        liste.append(medical_event.get('text'))




    with open('/Users/nassim/Desktop/Stage/' + filename, 'rt') as myfile:
      contents = myfile.read()
      espace = contents.split()
      saut = contents.split('\n')


    with open("/Users/nassim/Desktop/Stage/"+filename, 'rt') as fd:
        doc = xmltodict.parse(fd.read())
        space = doc['CR']['contenu'].split()





    for sentence in space:

        for l in liste:
            start = int(sentence.find(l))
            end = start + len(l)
            start_end.append(start)
            start_end.append(end)





    return render_template('annotation.html', data=data,espace=espace, root=root, tree=tree, saut=saut, space=space,
                           doc=doc, liste=liste, start_end=start_end, start=start, end=end)



@app.route('/affectation/')
def affectation():
    data = {
        'title': 'Affectation',
    }
    return render_template('affectation.html', data=data)


@app.route('/guide/')
def guide():
    data = {
        'title': 'Utilisations'
    }
    return render_template('guide.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, port=3000)