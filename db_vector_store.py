from mongoengine import *
from datetime import datetime
from gpt_functions import updateAssistantInstruction
connect(host="mongodb://127.0.0.1:27017/ekko?directConnection=true&serverSelectionTimeoutMS=2000")

# Define the MongoDB document schema using mongoengine
class Store_folder(Document):
    id = SequenceField(primary_key=True)
    store_id= StringField()
    files = ListField(DictField())  # {Filename, URL} {file_id: {file_url:{}, "file_name":{}, file_address:{}}}
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


def insert_into_vector(store_id):
    new_store = Store_folder(
        store_id = store_id,
        created_at = datetime.now()
    )
    new_store.save()

insert_into_vector("vs_joHKCuQfUT45GKH1ppZtqK7y")


def update_files(file_arr):
    vect_store = Store_folder.objects().first()
    vect_store.files = file_arr
    vect_store.save()

file_arr = [{
        'file-gWOn52MgfrnPgPzx9wihMznS': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/ml3AJ_aligning-values-goals-2024-nick-regan-cpcc-lhaje.html',
          "file_name": 'aligning-values-goals-2024-nick-regan-cpcc-lhaje.html'
        }
      },
      {
        'file-mWkKanjFNFZpwVKiCpjroIaa': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/xeImD_buzz-challenge-nick-regan.html',
          "file_name": 'buzz-challenge-nick-regan.html'
        }
      },
      {
        'file-6ILygpiyBwTXGnk79Hh2eBrh': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/w6mHE_creating-philosophy-stance-example-team-coaching-nick-regan-cpcc.html',
          "file_name": 'creating-philosophy-stance-example-team-coaching-nick-regan-cpcc.html'
        }
      },
      {
        'file-RmroJwdpDqzwNIHZhxXsa9BS': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/ZBRDZ_feeling-alive-teams-nick-regan.html',
          "file_name": 'feeling-alive-teams-nick-regan.html'
        }
      },
      {
        'file-5CJxedFu7AXD7dR4AXIULZuh': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/3V6VD_future-ai-human-ness-leaders-teams-nick-regan-cpcc.html',
          "file_name": 'future-ai-human-ness-leaders-teams-nick-regan-cpcc.html'
        }
      },
      {
        'file-kNrxzeKwi8d1Lj58Pagcjj5N': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/fDLMj_how-measure-magic-generated-effective-teams-nick-regan.html',
          "file_name": 'how-measure-magic-generated-effective-teams-nick-regan.html'
        }
      },
      {
        'file-PnXT8a2vLQcTUEXa6dNbtgWv': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/SSzoH_joy-receivingan-unexpected-gift-from-your-team-mates-nick-regan.html',
          "file_name": 'joy-receivingan-unexpected-gift-from-your-team-mates-nick-regan.html'
        }
      },
      {
        'file-gULLA2IziByLBt1jjYMJuTfB': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/NrZR7_time-battle-our-nick-regan-cpcc-c2bec.html',
          "file_name": 'time-battle-our-nick-regan-cpcc-c2bec.html'
        }
      },
      {
        'file-c6V59ZoxUXitObZSkpvh0sA0': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/Vl6o8_upskilling-our-creativity-lets-experiment-learn-nick-regan-cpcc.html',
          "file_name": 'upskilling-our-creativity-lets-experiment-learn-nick-regan-cpcc.html'
        }
      },
      {
        'file-NvWSH4Tf7LGdlUMWtFkXHNM4': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/LqSDM_what-your-favorite-metaphors-nick-regan.html',
          "file_name": 'what-your-favorite-metaphors-nick-regan.html'
        }
      },
      {
        'file-rpopMVQuS5rJGZHp2LFtBGyj': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/zUTg1_when-can-i-call-myself-coach-nick-regan.html',
          "file_name": 'when-can-i-call-myself-coach-nick-regan.html'
        }
      },
      {
        'file-ot6MrcL6BxHYql61QoNLEQti': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/ewurV_who-am-i-you-nick-regan.html',
          "file_name": 'who-am-i-you-nick-regan.html'
        }
      },
      {
        'file-4gkz5Z06Sx12kTJxfYymZePo': {
          "file_url": 'http://78.142.47.22:3000/static/training_files/VRRu7_Nick Regan LinkedIn Posts good.pdf',
          "file_name": 'Nick Regan LinkedIn Posts good.pdf'
        }
      }

]
update_files(file_arr)