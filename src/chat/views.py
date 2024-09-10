from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Session, Message, CacheItem
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import openai 
from dotenv import load_dotenv
import json
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
openai.api_key = os.getenv("api_key")

def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def create_session(request):
    # Create a new session
    session = Session.objects.create(name="User Chat Session")
    return redirect('session_detail', session_id=session.session_id)

def session_detail(request, session_id):
    session = get_object_or_404(Session, session_id=session_id)
    return render(request, 'session_detail.html', {'session': session})


 # Add a message to an existing session
@csrf_exempt
def add_message(request, session_id):
    session = get_object_or_404(Session, session_id=session_id)

    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        completion = request.POST.get('completion')
        prompt_tokens = len(prompt.split())
        completion_tokens = len(completion.split())

        session.add_message(
            prompt=prompt,
            prompt_tokens=prompt_tokens,
            completion=completion,
            completion_tokens=completion_tokens
        )
        
        # Redirect to the session detail page
        return redirect('session_detail', session_id=session.session_id)
    else:
        return render(request, 'session_detail.html', {'session': session})

@csrf_exempt
def generate_response(request, session_id):
    # Generate a response using OpenAI for a particular session
    session = get_object_or_404(Session, session_id=session_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('user_input')

            # Check if the user input exists in the cache
            cached_item = CacheItem.objects.filter(prompts=user_input).first()
            if cached_item:
                generated_text = cached_item.completion
            else:
                # Generate response using the OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # Adjust to your preferred GPT model
                    messages=[
                        {"role": "system", "content": "You are my coding assistant."},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                generated_text = response['choices'][0]['message']['content'].strip()

                # Save the new prompt and response in the cache
                CacheItem.objects.create(prompts=user_input, completion=generated_text)

            # Track tokens for the session
            prompt_tokens = len(user_input.split())
            response_tokens = len(generated_text.split())
            session.add_message(prompt=user_input, prompt_tokens=prompt_tokens, completion=generated_text, completion_tokens=response_tokens)

            return JsonResponse({'response': generated_text}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def chat_interface(request):
    return render(request, 'chat_interface.html')

def update_message(request, session_id, message_id):
    # Update an existing message in a session
    session = get_object_or_404(Session, session_id=session_id)
    message = get_object_or_404(Message, session_id=message_id)
    # Update the message
    session.update_message(message_id=message.id)
    return render(request, 'session_detail.html', {'session': session, 'message': message})

def check_and_cache(request):
    # Check if a similar prompt exists in the cache
    prompt = request.GET.get('prompt')
    cache_item = CacheItem.objects.filter(prompts=prompt).first()

    if cache_item:
        completion = cache_item.completion
    else:
        # Generate a mock completion or fallback response
        generated_completion = "I'm fine, thank you!"
        cache_item = CacheItem(prompts=prompt, completion=generated_completion)
        cache_item.save()

    return render(request, 'cache_detail.html', {'cache_item': cache_item})