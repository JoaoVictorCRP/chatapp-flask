from flask import Flask, render_template
from flask import request, redirect, url_for 
from flask_socketio import SocketIO # Comunicação bidirecional
from flask_socketio import join_room

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))
    
@socketio.on('join_room') # Evento de entrar na sala
def join_room_event(data):
    app.logger.info(f'{data["username"]} entrou na sala {data["room"]}') # Logando informação
    join_room(data['room'])
    socketio.emit('anuncio_de_entrada', data)
    

if __name__ == '__main__':
    socketio.run(app, debug=True)