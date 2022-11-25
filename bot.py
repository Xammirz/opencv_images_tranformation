import os
import random
import telebot
from telebot import types
import photo_tranformation

bot = telebot.TeleBot('')
buttons_photo_pix = {'64_64p': '64_im', '128_128p':'128_im',
            '256_256p': '256_im'}
buttons_photo_categorys = {'pixels': 'pixels', 'filters': 'filters'}
buttons_photo_filters = {'bilateralFilter':'bilateralFilter', 'black and white':'black_and_white', 'image sharpness':'image_sharpness'}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Я бот который преобразует ваши фотки/видео так, как вы захотите. Отправьте фото или видео если вы хотите попробовать')


@bot.message_handler(content_types=['text'])
def diameter(message):
    global diametr
    diametr = message.text
    msg = bot.send_message(message.chat.id, 'обозначает сигму фильтра в цветовом пространстве')
    bot.register_next_step_handler(msg, sigmaColor)

def sigmaColor(message):
    global sgmaColor
    sgmaColor = message.text
    msg = bot.send_message(message.chat.id, 'обозначает сигму фильтра в координатном пространстве.')
    bot.register_next_step_handler(msg, sigmaSpace)

def sigmaSpace(message):
    global sgmaSpace
    sgmaSpace = message.text
    output_image = photo_tranformation.bilateralFilter(input_image,int(diametr),int(sgmaColor),int(sgmaSpace))
    bot.send_photo(message.chat.id, photo=open(output_image, 'rb'))
    os.remove(input_image)
    os.remove(output_image)


@bot.message_handler(content_types=['photo'])
def accept_transfor_photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    global input_image
    input_image = f'input{random.randint(1,5000)}.jpg'
    with open(input_image, 'wb') as new_file:
        new_file.write(downloaded_file)
    markup = types.InlineKeyboardMarkup(row_width=2)
    for button_name, button_callbak in buttons_photo_categorys.items():
        button_name = types.InlineKeyboardButton(button_name, callback_data=button_callbak)
        markup.add(button_name)
    bot.send_message(message.chat.id, "Фото получено, как вы хотите его преобразовать?", reply_markup=markup)


@bot.message_handler(content_types=['video'])
def accept_transfor_video(message):
    fileID = message.video.file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    global input_video
    input_video = f'input{random.randint(1,5000)}.mp3'
    with open(input_video, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_audio(message.chat.id, open(input_video, 'rb'))
    bot.send_message(message.chat.id, 'Извлечено из видео!')
    os.remove(input_video)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Принято!')

    if call.data == 'filters':
        markup = types.InlineKeyboardMarkup(row_width=2)
        for button_name, button_callbak in buttons_photo_filters.items():
            button_name = types.InlineKeyboardButton(button_name, callback_data=button_callbak)
            markup.add(button_name)
        bot.send_message(call.message.chat.id, 'Выберите каким фильтром вы хотите воспользоваться:', reply_markup=markup)

    if call.data == 'image_sharpness':
        output_image = photo_tranformation.image_sharpness(input_image)
        bot.send_photo(call.message.chat.id, photo=open(output_image, 'rb'))
        os.remove(input_image)
        os.remove(output_image)

    if call.data == 'black_and_white':
        output_image = photo_tranformation.black_and_white(input_image)
        bot.send_photo(call.message.chat.id, photo=open(output_image, 'rb'))
        os.remove(input_image)
        os.remove(output_image)

    if call.data == 'bilateralFilter':
        msg = bot.send_message(call.message.chat.id, 'обозначает диаметр окрестности пикселя (целочисленный тип)')
        bot.register_next_step_handler(msg, diameter)

    if call.data == 'pixels':
        markup = types.InlineKeyboardMarkup(row_width=2)
        for button_name, button_callbak in buttons_photo_pix.items():
            button_name = types.InlineKeyboardButton(button_name, callback_data=button_callbak)
            markup.add(button_name)
        bot.send_message(call.message.chat.id, "Выберите, пожалуйста, число пикселей", reply_markup=markup)

    if call.data == '64_im':
        try:
            output_image = photo_tranformation.pixels(input_image, 64, 64)
            bot.send_photo(call.message.chat.id, photo=open(output_image, 'rb'))
            os.remove(input_image)
            os.remove(output_image)
        except Exception:
            bot.send_message(call.message.chat.id, 'Надо прислать новую фотку!')

    if call.data == '128_im':
        try:
            output_image = photo_tranformation.pixels(input_image, 128, 128)
            bot.send_photo(call.message.chat.id, photo=open(output_image, 'rb'))
            os.remove(input_image)
            os.remove(output_image)
        except Exception as e:
            bot.send_message(call.message.chat.id, 'Надо прислать новую фотку!')

    if call.data == '256_im':
        try:
            output_image = photo_tranformation.pixels(input_image, 256, 256)
            bot.send_photo(call.message.chat.id, photo=open(output_image, 'rb'))
            os.remove(input_image)
            os.remove(output_image)
        except Exception as e:
            bot.send_message(call.message.chat.id, 'Надо прислать новую фотку!')

bot.polling(none_stop=True)