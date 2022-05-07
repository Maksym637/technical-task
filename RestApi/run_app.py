from blueprint.user import user
from app import app

app.register_blueprint(user)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')