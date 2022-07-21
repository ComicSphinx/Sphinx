# @Author: Daniil Maslov (ComicSphinx)

from flask import Flask, redirect, url_for, request, session
from flask.templating import render_template
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_sslify import SSLify
from Models import db, BudgetFields, Budget
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
migrate = Migrate(app, db)
api = Api(app)
sslify = SSLify(app)
db.init_app(app)
app.secret_key = "b'z\x8a#\n8\x06\xe2\xd5\xe7\xba\x0c\xbc\xc6\x1d&*'"

class BudgetService(Resource):
    #TODO: надо авторизацию будет намутить
    @app.route('/budget', methods=['GET', 'POST'])
    def budget():
        if request.method == 'GET':
            return render_template('budget.html') # TODO: и надо вернуть в шаблон данные
        elif requset.method == 'POST'