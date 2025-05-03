from flask import Flask
from controllers.auth_controller import auth
from dotenv import load_dotenv
import os

app = Flask(__name__) 
app.secret_key = os.getenv("SECRET_KEY")

# Register Blueprints
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)