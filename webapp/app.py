import json
import os
import subprocess

from flask import Flask, render_template, request, url_for, redirect, Response
from flask import session, g

from ircb.models.user import User
from ircb.models.network import Network
from ircb.models.channel import Channel
from ircb.models.lib import get_session

from forms import LoginForm, NetworkForm, RegisterForm
from session import RedisSessionInterface

from functools import wraps
import uuid

import conf
import lounge

app = Flask(__name__)
app.session_interface = RedisSessionInterface()

db = get_session()


def login_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if session.get('is_authenticated', False):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return decorated_func


def login_user(user):
    session['is_authenticated'] = True
    session['user_id'] = user.id
    session['username'] = user.username
    g.user = user


def logout_user():
    session.clear()
    g.user = None


class AnonymousUser(object):
    def __init__(self):
        self.is_authenticated = False
        self.id = str(uuid.uuid4().hex[:10])
        self.is_anonymous = True


@app.before_request
def load_user():
    if session.get("user_id"):
        user = db.query(User).filter(User.id == session['user_id']).first()
    else:
        user = AnonymousUser()  # Make it better, use an anonymous User instead

    g.user = user


@app.route('/', methods=['GET', 'POST'])
def index():
    if g.user and g.user.is_authenticated:
        return redirect(url_for('add_network'))
    form = LoginForm(request.form)
    rform = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.query(User).filter(User.username == username).first()
        if user and user.authenticate(password):
            login_user(user)
            return redirect(url_for('list_network'))
    return render_template('index.html', form=form, rform=rform)


@app.route('/list-network', methods=['GET', 'POST'])
@login_required
def list_network():
    networks = db.query(Network).filter(Network.user_id == g.user.id).all()
    payload = []
    for network in networks:
        channels = db.query(Channel).filter(
            Channel.network_id == network.id).all()
        channel_names = [c.name for c in channels]
        if channel_names:
            payload.append({
                'network': network.name,
                'channels': channel_names
            })

    print(payload)
    return render_template('network_list.html', payload=payload)


@app.route('/network/<network>/channel/<channel>', methods=['GET'])
@login_required
def channel_details(network, channel):
    network = db.query(Network).filter(
        Network.user_id == g.user.id,
        Network.name == network).one()
    channel = db.query(Channel).filter(
        Channel.name == '#' + channel,
        Channel.network_id == network.id
    ).one()
    return render_template('channel_details.html', payload={
        'network': network,
        'channel': channel
    })


@app.route('/add-network', methods=['GET', 'POST'])
@login_required
def add_network():
    form = NetworkForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form.get('network')
        hostname = request.form.get('hostname')
        port = request.form.get('port')
        nickname = request.form.get('nick')
        realname = request.form.get('realname')
        channels = request.form.get('channels')

        user = g.user

        network = Network(
            name=name, nickname=nickname, hostname=hostname,
            port=port, realname=realname, username='',
            password='', usermode='0', ssl=False,
            ssl_verify='CERT_NONE', user_id=user.id
        )
        db.add(network)
        db.commit()
        data = {
            'name': network.name,
            'host': conf.IRCB_HOST,
            'port': conf.IRCB_PORT,
            'password': network.access_token,
            'nick': network.nickname,
            'username': g.user.username,
            'realname': network.realname,
            'join': channels
        }
        lounge.add_network(data, session)

        return redirect(url_for('list_network'))
    return render_template('network.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(username=username, email=email, password=password)
        db.add(user)
        db.commit()
        subprocess.check_output(
            [conf.LOUNGE_BINARY, 'add', user.username, password])

        if user and user.authenticate(password):
            login_user(user)
            return redirect(url_for('add_network'))


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    from ircb.models import create_tables
    create_tables()
    app.run(debug=True)
