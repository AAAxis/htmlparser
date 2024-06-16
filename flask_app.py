import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello @{update.effective_user.first_name}')

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Please provide link here')



# Define a function to parse data from a link
def parse_link(link_url):
    try:
        response = requests.get(link_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract the title from the webpage
            title = soup.get_text()
            return title
    except Exception as e:
        print(f"An error occurred while parsing the link: {e}")
    return None

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        link_url = update.message.text
        parsed_data = parse_link(link_url)

        if parsed_data:
            await update.message.reply_text(f'Data from the link: {parsed_data}')
        else:
            await update.message.reply_text('Unable to parse data from the provided link')

app = ApplicationBuilder().token("TOKEN").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("link", link))

app.add_handler(MessageHandler(filters.TEXT, handle_link))

app.run_polling()


