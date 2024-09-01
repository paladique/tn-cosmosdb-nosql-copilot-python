from .models import CacheItem

def check_cache(prompt):
    return CacheItem.objects.filter(prompts=prompt).first()

def save_to_cache(vectors, prompt, completion):
    cache_item = CacheItem(vectors=vectors, prompts=prompt, completion=completion)
    cache_item.save()
    return cache_item
