from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Session, Message, CacheItem
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import openai 
from openai import AzureOpenAI
from django.http import JsonResponse
import json
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Access the API key
openai.api_key = '93300d90b1e5406d919dc9c3e8d0a799'

def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def create_session(request):
    # Create a new session
    session = Session.objects.create(name="User Chat Session")
    return redirect('session_detail', session_id=session.id)

def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    return render(request, 'session_detail.html', {'session': session})

@csrf_exempt
def add_message(request, session_id):
    session = get_object_or_404(Session, id=session_id)

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
        return redirect('session_detail', session_id=session.id)
    else:
        return render(request, 'session_detail.html', {'session': session})

@csrf_exempt  # Allows POST requests without CSRF token (for dev only)
def generate_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('user_input')

            response = openai.chat.completions.create(
                model="gpt-4 0613",  # You can switch to gpt-4 if needed
                messages=[
                    {"role": "system", "content": "You are my coding assistant."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150,
                temperature=0.7,  # Controls randomness
            )
            print(response.choices[0].message.content)

            # Extract response from OpenAI API
            generated_text = response['choices'][0]['message']['content'].strip()
            return JsonResponse({'response': generated_text}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def chat_interface(request):
    return render(request, 'chat_interface.html')

def update_message(request, session_id, message_id):
    session = get_object_or_404(Session, id=session_id)
    message = get_object_or_404(Message, id=message_id)
    # Update the message
    session.update_message(message_id=message.id)
    return render(request, 'session_detail.html', {'session': session, 'message': message})

def check_and_cache(request):
    # Check if a similar prompt exists in the cache
    cache_item = CacheItem.objects.filter(prompts="Hello, how are you?").first()
    if cache_item:
        completion = cache_item.completion
    else:
        generated_completion = "I'm fine, thank you!"
        cache_item = CacheItem(vectors=[0.1, 0.2, 0.3], prompts="Hello, how are you?", completion=generated_completion)
        cache_item.save()
    return render(request, 'cache_detail.html', {'cache_item': cache_item})
