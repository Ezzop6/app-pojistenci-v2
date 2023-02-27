from flask import Flask, render_template, request, redirect, url_for, g, session, abort
from flask_login import current_user, login_required, LoginManager, UserMixin, login_user, logout_user
import os
from databaze import DbUsers, DbProducts
from functools import wraps

from form import *
from customtools.tools import *
from customtools.vtipky import error_page_joke


app = Flask(__name__)
app.config["SECRET_KEY"] = random_secret_key()
app.config['PERMANENT_SESSION_LIFETIME'] = 60000
login_manager = LoginManager()
login_manager.init_app(app)

db_user = DbUsers()
db_product = DbProducts()

class User(UserMixin):
    def __init__(self, login):
        self.id = db_user.get_user_id(login)
        user_id = self.id
        self.role = db_user.get_user_role(user_id)
        self.user_data = db_user.get_user_data(user_id)

def role_required(role):
    '''Requires login with the specified role '''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not (current_user.role == "user" or current_user.role == 'admin'):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.errorhandler(404)
def access_denied(error):
    message = error_page_joke("404")
    return render_template('404.html',error = error, message = message)

@app.errorhandler(403)
def access_denied(error):
    message = error_page_joke("403")
    return render_template('403.html',error = error, message = message)

@app.errorhandler(401)
def access_denied(error):
    message = error_page_joke("401")
    return render_template('401.html',error = error, message = message)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.before_request
def before_request():
    g.user = None
    if "user" in session:
        g.user = session["user"]

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        cprint("validace v poradku clicked")

        return render_template('index.html')
    return render_template('login.html', form_login = form_login)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form_register = RegisterForm()
    if form_register.validate_on_submit():
        return redirect(url_for('complete_registration', login = form_register.login.data))
    return render_template('register.html',form_register = form_register)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index_page'))

@app.route('/register/<login>', methods=['GET', 'POST'])
@login_required
@role_required("user")
def complete_registration(login):
    form_complete_register = CompleteRegisterForm()
    if form_complete_register.validate_on_submit():
        print(current_user.id)
        db_user.update_user_data(current_user.id, form_complete_register.name.data, form_complete_register.surname.data)
        cprint("validace v poradku clicked") 
    return render_template('complete_registration.html', 
                        login = login, 
                        user = db_user.get_user_data(current_user.id), 
                        form_complete_register = form_complete_register)


@app.route('/login_test_user')
def login_test_user():
    return redirect(url_for('index_page'))







@app.route('/user', methods=['GET', 'POST'])
@login_required
@role_required("user")
def user_page():
    return render_template('user.html',user = db_user.get_user_data(current_user.id))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def admin_page():
    return render_template('admin.html')

@app.route('/admin/edit_product', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def edit_products_page():
    new_produkt = EditProductForm()
    products = db_product.get_all_products()
    return render_template('all_products.html', form = new_produkt, products = products)


@app.route('/base', methods=['GET', 'POST'])
def base_page():
    '''Tato stranka je pouze pro testovani'''
    return render_template('base.html')




@app.route('/admin/edit_product/<id>', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def edit_product(id):

    return render_template('edit_product.html', product = product, form = edited_product)


@app.route('/admin/delete/<id>', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def delete_product(id):
    form = YesNoForm()
    product = db_product.get_product_by_name(id)
    if form.validate_on_submit():
        if form.yes.data == True:
            db_product.delete_product(id)
            return redirect(url_for('edit_products_page'))
        else: return redirect(url_for('edit_products_page'))
    return render_template('delete_product.html', product = product , form = form)

# @app.route('/test', methods=['GET', 'POST'])
# def test_page():
#     form_login = LoginForm()
#     register_form = RegisterForm()
#     if form_login.validate_on_submit():
#         cprint("validace form_login v poradku clicked")
#     if register_form.validate_on_submit():
#         cprint("validace register_form v poradku clicked")
    
#     return render_template('form_testing.html',
#                             form_login = form_login,
#                             form_register = register_form,
#                             login_error = form_login.errors,
#                             register_error = register_form.errors)



if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.debug = True
    app.run(host=host, port=port)