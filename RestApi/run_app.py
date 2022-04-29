from flask import Flask

app = Flask(__name__)

from blueprint.user import user

app.register_blueprint(user)

if __name__ == "__main__":
    app.run(debug=True)