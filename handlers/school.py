# handlers/school.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Kiber-Maktab asosiy menyusi
@router.callback_query(F.data == "cyber_school")
async def cyber_school_menu(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧠 Kiber-Gigiyena testi", callback_data="start_quiz")],
            [InlineKeyboardButton(text="📖 Asosiy qoidalar", callback_data="security_rules")],
            [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")]
        ]
    )
    await callback.message.edit_text(
        "📚 **Kiber-Maktabga xush kelibsiz!**\n\n"
        "Bu yerda siz raqamli xavfsizlik qoidalarini o'rganishingiz va bilimlaringizni sinab ko'rishingiz mumkin.\n\n"
        "Bo'limni tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

# Testni boshlash (1-savol)
@router.callback_query(F.data == "start_quiz")
async def start_quiz(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="A) Darhol kodni aytaman", callback_data="quiz_wrong")],
            [InlineKeyboardButton(text="B) Hech kimga bermayman va o'chiraman", callback_data="quiz_correct")],
            [InlineKeyboardButton(text="C) Do'stimga yuboraman", callback_data="quiz_wrong")]
        ]
    )
    await callback.message.edit_text(
        "🧠 **1-savol:**\n\n"
        "Sizga noma'lum raqamdan qo'ng'iroq qilishib, bank xodimi ekanligini aytishdi va SMS kodni so'rashdi. Siz nima qilasiz?",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

# To'g'ri javob
@router.callback_query(F.data == "quiz_correct")
async def quiz_correct_answer(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Testni qayta boshlash", callback_data="start_quiz")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="cyber_school")]
        ]
    )
    await callback.message.edit_text(
        "✅ **To'g'ri! Barakalla!**\n\n"
        "Hech qachon va hech kimga (bank xodimiga ham) SMS kodlarni bermang. Haqiqiy bank xodimlari hech qachon SMS kodni so'rashmaydi.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

# Noto'g'ri javob
@router.callback_query(F.data == "quiz_wrong")
async def quiz_wrong_answer(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Qayta urinib ko'rish", callback_data="start_quiz")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="cyber_school")]
        ]
    )
    await callback.message.edit_text(
        "❌ **Xato! Bu juda xavfli!**\n\n"
        "Agar SMS kodni boshqalarga bersangiz, firibgarlar akkauntingiz yoki bank kartangizni boshqarib olishi mumkin. Hushyor bo'ling!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

# Xavfsizlik qoidalari
@router.callback_query(F.data == "security_rules")
async def security_rules(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="cyber_school")]
        ]
    )
    await callback.message.edit_text(
        "📖 **Eng muhim 3 ta kiberxavfsizlik qoidasi:**\n\n"
        "1. **Parollar:** Har bir sayt uchun alohida va murakkab parol ishlating.\n"
        "2. **Ikki bosqichli tasdiqlash (2FA):** Telegram va boshqa ijtimoiy tarmoqlaringizda 2 bosqichli parolni yoqib qo'ying.\n"
        "3. **Shubhali havolalar:** Tanish bo'lmagan havolalarga kirmang va shaxsiy ma'lumotlaringizni kiritmang.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()