from flask import Flask

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')

from app.routes import *

if __name__ == '__main__':
    app.run(debug=True)