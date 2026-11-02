# handlers/leaderboard.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import aiosqlite
from database import DB_NAME

router = Router()

@router.callback_query(F.data == "leaderboard")
async def show_leaderboard(callback: CallbackQuery):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT full_name, points FROM users ORDER BY points DESC LIMIT 10;") as cursor:
            top_users = await cursor.fetchall()

    text = "🏆 **Top 10 Kiber-Himoyachilar Reytingi**\n\n"
    
    if not top_users:
        text += "📭 Hozircha reytingda foydalanuvchilar yo'q."
    else:
        for idx, (name, pts) in enumerate(top_users, 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
            safe_name = name or "Foydalanuvchi"
            score = pts if pts is not None else 0
            text += f"{medal} **{safe_name}** — `{score}` ball\n"

    text += "\n💡 *Ball to'plash uchun Kiber-Maktab testlaridan o'ting!*"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")]]
    )
    
    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    except Exception:
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
        
    await callback.answer()