from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

# тут будем писать наш код :)
async def start(update, context):
  dialog.mode = "main"
  text = load_message("main")
  await send_photo(update, context, "main")
  await send_text(update, context, text)
  await show_main_menu(update, context, {
    "start": "главное меню бота",
    "profile": "генерация Tinder-профиля 😎",
    "opener": "сообщение для знакомства 🥰",
    "message": "переписка от вашего имени 😈",
    "date": "переписка со звездами 🔥",
    "gpt": "задать вопрос ChatGPT"
  })
  
async def hello(update, context):
  if dialog.mode == "gpt":
    await gpt_dialog(update, context)
  else:
    await send_text(update, context, "Привет!")
    await send_text(update, context, "Как дела, *дружище*?")
    await send_text(update, context, "Ты написал " + update.message.text)
    await send_photo(update, context, "avatar_main")
    await send_text_buttons(update, context, "Запустить процесс?",{
      "start":"Запустить",
      "stop":"Остановить"
    })

async def hello_button(update, context):
  query = update.callback_query.data
  if query == "start":
    await send_text(update, context, "Процесс запущен")
  else:
    await send_text(update, context, "Процесс остановлен")

async def gpt(update, context):
  dialog.mode = "gpt"
  await send_photo(update, context, "gpt")
  await send_text(update, context, "Напишите сообщение *ChatGPT*:")

dialog = Dialog()
dialog.mode = "main"


async def gpt_dialog(update, context):
  prompt = load_prompt("gpt")
  text = update.message.text
  answer = await chatgpt.send_question("Дай четкий и короткий ответ на вопрос", text)
  await send_text(update, context, answer)



chatgpt = ChatGptService(token="IMAtcJ134WVIxVeFe7I2JFkblB3TH88zgyZ5JYpVQKKxZnKk")

app = ApplicationBuilder().token("6721687181:AAFfQ5GwARdROtJjOGOfypDR2BUQmhm14GE").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
