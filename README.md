# Waartaa demo at Flock 2016

## Dependencies

- python 3.5
- node
- nginx


## System configuration

### nginx
```
sudo cp nginx/demo.waartaa.com.conf /etc/nginx/conf.d/
sudo service nginx restart
```

### hosts

Edit ``/etc/hosts`` to point ``demo.waartaa.com``, ``chat.waartaa.com`` to
``127.0.0.1``

## Install

### webapp

```
pip install -r requirements.txt
cd webapp
touch ircb.db
```

### chat app

```
cd lounge
npm install
```

## Run

### ircb

``IRCB_SETTING=ircb.settings.py ircb run server -m allinone --port 11000``

### webapp
```
python webapp/app.py
```

### chat application
```
./lounge/index.js add admin
cp config.js ~/.lounge/config.js
./lounge/index.js
```
