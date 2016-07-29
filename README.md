# Waartaa demo at Flock 2016

## Dependencies

- python 3.5
- node


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
./lounge/index.js
```
