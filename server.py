import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import requests, yaml
from telebot import TeleBot

TOKEN_SERVERBOT = ""
TOKEN_BOT = ""
ADMIN_ID = ""
with open("mybot/actions/config.yml") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    TOKEN_SERVERBOT = data["token_serverbot"]
    TOKEN_BOT = data["token_bot"]
teleBot = TeleBot(TOKEN_BOT)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

headers = {
    'Content-Type': 'application/json'
}



# api_get_conversations = "http://localhost:5005/conversations"
# responses = requests.get(api_get_conversations)
#
# if responses.status_code == 200:
#     conversation_ids = [conv['conversation_id'] for conv in responses.json()]
#     print(conversation_ids)
# else:
#     print("Error getting conversation list. Status code:", responses.status_code)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Xin chào Admin, Chúc bạn một ngày làm việc tốt lành!")


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Xin lỗi, tôi không biết lệnh đó!!!")


async def resume_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_message = ' '.join(context.args).upper()
    api_get_tracker = "http://localhost:5005/conversations/{conversation_id}/tracker".format(
        conversation_id=text_message)
    response = requests.get(api_get_tracker, headers=headers)
    print(response.json())

    response_text = "Không thể bật lại bot cho người dùng với ID: {} hoặc có lỗi xảy ra".format(text_message)
    if "events" in response.json():
        if len(response.json()["events"]) > 3:
            api = "http://localhost:5005/conversations/{conversation_id}/tracker/events".format(
                conversation_id=text_message)
            response = requests.post(api, json={"event": "restart"}, headers=headers)

            response_text = "Đã mở lại bot CTU Students Advisor cho người dùng với ID: {}".format(text_message)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)


async def rep_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response_text = "không thể gửi tin nhắn"

    if len(context.args) >= 2:
        ID = context.args[0]
        message = ' '.join(context.args[1:])
        teleBot.send_message(ID, message)
        response_text = "Đã gửi tin nhắn cho {} thành công".format(ID)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN_SERVERBOT).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    caps_handler = CommandHandler('caps', caps)
    application.add_handler(caps_handler)

    resume_handler = CommandHandler('resume', resume_bot)
    application.add_handler(resume_handler)

    rep_handler = CommandHandler('rep', rep_chat)
    application.add_handler(rep_handler)

    application.run_polling()