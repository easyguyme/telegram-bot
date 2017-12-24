import re
import time
import telebot
import instagram_engine
import datetime
import pytz
import logging
import settings
from telebot import util
from dbhelper import DBHelper
from apscheduler.schedulers.background import BackgroundScheduler


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
scheduler = BackgroundScheduler()
bot = telebot.TeleBot(settings.token)
db = DBHelper()


# ============================================= #


#WEBHOOK_HOST = '0.0.0.0'
#WEBHOOK_PORT = 8443  # 443, 80, 88, 8443 
#WEBHOOK_LISTEN = '0.0.0.0'  

#WEBHOOK_SSL_CERT = './webhook_cert.pem'  
#WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  

#WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
#WEBHOOK_URL_PATH = "/%s/" % (settings.token)



# ============================================= #


chat_id = settings.chat_id
tlgrmList = []
usersList = []
oldUsers = []
superadmins = [236514781]


# ============================================= #


def game():
    global usersList
    global tlgrmList
    global oldUsers
    try:
        roundList = list(usersList)
        usersList = []
        tlgrmList = []
        leechers = {}
        allUsers = oldUsers + roundList
        print "All users: ", allUsers
        for insta_data in allUsers:
            print insta_data
            username_index = allUsers.index(insta_data)
            print username_index
            if username_index < 5:
                pass
            else:                
                points = 0
                insta_username = dict(insta_data).keys()[0]                
                insta_self_id = instagram_engine.get_id(insta_username)                
                offset = username_index - 5
                slicedList = allUsers[offset:(username_index - 1)]
                for post_data in slicedList:
                    post = dict(post_data).values()[0]
                    shortcode = post.split('/')[4]
                    try:
                        likesList = instagram_engine.get_likes(shortcode)
                        commentsList = instagram_engine.get_comments(shortcode)
                        if str(insta_self_id) in likesList and str(insta_self_id) in commentsList:
                            points += 1
                        else:
                            pass
                    except Exception as e:
                        points += 1
                        print e
                        continue
                if points >= 1:
                    pass
                else:
                    warnings = db.get_warnings(insta_username)
                    tlgrm_id = db.get_tlgrm_id(insta_username)
                    if warnings == 3:
                        bot.kick_chat_member(chat_id, tlgrm_id)
                        db.del_tlgrm_user(tlgrm_id)
                    else:
                        db.add_warning(insta_username)
                        leechers[insta_username] = (warnings + 1)
        if len(leechers) > 0:
            text = 'GROUP LEECHERS:\n\n'
            for leecher in leechers.keys():
                warnings = leechers[leecher]
                text += '<b>@' + (str(leecher) + '</b> - ' + str(warnings) + '/3 warnings\n')
            bot.send_message(chat_id, text, parse_mode='HTML')
        else:
            bot.send_message(chat_id, 'GROUP LEECHERS:\n\nIn the last 30 minutes we had no leechers!')
        oldUsers = list(allUsers[-5:])
        roundList = []
        allUsers = []
    except Exception as e:
        print e


# ============================================= #


#@bot.message_handler(content_types=['text'])
#def handle_text(message):
#    print message


@bot.message_handler(commands=['start'])
def handle_text(message):
    if message.chat.type == "private":        
        text = "Hello %s! Contact @ajcartas to join the game." % message.from_user.first_name
        bot.send_message(tlgrm_id, text)


@bot.message_handler(commands=['alladmins'])
def handle_text(message):
    if message.chat.type == "private" and message.from_user.id in superadmins:
        admins = db.all_admins()
        text = "All admins:\n\n"
        for admin in admins:
            if str(admin[0]) == 'none':
                pass
            else:
                text += "<b>@%s</b>\n" % (str(admin[0]))
        bot.send_message(message.from_user.id, text, parse_mode='HTML')



@bot.message_handler(commands=['addadmin'])
def handle_text(message):
    if message.chat.type == "private" and message.from_user.id in superadmins:
        text = "Send me an instagram username without @."
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, add_admin)


def add_admin(message):
    global admins
    insta_user = db.get_insta_username(message.text)
    if insta_user is not None:
        tlgrm_id = db.get_tlgrm_id(insta_user) 
        db.add_admin(tlgrm_id)
        bot.send_message(message.chat.id, 'Admin added!')
    else:
        bot.send_message(message.chat.id, 'Incorrect username. Try again.')
        

@bot.message_handler(commands=['deladmin'])
def handle_text(message):
    if message.chat.type == "private" and message.from_user.id in superadmins:
        text = "Send me an instagram username without @."
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, del_admin)


def del_admin(message):
    global admins
    insta_user = db.get_insta_username(message.text)
    if insta_user is not None:
        tlgrm_id = db.get_tlgrm_id(insta_user)        
        db.del_admin(tlgrm_id)
        bot.send_message(message.chat.id, 'Admin deleted!')    
    else:
        bot.send_message(message.chat.id, 'Incorrect username. Try again.')
       
        

@bot.message_handler(commands=['delwarning'])
def handle_text(message):
    if message.chat.type == "private" and message.from_user.id in superadmins:
        text = "Send me an instagram username without @"
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, del_warning)


def del_warning(message):
    insta_user = db.get_insta_username(message.text)
    if insta_user is not None:
        db.del_warning(insta_user)
        bot.send_message(message.chat.id, 'Warning removed!')
    else:
        bot.send_message(message.chat.id, 'Incorrect username. Try again.')
        

@bot.message_handler(commands=['allwarnings'])
def handle_text(message):
    if message.chat.type == "private" and message.from_user.id in superadmins:
        warnings = db.all_warnings()
        text = "All warnings:\n\n"
        for warning in warnings:
            if str(warning[0]) == 'none':
                pass
            else:
                text += "<b>@%s</b>: %s\n" % (str(warning[0]), str(warning[1]))
        splitted_text = util.split_string(text, 3000)
        for text in splitted_text:
            bot.send_message(message.chat.id, text, parse_mode='HTML')


# ============================================= #


@bot.message_handler(content_types=['text'])
def handle_text(message):
    global tlgrmList
    global usersList
    tlgrm_id = message.from_user.id
    words = message.text.replace('\n', ' ')
    words = words.split(' ')
    if message.text.lower().startswith('dx5'): 
        if len(words) == 3:            
            insta_user = words[1].replace('@', '')
            post = words[2]
            shortcode = post.split('/')[4]
            if {insta_user: post} in usersList or {insta_user: post} in oldUsers:
                bot.delete_message(chat_id, message.message_id)
            else:
                try:
                    insta_self_id = instagram_engine.get_id(insta_user)
                    post_owner_id = instagram_engine.get_post_owner(shortcode)
                    followers = instagram_engine.get_followers(insta_user)
                    if str(insta_self_id) != str(post_owner_id):
                        bot.delete_message(chat_id, message.message_id)
                        text = "Dear %s, I deleted your message because the given link doesn't match to given username. Try again." % message.from_user.first_name
                        bot.send_message(chat_id, text, parse_mode='HTML')
                    elif followers < 100:
                        bot.delete_message(chat_id, message.message_id)
                        text = "Dear %s, I deleted your message because you don't have enough followers." % message.from_user.first_name
                        bot.send_message(chat_id, text, parse_mode='HTML')
                    else:
                        if tlgrm_id in tlgrmList[-5:]:
                            bot.delete_message(chat_id, message.message_id)
                            text = "Dear %s, please don't flood, you are already sent your username and post." % message.from_user.first_name
                            bot.send_message(chat_id, text, parse_mode='HTML')
                        else:
                            bot.pin_chat_message(chat_id, message.message_id)
                            tlgrmList.append(tlgrm_id)
                            usersList.append({insta_user: post})
                            check_user = db.get_tlgrm_user(tlgrm_id)        
                            if check_user is None:
                                db.add_tlgrm_user(tlgrm_id, insta_user)
                            elif check_user is not None:
                                db.change_insta_user(insta_user, tlgrm_id)
                except Exception as e:
                    bot.delete_message(chat_id, message.message_id)
                    print e
        elif len(words) > 3:
            bot.delete_message(chat_id, message.message_id)
            text = "Dear %s, I deleted your message because it doesn't match the format. Please send only messages like this:\n\nDx5 <b>@username</b>\nhttps://instagram.com/p/{post-id}/" % message.from_user.first_name
            bot.send_message(chat_id, text, parse_mode='HTML')
    elif re.findall(r'admin.post', message.text, re.IGNORECASE) != []:
        is_admin = db.get_admin(message.from_user.id)
        if is_admin != 'none':
            pass
        else:
            bot.delete_message(chat_id, message.message_id)
            text = 'User trying to send admin post:\n\nFirst name: %s\nLast name: %s\nUsername: %s' % (message.from_user.first_name, message.from_user.last_name, message.from_user.username)
            bot.send_message(superadmins[0], text)
    elif re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                    message.text, re.IGNORECASE) != []:
        bot.delete_message(chat_id, message.message_id)
        text = "Dear %s, I deleted your message because it doesn't match the format. Please send only messages like this:\n\nDx5 <b>@username</b>\nhttps://instagram.com/p/{post-id}/" % message.from_user.first_name
        bot.send_message(chat_id, text, parse_mode='HTML')    
    
    
            
    
    
# ============================================= #


#bot.remove_webhook()
#time.sleep(3)
#bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
#certificate=open(WEBHOOK_SSL_CERT, 'r'))


# ============================================= #



scheduler.add_job(game, 'interval', minutes=30)
scheduler.start()

print "Bot started"

while True:
    try:      
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(e)
        time.sleep(15)
        continue
