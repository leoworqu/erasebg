from datetime import timedelta
import secrets
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '46af1a55a3a392bdb12d4658e9a96e7'
app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(hours=0.1)


from BGremove import routes