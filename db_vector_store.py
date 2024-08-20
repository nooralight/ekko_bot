from mongoengine import *
from datetime import datetime
from gpt_functions import updateAssistantInstruction
connect(host="mongodb://127.0.0.1:27017/ekko?directConnection=true&serverSelectionTimeoutMS=2000")

# Define the MongoDB document schema using mongoengine
class Store_folder(Document):
    id = SequenceField(primary_key=True)
    store_id= StringField()
    files = ListField(DictField())  # {Filename, URL} {file_id: {file_url:{}, file_name:{}, file_address:{}}}
    created_at = DateTimeField()

def get_vector_store():
    return Store_folder.objects().first()


def add_new_files(files_dicts):

    model = Store_folder.objects().first()

    for item in files_dicts:
        model.files.append(item)

    model.save()


def delete_file_from_db(file_id):
    model = Store_folder.objects().first()

    model.files =  [file_dict for file_dict in model.files if file_id not in file_dict]

    model.save()
    print("File deleted")


    
