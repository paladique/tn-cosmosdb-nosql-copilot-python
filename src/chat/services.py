from .models import CacheItem
from azure.cosmos import CosmosClient, PartitionKey, exceptions

def check_cache(prompt):
    return CacheItem.objects.filter(prompts=prompt).first()

def save_to_cache(vectors, prompt, completion):
    cache_item = CacheItem(vectors=vectors, prompts=prompt, completion=completion)
    cache_item.save()
    return cache_item


# Initialize the Cosmos client
def get_cosmos_client():
    endpoint = "your-cosmosdb-endpoint"
    key = "your-cosmosdb-key"
    client = CosmosClient(endpoint, key)
    return client

def get_database():
    client = get_cosmos_client()
    database_name = "your-database-name"
    return client.get_database_client(database_name)

def get_container():
    database = get_database()
    container_name = "your-container-name"
    return database.get_container_client(container_name)

# Function to create or query items
def create_or_query_item(item_data):
    container = get_container()
    try:
        container.create_item(item_data)
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error creating item: {str(e)}")
