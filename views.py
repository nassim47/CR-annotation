


import os
import xml.dom.minidom
from os.path import basename
from lxml import etree
import re
import xmltodict
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse

from flask import Flask, render_template, request, redirect, flash, url_for, send_file, safe_join
from werkzeug.utils import secure_filename
from flask import send_from_directory
# ------------------------------------------------


# Chemin d'accès au dossier de téléchargement
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static') # fichier téléchargé sera stocké dans le fichier 'static'

# Extensions autorisées des fichiers à téléchargé
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'log', 'xml', 'json'])

# Ajout du répertoir UPLOAD_Folder dans Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key" # version sécurisé du fichier téléchargé

# Vérifie si l'extension est valide
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Page racine
@app.route('/')
def index():
    data = {
        'title': 'AppTool',
    }
    return render_template('index.html', data=data)



# Page de chargement du fichier XML
@app.route('/chargement/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Vérifie si le file est dans le post request
        if 'file' not in request.files:
            flash(u'No file part')
            return redirect(request.url)
        file = request.files['file']
        # Si l'urtilisateur ne séléctionne pas de fichier
        if file.filename == '':
            flash(u'No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # sécurisé le nom du fichier
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # sauvegarder

            return redirect(url_for('annotation', filename=filename)) # aller à 'annotation/filename'
    return render_template('chargement.html')



# Page d'affichage du fichier téléchargé
@app.route('/annotation/<filename>')
def annotation(filename):
    data = {
        'title': 'Annotation',
    }

    # Parser le fichier XML
    # Chemin à modifier selon l'emplacement de votre XML dans le projet Pycharm IDE
    tree = ET.parse("/Users/nassim/PycharmProjects/flask/Apptool/static/" + filename  )
    root = tree.getroot()

    liste = [] #liste qui contient les attributs 'text, start, end' dans les balises medical_event


    # Ajout des attributs à 'liste'
    for medical_event in root.findall('sentences/sentence/medical_event'):
        liste.append(medical_event.get('text'))
        liste.append(medical_event.get('start'))
        liste.append(medical_event.get('end'))

    # Lire le fichier XML
    with open("/Users/nassim/PycharmProjects/flask/Apptool/static/" +filename, 'rt') as fd:
        # Convertir XML en Dictionnaire
        dic = xmltodict.parse(fd.read())
        # Séparer le text entre les balises '<contenu>' par des espaces
        # Pour pouvoir le parcourir mot par mot
        space = dic['CR']['contenu'].split()

    # Dans le render_template, il faut mettre les variables dont tu souhaite les utilisé dans le HTML
    return render_template('annotation.html', data=data, root=root, tree=tree, space=space,
                           dic=dic, liste=liste)

# Page modification
@app.route('/modification/')
def modifier():
    data = {
        'title': 'modification',
    }

    # Ici faudra revoir comment automatisé le chemin vers le XML téléchargé
    # J'ai mis le nom du XML téléchargé, il faudra revoir sa
    tree = ET.parse("/Users/nassim/PycharmProjects/flask/Apptool/static/CR_fictif_extraction.xml")
    root = tree.getroot()

    liste = []  # liste qui contient les attributs 'text, start, end' dans les balises medical_event

    # Ajout des attributs à 'liste'
    for medical_event in root.findall('sentences/sentence/medical_event'):
        liste.append(medical_event.get('text'))
        liste.append(medical_event.get('start'))
        liste.append(medical_event.get('end'))

    with open("/Users/nassim/PycharmProjects/flask/Apptool/static/CR_fictif_extraction.xml", 'rt') as fd:
        # Convertir XML en Dictionnaire
        dic = xmltodict.parse(fd.read())
        # Séparer le text entre les balises '<contenu>' par des espaces
        # Pour pouvoir le parcourir mot par mot
        space = dic['CR']['contenu'].split()



    return render_template('modification.html', data=data, root=root, tree=tree, space=space, dic=dic, liste=liste   )



# Page d'affectation
@app.route('/affectation/')
def affectation():
    data = {
        'title': 'Affectation',
    }
    return render_template('affectation.html', data=data)


# Page guide d'utilisation
@app.route('/guide/')
def guide():
    data = {
        'title': 'Utilisations'
    }
    return render_template('guide.html', data=data)


# Lancer le serveur sur le port 3000 avec debug
if __name__ == '__main__':
    app.run(debug=True, port=3000)