from flask import Blueprint, render_template, request, redirect, url_for

from flask_login import login_user, logout_user, current_user

from app import db, login_manager

from app.models.user import User
from app.models.product import Product
from app.models.therapy import Therapy
from app.models.cart_product import Cart_Product
from app.models.cart_therapy import Cart_Therapy


# Instancia do Blueprint login
login = Blueprint('login', __name__,
                  template_folder="../../templates",
                  static_folder="../../static")


@login.route('/login', methods=['GET', 'POST'])
def log_user():
    if(request.method == 'GET'):
        return render_template('login/login.html')
    if(request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if(not user or not user.verify_password(password)):
            return render_template('login/login.html',
                                   error=True)
        else:
            login_user(user)
            user_id = current_user.get_id()
            user = User.query.get(user_id)
            user.set_age()
            db.session.commit()
            return redirect(url_for('home.index'))


@login.route('/logout', methods=['GET'])
def logout():
    if (request.method == 'GET'):
        logout_user()
        return redirect('/')


@login.route('/cart', methods=['GET'])
def cart():
    if (request.method == 'GET'):

        # Get current_user if it's authenticated
        user = current_user
        if(user):

            # Get all chart_products with user's id
            user_cart_products = user.products

            # Get all products objects that were in chart_products
            user_products = []
            for item in user_cart_products:
                product = Product.query.get(item.id_product)
                user_products.append(product)

            # Get all chart_therapies with user's id
            user_cart_therapies = user.therapies

            # Get all therapies objects that were in chart_therapies
            user_therapies = []
            for item in user_cart_therapies:
                therapy = Therapy.query.get(item.id_therapy)
                user_therapies.append(therapy)

        # Return the products and therapies
        return render_template('login/cart.html',
                               user_products=user_products,
                               user_therapies=user_therapies)


@login.route('/cart/delete/product/<product_id>', methods=['GET'])
def delete_product(product_id):
    if(request.method == 'GET'):
        user = current_user
        if(user):
            cart_id = Cart_Product.query.filter_by(id_user=user.id, id_product=int(product_id)).first()
            db.session.delete(cart_id)
            db.session.commit()
            return redirect(url_for('login.cart'))


@login.route('/cart/delete/therapy/<therapy_id>', methods=['GET'])
def delete_therapy(therapy_id):
    if(request.method == 'GET'):
        user = current_user
        if(user):
            cart_id = Cart_Therapy.query.filter_by(id_user=user.id, id_therapy=int(therapy_id)).first()
            db.session.delete(cart_id)
            db.session.commit()
            return redirect(url_for('login.cart'))


@login.route('/<user_email>/change_password', methods=['GET', 'POST'])
def change_password(user_email):
    if(request.method == 'GET'):
        return render_template('change_pwd.html')
    if(request.method == 'POST'):
        pwd = request.form['old_password']
        new_pwd = request.form['new_password']
        user = User.query.filter_by(email=user_email).first()
        if user and user.verify_password(pwd):
            user.password = new_pwd
            db.session.commit()
            return render_template('login/login.html')
        else:
            return render_template('login/login.html',
                                   error=True)


@login.route('/<user_email>/change_data', methods=['GET', 'POST'])
def change_data(user_email):
    if(request.method == 'GET'):
        return render_template('change_data.html')
    if(request.method == 'POST'):
        email = request.form['email']
        cep = request.form['cep']
        number = request.form['number']
        complement = request.form['complement']
        fname = request.form['fname']
        lname = request.form['lname']
        pwd = request.form['password']
        user = User.query.filter_by(email=user_email).first()
        if user and user.verify_password(pwd):
            user.email = email
            user.cep = cep
            user.number = number
            user.complement = complement
            user.fname = fname
            user.lname = lname
            try:
                if(user.set_Addres() is True):
                    db.session.commit()
                    return render_template('login/login.html')
            except Exception:
                return render_template('login/login.html',
                                       error=True)
        else:
            return render_template('login/login.html',
                                   error=True)


@login.route('/<user_email>/delete', methods=['GET', 'POST'])
def delete_user(user_email):
    if(request.method == 'GET'):
        return render_template('delete_account.html')
    if(request.method == 'POST'):
        pwd = request.form['password']
        user = User.query.filter_by(email=user_email).first()
        if user and user.verify_password(pwd):
            db.session.delete(user)
            db.session.commit()
            return render_template('index.html')
        else:
            return render_template('delete_account.html',
                                   check_error=True)
