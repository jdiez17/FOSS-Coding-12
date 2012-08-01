# euskalMap API Server
The config file is in euskalmap/config.ini. You can create one by copying the configuration example, euskalmap/config.ini.example.

## Standalone
To run the server, just run ```python app.py```.

## gunicorn
You can run the server with gunicorn with ```gunicorn -w 4 -b 0.0.0.0:5000 app:app```.
