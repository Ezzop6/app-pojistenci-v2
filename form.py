from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, widgets, StringField, PasswordField, SubmitField, DateField, validators,ValidationError
from databaze import DbUsers
import datetime
db_user = DbUsers()
forbidden_words = ["admin","root","administrator"]
forrbiden_letters = "!@#$%^&*()_+{}|:<>?/.,;'[]\=-`~"

class CustomTest:
    @staticmethod
    def contains_rorbidden_letters(data):
        for letter in data:
            if letter in forrbiden_letters:
                return True
            
    def contains_digit(data):
        for letter in data:
            if letter.isdigit():
                return True
    
class LoginForm(FlaskForm):
    login = StringField("Login", widget = widgets.Input(input_type = "text"),
        render_kw={"placeholder": "Uživatelské jméno"},
        validators=[validators.DataRequired(message="Musíte zadat login"),
                    validators.Length(min=3, max=20, message="Login musí mít 3 až 20 znaků")])
    password = PasswordField("Heslo", widget = widgets.Input(input_type = "password"),
        render_kw={"placeholder": "Heslo"},
        validators=[validators.DataRequired(message="Musíte zadat heslo"),
                    validators.Length(min=4, message="Heslo musí mít minimálně 4 znaků")])
    submit = SubmitField("Přihlásit se")
    
    def validate_login(self, login):
        login = login.data
        if not db_user.check_if_login_exists(login):
            raise ValidationError(f"Login: {login} neexistuje")
        
    def validate_password(self, password):
        login = self.login.data
        password = password.data
        if not db_user.try_login(login, password):
            raise ValidationError("Špatné heslo")

class EditProductForm(FlaskForm):
    name = StringField("Název", widget = widgets.Input(input_type = "text"),render_kw = {"placeholder": "Název"})
    description = StringField("Popis", widget = widgets.Input(input_type = "text"),render_kw = {"placeholder": "Popis"})
    price_per_month = IntegerField("Cena", widget = widgets.Input(input_type = "number"),render_kw = {"placeholder": "Cena"},default = 0)
    submit = SubmitField("Uložit")
    
class YesNoForm(FlaskForm):
    yes = SubmitField("Ano")
    no = SubmitField("Ne")
    
class CompleteRegisterForm(FlaskForm):
    name = StringField("Jméno", widget = widgets.Input(input_type = "text"),
                        render_kw = {"placeholder": "Jméno"},
                        validators=[validators.DataRequired(message="Musíte zadat jméno"),
                                    validators.Length(min=2, max=20, message="Jméno musí mít 2 až 20 znaků")])
    surname = StringField("Příjmení", widget = widgets.Input(input_type = "text"),
                        render_kw = {"placeholder": "Příjmení"},
                        validators=[validators.DataRequired(message="Musíte zadat příjmení"),
                                    validators.Length(min=2, max=20, message="Příjmení musí mít 2 až 20 znaků")])
    birt_date = DateField("Datum narození", widget = widgets.Input(input_type = "date"),
                        render_kw = {"placeholder": "Datum narození "},
                        validators=[validators.DataRequired(message="Musíte zadat datum narození")])
    submit = SubmitField("Uložit")
    
    def validate_name(self, name):
        name = name.data
        if name in forbidden_words:
            raise ValidationError(f"nesmíš použít toto jméno: {name}")
        if CustomTest.contains_rorbidden_letters(name):
            raise ValidationError(f"nesmíš použít tyto znaky v jménu: {forrbiden_letters}")
        if CustomTest.contains_digit(name):
            raise ValidationError(f"nesmíš použít číslice v jménu: {name}")
        
    def validate_surname(self, surname):
        surname = surname.data
        if surname in forbidden_words:
            raise ValidationError(f"nesmíš použít toto příjmení: {surname}")
        if CustomTest.contains_rorbidden_letters(surname):
            raise ValidationError(f"nesmíš použít tyto znaky v  příjmení: {forrbiden_letters}")
        if CustomTest.contains_digit(surname):
            raise ValidationError(f"nesmíš použít číslice v příjmení: {surname}")
        
    def validate_birt_date(self, birt_date):
        birt_date = birt_date.data
        if birt_date > datetime.date.today():
            raise ValidationError(f"Sorry tahle aplikace nepodporuje cesty časem: {birt_date}")
        
        
class RegisterForm(FlaskForm):
    login = StringField("Login", widget=widgets.Input(input_type = "text"),
        render_kw = {"placeholder": "Uživatelské jméno"}, 
        validators=[validators.DataRequired(message="Musíte zadat login"),
                    validators.Length(min=3, max=20, message="Login musí mít 3 až 20 znaků")])
    password = PasswordField("Heslo", widget=widgets.Input(input_type = "password"),
        render_kw = {"placeholder": "Heslo"}, 
        validators = [validators.DataRequired(message="Musíte zadat heslo")])
    password2 = PasswordField("Zopakujte heslo", widget = widgets.Input(input_type = "password"),
        render_kw={"placeholder": "Zopakujte heslo"},
        validators=[validators.DataRequired(message="Musíte zadat heslo")])
    submit = SubmitField("Registrovat se")
    
    def validate_login(self, login):
        login = login.data
        if login in forbidden_words:
            raise ValidationError(f"nesmíš použít tento login: {login}")
        if db_user.check_if_login_exists(login) != None:
            raise ValidationError(f"Uživatel s loginem {login} již existuje")
    
    def validate_password(self, password):
        password = password.data
        special_characters = "!@#$%^&*()_+|:<>?[]\;',./`~ěščřžýáíéúůťďňóĚŠČŘŽÝÁÍÉÚŮŤĎŇÓ"
        min_length = 8
        digit = sum(1 for letter in password if letter.isdigit())
        special = sum(1 for letter in password if letter in special_characters)
        small_letter = sum(1 for letter in password if letter.islower())
        big_letter = sum(1 for letter in password if letter.isupper())
        
        if min_length > len(password):
            raise ValidationError(f"Heslo musí mít minimálně {min_length} znaků")
        elif digit == 0:
            raise ValidationError("Heslo musí obsahovat alespoň jedno číslo")
        elif special == 0:
            raise ValidationError("Heslo musí obsahovat alespoň jeden speciální znak")
        elif small_letter == 0:
            raise ValidationError("Heslo musí obsahovat alespoň jedno malé písmeno")
        elif big_letter == 0:
            raise ValidationError("Heslo musí obsahovat alespoň jedno velké písmeno")
        elif password != self.password2.data:
            raise ValidationError("Hesla se neshodují")
        