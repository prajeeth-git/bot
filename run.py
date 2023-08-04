from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from web_scarpping import AttendanceScraper
import os
scraper = AttendanceScraper()

print("Server is running.... ")
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton

def start_function(update: Update, context):
    command_list = []
    print(dispatcher.handlers)
    for handler in dispatcher.handlers[0]:
        print(handler)
        if isinstance(handler, CommandHandler):
            command_list.append("/"+handler.command[0])
    print(command_list,"dsv")
    # Create keyboard buttons for each command
    buttons = [InlineKeyboardButton(command, callback_data=command) for command in command_list]
    
    # Create the inline keyboard markup
    reply_markup = InlineKeyboardMarkup([buttons])
    
    update.message.reply_text(
        "Welcome to IARE Attendance Bot!\n\nPlease select a command from the options below:",
        reply_markup=reply_markup
    )
def help_function(update: Update, context):
    command_list = []
    print(dispatcher.handlers[0])

    for handler in dispatcher.handlers[0]:
        if isinstance(handler, CommandHandler):
            command_list.append("/"+handler.command[0])
    command_options = "\n".join(command_list)

    help_message = f"Available commands:\n\n{command_options}"
    context.bot.send_message(text=help_message,chat_id=update.effective_chat.id)

def attendance_function(update: Update, context):
    context.bot.send_message(text="To view your attendance summary, please provide your roll number.",chat_id=update.effective_chat.id)
    handle_roll_number(update,context)

def schedule_function(update: Update, context):
    update.message.reply_text("To view your class schedule, please provide your roll number.")

def handle_roll_number(update: Update, context):
    roll_number = update.message.text
    if roll_number and not roll_number.startswith('/'):
        # Use the roll number to retrieve attendance data
        attendance_data = scraper.scrape_attendance(roll_number)
        # Process the attendance data and send the response to the user
        if attendance_data=="Invalid":
            update.message.reply_text("Please provide vaild roll number")
        else:
            response = scraper.display_attendance(attendance_data)
            update.message.reply_text(response)
def is_non_command_text(update: Update) -> bool:
    """Check if the message is non-empty text and not a command."""
    message_text = update.message.text
    return bool(message_text and not message_text.startswith('/'))
def callback_handler(update: Update, context):
    query = update.callback_query
    command = query.data
    query.answer()
    
    if command == '/attendance':
        attendance_function(update, context)
    elif command == '/schedule':
        schedule_function(update, context)
    elif command=="/start":
        start_function(update,context)
    else:
        help_function(update, context)

def message_handler_function(update: Update, context):
    update.message.reply_text("I'm sorry, I don't understand that command. Please use one of the available commands.")

# Create an Updater instance using your bot token
updater = Updater(token=os.environ.get('API_KEY'), use_context=True)

# Get the Dispatcher instance from the Updater
dispatcher = updater.dispatcher

# Define the command handlers
start_handler = CommandHandler('start', start_function)
help_handler = CommandHandler('help', help_function)
attendance_handler = CommandHandler('attendance', attendance_function)
schedule_handler = CommandHandler('schedule', schedule_function)

# Register the command handlers with the dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(attendance_handler)
dispatcher.add_handler(schedule_handler)
dispatcher.add_handler(help_handler)

callback_query_handler = CallbackQueryHandler(callback_handler)

# Define the message handler
message_handler = MessageHandler(Filters.text & ~Filters.command, handle_roll_number)

# Register the message handler with the dispatcher
dispatcher.add_handler(message_handler)
dispatcher.add_handler(callback_query_handler)
# Start the bot
updater.start_polling()

# Run the bot
updater.idle()
