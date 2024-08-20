from mongoengine import *
from datetime import datetime
from gpt_functions import updateAssistantInstruction
connect(host="mongodb://127.0.0.1:27017/ekko?directConnection=true&serverSelectionTimeoutMS=2000")

class Gpt_model(Document):
    id = SequenceField(primary_key = True)
    assistant_id = StringField()
    instruction = StringField()
    created_at = DateTimeField()
    updated_at = DateTimeField()



def get_gpt_model():

    return Gpt_model.objects().first()

def update_instruction(instruction):

    model = Gpt_model.objects().first()
    model.instruction = instruction
    model.updated_at = datetime.now()
    updateAssistantInstruction(model.assistant_id, instruction)
    model.save()
    print("Instruction has been updated")


