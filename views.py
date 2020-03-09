import os
import xml.dom.minidom

import xml.etree.ElementTree as ET
from xml.dom.minidom import parse



from flask import Flask , render_template, request, redirect, flash, url_for, send_file,safe_join
from werkzeug.utils import secure_filename
from flask import send_from_directory


UPLOAD_FOLDER = '/Users/nassim/Desktop/Stage'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'log', 'xml'])



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    data ={
        'title':'AppTool',
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
            return redirect(url_for('afficher',
                                    filename=filename))
    return render_template('chargement.html')


'''@app.route('/afficher/<filename>')
def uploaded_file(filename):

    n = send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    return n
'''

@app.route('/afficher/<filename>')
def afficher(filename):
    data ={
        'title':'Afficher',
       }
    doc = xml.dom.minidom.parse("/Users/nassim/Desktop/Stage/"+filename)
    return render_template('afficher.html', data=data, doc=doc)



@app.route('/annotation/')
def annotation():
    data = {
        'title': 'Annotation',
    }
    return render_template('annotation.html', data=data)

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
    app.run(debug=True, port= 3000)
