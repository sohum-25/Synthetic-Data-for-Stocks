from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

# Function to generate and send random numbers
def generate_random_numbers():
    while True:
        random_number = random.randint(1, 100)
        socketio.emit('random_number', {'number': random_number})
        time.sleep(1)

# Thread for generating and sending random numbers
random_thread = threading.Thread(target=generate_random_numbers)
random_thread.daemon = True
random_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
