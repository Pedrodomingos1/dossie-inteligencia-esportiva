import os
from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from scraper import get_daily_games, get_game_statistics

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_default_secret_key_for_development')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dossie.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from models import User, Dossier

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    games = get_daily_games()
    dossiers = Dossier.query.filter_by(user_id=current_user.id).order_by(Dossier.created_at.desc()).all()
    return render_template('index.html', games=games, dossiers=dossiers)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dossier/generate/<event_id>/<game_name>')
@login_required
def generate_dossier(event_id, game_name):
    stats = get_game_statistics(event_id)
    if not stats:
        flash('Could not retrieve statistics for this game.', 'danger')
        return redirect(url_for('dashboard'))

    new_dossier = Dossier(
        event_id=event_id,
        game_name=game_name,
        statistics=stats,
        user_id=current_user.id
    )
    db.session.add(new_dossier)
    db.session.commit()
    
    flash('Dossier generated successfully!', 'success')
    return redirect(url_for('view_dossier', dossier_id=new_dossier.id))

@app.route('/dossier/view/<int:dossier_id>')
@login_required
def view_dossier(dossier_id):
    dossier = Dossier.query.get_or_404(dossier_id)
    if dossier.user_id != current_user.id:
        flash('You are not authorized to view this dossier.', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('jogo.html', dossier=dossier)

if __name__ == '__main__':
    app.run(debug=True)
