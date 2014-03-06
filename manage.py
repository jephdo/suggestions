from suggestions.app import app
from suggestions import models

if __name__ == '__main__':
    models.create_all()

    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8080, app)
    print('Serving at localhost on port 8080...')
    server.serve_forever()