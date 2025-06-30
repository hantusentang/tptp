from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import logging
import os

API_TOKEN = os.getenv("A8118828836:AAGiHoK4LE7rf0ihCJfBt8AA_zDPnTrfySM")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    contact_btn = KeyboardButton("📱 Bagikan Kontak", request_contact=True)
    keyboard.add(contact_btn)
    await message.answer("Halo! 👋\nSilakan bagikan kontak kamu:", reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact_handler(message: types.Message):
    contact = message.contact
    user_id = message.from_user.id
    user_data[user_id] = {'contact': contact}
    await message.answer("✅ Kontak diterima!\n\nSekarang, silakan ketik pesan kamu:")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def text_handler(message: types.Message):
    user_id = message.from_user.id
    user_msg = message.text

    if user_id in user_data and 'contact' in user_data[user_id]:
        contact = user_data[user_id]['contact']

        await message.answer(
            f"📞 Kontak:\nNama: {contact.first_name}\nNomor: {contact.phone_number}\n\n"
            f"💬 Pesan kamu:\n{user_msg}"
        )

        del user_data[user_id]
    else:
        await message.answer("❗ Silakan kirim kontak terlebih dahulu.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
