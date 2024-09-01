# Create your models here.
from django.db import models
from django.utils import timezone
import uuid

# CacheItem Model
class CacheItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vectors = models.JSONField()  # Storing the vectors as a JSON list of floats
    prompts = models.TextField()
    completion = models.TextField()

    def __str__(self):
        return f'CacheItem {self.id}'

# Message Model
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50, default='Message')
    session = models.ForeignKey('Session', related_name='messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    prompt = models.TextField()
    prompt_tokens = models.IntegerField()
    completion = models.TextField(blank=True, null=True)
    completion_tokens = models.IntegerField(default=0)

    def __str__(self):
        return f'Message {self.id} in Session {self.session.id}'

# Session Model
class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50, default='Session')
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    tokens = models.IntegerField(default=0, null=True, blank=True)
    name = models.CharField(max_length=100, default='New Chat')

    def __str__(self):
        return f'Session {self.id}'

    def add_message(self, prompt, prompt_tokens, completion='', completion_tokens=0):
        message = Message(
            session=self,
            prompt=prompt,
            prompt_tokens=prompt_tokens,
            completion=completion,
            completion_tokens=completion_tokens
        )
        message.save()
        self.tokens += prompt_tokens + completion_tokens
        self.save()

    def update_message(self, message_id, prompt=None, completion=None, completion_tokens=None):
        message = self.messages.get(id=message_id)
        if prompt is not None:
            message.prompt = prompt
        if completion is not None:
            message.completion = completion
        if completion_tokens is not None:
            self.tokens += completion_tokens - message.completion_tokens
            message.completion_tokens = completion_tokens
        message.save()
        self.save()
