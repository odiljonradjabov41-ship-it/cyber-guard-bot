# handlers/security_tools.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import hashlib
import random
import string
import aiohttp
from config import VIRUSTOTAL_API_KEY

router = Router()

# Parol generatori
@router.callback_query(F.data == "generate_password")
async def generate_password_handler(callback: CallbackQuery):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    pwd = "".join(random.choice(chars) for _ in range(16))
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Yangisini yaratish", callback_data="generate_password")],
            [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")]
        ]
    )
    
    await callback.message.edit_text(
        f"🔐 **Maxsus Xavfsiz Parol Yaratildi:**\n\n"
        f"`{pwd}`\n\n"
        f"💡 *Bu parol 16 ta belgidan iborat bo'lib, xavfsiz hisoblanadi.*",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()


# .APK faylni tekshirish
class ApkCheckState(StatesGroup):
    waiting_for_apk = State()

@router.callback_query(F.data == "check_apk")
async def ask_apk(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📱 **Soxta .apk Ilovani Tekshirish**\n\n"
        "Iltimos, tekshirmoqchi bo'lgan Android ilovangizni (`.apk` fayl ko'rinishida) botga yuboring:"
    )
    await state.set_state(ApkCheckState.waiting_for_apk)
    await callback.answer()

@router.message(ApkCheckState.waiting_for_apk, F.document)
async def process_apk_file(message: Message, state: FSMContext):
    document = message.document
    if not document.file_name.endswith('.apk'):
        await message.answer("❌ Bu fayl `.apk` formatida emas. Iltimos, haqiqiy Android dastur faylini yuboring:")
        return

    wait_msg = await message.answer("⏳ Fayl yuklanib, xavfsizlik bazalarida (VirusTotal) tahlil qilinmoqda...")

    try:
        file = await message.bot.get_file(document.file_id)
        file_bytes = await message.bot.download_file(file.file_path)
        file_hash = hashlib.sha256(file_bytes.read()).hexdigest()

        headers = {"x-apikey": VIRUSTOTAL_API_KEY}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    stats = data["data"]["attributes"]["last_analysis_stats"]
                    malicious = stats.get("malicious", 0)
                    
                    if malicious > 0:
                        result = f"⚠️ **DIQQAT! BU ILOVA XAVFLI (VIRUS TOPILDI)!** 🔴\nTahdidlar soni: `{malicious}`"
                    else:
                        result = "✅ **Toza.** Bu fayl xavfsiz deb topildi."
                else:
                    result = "🛡 Fayl bazada topilmadi, lekin noma'lum dasturlarni o'rnatishda ehtiyot bo'ling!"
        
        await wait_msg.edit_text(result, parse_mode="Markdown")
    except Exception:
        await wait_msg.edit_text("⚠️ Tahlil qilish vaqtida xatolik yuz berdi.")
    
    await state.clear()