from flask import Flask, render_template, request
from pymongo import MongoClient
import base64

app = Flask(__name__)
client = MongoClient('mongodb+srv://RAK_MANIAK:123370@python-lab-11.2hfteul.mongodb.net/test')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        img_base64 = base64.b64encode(request.files.get('picture').read())
        print(str(img_base64)[2:-1])

        return render_template('MangaShelf.html', test='data:;base64,' + str(img_base64)[2:-1])
    else:
        return render_template('MangaShelf.html', test='error')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/main')
def main():
    return render_template('MangaShelf.html')

if __name__ == '__main__':
    app.run(debug=True)
