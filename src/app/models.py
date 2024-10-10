from datetime import datetime, timezone
import uuid

# CacheItem Model
class CacheItem:
    def __init__(self, id, vectors, prompts, completion):
        self.id = id
        self.vectors = vectors
        self.prompts = prompts
        self.completion = completion
        self.created_at = datetime.now(timezone.utc).isoformat() # Timestamp for cache invalidation purposes

    def save(self):
        item = {
            'id': self.id,
            'vectors': self.vectors,
            'prompts': self.prompts,
            'completion': self.completion,
            'created_at': self.created_at
        }
        # cosmos_db.create_item(item)

    def __str__(self):
        return f'CacheItem {self.id} - Prompt: {self.prompts[:50]}'


# Message Model
# This model stores individual user prompts and OpenAI-generated responses within a session.
class Message:
    def __init__(self, session_id, prompt, prompt_tokens=0, completion='', completion_tokens=0):
        self.id = str(uuid.uuid4())
        self.session_id = session_id
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.prompt = prompt
        self.prompt_tokens = prompt_tokens
        self.completion = completion
        self.completion_tokens = completion_tokens

    def __str__(self):
        return f'Message {self.id} in Session {self.session.id} - Prompt: {self.prompt[:50]}'
    
    def save(self):
        item = {
            'id': self.id,
            'session_id': self.session_id,
            'timestamp': self.timestamp,
            'prompt': self.prompt,
            'prompt_tokens': self.prompt_tokens,
            'completion': self.completion,
            'completion_tokens': self.completion_tokens
        }
        # cosmos_db.create_item(item)

    def generate_completion(self):
        from .services import AIService
        ai_service = AIService()
        completion = self.completion = ai_service.get_completion(self.prompt)
        return completion
    

# Session Model
class Session:
     def __init__(self, session_id=None, tokens=None, name='New Chat'):
        self.session_id = session_id or str(uuid.uuid4())
        self.tokens = tokens or 0
        self.name = name

     def __str__(self):
        return f'Session {self.session_id} - {self.name}'

     def add_message(self, prompt, prompt_tokens, completion='', completion_tokens=0):
        # Create and save the message
        message = Message(
            session=self,
            prompt=prompt,
            prompt_tokens=prompt_tokens,
            completion=completion,
            completion_tokens=completion_tokens
        )
        message.save()

        # Update session tokens
        self.tokens = (self.tokens or 0) + prompt_tokens + completion_tokens
        self.save()

        def update_message(self, message_id, prompt=None, completion=None, completion_tokens=None):
            message = self.messages.get(id=message_id)
            if prompt is not None:
                message.prompt = prompt
            if completion is not None:
                message.completion = completion
            if completion_tokens is not None:
                self.tokens = (self.tokens or 0) + completion_tokens - message.completion_tokens
                message.completion_tokens = completion_tokens
            message.save()
            self.save()
