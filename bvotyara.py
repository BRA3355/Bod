
import random as ran 

import telebot
from telebot import types

bot = telebot.TeleBot('7806140546:AAGSH208A7jttfHJue-YDr1S0NP2rPQHxf4')


PRICES = {
    '10 Stars': 10,   
    '50 Stars': 45,   
    '100 Stars': 80,  
    '500 Stars': 350  
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    buttons = [types.KeyboardButton(product) for product in PRICES.keys()]
    markup.add(*buttons)
    bot.reply_to(message, 
                 "Welcome to Stars Payment Bot!\nPlease select amount of stars to purchase:",
                 reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in PRICES.keys())
def handle_product_selection(message):

    product = message.text
    price = PRICES[product]
    
    prices = [types.LabeledPrice(label=product, amount=price)]
    
    bot.send_invoice(
        message.chat.id, 
        title=f"Purchase {product}",  
        description=f"Buy {product} for your account", 
        provider_token='',  
        currency='XTR', 
        prices=prices,  
        start_parameter='stars-payment',  
        invoice_payload=product
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    product = message.successful_payment.invoice_payload
    bot.reply_to(message, 
                 f"Payment for {product} successful!")


bot.polling()