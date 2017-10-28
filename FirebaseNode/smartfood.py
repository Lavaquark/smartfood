import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('SmartFood-ed238d476c11.json')
default_app = firebase_admin.initialize_app(cred)
