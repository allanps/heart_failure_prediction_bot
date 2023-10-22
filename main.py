import telebot
import os
from ngboost import NGBClassifier
import pickle as pkl
import pandas as pd
import traceback
from dotenv import load_dotenv
import joblib

print("Code initializing...")

load_dotenv()
API_KEY = os.environ.get("TELEGRAM_API_KEY")

bot = telebot.TeleBot(API_KEY)

USER_STATE = {}


"""
Model methods
#TODO: create a class for the model
"""

def load_model() -> NGBClassifier:
    # model = joblib.load("ng_boost_model.joblib")
    # return model
    with open("ng_boost_model.pkl", "rb") as f:
        return pkl.load(f)
    

def predict(model: NGBClassifier, X_test: pd.DataFrame):
    return model.predict_proba(X_test)

def predict_for_input(age_input: str or int, cholesterol_input: str or int) -> int or float:
    age = int(age_input)
    cholesterol = int(cholesterol_input)

    model = load_model()
    prediction = predict(model, [[age, cholesterol]])[0][1]

    prediction = round(prediction * 100, 2)

    return prediction

def set_user_state(user_id, state):
    USER_STATE[user_id] = state

def get_user_state(user_id):
    return USER_STATE.get(user_id, None)


"""
Message handlers
"""

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Vou fazer a predição da probabilidade de falha cardíaca. Qual sua idade?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    try:
        age = int(message.text)
        bot.send_message(message.chat.id, 'Agora, me diga seu nível de colesterol. ')
        bot.register_next_step_handler(message, get_cholesterol, age)
    except ValueError:
        bot.send_message(message.chat.id, 'Entrada inválida. Por favor, digite um valor numérico.')
        print(f"Error while running the code: {e}")
        traceback.print_exc()
        start(message)

def get_cholesterol(message, age):
    try:
        cholesterol = int(message.text)
        prediction = predict_for_input(age, cholesterol)
        bot.send_message(
            message.chat.id,
            f'Probabilidade de falha cardíaca para a idade {age} e colesterol {cholesterol}: {prediction}%'
            )
    except ValueError:
        bot.send_message(message.chat.id, 'Entrada inválida. Por favor, digite um valor numérico.')
        print(f"Error while running the code: {e}")
        traceback.print_exc()
        start(message)

try:
    print("Done! \n >> Waiting for mesages from Telegram <<")
    bot.polling()
    print("Code running...")

except Exception as e:
    print(f"Error while running the code: {e}")
    traceback.print_exc()
