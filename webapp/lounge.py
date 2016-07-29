from socketIO_client import SocketIO


def add_network(data, session):
    with SocketIO(
            'http://localhost', 9000, cookies={'session': session.sid}) as socketio:
        socketio.emit('open', None)
        socketio.emit('conn', data)
        socketio.emit('open', '1')
