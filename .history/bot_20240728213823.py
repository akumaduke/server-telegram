from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import os
import shutil

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# List of authorized users
username_list = ['irrefrac']

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    reply = "Welcome to my world. \nI am a bot developed by Othniel.\nSend /help command to see what I can do."
    await update.message.reply_text(reply)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    admin = update.message.from_user.username
    if admin == username_list[0]:
        reply = '''Send /get folder_name/file_name.extension to receive a file. 
                \nSend /ls folder_name to show list of files.
                \nSend /put folder_name/file_name.extension to upload last sent file.
                \nSend /mkdir folder_name to create a Folder.
                \nSend /remove folder_name/filename.extension to delete a file.
                \nSend /adduser username to give access.
                \nSend /removeuser username to revoke access.
                \nSend /showuser to show list of users
                '''    
    else:
        reply = '''Send /get folder_name/file_name.extension to receive a file. 
                \nSend /ls folder_name to show list of files.
                \nSend /put folder_name/file_name.extension to upload last sent file.
                \nSend /mkdir folder_name to create a Folder.
                '''
    await update.message.reply_text(reply)

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send requested file."""
    username = update.message.from_user.username
    if username not in username_list:
        await update.message.reply_text("You are not Authorized.")
        return
    file = update.message.text.split(" ")[-1]
    if file == "/send":
        await update.message.reply_text("Invalid File name.")
    else:
        reply = "Finding and Sending the requested file to you. Hold on..."
        await update.message.reply_text(reply)
        path = os.getcwd() + '/' + file
        if os.path.exists(path):
            await context.bot.send_document(chat_id=update.message.chat_id, document=open(path, 'rb'))
        else:
            await update.message.reply_text("File not Found.")

async def ls(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show files in requested directory."""
    username = update.message.from_user.username
    if username not in username_list:
        await update.message.reply_text("You are not Authorized.")
        return
    file = update.message.text.split(" ")[-1]
    if file == "/show":
        await update.message.reply_text("Invalid Directory name.")
    else:
        reply = "Finding and Sending a list of files to you. Hold on..."
        await update.message.reply_text(reply)
        path = os.getcwd() + '/' + file
        if os.path.exists(path):
            await update.message.reply_text(str(os.listdir(path)))
        else:
            await update.message.reply_text("Directory not Found.")

async def put(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    f = open(str(os.getcwd()) + "/file", "r")
    file_id = f.read()
    f.close()
    if file_id == "":
        await update.message.reply_text("You didn't upload file.")
    else:
        new_file = await context.bot.get_file(file_id)
        message = update.message.text.split(" ")
        path = message[-1]
        if len(path) < 1:
            await update.message.reply_text("Enter Path correctly.")
        else:
            await new_file.download_to_drive(os.getcwd() + '/' + path)
            await update.message.reply_text("File Stored.")

async def mkdir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text.split(" ")
    if len(message) < 1 or message[-1] == "/mkdir":
        await update.message.reply_text("Invalid Syntax. Refer syntax in help section.")
        return
    path = os.getcwd() + "/" + message[-1]
    os.mkdir(path)
    await update.message.reply_text("Folder Created.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    if update.message.document:
        file_id = update.message.document.file_id
        f = open(str(os.getcwd()) + "/file", "w")
        f.write(file_id)
        f.close()
        await update.message.reply_text("Received. Now send file name and location to store using /put command.")
    else:
        reply = "Invalid Input."
        await update.message.reply_text(reply)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    admin = update.message.from_user.username
    if admin == username_list[0]:
        username = update.message.text.split(" ")[-1]
        username_list.append(username)
        await update.message.reply_text("User added.")
    else:
        await update.message.reply_text("You are not Authorized.")

async def show_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    admin = update.message.from_user.username
    if admin == username_list[0]:
        await update.message.reply_text(str(username_list))
    else:
        await update.message.reply_text("You are not Authorized.")

async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    admin = update.message.from_user.username
    if admin == username_list[0]:
        username = update.message.text.split(" ")[-1]
        username_list.remove(username)
        await update.message.reply_text("User Removed.")
    else:
        await update.message.reply_text("You are not Authorized.")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    admin = update.message.from_user.username
    if admin == username_list[0]:
        filename = update.message.text.split(" ")[-1]
        os.remove(os.getcwd() + "/" + filename)
        await update.message.reply_text("File Removed.")
    else:
        await update.message.reply_text("You are not Authorized.")

async def rmdir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    admin = update.message.from_user.username
    if admin == username_list[0]:
        filename = update.message.text.split(" ")[-1]
        shutil.rmtree(os.getcwd() + "/" + filename)
        await update.message.reply_text("Folder Removed.")
    else:
        await update.message.reply_text("You are not Authorized.")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    TOKEN = os.environ['TOKEN']
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("get", get))
    application.add_handler(CommandHandler("ls", ls))
    application.add_handler(CommandHandler("put", put))
    application.add_handler(CommandHandler("mkdir", mkdir))

    # admin functionalities
    application.add_handler(CommandHandler("adduser", add_user))
    application.add_handler(CommandHandler("showuser", show_user))
    application.add_handler(CommandHandler("removeuser", remove_user))
    application.add_handler(CommandHandler("remove", remove))
    application.add_handler(CommandHandler("rmdir", rmdir))

    # on noncommand i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.Document.ALL, echo))

    # log all errors
    application.add_error_handler(error)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()