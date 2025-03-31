import telebot
from telebot import types
import os
from dotenv import load_dotenv
import logging

load_dotenv()  # Загружаем переменные из .env

TOKEN = os.getenv('BOT_TOKEN')  # Получаем токен из .env
CHANNEL_ID = -1002641394600  # Замените на ID вашего канала

if TOKEN is None:
    print("Ошибка: Не найден токен бота в переменной окружения BOT_TOKEN")
    exit()

bot = telebot.TeleBot(TOKEN)

user_states = {}  # Словарь для хранения состояний пользователей: {user_id: {'state': 'manager' или 'question', 'message_id': message_id}}

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Пути к изображениям
IMAGE_PATH = 'images/imageslogo.png'
IMAGE_TUMBLER_ON = 'images/tumbler_on.png'
IMAGE_TUMBLER_OFF = 'images/tumbler_off.png'
IMAGE_KASSAVROZETKY = 'images/kassavrozetky.png'
RSA_CERT_PROBLEM_IMAGE = 'images/rsa_cert_problem.jpg'  # Картинка для RSA
UTM_DB_PROBLEM_IMAGE = 'images/utm_db_problem.jpg'  # Картинка для проблем с БД
RSA_PC_STEP1_IMAGE = 'images/rsa_pc_step1.jpg'  # Картинка для шага 1
RSA_PC_STEP2_IMAGE = 'images/rsa_pc_step2.jpg'
RSA_PC_STEP3_IMAGE = 'images/rsa_pc_step3.jpg'
RSA_PC_STEP4_IMAGE = 'images/rsa_pc_step4.jpg'
RSA_PC_STEP5_IMAGE = 'images/rsa_pc_step5.jpg'
EVOTOR_RSA_STEP1_IMAGE = 'images/evotor_rsa_step1.jpg'
EVOTOR_RSA_STEP2_IMAGE = 'images/evotor_rsa_step2.jpg'
EVOTOR_RSA_STEP3_IMAGE = 'images/evotor_rsa_step3.jpg'
REINSTALL_UTM_STEP1_IMAGE = 'images/reinstall_utm_step1.jpg'
REMOVE_UTM_STEP1_IMAGE = 'images/remove_utm_step1.jpg'

# Пути к файлам с информацией
BATTERY_INFO_FILE = 'battery_info.txt'
ST2F_INSTRUCTION_FILE = 'st2finstrukt.txt'

# Читаем информацию об аккумуляторах из файла
try:
    with open(BATTERY_INFO_FILE, 'r', encoding='utf-8') as f:
        battery_info = f.read()
except FileNotFoundError:
    battery_info = "Информация об аккумуляторах не найдена."
    print(f"Ошибка: Файл '{BATTERY_INFO_FILE}' не найден.")
except Exception as e:
    battery_info = f"Ошибка при чтении информации об аккумуляторах: {e}"
    print(f"Ошибка при чтении файла '{BATTERY_INFO_FILE}': {e}")

# Читаем инструкцию для СТ2Ф из файла
try:
    with open(ST2F_INSTRUCTION_FILE, 'r', encoding='utf-8') as f:
        st2f_instruction = f.read()
except FileNotFoundError:
    st2f_instruction = "Инструкция для СТ2Ф не найдена."
    print(f"Ошибка: Файл '{ST2F_INSTRUCTION_FILE}' не найден.")
except Exception as e:
    st2f_instruction = f"Ошибка при чтении инструкции для СТ2Ф: {e}"
    print(f"Ошибка при чтении файла '{ST2F_INSTRUCTION_FILE}': {e}")

# Глобальный список для хранения message_id
messages_to_delete = []

# Флаг, чтобы указать, что мы находимся в разделе ST2F
in_st2f_section = False


def delete_messages(call):
    """Удаляет сообщения из messages_to_delete."""
    global messages_to_delete
    chat_id = call.message.chat.id
    logging.debug(f"Попытка удаления сообщений в чате {chat_id}. Список сообщений: {messages_to_delete}")
    try:
        for message_id in messages_to_delete:
            bot.delete_message(chat_id, message_id)
            logging.debug(f"Удалено сообщение {message_id} в чате {chat_id}")
    except Exception as e:
        logging.error(f"Не удалось удалить сообщение {message_id} в чате {chat_id}: {e}")
    messages_to_delete = []
    logging.debug(f"Список сообщений после удаления: {messages_to_delete}")


@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start."""
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Команда /start от пользователя {message.from_user.id}")
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton('Начать', callback_data='show_main_menu')  # Кнопка "Начать"
    markup.add(start_button)

    # Проверяем, существует ли файл с картинкой
    if os.path.exists(IMAGE_PATH):
        try:
            with open(IMAGE_PATH, 'rb') as photo:
                sent_message = bot.send_photo(message.chat.id, photo, caption="🖐️Привет! Я официальный бот технической поддержки компании \"Админ38\" помогу в решении ваших вопросов, если у меня не получиться, то передам ваш вопрос сотрудникам технической поддержки👌.  Для решения вашего вопроса, выберите производителя оборудования или программного обеспечения в меню ниже👇👇👇", reply_markup=markup)
                messages_to_delete.append(sent_message.message_id)
                logging.debug(f"Отправлено фото с message_id {sent_message.message_id}")
        except Exception as e:
            print(f"Ошибка при отправке фото: {e}")
            sent_message = bot.send_message(message.chat.id, "Произошла ошибка при загрузке изображения. Пожалуйста, попробуйте позже.", reply_markup=markup)
            messages_to_delete.append(sent_message.message_id)
            logging.debug(f"Отправлено текстовое сообщение об ошибке с message_id {sent_message.message_id}")
    else:
        sent_message = bot.send_message(message.chat.id, "Ошибка: Не удалось найти файл с изображением.", reply_markup=markup)  # Если картинка не найдена
        messages_to_delete.append(sent_message.message_id)
        logging.debug(f"Отправлено сообщение об отсутствии файла с message_id {sent_message.message_id}")
        sent_message = bot.send_message(message.chat.id, "🖐️Привет! Я официальный бот технической поддержки компании \"Админ38\" помогу в решении ваших вопросов, если у меня не получиться, то передам ваш вопрос сотрудникам технической поддержки👌.  Для решения вашего вопроса, выберите производителя оборудования или программного обеспечения в меню ниже👇👇👇", reply_markup=markup)
        messages_to_delete.append(sent_message.message_id)
        logging.debug(f"Отправлено приветственное сообщение с message_id {sent_message.message_id}")


@bot.callback_query_handler(func=lambda call: call.data == 'show_main_menu')
def show_main_menu(call):
    """Показывает главное меню с производителями."""
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Нажата кнопка 'Начать' пользователем {call.from_user.id}")
    delete_messages(call)  # Удаляем старые сообщения

    markup = types.InlineKeyboardMarkup()
    evotor_button = types.InlineKeyboardButton('Эвотор', callback_data='evotor_menu')
    sigma_button = types.InlineKeyboardButton('Sigma', callback_data='sigma_menu')
    atol_button = types.InlineKeyboardButton('Атол', callback_data='atol_menu')
    roznica_1с_button = types.InlineKeyboardButton('1C Розница', callback_data='розница_1с_menu')
    другое_button = types.InlineKeyboardButton('Другое', callback_data='другое_menu')
    svyaz_s_menedzherami_button = types.InlineKeyboardButton('Связь с менеджерами', callback_data='связь_с_менеджерами_menu')

    markup.add(evotor_button)
    markup.add(sigma_button, atol_button, roznica_1с_button, другое_button, svyaz_s_menedzherami_button)

    sent_message = bot.send_message(call.message.chat.id, "Выберите производителя:", reply_markup=markup)
    messages_to_delete.append(sent_message.message_id)
    logging.debug(f"Отправлено сообщение 'Выберите производителя' с message_id {sent_message.message_id}")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'evotor_menu')
def evotor_menu(call):
    """Меню раздела Эвотор с Inline-кнопками."""
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбран раздел 'Эвотор' пользователем {call.from_user.id}")
    delete_messages(call)  # Удаляем старые сообщения
    markup = types.InlineKeyboardMarkup(row_width=2)  # row_width=2: 2 кнопки в ряд

    button1 = types.InlineKeyboardButton('Не включается касса', callback_data='no_power')
    button2 = types.InlineKeyboardButton('Не запускается УТМ', callback_data='utm_problem')
    button3 = types.InlineKeyboardButton('Нет сети', callback_data='no_network')
    button4 = types.InlineKeyboardButton('Свой вопрос', callback_data='custom_question')
    button5 = types.InlineKeyboardButton('Главное меню', callback_data='show_main_menu')  # Направляет в самое начало

    markup.add(button1, button2, button3, button4, button5)
    sent_message = bot.send_message(call.message.chat.id, "Выберите раздел Эвотор:", reply_markup=markup)
    messages_to_delete.append(sent_message.message_id)
    logging.debug(f"Отправлено сообщение 'Выберите раздел Эвотор' с message_id {sent_message.message_id}")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'no_power')
def no_power_menu(call):
    """Меню выбора модели Эвотора."""
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбран раздел 'Не включается касса' пользователем {call.from_user.id}")
    delete_messages(call)  # Удаляем старые сообщения
    markup = types.InlineKeyboardMarkup(row_width=2)

    button1 = types.InlineKeyboardButton('СТ3Ф, СТ5Ф, СТ51Ф, 10', callback_data='evotor_model_info')
    button2 = types.InlineKeyboardButton('СТ2Ф', callback_data='st2f_info')
    button3 = types.InlineKeyboardButton('Power', callback_data='power_info')
    button4 = types.InlineKeyboardButton('Эвотор6', callback_data='evotor6_info')
    button5 = types.InlineKeyboardButton('Список проблем Эвотор', callback_data='problem_list')
    back_button = types.InlineKeyboardButton('Назад', callback_data='evotor_menu')
    main_menu_button = types.InlineKeyboardButton('Главное меню', callback_data='show_main_menu')  # Кнопка "Главное меню"

    markup.add(button1, button2, button3, button4, button5, back_button, main_menu_button)

    sent_message = bot.send_message(call.message.chat.id, "Выберите модель своего ЭВОТОРа👇\nМодель можно узнать с обратной стороны Смарт-терминала", reply_markup=markup)  # Отправляем новое сообщение с выбором модели
    messages_to_delete.append(sent_message.message_id)
    logging.debug(f"Отправлено сообщение 'Выберите модель Эвотора' с message_id {sent_message.message_id}")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'problem_list')
def problem_list_menu(call):
    """Меню списка проблем Эвотор."""
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбран раздел 'Список проблем Эвотор' пользователем {call.from_user.id}")
    delete_messages(call)  # Удаляем старые сообщения
    markup = types.InlineKeyboardMarkup(row_width=2)

    button1 = types.InlineKeyboardButton('Не включается касса', callback_data='no_power')
    button2 = types.InlineKeyboardButton('Не запускается УТМ', callback_data='utm_problem')
    button3 = types.InlineKeyboardButton('Нет сети', callback_data='no_network')
    button4 = types.InlineKeyboardButton('Свой вопрос', callback_data='custom_question')
    main_menu_button = types.InlineKeyboardButton('Главное меню', callback_data='show_main_menu')
    back_button = types.InlineKeyboardButton('Назад', callback_data='no_power')  # Кнопка "Назад"

    markup.add(button1, button2, button3, button4, main_menu_button, back_button)

    sent_message = bot.send_message(call.message.chat.id, "Выберите проблему:", reply_markup=markup)
    messages_to_delete.append(sent_message.message_id)
    logging.debug(f"Отправлено сообщение 'Выберите проблему' с message_id {sent_message.message_id}")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'evotor_model_info')
def evotor_model_info(call):
    """Информация о модели СТ3Ф, СТ5Ф, СТ51Ф, 10."""
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбрана модель 'СТ3Ф, СТ5Ф, СТ51Ф, 10' пользователем {call.from_user.id}")
    delete_messages(call)
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Выбор модели", callback_data="no_power")
    button2 = types.InlineKeyboardButton("Проблемы ЭВОТОРов", callback_data="problem_list")
    button3 = types.InlineKeyboardButton("Главная страница", callback_data="show_main_menu")
    markup.add(button1, button2, button3)

    sent_message = bot.send_message(call.message.chat.id, battery_info, reply_markup=markup)
    messages_to_delete.append(sent_message.message_id)
    logging.debug(f"Отправлена информация об аккумуляторах с message_id {sent_message.message_id}")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'st2f_info')
def st2f_info(call):
    """Информация о модели СТ2Ф."""
    global in_st2f_section
    in_st2f_section = True  # Устанавливаем флаг, что мы в разделе ST2F
    logging.debug(f"Выбрана модель 'СТ2Ф' пользователем {call.from_user.id}")

    # Удаляем старые сообщения (если были) - ПЕРЕД отправкой новых!
    delete_messages(call)

    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Выбор модели", callback_data="no_power")
    button2 = types.InlineKeyboardButton("Проблемы ЭВОТОРов", callback_data="problem_list")
    button3 = types.InlineKeyboardButton("Главная страница", callback_data="show_main_menu")
    markup.add(button1, button2, button3)

    try:
        # Отправляем сообщение "Выполните проверку по шагам:"
        sent_message = bot.send_message(call.message.chat.id, "Выполните проверку по шагам:")
        messages_to_delete.append(sent_message.message_id)
        logging.debug(f"Отправлено сообщение 'Выполните проверку по шагам' с message_id {sent_message.message_id}")

        # Отправляем изображения
        with open(IMAGE_TUMBLER_ON, 'rb') as photo_on:
            sent_photo = bot.send_photo(call.message.chat.id, photo_on, caption="Тумблер включен")
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Тумблер включен' с message_id {sent_photo.message_id}")

        with open(IMAGE_TUMBLER_OFF, 'rb') as photo_off:
            sent_photo = bot.send_photo(call.message.chat.id, photo_off, caption="Тумблер выключен")
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Тумблер выключен' с message_id {sent_photo.message_id}")

        with open(IMAGE_KASSAVROZETKY, 'rb') as photo_rozetka:
            sent_photo = bot.send_photo(call.message.chat.id, photo_rozetka, caption="Проверьте подключение кассы к розетке")
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Проверьте подключение кассы к розетке' с message_id {sent_photo.message_id}")

        # Отправляем инструкцию и клавиатуру
        sent_instruction = bot.send_message(call.message.chat.id, st2f_instruction, reply_markup=markup)
        messages_to_delete.append(sent_instruction.message_id)
        logging.debug(f"Отправлена инструкция СТ2Ф с message_id {sent_instruction.message_id}")

    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка при отправке фото или инструкции: {e}", reply_markup=markup)

    # Удаляем сообщение с кнопкой "СТ2Ф"
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'power_info')
def power_info(call):
    """Информация о Power."""
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбрана модель 'Power' пользователем {call.from_user.id}")
    delete_messages(call) # Удаляем старые сообщения
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Выбор модели", callback_data="no_power")
    button2 = types.InlineKeyboardButton("Проблемы ЭВОТОРов", callback_data="problem_list")
    button3 = types.InlineKeyboardButton("Главная страница", callback_data="show_main_menu")
    markup.add(button1, button2, button3)
    text = """Не включается Эвотор Power
Проверьте, подключен ли Эвотор к электросети (в розетку). Если подключен в розетку, но не работает, то отключите его от сети и подключите заново, нажмите на кнопку питания на торце Эвотора.

Если не помогло, обратитесь в сервисный центр"""  # Замените на реальную информацию
    sent_message = bot.send_message(call.message.chat.id, text, reply_markup=markup)
    messages_to_delete.append(sent_message.message_id)
    logging.debug(f"Отправлена информация о Power с message_id {sent_message.message_id}")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'evotor6_info')
def evotor6_info(call):
    """Информация о модели Эвотор6."""
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбрана модель 'Эвотор6' пользователем {call.from_user.id}")
    delete_messages(call)
    text = """Если Эвотор 6 не включается, скорее всего, у него разрядились аккумуляторы. Чтобы зарядить их:

Подключите Эвотор к электросети.
Подождите 40 минут.
Отключите Эвотор от сети и подключите заново.
Повторяйте, пока Эвотор не включится (2-3 раза).

Если это не помогло, обратитесь в сервисный центр"""  # Замените на реальную информацию

    # Добавляем кнопки
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_vybor_modeli = types.InlineKeyboardButton("Выбор модели", callback_data="no_power")
    button_problemy_evotorov = types.InlineKeyboardButton("Проблемы ЭВОТОРов", callback_data="problem_list")
    button_glavnaya_stranica = types.InlineKeyboardButton("Главная страница", callback_data="show_main_menu")
    markup.add(button_vybor_modeli, button_problemy_evotorov, button_glavnaya_stranica)

    sent_message = bot.send_message(call.message.chat.id, text, reply_markup=markup)
    messages_to_delete.append(sent_message.message_id)
    logging.debug(f"Отправлена информация о Эвотор6 с message_id {sent_message.message_id}")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'utm_problem')
def utm_problem_menu(call):
    """Меню проблем с УТМ."""
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбран раздел 'Не запускается УТМ' пользователем {call.from_user.id}")
    delete_messages(call)  # Удаляем старые сообщения

    # 1. Отправляем сообщение о возможных проблемах
    sent_message = bot.send_message(call.message.chat.id, "Возможные проблемы и их решение:")
    messages_to_delete.append(sent_message.message_id)

    # 2. Отправляем картинку с RSA-сертификатом
    try:
        with open(RSA_CERT_PROBLEM_IMAGE, 'rb') as rsa_photo:
            sent_photo = bot.send_photo(call.message.chat.id, rsa_photo, caption="При проблемах с RSA-сертификатом может потребоваться перезапись сертификата.")
            messages_to_delete.append(sent_photo.message_id)
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением RSA сертификата.")

    # 3. Отправляем картинку с проблемами с БД
    try:
        with open(UTM_DB_PROBLEM_IMAGE, 'rb') as db_photo:
            sent_photo = bot.send_photo(call.message.chat.id, db_photo, caption="При проблемах с базой данных может потребоваться удаление БД или переустановка УТМ.")
            messages_to_delete.append(sent_photo.message_id)
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением проблем с БД УТМ.")

    markup = types.InlineKeyboardMarkup(row_width=1)  # Кнопки в столбик

    button1 = types.InlineKeyboardButton('Перезапись RSA на ПК', callback_data='rsa_pc')
    button2 = types.InlineKeyboardButton('Перезапись RSA на Эвоторе', callback_data='rsa_evotor')
    button3 = types.InlineKeyboardButton('Переустановка УТМ', callback_data='reinstall_utm')
    button4 = types.InlineKeyboardButton('Удаление УТМ', callback_data='remove_utm')
    button5 = types.InlineKeyboardButton('Назад к проблемам Эвотор', callback_data='evotor_menu')  # Кнопка "Назад"

    markup.add(button1, button2, button3, button4, button5)

    sent_keyboard = bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)  # Отправляем новое сообщение
    messages_to_delete.append(sent_keyboard.message_id)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'rsa_pc')
def rsa_pc_info(call):
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбран пункт 'Перезапись RSA на ПК' пользователем {call.from_user.id}")
    delete_messages(call)

    # Шаг 1
    step1_text = """Шаг 1. Удалите текущий ключ RSA
Перед тем как перезаписывать ключ RSA, удалите старый ключ.

Ключевая пара ГОСТ Р
Если на ЭЦП, помимо сертификатов ГОСТ и RSA, записана Ключевая пара ГОСТ Р, её необходимо удалить при перезаписи RSA, так как она может препятствовать работе с ЕГАИС. 

Ключевая пара Рутокен состоит из двух ключей:

Приватный — секретный ключ, который используется для расшифровки информации.
Публичный — открытый ключ, которым можно поделиться. Используется для шифрования данных."""
    sent_message = bot.send_message(call.message.chat.id, step1_text)
    messages_to_delete.append(sent_message.message_id)

    # Картинка для шага 1
    try:
        with open(RSA_PC_STEP1_IMAGE, 'rb') as step1_photo:
            sent_photo = bot.send_photo(call.message.chat.id, step1_photo)
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Шаг 1' с message_id {sent_photo.message_id}")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением для шага 1.")
        logging.error(f"Не удалось найти файл: {RSA_PC_STEP1_IMAGE}")

    # Шаг 2
    step2_text = """Шаг 2. Выпустите новый RSA сертификат в ЕГАИС
Выпустить RSA сертификат в ЕГАИС можно двумя способами: в приложении УТМ на ПК либо прямо на вашем Эвоторе.

Как выпустить RSA сертификат в приложении «УТМ» на ПК
Для корректной записи RSA сертификата на ключевом носителе должна быть только одна подпись.

Прежде чем приступить к выпуску RSA сертификата, скачайте и установите на свой компьютер приложение «УТМ» с официального сайта ЕГАИС.

Подключите ключевой носитель с УКЭП на физическое лицо к вашему компьютеру.
Запустите приложение «УТМ»‎.
В приложении «УТМ» нажмите Домашняя страница."""
    sent_message = bot.send_message(call.message.chat.id, step2_text)
    messages_to_delete.append(sent_message.message_id)

    # Картинка для шага 3
    try:
        with open(RSA_PC_STEP2_IMAGE, 'rb') as step2_photo:
            sent_photo = bot.send_photo(call.message.chat.id, step2_photo)
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Шаг 2' с message_id {sent_photo.message_id}")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением для шага 2.")
        logging.error(f"Не удалось найти файл: {RSA_PC_STEP2_IMAGE}")

         # Шаг 3
    step3_text = "Перейдите в раздел Генерация ключа доступа к ЕГАИС.\nВыберите Руководитель ИП. Даже если у вас «ООО»."
    sent_message = bot.send_message(call.message.chat.id, step3_text)
    messages_to_delete.append(sent_message.message_id)

    # Картинка для шага 4
    try:
        with open(RSA_PC_STEP3_IMAGE, 'rb') as step3_photo:
            sent_photo = bot.send_photo(call.message.chat.id, step3_photo)
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Шаг 3' с message_id {sent_photo.message_id}")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением для шага 3.")
        logging.error(f"Не удалось найти файл: {RSA_PC_STEP3_IMAGE}")

        # Шаг 4
    step4_text = "Выберите место осуществления деятельности и подтвердите Заявление на выдачу ключа доступа к ЕГАИС."
    sent_message = bot.send_message(call.message.chat.id, step4_text)
    messages_to_delete.append(sent_message.message_id)

    # Картинка для шага 5
    try:
        with open(RSA_PC_STEP4_IMAGE, 'rb') as step4_photo:
            sent_photo = bot.send_photo(call.message.chat.id, step4_photo)
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Шаг 4' с message_id {sent_photo.message_id}")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением для шага 4.")
        logging.error(f"Не удалось найти файл: {RSA_PC_STEP4_IMAGE}")

        # Шаг 5
    step5_text = "Нажмите кнопку Сгенерировать сертификат и дождитесь подтверждения о его записи на ключевой носитель."
    sent_message = bot.send_message(call.message.chat.id, step5_text)
    messages_to_delete.append(sent_message.message_id)

    # Картинка для шага 6
    try:
        with open(RSA_PC_STEP5_IMAGE, 'rb') as step5_photo:
            sent_photo = bot.send_photo(call.message.chat.id, step5_photo)
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Шаг 5' с message_id {sent_photo.message_id}")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением для шага 5.")
        logging.error(f"Не удалось найти файл: {RSA_PC_STEP5_IMAGE}")

        # Шаг 6
    step6_text = """Вставьте ключевой носитель в Эвотор.
Перейдите в раздел Настройки → ЕГАИС → Настроить УТМ.
Готово! Выберите способ настройки УТМ — На терминале и используйте сертификат в работе."""
    

    # Кнопка "Предыдущее меню"
        # Кнопка "Предыдущее меню"
    markup = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton("Предыдущее меню", callback_data="utm_problem")
    markup.add(button_back)

    logging.error("Кнопка 'Предыдущее меню' не отправлена")
    sent_message = bot.send_message(call.message.chat.id, step6_text , reply_markup=markup)
    messages_to_delete.append(sent_message.message_id)

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'rsa_evotor')
def rsa_evotor_info(call):
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбран пункт 'Перезапись RSA на Эвоторе' пользователем {call.from_user.id}")
    delete_messages(call)

    # Шаг 1
    step1_text = """Как выпустить RSA сертификат на Эвоторе

Для корректной записи RSA сертификата на ключевом носителе должна быть только одна подпись."""
    sent_message = bot.send_message(call.message.chat.id, step1_text)
    messages_to_delete.append(sent_message.message_id)

    # Шаг 2
    step2_text = """Подключите ключевой носитель с УКЭП на физическое лицо к вашему Эвотору.

Перейдите в раздел Настройки → ЕГАИС → Настроить УТМ → На терминале.
После настройки нажмите Подробнее об УТМ."""
    sent_message = bot.send_message(call.message.chat.id, step2_text)
    messages_to_delete.append(sent_message.message_id)

    # Картинка для шага 3
    try:
        with open(EVOTOR_RSA_STEP1_IMAGE, 'rb') as step1_photo:
            sent_photo = bot.send_photo(call.message.chat.id, step1_photo)
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Шаг 1' с message_id {sent_photo.message_id}")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением для шага 1.")
        logging.error(f"Не удалось найти файл: {EVOTOR_RSA_STEP1_IMAGE}")
    
    # Шаг 3
    step3_text = "Нажмите на три полоски в правом верхнем углу, а затем выберите пункт Генерация ключа доступа к ЕГАИС."
    sent_message = bot.send_message(call.message.chat.id, step3_text)
    messages_to_delete.append(sent_message.message_id)

    # Картинка для шага 6
    try:
        with open(EVOTOR_RSA_STEP2_IMAGE, 'rb') as step2_photo:
            sent_photo = bot.send_photo(call.message.chat.id, step2_photo)
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Шаг 2' с message_id {sent_photo.message_id}")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением для шага 2.")
        logging.error(f"Не удалось найти файл: {EVOTOR_RSA_STEP2_IMAGE}")

    # Шаг 4
    step4_text = "Выберите Руководитель ИП."
    sent_message = bot.send_message(call.message.chat.id, step4_text)
    messages_to_delete.append(sent_message.message_id)

    # Шаг 5
    step5_text = "Выберите место осуществления деятельности и подтвердите Заявление на выдачу ключа доступа к ЕГАИС."
    sent_message = bot.send_message(call.message.chat.id, step5_text)
    messages_to_delete.append(sent_message.message_id)

    # Картинка для шага 7
    try:
        with open(EVOTOR_RSA_STEP3_IMAGE, 'rb') as step3_photo:
            sent_photo = bot.send_photo(call.message.chat.id, step3_photo)
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Шаг 3' с message_id {sent_photo.message_id}")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением для шага 3.")
        logging.error(f"Не удалось найти файл: {EVOTOR_RSA_STEP3_IMAGE}")

    # Шаг 6
    step6_text = "Нажмите Сгенерировать сертификат и дождитесь подтверждения о его записи на ключевой носитель."
    sent_message = bot.send_message(call.message.chat.id, step6_text)
    messages_to_delete.append(sent_message.message_id)

    # Шаг 7
    step7_text = "Вернитесь в раздел Настройки → ЕГАИС → Настроить УТМ → На терминале.\n\n*Важно:\nВ процессе запуска УТМ при вводе реквизитов необходимо указывать данные юридического лица. В ином случае при продаже алкоголя будет возникать ошибка.*"

    # Кнопка "Предыдущее меню"
    markup = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton("Предыдущее меню", callback_data="utm_problem")
    markup.add(button_back)

    sent_message = bot.send_message(call.message.chat.id, step7_text, reply_markup=markup)
    messages_to_delete.append(sent_message.message_id)

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'reinstall_utm')
def reinstall_utm_info(call):
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбран пункт 'Переустановка УТМ' пользователем {call.from_user.id}")
    delete_messages(call)

    # Картинка для шага 1
    try:
        with open(REINSTALL_UTM_STEP1_IMAGE, 'rb') as step1_photo:
            sent_photo = bot.send_photo(call.message.chat.id, step1_photo)
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Шаг 1' с message_id {sent_photo.message_id}")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением для шага 1.")
        logging.error(f"Не удалось найти файл: {REINSTALL_UTM_STEP1_IMAGE}")

 # Шаг 1
    step1_text = """Если УТМ нужно переустановить, рекомендую зайти в Настройки → ЕГАИС → УТМ на терминале и сделать фото или переписать реквизиты организации, так как они могут не подгрузиться. КПП для юрлиц КПП потребуется тоже вводить вручную. После этого:

Откройте на Эвоторе Настройки → ЕГАИС.

Нажмите Переустановить УТМ. Таким образом автоматически запускается удаление, скачивание УТМ и установка и запуск."""

    # Кнопка "Предыдущее меню"
    markup = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton("Предыдущее меню", callback_data="utm_problem")
    markup.add(button_back)

    sent_message = bot.send_message(call.message.chat.id, step1_text, reply_markup=markup)
    messages_to_delete.append(sent_message.message_id)

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'remove_utm')
def remove_utm_info(call):
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбран пункт 'Удаление УТМ' пользователем {call.from_user.id}")
    delete_messages(call)

    # Шаг 1
    step1_text = """Удаление УТМ нужно, если вы перестали продавать алкоголь, перешли на УТМ, работающий по локальной сети, или если УТМ не запускается."""
    sent_message = bot.send_message(call.message.chat.id, step1_text)
    messages_to_delete.append(sent_message.message_id)

    # Картинка для шага 2
    try:
        with open(REMOVE_UTM_STEP1_IMAGE, 'rb') as step1_photo:
            sent_photo = bot.send_photo(call.message.chat.id, step1_photo)
            messages_to_delete.append(sent_photo.message_id)
            logging.debug(f"Отправлено фото 'Шаг 1' с message_id {sent_photo.message_id}")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: Не удалось найти файл с изображением для шага 1.")
        logging.error(f"Не удалось найти файл: {REMOVE_UTM_STEP1_IMAGE}")

    # Шаг 2
    step2_text = """Откройте на Эвоторе Настройки → ЕГАИС.
Нажмите Удалить УТМ."""

    # Кнопка "Предыдущее меню"
    markup = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton("Предыдущее меню", callback_data="utm_problem")
    markup.add(button_back)

    sent_message = bot.send_message(call.message.chat.id, step2_text, reply_markup=markup)
    messages_to_delete.append(sent_message.message_id)

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'no_network')
def no_network_menu(call):
    global in_st2f_section
    in_st2f_section = False  # Сбрасываем флаг
    logging.debug(f"Выбран раздел 'Нет сети' пользователем {call.from_user.id}")
    delete_messages(call)

    # Шаг 1
    step1_text = """Зажмите кнопку включения Эвотора на 3 секунды и в появившемся окне выберите Перезагрузить.
После перезагрузки зайдите в ‎Ещё → ‎Настройки → ‎Передача данных → ‎Мобильные, убедитесь что Передача данных включена, а Лимит трафика отключён.
Если это не помогло, перейдите в Ещё → ‎Настройки → ‎Wi-Fi и выключите Wi-Fi.
Если это не помогло, выполните сброс сетевых настроек. Для этого откройте ‎Если 3G не ловит, а ловит E, зайдите в Ещё → ‎Настройки → Передача данных → Мобильные. Нажмите на иконку с тремя точками, выберите ‎Мобильные сети. Выберите тип сети 2G. Если находитесь в отдалённом регионе, включите интернет-роуминг в том же меню. Если сигнала сети совсем нет, замените смарт-карту на другую из комплекта Эвотор.
Если предыдущие действия не помогли, обратитесь в сервисный центр.
Во избежание потенциальных проблем с интернетом воспользуйтесь универсальной смарт-картой Эвотор, которая автоматически подключается к лучшему сигналу связи."""

    # Кнопка "Предыдущее меню"
    markup = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton("Предыдущее меню", callback_data="evotor_menu")
    markup.add(button_back)

    sent_message = bot.send_message(call.message.chat.id, step1_text, reply_markup=markup)
    messages_to_delete.append(sent_message.message_id)

    bot.answer_callback_query(call.id)


def show_sigma_menu(call):
    bot.send_message(call.message.chat.id, "Раздел Sigma в разработке")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)


def show_atol_menu(call):
    bot.send_message(call.message.chat.id, "Раздел Атол в разработке")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)


def show_розница_1с_menu(call):
    bot.send_message(call.message.chat.id, "Раздел 1С Розница в разработке")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)


def show_другое_menu(call):
    bot.send_message(call.message.chat.id, "Раздел Другое в разработке")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'contact_managers_menu')
def contact_managers_menu(call):
    markup = create_contact_managers_menu() # type: ignore
    bot.send_message(call.message.chat.id, "Выберите опцию:", reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'show_phone')
def show_phone(call):
    bot.send_message(call.message.chat.id, "Вы можете связаться с нашими менеджерами по телефону +7 (XXX) XXX-XX-XX")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'ask_question')
def ask_question(call):
    user_id = call.from_user.id
    print(f"ask_question: user_id = {user_id}")
    bot.send_message(user_id, "Пожалуйста, напишите ваш вопрос менеджерам:")
    user_states[user_id] = {'state': 'manager', 'message_id': call.message.id}
    print(f"ask_question: user_states = {user_states}")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'own_question')
def own_question(call):
    user_id = call.from_user.id
    bot.send_message(user_id, "Пожалуйста, напишите ваш вопрос:")
    user_states[user_id] = {'state': 'question', 'message_id': call.message.id}
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    print(f"handle_message: message.from_user.id = {message.from_user.id}") # Добавьте для отладки
    user_id = message.from_user.id
    if user_id in user_states:
        print(f"handle_message: user_id in user_states") # Добавьте для отладки
        state = user_states[user_id]['state']
        print(f"handle_message: state = {state}") # Добавьте для отладки
        if state == 'manager':
            print(f"handle_message: state == 'manager'") # Добавьте для отладки
            caption = f"Вопрос для менеджеров от пользователя {message.from_user.username} ({message.from_user.id}):"
        elif state == 'question':
            print(f"handle_message: state == 'question'") # Добавьте для отладки
            caption = f"Свой вопрос от пользователя {message.from_user.username} ({message.from_user.id}):"
        else:
            caption = f"Сообщение от пользователя {message.from_user.username} ({message.from_user.id}):"

        try:
            bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)
            print(f"handle_message: Сообщение переслано в канал")
        except Exception as e:
            bot.send_message(user_id, f"Ошибка при пересылке сообщения: {e}")
            logging.error(f"Ошибка при пересылке сообщения: {e}")
            print(f"handle_message: Ошибка при пересылке: {e}")
        finally:
            del user_states[user_id] #сбрасываем состояние пользователя
            bot.send_message(message.chat.id, "Ваш вопрос отправлен!")
    else:
        print(f"handle_message: user_id NOT in user_states") # Добавьте для отладки
        pass  # Обработка обычных сообщений

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Обработчик нажатий на Inline-кнопки."""
    global messages_to_delete, in_st2f_section

    # Сохраняем message_id нажатой кнопки в messages_to_delete
    messages_to_delete.append(call.message.message_id)

    #  Проверяем, перешли ли мы из раздела ST2F в другой
    if in_st2f_section:
        # Если да, то удаляем старые сообщения
        delete_messages(call)
        in_st2f_section = False

    if call.data == 'evotor_menu':
        evotor_menu(call)  # показывает кнопки "Эвотор"
    elif call.data == 'show_main_menu':
        show_main_menu(call)  # показывает главное меню
    elif call.data == 'sigma_menu':
        show_sigma_menu(call)
    elif call.data == 'atol_menu':
        show_atol_menu(call)
    elif call.data == 'розница_1с_menu':
        show_розница_1с_menu(call)
    elif call.data == 'другое_menu':
        show_другое_menu(call)
    elif call.data == 'no_power':
        no_power_menu(call)  # показывает кнопку выбора моделей
    elif call.data == 'problem_list':
        problem_list_menu(call)  # показывает список проблем
    elif call.data == 'custom_question':
        text = "Опишите свой вопрос, и мы постараемся вам помочь."
        bot.send_message(call.message.chat.id, text)
        # TODO: Здесь можно добавить функциональность для обработки вопросов пользователей

    bot.answer_callback_query(call.id)  # Убираем "часики" на кнопке

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    bot.infinity_polling()