from TsetlinMachineScripts import ChessTM
import socketio

sio = socketio.Client()

@sio.on('message')
def message(obj):
    data = "Some data"
    sio.emit('prediction',data)

@sio.event
def connect():
    print("Connected")

def Connect():
    try:
        sio.connect('http://localhost:80')
        sio.wait()
    except:
        print("Could not connect")

Connect()