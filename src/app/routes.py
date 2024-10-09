from flask import Blueprint, Flask, render_template, current_app, redirect, url_for, request, render_template, session
import uuid

app = Blueprint('app', __name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Create a new session
@app.route('/session/create/', methods=['GET'])
def create_session():
    # session = Session.objects.create(name="User Chat Session")
    return render_template('session_detail.html', session_id=session.session_id)
