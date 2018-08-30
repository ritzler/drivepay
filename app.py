from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import requests

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['UPLOAD_FOLDER'] = r'''C:\Users\sritzler\workspace\uploads'''

def dw_register(image, secret):
    url = 'http://localhost:8080/v1/register'
    headers = {
        'bucket_url': image,
        'secret': secret,
        'Content-type': 'application/json'
    }
    r = requests.get(url, headers=headers)
    print(r.text)
    return

def dw_auth(image):
    url = 'http://localhost:8080/v1/auth'
    headers = {
        'bucket_url': image,
        'secret': 'secret',
        'amount': '10.0',
        'Content-type': 'application/json'
    }
    r = requests.get(url, headers=headers)
    print(r.text)
    return

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def register():
    return render_template('signup.html')

@app.route('/auth')
def auth():
    """Take an image and look up the user"""
    return render_template('auth.html')

@app.route('/auth/submit')
def submit_amount():
    """After looking up a user with the image, require the secret"""
    return render_template('submit.html')

@app.route('/process', methods=['POST'])
def process():
    plate = request.form['plate']
    secret = request.form['secret']
    image = request.files['imageFile']
    if image:
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        try:
            dw_register(filepath, secret)
        except Exception as e:
            return render_template('error.html', error = e)
    return render_template('thankyou.html', plate = plate)

if __name__ == '__main__':
    app.run(debug=True)
