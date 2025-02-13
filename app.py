from flask import Flask , render_template , flash,redirect, url_for
from forms  import RegisterForm , LoginForm
from models import db, User
from flask_bcrypt import Bcrypt

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'FJALKDJFSDY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dbpass@localhost:5432/Flask_auth_db'
    bcrypt = Bcrypt()

    db.init_app(app)
    bcrypt.init_app(app)


    with app.app_context():
        db.create_all()

   




    @app.route('/')
    def index():
        return render_template("home.html")
    
    @app.route('/login')
    def login():
        form = LoginForm()
        return render_template("login.html", form=form)
    
    @app.route('/register',methods=['GET','POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            hased_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                username = form.username.data,
                email = form.email.data,
                password = hased_password,
            )

            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!!','success')
            return redirect(url_for('login'))
        return render_template("register.html", form=form)
    
    return app
    
if __name__ == "__main__":
    app = create_app()
    app.run(debug = True, port=7000)