import pymongo
from openai import OpenAI
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
import merge
from merge.client import Merge

load_dotenv()

# for openai client
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)

# for mongodb atlas client
mongodb_atlas_uri = os.getenv("MONGODB_SRV")
mongodb_atlas_client = MongoClient(host=mongodb_atlas_uri)

# for merge api client
merge_api_key = os.getenv("MERGE_API_KEY")
merge_account_token = os.getenv("TEST_LINKED_ACCOUNT_TOKEN")
merge_client = Merge(api_key="YOUR_API_KEY", account_token="YOUR_ACCOUNT_TOKEN")
