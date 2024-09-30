from .models import CacheItem
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from openai import AzureOpenAI
import os

# os.environ.get("NAME")

# from dotenv import load_dotenv

# config = load_dotenv()
# AOAI_COMPLETION_DEPLOYMENT = config['AOAI_COMPLETION_DEPLOYMENT']
# AOAI_KEY = config['AOAI_KEY']
# AOAI_ENDPOINT = config['AOAI_ENDPOINT']
# API_VERSION = '2024-02-01'

AOAI_COMPLETION_DEPLOYMENT = os.environ.get('AOAI_COMPLETION_DEPLOYMENT')
AOAI_KEY = os.environ.get('AOAI_KEY')
AOAI_ENDPOINT = os.environ.get('AOAI_ENDPOINT')
API_VERSION = '2024-02-01'
COSMOSDB_ENDPOINT = os.environ.get('COSMOSDB_ENDPOINT')
COSMOSDB_KEY = os.environ.get('COSMOSDB_KEY')

def check_cache(prompt):
    return CacheItem.objects.filter(prompts=prompt).first()

def save_to_cache(vectors, prompt, completion):
    cache_item = CacheItem(vectors=vectors, prompts=prompt, completion=completion)
    cache_item.save()
    return cache_item




# Initialize AOAI Service

class AIService:
    def __init__(self):
        self.endpoint = AOAI_ENDPOINT
        self.key = AOAI_KEY
        self.client =  AzureOpenAI(
        azure_endpoint=AOAI_ENDPOINT,
        api_key=AOAI_KEY,  
        api_version= API_VERSION
        )

    def get_completion(self, prompt):
        completion = self.client.chat.completions.create(
            model=AOAI_COMPLETION_DEPLOYMENT,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
        return completion.choices[0].message.content
    


    def get_completion(self, prompt):
        completion = self.client.chat.completions.create(
            model=AOAI_COMPLETION_DEPLOYMENT,
            messages= [
            {
            "role": "user",
            "content": prompt
            }],
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
        return completion.choices[0].message.content
    

class CosmosService:
    def __init__(self):
        self.client = CosmosClient(COSMOSDB_ENDPOINT, 
                                   COSMOSDB_KEY)

    def get_database(self, database_name):
       self.database = self.client.get_database_client(database_name)

    def get_container(self, container_name):
        self.container = self.database.get_container_client(container_name)

    def add_item(self, item_data):
        try:
            self.container.create_item(item_data)
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error creating item: {str(e)}")

    # Function to create or query items
    # def create_or_query_item(item_data):
    #     get_container()
    #     try:
    #         container.create_item(item_data)
    #     except exceptions.CosmosHttpResponseError as e:
    #         print(f"Error creating item: {str(e)}")