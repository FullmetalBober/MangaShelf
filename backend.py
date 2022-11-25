# import cv2 as cv
from flask import Flask, render_template, request
# import numpy
from pymongo import MongoClient
from werkzeug.utils import secure_filename
# from models import Img

app = Flask(__name__)
client = MongoClient('mongodb+srv://RAK_MANIAK:Vlad123370@python-lab-11.2hfteul.mongodb.net/test')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
    #     pic = request.files['picture']
    #     if not pic:
    #         return render_template('MangaShelf.html')
    #     filename = secure_filename(pic.filename)
    #     mimetype = pic.mimetype
    #     img = Img(img=pic, mimetype=mimetype, filename=filename)
    #     return render_template('MangaShelf.html', img=img)

        # filestr = request.files.get('picture').read()
        # file_bytes = numpy.fromstring(filestr, numpy.uint8)
        # img = cv.imdecode(file_bytes, cv.IMREAD_UNCHANGED)
        # return render_template('MangaShelf.html', test=request.form.get('picture'))
        return render_template('MangaShelf.html', test=request.files.get('picture'))#Шось непонятне
    else:
        return render_template('MangaShelf.html', test='error')


if __name__ == '__main__':
    app.run(debug=True)
