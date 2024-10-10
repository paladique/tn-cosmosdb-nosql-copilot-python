from flask import Blueprint, Flask, jsonify, render_template, current_app, redirect, url_for, request, render_template, session
import uuid
from .models import Session, Message, CacheItem


app = Blueprint('app', __name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Create a new session
@app.route('/session/create/', methods=['GET'])
def create_session():
    session = Session()
    return render_template('session_detail.html', session_id=session.session_id)

@app.route('/generate_response/<session_id>', methods=['POST'])
def generate_response(session_id):
    data = request.json
    user_input = data.get('user_input')

    message = Message(session_id=session_id, prompt=user_input)
    message.generate_completion()

    # Generate a response (this is just a placeholder, replace with your actual logic)
    response = f"Generated response: {message.completion}"

      # Track tokens
    # prompt_tokens = len(user_input.split())
    # response_tokens = len(generated_text.split())
    # session.add_message(
    #     prompt=user_input,
    #     prompt_tokens=prompt_tokens,
    #     completion=generated_text,
    #     completion_tokens=response_tokens
    # )
    # Save the message to Cosmos DB
    message = Message(
        session_id=session_id,
        prompt=user_input,
        prompt_tokens=len(user_input.split()),
        completion=response,
        completion_tokens=len(response.split())
    )

    # generated_text = message.generate_completion()

    # Save to cache
    # CacheItem(
    #     prompts=user_input,
    #     completion=generated_text
    # ).save()

  


    message.save()

    return jsonify({'response': response})