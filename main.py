import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from telegram.error import BadRequest

# Set up logging to see the incoming messages
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to check if the user is an admin or owner
async def is_admin_or_owner(update: Update, user_id: int, context: CallbackContext) -> bool:
    chat_id = update.message.chat_id
    admins = await context.bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in admins]
    
    # Check if the user is the owner (admins include the owner, so this will be handled)
    if user_id in admin_ids:
        return True
    return False

# Function to delete messages that contain links
async def delete_message(update: Update, context: CallbackContext):
    # Log the incoming message to check if the bot is receiving it
    
    
    user_id = update.message.from_user.id
    message = update.message.text
    link_keywords = ["http", "www", "@","join","Join"]

    # Check if the message contains any link (http://, t.me, www)
    if any(keyword in message for keyword in link_keywords):
        # Log the message that contains a link
        logger.info(f"Message contains a link, checking if user is admin or owner...")
        logger.info(f"Received message: {message} from {user_id}")
        # Check if the user is not an admin or owner
        if not await is_admin_or_owner(update, user_id, context):
            try:
                # Delete the message
                logger.info(f"Deleting message from {user_id}")
                await update.message.delete()
            except BadRequest:
                pass  # Ignore errors that may happen when trying to delete messages

# Main function to set up the bot
def main():
    # Replace 'YOUR_BOT_API_TOKEN' with your actual bot token
    application = Application.builder().token("telegrambottoken").build()

    # Register a message handler to delete any messages containing links
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_message))

    # Run the bot with polling
    application.run_polling()

if __name__ == "__main__":
    main()
