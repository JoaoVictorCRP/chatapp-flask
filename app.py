from flask import Flask, render_template
from flask import request, redirect, url_for 
from flask_socketio import SocketIO
from flask_login import LoginManager , login_user, login_required, logout_user
from flask_login import current_user
from flask_socketio import join_room
# User object:
from user import check_user_password, User
import db
# Secret Key:
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = "login" # <- the page that an unlogged user will get when it tries to acess a login_required page
login_manager.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = db.get_user(username)
        if user and check_user_password(user.password, password_input):
            login_user(user)
            # app.logger.info(f'{current_user.username} is authenticated? {current_user.is_authenticated()}')
            return redirect(url_for('home'))
        else:
            message = 'Usuário/Senha incorreto.'
    return render_template('login.html', message=message)

@app.route("/register/", methods=['GET', 'POST'])
def register():
    message = ''
    if current_user.is_authenticated: # If user is already logged in, will redirect to index.
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('passwordConfirm')

        # Verification #1: do passwords match?
        if not password==password_confirm:
            return render_template('register.html', message='As senhas não coincidem.')
        
        # Verification #2: email exists?
        if(db.email_exists(email)):
            return render_template('register.html', message='Email já cadastrado.')

        new_user = User(username,email, password)
        db.save_user(new_user)
        message = 'Usuário registrado com sucesso!<br>Por favor, verique a caixa de entrada do seu e-mail para realizar a confirmação da sua conta.'
        return render_template('login.html', message=message)
    
    return render_template('register.html', message=message)
    

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))
    
@socketio.on('entrou_sala')
def join_room_event(data):
    room = data['room']
    join_room(room)
    socketio.emit('anuncio_de_entrada', data, room=data["room"])

@socketio.on('enviou_msg')
def send_msg_event(data):
    app.logger.info(f'{data["username"]} disse: "{data["message"]}" na sala {data["room"]}')
    socketio.emit('receber_msg', data, room=data['room'])

@socketio.on('apertou_sair')
def leave_room(data):
    try:
        username = data.get("username")
        room = data.get("room")
        if username and room:
            app.logger.info(f'{username} saiu da sala {room}')
            socketio.emit('anuncio_de_saida', data, room=room)
        else:
            app.logger.error("Dados incompletos: 'username' ou 'room' faltando")
    except Exception as e:
            app.logger.error(f"Erro ao processar saída da sala: {e}")

@login_manager.user_loader
def load_user(username):
    return db.get_user(username)

if __name__ == '__main__':
    socketio.run(app, debug=True)