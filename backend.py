from flask import Flask, render_template, request, flash
from pymongo import MongoClient
import base64

app = Flask(__name__)
client = MongoClient('mongodb+srv://RAK_MANIAK:123370@mangashelf.3ortmjy.mongodb.net/test')
app.db = client.MangaShelf

@app.route('/')
def index():
    return render_template('MangaShelf.html')


@app.route('/add', methods=['GET', 'POST'])
def addToMangaShelfCatalogue():
    if request.method == 'POST':
        img_base64 = base64.b64encode(request.files.get('image').read())
        return render_template('MangaShelf.html', test='data:;base64,' + str(img_base64)[2:-1])
    else:
        return render_template('MangaShelf.html', test='error')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/main')
def main():
    return render_template('MangaShelf.html')

@app.route('/registration', methods=['GET', 'POST'])
def addToMangaShelfUsers():
    if request.method == 'POST':

        # if request.form.get("name") == '' or request.form.get("password") == '':
        #     return render_template('MangaShelf.html', test='empty fields')
        #
        # if app.db.users.find_one({'login': request.form['login']}):
        #     flash('user already exists')
        #     return render_template('MangaShelf.html', message=flash)
        name = request.form.get("name")
        password = request.form.get("password")

        app.db.Users.insert_one({ "name": name, "password": password})
        return render_template('MangaShelf.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/main')
def main():
    return render_template('MangaShelf.html')

if __name__ == '__main__':
    app.run(debug=True)