from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Session, Message, CacheItem
from django.views.decorators.csrf import csrf_exempt
from django.template import loader

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
