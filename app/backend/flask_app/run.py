from src.config import Config
from src.app import create_app, celery

app = create_app(Config)

if __name__ == "__main__":
    # with ssl cert
    #app.run(host=Config.APP_HOST_IP, debug=Config.FLASK_DEBUG, ssl_context=('/app/backend/flask_app/ssl-certificates/server.crt', '/app/backend/flask_app/ssl-certificates/server.key'))

    #without ssl cert
    app.run(host=Config.APP_HOST_IP, debug=Config.FLASK_DEBUG, port=Config.APP_HOST_PORT)
