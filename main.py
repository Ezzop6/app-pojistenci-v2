from flask import Flask, render_template, request, redirect, url_for, g, session, abort
from flask_login import current_user, login_required, LoginManager, UserMixin, login_user, logout_user
import os
from databaze import DbUsers, DbProducts, DbUsersProducts
from functools import wraps

from form import *
from customtools.tools import *
from customtools.vtipky import error_page_joke


app = Flask(__name__)
app.config["SECRET_KEY"] = random_secret_key()
app.config['PERMANENT_SESSION_LIFETIME'] = 60000 # time to logout user
login_manager = LoginManager()
login_manager.init_app(app)

db_user = DbUsers()
db_product = DbProducts()
db_up = DbUsersProducts()
class User(UserMixin):
    def __init__(self, login):
        self.id = login
        self.role = db_user.get_user_role(login)
        self.login = db_user.get_user_login(login)

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

'''error pages'''
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
    '''Callback to reload the user object from the user ID stored in the session'''
    return User(user_id)

@app.before_request
def before_request():
    g.user = None
    if "user" in session:
        g.user = session["user"]
        
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index_page'))

@app.route('/')
def index_page():
    '''Main page'''
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    '''Login page'''
    form_login = LoginForm()
    if form_login.validate_on_submit():
        user_id = db_user.get_user_id(form_login.login.data)
        current_user = User(user_id)
        login_user(current_user)
        return render_template('index.html')
    return render_template('login.html', form_login = form_login)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    '''Register page'''
    form_register = RegisterForm()
    if form_register.validate_on_submit():
        db_user.add_user(form_register.login.data, form_register.password.data)
        user_id = db_user.get_user_id(form_register.login.data)
        current_user = User(user_id)
        login_user(current_user)
        return redirect(url_for('complete_registration', login = form_register.login.data))
    return render_template('register.html',
                        form_register = form_register)

@app.route('/register/<login>', methods=['GET', 'POST'])
@login_required
@role_required("user")
def complete_registration(login):
    '''Complete registration page'''
    form_complete_register = CompleteRegisterForm()
    if form_complete_register.validate_on_submit():
        user_id = db_user.get_user_id(login)
        db_user.update_user_name(user_id, form_complete_register.name.data)
        db_user.update_user_surname(user_id, form_complete_register.surname.data)
        db_user.update_user_birthdate(user_id, form_complete_register.birt_date.data)
        return redirect(url_for('index_page'))
    return render_template('complete_registration.html', 
                        login = login, 
                        user = db_user.get_user_data(current_user.id), 
                        form_complete_register = form_complete_register)

@app.route('/user/<login>', methods=['GET', 'POST'])
@login_required
@role_required("user")
def user_page(login):
    '''User page with user data and products'''
    user_form = EditUserDataForm()
    change_password_form = ChangePasswordForm()
    role_form = EditUserRoleForm()
    

    if request.method == 'POST' and 'user_form' in request.form:
        if user_form.validate_on_submit():
            for form, data in user_form.data.items():
                if form == "csrf_token" or form == "submit":
                    continue
                if data != "":
                    db_user.update_user_data(current_user.id, form, data)
            return redirect(url_for('user_page', login=login))

    if request.method == 'POST' and 'change_password_form' in request.form:
        if change_password_form.validate_on_submit():
            db_user.update_user_data(current_user.id, "password", change_password_form.password.data)

    return render_template('user.html', 
                        user = db_user.get_user_data(current_user.id),
                        user_form = user_form,
                        role_form = role_form,
                        change_password_form = change_password_form)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def admin_page():
    '''Admin page with fake user generator'''
    fake_user_generator = AddFakeUserForm()
    if fake_user_generator.validate_on_submit():
        db_user.create_fake_users(fake_user_generator.number_users.data)
    return render_template('admin.html', fake_user_generator = fake_user_generator)

@app.route('/admin/edit_product', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def edit_products_page():
    '''Admin page with products and form for adding new products
    edited products are saved to database'''
    new_produkt = EditProductsForm()
    products = db_product.get_all_products()
    if new_produkt.validate_on_submit():
        new_produkt = {"imgs_path":new_produkt.imgs_path.data,"name": new_produkt.name.data, "price": new_produkt.price_per_month.data, "description": new_produkt.description.data}
        db_product.add_product(new_produkt)
        return redirect(url_for('edit_products_page'))
    return render_template('all_products.html', new_produkt = new_produkt, products = products)

@app.route('/admin/edit_user', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def edit_users_page():
    users = db_user.get_all_users()

    return render_template('all_users.html', users = users)

@app.route('/admin/edit_user/<id>', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def edit_user(id):
    '''Admin page with form for editing users'''
    user_form = EditUserDataForm()
    change_password_form = ChangePasswordForm()
    role_form = EditUserRoleForm()
    user_id = id
    
    if request.method == 'POST' and 'user_form' in request.form:
        if user_form.validate_on_submit():
            for form, data in user_form.data.items():
                if form == "csrf_token" or form == "submit":
                    continue
                if data != "":
                    db_user.update_user_data(user_id, form, data)
                    
    if request.method == 'POST' and 'change_password_form' in request.form:
        if change_password_form.validate_on_submit():
            db_user.update_user_data(current_user.id, "password", change_password_form.password.data)

    if request.method == 'POST' and 'change_role_form' in request.form:
        if role_form.validate_on_submit():
            db_user.update_user_data(user_id, "role", role_form.role.data)
            cprint("Welcome new admin!")
            
    return render_template('user.html', user_form = user_form,
                        change_password_form = change_password_form,
                        role_form = role_form, 
                        user = db_user.get_user_data(user_id))

@app.route('/admin/edit_user/delete/<id>', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def delete_user(id):
    '''Admin page with form for editing users'''
    form = YesNoForm()
    user = db_user.get_user_data(id)
    if form.validate_on_submit():
        if form.yes.data:
            db_user.delete_user(id)
            return redirect(url_for('edit_users_page'))
        else: return redirect(url_for('edit_users_page'))
    return render_template('delete_product.html', product = user , form = form)

@app.route('/base', methods=['GET', 'POST'])
def base_page():
    '''base page for testing purposes'''
    return render_template('base.html')

@app.route('/admin/edit_product/<id>', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def edit_product(id):
    '''Admin page with form for editing products'''
    edited_product = EditProduct()
    product = db_product.get_product_by_name(id)
    edited_product.description.render_kw = {"placeholder": product["description"]}
    edited_product.price_per_month.render_kw = {"placeholder": product["price"]}
    if edited_product.validate_on_submit():
        db_product.add_product_imgs_path(id, edited_product.imgs_path.data)
        db_product.update_product(id, edited_product.description.data, edited_product.price_per_month.data)
        return redirect(url_for('edit_products_page'))
    return render_template('edit_product.html', product = product, form = edited_product)

@app.route('/admin/delete/<id>', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def delete_product(id):
    '''delete product page with confirmation'''
    form = YesNoForm()
    product = db_product.get_product_by_name(id)
    if form.validate_on_submit():
        if form.yes.data == True:
            db_product.delete_product(id)
            return redirect(url_for('edit_products_page'))
        else: return redirect(url_for('edit_products_page'))
    return render_template('delete_product.html', product = product , form = form)


# TODO remove this after development
@app.route('/login_test_user', methods=['GET', 'POST'])
def login_test_user():
    '''only for testing delete it after development'''
    log_this_account = 'admin'
    if log_this_account == 'user':
        current_user = User("63fdba6ee32d2888e837368a")#test user
    if log_this_account == 'admin':
        current_user = User("63fcd1d350ed7141f41f1a17")#admin
    login_user(current_user)
    return redirect(url_for('index_page'))



if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.debug = True #TODO remove this after development
    app.run(host=host, port=port)