from flask import Flask, render_template
from flask import request, redirect, url_for 
from flask_socketio import SocketIO
from flask_login import LoginManager , login_user
from flask_socketio import join_room
import db
import user as u

login_manager = LoginManager()
app = Flask(__name__)
socketio = SocketIO(app)

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

        if user and u.check_user_password(user[-1], password_input):
            login_user(user) # FIXME: SQLITE query is returning a TUPLE... But it should return a User object, so we can use its methods.
            return redirect(url_for('home'))
        else:
            message = 'Usuário/Senha incorreto.'
    return render_template('login.html', message=message)


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

if __name__ == '__main__':
    login_manager.init_app(app)
    socketio.run(app, debug=True)