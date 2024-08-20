from flask import Flask, render_template, request, jsonify,session, redirect, url_for
from flask_session import Session
import time
from mongoengine import *
from gpt_functions import initiate_interaction, sendNewMessage_to_existing_thread, trigger_assistant, checkRunStatus, retrieveResponse, upload_file_into_vector_store, saveFile_intoOpenAI, deleteFile

from db_gpt_model import get_gpt_model, update_instruction
from db_vector_store import get_vector_store, add_new_files, delete_file_from_db
from db_users import create_new_user, check_email_found, check_password_of_user

from datetime import datetime,timedelta
from dotenv import load_dotenv
load_dotenv()

import random
import string

ASSISTANT_ID = "asst_p49pPeEDQFcOJ1ZRamfFiBzc"
# thread_id_dict = dict()

app = Flask(__name__)
app.config['secret_key'] = '5800d5d9e4405020d527f0587538abbe'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # Include letters (both cases) and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


@app.route('/', methods=['GET','POST'])
def home():
    if 'user' in session:
        user_logged = "yes"
        return render_template("index.html", user_logged = user_logged)
    return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        email_check = check_email_found(email)
        if email_check:
            pass_check = check_password_of_user(email, password)
            if pass_check:
                session["user"] = pass_check.id
                return redirect(url_for('home'))
            else:
                return render_template("login.html", password_error = "yes")
        else:
            return render_template("login.html", user_not_exist = "yes")
    
    return render_template("login.html")


@app.route('/signup', methods=['GET','POST'])
def gotoSignup():
    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        create_new_user(name, email, password)
        return redirect(url_for('login'))
    return render_template("registration.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/chat', methods=['GET','POST'])
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("a_chat.html")

@app.route('/training', methods=['GET','POST'])
def training():
    if 'user' not in session:
        return redirect(url_for('login'))
    train = get_gpt_model()
    files = get_vector_store()
    return render_template("train.html", train = train, files = files)


@app.route('/get_response', methods=['POST'])
def get_response():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_message = request.json.get('user_message')
    final_response = None

    if 'my_thread_id' not in session:
        my_thread_id = initiate_interaction(user_message)
        session['my_thread_id'] = my_thread_id
    else:
        my_thread_id = session.get('my_thread_id')
        sendNewMessage_to_existing_thread(my_thread_id, user_message)

    # Getting GPT model from database
    model = get_gpt_model()

    run = trigger_assistant(my_thread_id, model.assistant_id)

    while True:
        run_status = checkRunStatus(my_thread_id , run.id)
        print(f"Run status: {run_status.status}")
        if run_status.status == "failed":
            final_response = "No response now"
            break
        elif run_status.status == "completed":
            # Extract the bot's response
            final_response = retrieveResponse(my_thread_id)
            break
        time.sleep(1)

    return jsonify(final_response)

@app.route('/edit_instruction', methods=['GET','POST'])
def edit_instruction():
    if 'user' not in session:
        return redirect(url_for('login'))
    referrer = request.referrer
    new_instruction = request.form['change_instruction']
    updated_assistant = update_instruction(new_instruction)
    return redirect(referrer)


@app.route('/upload_new_file', methods=['GET','POST'])
def uploadnewFile():
    if 'user' not in session:
        return redirect(url_for('login'))
    referrer = request.referrer
    files = request.files.getlist('new_file')
    # print(file.filename)
    assistant = get_gpt_model()

    file_ids = []
    final_file_dict = []
    for file in files:
        print("I am here")
        rn = generate_random_string(5)
        file_location = f'static/training_files/{rn}_{file.filename}'
        file.save(f'static/training_files/{rn}_{file.filename}')
        file_id = saveFile_intoOpenAI(file_location)
        file_ids.append(file_id)
        final_file_dict.append({file_id: {"file_url": f"http://159.65.152.150:3000/{file_location}", "file_name":file.filename}})

    vector_store = get_vector_store()
    upload_file_into_vector_store(vector_store.store_id, file_ids)
    add_new_files(final_file_dict)
    # print(file_id)
    # addFileToAssistant(assistant.assistant_id,file_id)
    # temp_file_dict = assistant.file_dict
    # temp_file_dict['http://46.101.129.241:5000/'+file_location] = file_id
    # print(temp_file_dict)
    # # temp_assistant_id = assistant.assistant_id
    # # temp_assistant_files = assistant.file_dict
    # # deleteAssistant(temp_assistant_id)
    # # for key , value in temp_assistant_files.items():
    # #     deleteFile(value)
    # assistant.delete()
    # insert_into_openai_api(new_assistant_id,prev_instruction, temp_file_dict)

    return redirect(referrer)

@app.route('/delete_file/<file_id>', methods=['GET','POST'])
def delete_file(file_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    referrer = request.referrer
    print(deleteFile(file_id))
    delete_file_from_db(file_id)

    return redirect(referrer)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=3000)