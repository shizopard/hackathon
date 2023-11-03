import telebot
from telebot import types
import json

bot = telebot.TeleBot(' ')

with open('vacancies.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
current_vacancy_index = 0

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        navigator_button = types.KeyboardButton("⭐ Навигатор МГКЭИТ")
        vacancy_button = types.KeyboardButton("🎓 Вакансии")
        skip = types.KeyboardButton("")
        job_button = types.KeyboardButton("💼 Помощь в трудоустройстве")
        resume_tips = types.KeyboardButton("📄 Советы по резюме")
        buttons.add(navigator_button, vacancy_button, skip, job_button, resume_tips)
        bot.send_message(message.chat.id, "Привет!\nБот помогает в трудоустройстве студентам МГКЭИТ\nДля просмотра основной информации, используй меню", reply_markup=buttons)
    
    elif message.text == "⭐ Навигатор МГКЭИТ":
        bot.send_message(message.chat.id, "Навигатор МГКЭИТ - удобный сервис, в котором также можно получить информацию по трудоустройству.\nНавигатор доступен по адресу: http://navigator.mgkeit")
    
    elif message.text == "🎓 Вакансии":
        markup = types.InlineKeyboardMarkup()
        it = types.InlineKeyboardButton("IT-отделение", callback_data="it")
        design = types.InlineKeyboardButton("Графический дизайн", callback_data="design")
        electrical_installation = types.InlineKeyboardButton("Электромонтажные работы", callback_data="electrical_installation")

        markup.row(it, design)
        markup.row(electrical_installation)
        bot.send_message(message.chat.id, "Выберите своё отделение", reply_markup=markup)
    
    elif message.text == "💼 Помощь в трудоустройстве":
        markup = types.InlineKeyboardMarkup()
        employment_department = types.InlineKeyboardButton("Отдел трудоустройства", callback_data="employment_department")
        individual_graphic = types.InlineKeyboardButton("Индивидуальный график", callback_data="individual_graphic")
        faq = types.InlineKeyboardButton("FAQ", callback_data="FAQ")
        markup.row(employment_department, individual_graphic)
        markup.row(faq)
        bot.send_message(message.chat.id, "Что вас интересует?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global current_vacancy_index

    def send_menu_message(chat_id):
        markup = types.InlineKeyboardMarkup()
        employment_department = types.InlineKeyboardButton("Отдел трудоустройства", callback_data="employment_department")
        individual_graphic = types.InlineKeyboardButton("Индивидуальный график", callback_data="individual_graphic")
        faq = types.InlineKeyboardButton("Составление резюме", callback_data="FAQ")
        markup.row(employment_department, individual_graphic)
        markup.row(faq)
        bot.send_message(chat_id, "Что вас интересует?", reply_markup=markup)

    markup = types.InlineKeyboardMarkup()
    back_to_menu = types.InlineKeyboardButton("Назад", callback_data="back_to_menu")
    back_to_start = types.InlineKeyboardButton("В меню", callback_data="back_to_start")
    markup.row(back_to_menu, back_to_start)

    if call.data == "employment_department":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Отдел трудоустройства МГКЭИТ помогает студентам в трудоустройстве: поиск подходящих вакансий, развитие собственного резюме и портфолио.",
                              reply_markup=markup)

    elif call.data == "individual_graphic":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Индивидуальный график обучения позволяет перевестись на самые разные формы обучения: заочная форма обучения или график 2/2, 3/3.\n\nПеревод на индивидуальный график доступен только студентам, работающим по специальности.\nПодробнее можно узнать у куратора группы или в отделе трудоустройства",
                              reply_markup=markup)

    elif call.data == "help_resources":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Навигатор МГКЭИТ: navigator.mgkeit\nТелеграм-канал Работа от МГКЭИТ: t.me/VacanciMGKEIT")

    elif call.data == "back_to_menu":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send_menu_message(call.message.chat.id)

    elif call.data == "FAQ":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="- Структура резюме: резюме должно содержать четкую и легко читаемую структуру. Обычно оно включает разделы: контактные данные, цель, образование, опыт работы, гибкие и профессиональные навыки. Рекомендуем включить сюда сертификаты с пройденных курсов, если таковые имеются.\n\n- Пишите резюме грамотно: избегайте грамматические и стилистические ошибки.\n\n- Старайтесь подстраивать резюме под разные вакансии: выделяйте опыт и навыки, наиболее соответствующие требованиям работодателей.\n\n- Укажите ссылки на профили в социальных сетях в самом резюме, это можно сделать в разделе 'Контакты'.\n\n- Используйте стандартные форматы файлов, чтоб они открывались на всех операционных системах. Лучший формат для резюме - .pdf",
                              reply_markup=markup)

    elif call.data == "back_to_start":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send_start_message(call.message.chat.id)

    # ВАКАНСИИ
    elif call.data == "it":
        vacancy_buttons = types.InlineKeyboardMarkup()
        back_to_start = types.InlineKeyboardButton("В меню", callback_data="back_to_start")
        next_button = types.InlineKeyboardButton(">", callback_data="next")
        back_button = types.InlineKeyboardButton("<", callback_data="back")
        vacancy_buttons.row(back_button, back_to_start, next_button)

        send_vacancy_message(call.message.chat.id, current_vacancy_index, call.message.message_id, vacancy_buttons)

    elif call.data == "next":
        if current_vacancy_index < len(data) - 1:
            current_vacancy_index += 1
            vacancy_buttons = types.InlineKeyboardMarkup()
            back_to_start = types.InlineKeyboardButton("В меню", callback_data="back_to_start")
            next_button = types.InlineKeyboardButton(">", callback_data="next")
            back_button = types.InlineKeyboardButton("<", callback_data="back")
            vacancy_buttons.row(back_button, back_to_start, next_button)
            send_vacancy_message(call.message.chat.id, current_vacancy_index, call.message.message_id, vacancy_buttons)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Это последняя доступная вакансия. Возвращаемся назад.")
            current_vacancy_index = 0

    elif call.data == "back":
        if current_vacancy_index > 0:
            current_vacancy_index -= 1
            vacancy_buttons = types.InlineKeyboardMarkup()
            back_to_start = types.InlineKeyboardButton("В меню", callback_data="back_to_start")
            next_button = types.InlineKeyboardButton(">", callback_data="next")
            back_button = types.InlineKeyboardButton("<", callback_data="back")
            vacancy_buttons.row(back_button, back_to_start, next_button)
            send_vacancy_message(call.message.chat.id, current_vacancy_index, call.message.message_id, vacancy_buttons)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Это первая доступная вакансия.")
            current_vacancy_index = 0

def send_vacancy_message(chat_id, vacancy_index, message_id, reply_markup=None):
    if 0 <= vacancy_index < len(data):
        vacancy = data[vacancy_index]
        vacancy_message = f"<b>Название вакансии:</b> {vacancy['name']}\n"
        vacancy_message += f"<b>Компания:</b> {vacancy['company']}\n"
        vacancy_message += f"<b>Зарплата:</b> {vacancy['salary'] if vacancy.get('salary') else 'Не указана'}\n"
        vacancy_message += f"<b>Задачи:</b>\n<i>{vacancy['tasks']}</i>\n"
        vacancy_message += f"<b>Требования:</b>\n<i>{vacancy['requirements']}</i>\n"
        vacancy_message += f"<b>График:</b>{vacancy['graphic']['name'] if vacancy.get('schedule') else 'Не указан'}\n"
        vacancy_message += f"<b>Ссылка на вакансию:</b><i>{vacancy['vacancy_link']}</i>\n"

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=vacancy_message, reply_markup=reply_markup, parse_mode="HTML")

def send_start_message(chat_id):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    navigator_button = types.KeyboardButton("⭐ Навигатор МГКЭИТ")
    vacancy_button = types.KeyboardButton("🎓 Вакансии")
    skip = types.KeyboardButton("")
    job_button = types.KeyboardButton("💼 Помощь в трудоустройстве")
    events = types.KeyboardButton("🗓️ События")
    resume_tips = types.KeyboardButton("📄 Советы по резюме")
    buttons.add(navigator_button, vacancy_button, skip, job_button, events, skip, resume_tips)
    bot.send_message(chat_id, "Привет!\nБот помогает в трудоустройстве студентам МГКЭИТ\nДля просмотра основной информации, используй меню", reply_markup=buttons)

bot.polling(none_stop=True, interval=0)
