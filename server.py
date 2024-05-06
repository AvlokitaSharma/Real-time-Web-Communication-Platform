from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Ensure this directory exists
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit for uploads

socketio = SocketIO(app)
login_manager = LoginManager(app)

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    return User(username)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    return '', 400

@socketio.on('send_file')
def handle_file(json, methods=['GET', 'POST']):
    filename = json['filename']
    room = json['room']
    emit('receive_file', {'filename': filename, 'room': room}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
