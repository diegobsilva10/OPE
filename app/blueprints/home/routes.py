from flask import Blueprint, render_template, request


# Instancia do Blueprint home
home = Blueprint('home', __name__,
                 template_folder="../../html_teste",
                 static_folder="../../estaticos_teste")


# URL da homepage
@home.route('/', methods=['GET'])
def index():
    if(request.method == 'GET'):
        return render_template('index_teste.html')
