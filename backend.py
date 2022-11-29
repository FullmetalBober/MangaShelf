from flask import Flask, render_template, request
from pymongo import MongoClient
import base64

app = Flask(__name__)
client = MongoClient('mongodb+srv://RAK_MANIAK:123370@mangashelf.3ortmjy.mongodb.net/test')
app.db = client.MangaShelf


class GiveToPage:
    Catalogue = [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']} for manga in
                 app.db.Catalogue.find({})]
    User = 'Sign In'

    @staticmethod
    def getDefaultUserName():
        return 'Sign In'

    @staticmethod
    def reloadCatalogue():
        GiveToPage.Catalogue = [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']}
                                for manga in app.db.Catalogue.find({})]

    @staticmethod
    def get_dictionary():
        return {'Catalogue': GiveToPage.Catalogue, 'User': GiveToPage.User}

    @staticmethod
    def get_dictionaryWithoutCatalogue():
        return {'User': GiveToPage.User}


@app.route('/')
def outputCatalogue():
    return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())


@app.route('/addElement', methods=['GET', 'POST'])
def addToMewMangaCatalogue():
    if request.method == 'POST':
        try:
            title = request.form.get("title")
            description = request.form.get("description")
            img_base64 = base64.b64encode(request.files.get('image').read())

            if not title or not description or not description or not img_base64 or app.db.Catalogue.find_one(
                    {"title": title}):
                return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())
            app.db.Catalogue.insert_one(
                {"title": title, "description": description, "image": 'data:;base64,' + str(img_base64)[2:-1]})
            GiveToPage.reloadCatalogue()
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())
        except:
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())


@app.route('/deleteElement', methods=['GET', 'POST'])
def deleteFromMewMangaCatalogueByTitle():
    if request.method == 'POST':
        try:
            title = request.form.get("titleDel")
            if not title or not app.db.Catalogue.find_one({"title": title}):
                return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())
            app.db.Catalogue.delete_one({"title": title})
            GiveToPage.reloadCatalogue()
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())
        except:
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())


@app.route('/updateElement', methods=['GET', 'POST'])
def updateFromMewMangaCatalogueByTitle():
    if request.method == 'POST':
        try:
            findByTitle = request.form.get("findByTitle")
            if not findByTitle or not app.db.Catalogue.find_one({"title": findByTitle}):
                return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())

            newTitle = request.form.get("newTitle")
            newDescription = request.form.get("newDescription")
            newImage = base64.b64encode(request.files.get('newImage').read())
            if newImage:
                app.db.Catalogue.update_one({"title": findByTitle},
                                            {"$set": {"image": 'data:;base64,' + str(newImage)[2:-1]}})
            if newDescription:
                app.db.Catalogue.update_one({"title": findByTitle}, {"$set": {"description": newDescription}})

            if newTitle:
                app.db.Catalogue.update_one({"title": findByTitle}, {"$set": {"title": newTitle}})

            GiveToPage.reloadCatalogue()
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())
        except:
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())


@app.route('/registration', methods=['GET', 'POST'])
def addToMangaShelfUsers():
    if request.method == 'POST':
        try:
            name = request.form.get("name")
            password = request.form.get("password")
            if not name or not password or app.db.Users.find_one({"name": name}):
                return render_template('MangaShelf.html')
            app.db.Users.insert_one({"name": name, "password": password})
            GiveToPage.User = name
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())
        except:
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())


@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'POST':
        try:
            name = request.form.get("login")
            password = request.form.get("password")
            if not name or not password or not app.db.Users.find_one({"name": name, "password": password}):
                return render_template('MangaShelf.html')
            GiveToPage.User = name
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())
        except:
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())


@app.route('/about')
def about():
    return render_template('About.html', entry=GiveToPage.get_dictionaryWithoutCatalogue())


@app.route('/main')
def main():
    return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())


if __name__ == '__main__':
    app.run(debug=True)
