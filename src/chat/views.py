# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Session, Message, CacheItem
from django.views.decorators.csrf import csrf_exempt
from django.template import loader

def create_session(request):
    # Create a new session
    session = Session.objects.create(name="User Chat Session")
    return render(request, '/session_detail.html', {'session': session})

def add_message(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    # Add a message to the session
    message = Message.objects.create(
        session_id=session.id,
        prompt="Hello, how are you?",
        prompt_tokens=5,
        completion="I'm fine, thank you!",
        completion_tokens=5
    )
    session.add_message(message)
    return render(request, '/session_detail.html', {'session': session, 'message': message})

def update_message(request, session_id, message_id):
    session = get_object_or_404(Session, id=session_id)
    message = get_object_or_404(Message, id=message_id)
    # Update the message
    session.update_message(message)
    return render(request, '/session_detail.html', {'session': session, 'message': message})

def check_and_cache(request):
    # Check if a similar prompt exists in the cache
    cache_item = CacheItem.objects.filter(prompts="Hello, how are you?").first()
    if cache_item:
        completion = cache_item.completion
    else:
        generated_completion = "I'm fine, thank you!"
        cache_item = CacheItem(vectors=[0.1, 0.2, 0.3], prompts="Hello, how are you?", completion=generated_completion)
        cache_item.save()
    return render(request, '/cache_detail.html', {'cache_item': cache_item})


def index(request):
    template = loader.get_template('/home.html')
    return HttpResponse(template.render())