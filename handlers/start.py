# handlers/start.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
import aiosqlite
from database import DB_NAME

router = Router()

def get_main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀 ── [ Mini App (Veb Panel) ] ── 🌐", web_app=WebAppInfo(url="https://sizning-sayt.uz/index.html")),
            ],
            [
                InlineKeyboardButton(text="🤖 AI Maslahatchi", callback_data="ai_consultant"),
                InlineKeyboardButton(text="🔍 Link Tekshiruv", callback_data="check_link")
            ],
            [
                InlineKeyboardButton(text="📱 APK Tahlil", callback_data="check_apk"),
                InlineKeyboardButton(text="🔗 URL Unpacker", callback_data="unpack_url")
            ],
            [
                InlineKeyboardButton(text="🔑 Parol Generator", callback_data="generate_password"),
                InlineKeyboardButton(text="📝 SMS Analizator", callback_data="scan_text")
            ],
            [
                InlineKeyboardButton(text="🕵️‍♂️ Qora Ro'yxat", callback_data="check_blacklist"),
                InlineKeyboardButton(text="🏆 Kiber-Reyting", callback_data="leaderboard")
            ],
            [
                InlineKeyboardButton(text="📚 Kiber-Maktab", callback_data="cyber_school"),
                InlineKeyboardButton(text="📊 Xavfsizlik Bali", callback_data="security_score")
            ],
            [
                InlineKeyboardButton(text="🚨 ── [ Kiber-Xabar & SOS ] ── 🚨", callback_data="report_scam")
            ]
        ]
    )

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id FROM users WHERE user_id = ?;", (user_id,)) as cursor:
            exists = await cursor.fetchone()

        if not exists:
            await db.execute(
                "INSERT INTO users (user_id, full_name, username, security_score) VALUES (?, ?, ?, ?);",
                (user_id, full_name, username, 60)
            )
        else:
            await db.execute(
                "UPDATE users SET full_name = ?, username = ? WHERE user_id = ?;",
                (full_name, username, user_id)
            )
        await db.commit()

    user_name = message.from_user.first_name
    welcome_text = (
        f"╔═══════════════════════════╗\n"
        f"  🛡 **CYBERGUARD UZBEKISTAN** 🛡\n"
        f"╚═══════════════════════════╝\n\n"
        f"Assalomu alaykum, **{user_name}**!\n"
        "Siz milliy raqamli xavfsizlik markazidasiz.\n\n"
        "Quyidagi premium xizmatlardan birini tanlang:"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    user_name = callback.from_user.first_name
    welcome_text = (
        f"╔═══════════════════════════╗\n"
        f"  🛡 **CYBERGUARD UZBEKISTAN** 🛡\n"
        f"╚═══════════════════════════╝\n\n"
        f"Assalomu alaykum, **{user_name}**!\n"
        "Quyidagi premium xizmatlardan birini tanlang:"
    )
    try:
        await callback.message.edit_text(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")
    except Exception:
        await callback.message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await callback.answer()