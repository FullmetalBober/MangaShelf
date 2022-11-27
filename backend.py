from flask import Flask, render_template, request
from pymongo import MongoClient
import base64
from itertools import islice

app = Flask(__name__)
client = MongoClient('mongodb+srv://RAK_MANIAK:123370@mangashelf.3ortmjy.mongodb.net/test')
app.db = client.MangaShelf


class User:
    login = 'Sign In'

@app.route('/')
def outputCatalogue():
    entry = {
    'Catalogue': [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']} for manga in app.db.Catalogue.find({})],
    'User': User.login
    }
    # print(entry['Catalogue']['title'])
    # entry['Catalogue'] = list(islice(entry['Catalogue'], 0, 10))
    # Catalogue = [(manga[0], manga[1], manga[2]) for manga in app.db.Catalogue.find()]
    return render_template('MangaShelf.html', entry=entry)


@app.route('/addElement', methods=['GET', 'POST'])
def addToMangaShelfCatalogue():
    if request.method == 'POST':
        entry = {
            'Catalogue': [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']} for
                          manga in app.db.Catalogue.find({})],
            'User': User.login
        }
        try:
            title = request.form.get("title")
            # miniDescription = request.form.get("miniDescription")
            description = request.form.get("description")
            img_base64 = base64.b64encode(request.files.get('image').read())

            # if not title or not miniDescription or not description or not description or not img_base64 or app.db.Catalogue.find_one(
            if not title or not description or not description or not img_base64 or app.db.Catalogue.find_one({"title": title}):
                return render_template('MangaShelf.html')
            app.db.Catalogue.insert_one(
                # {"title": title, "miniDescription": miniDescription, "description": description, "image": img_base64})
                {"title": title, "description": description, "image": 'data:;base64,' + str(img_base64)[2:-1]})
            entry = {
                'Catalogue': [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']}
                              for manga in app.db.Catalogue.find({})],
                'User': User.login
            }
            return render_template('MangaShelf.html', entry=entry)
        except:
            return render_template('MangaShelf.html', entry=entry)


@app.route('/deleteElement', methods=['GET', 'POST'])
def deleteFromMangaShelfCatalogue():
    if request.method == 'POST':
        entry = {
            'Catalogue': [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']} for
                          manga in app.db.Catalogue.find({})],
            'User': User.login
        }
        try:
            title = request.form.get("title")
            if not title or not app.db.Catalogue.find_one({"title": title}):
                return render_template('MangaShelf.html')
            app.db.Catalogue.delete_one({"title": title})
            entry = {
                'Catalogue': [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']}
                              for manga in app.db.Catalogue.find({})],
                'User': User.login
            }
            return render_template('MangaShelf.html', entry=entry)
        except:
            return render_template('MangaShelf.html', entry=entry)


@app.route('/registration', methods=['GET', 'POST'])
def addToMangaShelfUsers():
    if request.method == 'POST':
        entry = {
            'Catalogue': [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']} for
                          manga in app.db.Catalogue.find({})],
            'User': User.login
        }
        try:
            name = request.form.get("name")
            password = request.form.get("password")
            if not name or not password or app.db.Users.find_one({"name": name}):
                return render_template('MangaShelf.html')
            app.db.Users.insert_one({"name": name, "password": password})
            return render_template('MangaShelf.html', entry=entry)
        except:
            return render_template('MangaShelf.html', entry=entry)


@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'POST':
        entry = {
            'Catalogue': [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']} for
                          manga in app.db.Catalogue.find({})],
            'User': User.login
        }
        try:
            name = request.form.get("login")
            password = request.form.get("password")
            if not name or not password or not app.db.Users.find_one({"name": name, "password": password}):
                return render_template('MangaShelf.html')
            User.login = name
            entry = {
                'User': User.login
            }
            return render_template('MangaShelf.html', entry=entry)
        except:
            return render_template('MangaShelf.html', entry=entry)


@app.route('/about')
def about():
    entry = {
        'User': User.login
    }
    return render_template('About.html', entry=entry)


@app.route('/main')
def main():
    entry = {
    'Catalogue': [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']} for manga in app.db.Catalogue.find({})],
    'User': User.login
    }
    return render_template('MangaShelf.html', entry=entry)


if __name__ == '__main__':
    app.run(debug=True)