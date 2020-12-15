import telebot
import sqlite3

TOKEN = '1268365491:AAGmlas6mpDglUDRcLspq48cqvqe0C9aHVw'
#Bot init
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

#Keyboard creator
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Туда', 'Суда')

#DB init
def db_init():
    global conn, cursor
    conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

#Answer handling
@bot.message_handler(commands=['start'])
def start_message(message):
    db_init()
    
    cursor.execute("SELECT * FROM users WHERE user_id = {}".format(message.chat.id))
    # If we have no such dialogue in DB
    if cursor.fetchone() == None:
        # Save new user to DB
        cursor.execute("""INSERT INTO users 
                       VALUES ('{user_id}', '{nickname}', 
                       '{state}', '{location}')""".format(
                       user_id=message.chat.id, 
                       nickname='', 
                       state='registration', 
                       location='start'))
        # Save DB changes
        conn.commit()
        
        cursor.execute("SELECT * FROM users")
        print('New user created by {} user_id'.format(message.chat.id))
        
        # Ask for a nickname
        bot.send_message(message.chat.id, "Добро пожаловать в мир Ботии!\n"
                         "Дла начала следует создать персонажа, которым вы будете исследовать мир.\n"
                         "Пожалуйста, <b>напишите желаемое имя вашего персонажа</b> в сообщении - оно должно быть уникальным в мире Ботии, и его можно будет изменить позже.")
    else:
        bot.send_message(message.chat.id, 'Вы уже начинали со мной диалог, нет необходимости делать это снова.')
        print('User {} already exists in database'.format(message.chat.id))

@bot.message_handler(content_types=['text'])
def send_text(message):
    db_init()
    cursor.execute("SELECT state FROM users WHERE user_id = {}".format(message.chat.id))
    
    state = cursor.fetchone()[0]
    # Registration, setting nickname
    if state == 'registration':
        #добавить проверку на уникальность ника
        
        sql = """
        UPDATE users
        SET nickname = '{}', state = 'game started'
        WHERE user_id = '{}'""".format(message.text, message.chat.id)
        cursor.execute(sql)
        conn.commit()
        print('User {} registered in DB by nickname {}'.format(message.chat.id, message.text))
        bot.send_message(message.chat.id, 'Так и появился на свет Ботии герой {}!'.format(message.text), reply_markup=keyboard1)

print("Bot started")

#Prevent program from closing at the end of the script
bot.polling()