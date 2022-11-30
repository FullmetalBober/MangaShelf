from flask import Flask, render_template, request
from pymongo import MongoClient
from base64 import b64encode
from math import ceil

app = Flask(__name__)
client = MongoClient('mongodb+srv://RAK_MANIAK:123370@mangashelf.3ortmjy.mongodb.net/test')
app.db = client.MangaShelf


class GiveToPage:
    @staticmethod
    def getDefaultUserName():
        return 'Sign In'

    CataloguePage = 1
    CataloguePageCount = 8
    CataloguePages = ceil(app.db.Catalogue.count_documents({}) / CataloguePageCount) + 1
    Catalogue = [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']} for manga in
                 app.db.Catalogue.find({}).limit(CataloguePage * CataloguePageCount)]
    SavesCatalogues = [(CataloguePage, Catalogue)]
    User = getDefaultUserName()
    UserLogin = False

    @staticmethod
    def updateCataloguePages():
        GiveToPage.CataloguePages = ceil(app.db.Catalogue.count_documents({}) / GiveToPage.CataloguePageCount) + 1

    @staticmethod
    def addSaveCatalogue():
        if len(GiveToPage.SavesCatalogues) == 5:
            GiveToPage.SavesCatalogues.pop(0)
        if GiveToPage.CataloguePage not in [i[0] for i in GiveToPage.SavesCatalogues]:
            GiveToPage.SavesCatalogues.append((GiveToPage.CataloguePage, GiveToPage.Catalogue))

    @staticmethod
    def removeSaveCatalogue():
        GiveToPage.SavesCatalogues.pop([i[0] for i in GiveToPage.SavesCatalogues].index(GiveToPage.CataloguePage))

    @staticmethod
    def getSaveCatalogue():
        for i in GiveToPage.SavesCatalogues:
            if i[0] == GiveToPage.CataloguePage:
                return i[1]

    @staticmethod
    def reloadCatalogue(page=CataloguePage, update=False):
        if update:
            GiveToPage.removeSaveCatalogue()
        GiveToPage.updateCataloguePages()
        GiveToPage.CataloguePage = page
        save = GiveToPage.getSaveCatalogue()
        if save:
            GiveToPage.Catalogue = save
        else:
            GiveToPage.Catalogue = [{'title': manga['title'], 'description': manga['description'], 'image': manga['image']}
                                for manga in app.db.Catalogue.find({}).skip((page - 1) * GiveToPage.CataloguePageCount).limit(GiveToPage.CataloguePageCount)]
            GiveToPage.addSaveCatalogue()

    @staticmethod
    def setUserName(newUserName):
        GiveToPage.User = newUserName
        if newUserName != GiveToPage.getDefaultUserName():
            GiveToPage.UserLogin = True
        else:
            GiveToPage.UserLogin = False

    @staticmethod
    def get_dictionary():
        return {'Catalogue': GiveToPage.Catalogue, 'User': GiveToPage.User, 'UserLogin': GiveToPage.UserLogin, 'CataloguePages': GiveToPage.CataloguePages, 'CataloguePage': GiveToPage.CataloguePage}

    @staticmethod
    def get_dictionaryWithoutCatalogue():
        return {'User': GiveToPage.User}

    @staticmethod
    def get_dictionaryForMangaPage(title):
        manga = app.db.Catalogue.find_one({'title': title})
        return {'Manga': manga, 'User': GiveToPage.User, 'UserLogin': GiveToPage.UserLogin}


@app.route('/')
def outputCatalogue():
    return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())

@app.route('/mangaPage/<mangaName>')
def outputMangaPage(mangaName):
    return render_template('mangaPage.html', entry=GiveToPage.get_dictionaryForMangaPage(mangaName))

@app.route('/page:<int:page>')
def outputCataloguePage(page):
    GiveToPage.reloadCatalogue(page)
    return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())

@app.route('/page:Previous')
def outputCataloguePagePrevious():
    if GiveToPage.CataloguePage > 1:
        GiveToPage.reloadCatalogue(GiveToPage.CataloguePage - 1)
    return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())

@app.route('/page:Next')
def outputCataloguePageNext():
    if GiveToPage.CataloguePage + 1 < GiveToPage.CataloguePages:
        GiveToPage.reloadCatalogue(GiveToPage.CataloguePage + 1)
    return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())

@app.route('/addElement', methods=['GET', 'POST'])
def addToMewMangaCatalogue():
    if request.method == 'POST':
        try:
            title = request.form.get("title")
            description = request.form.get("description")
            img_base64 = b64encode(request.files.get('image').read())

            if not title or not description or not description or not img_base64 or app.db.Catalogue.find_one(
                    {"title": title}):
                return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())
            app.db.Catalogue.insert_one(
                {"title": title, "description": description, "image": 'data:;base64,' + str(img_base64)[2:-1]})
            GiveToPage.reloadCatalogue(GiveToPage.CataloguePage, True)
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
            GiveToPage.reloadCatalogue(GiveToPage.CataloguePage, True)
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
            newImage = b64encode(request.files.get('newImage').read())
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
            GiveToPage.setUserName(name)
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
            GiveToPage.setUserName(name)
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())
        except:
            return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    GiveToPage.setUserName(GiveToPage.getDefaultUserName())
    return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())

@app.route('/about')
def about():
    return render_template('About.html', entry=GiveToPage.get_dictionaryWithoutCatalogue())


@app.route('/main')
def main():
    return render_template('MangaShelf.html', entry=GiveToPage.get_dictionary())

@app.route('/mangaPage')
def mangaPage():
    return render_template('mangaPage.html', entry=GiveToPage.get_dictionary())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
