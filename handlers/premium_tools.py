# handlers/premium_tools.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import aiohttp
import aiosqlite
from database import DB_NAME

router = Router()

# URL Unpacker (Qisqartirilgan linkni ochish)
class UrlUnpackState(StatesGroup):
    waiting_for_url = State()

@router.callback_query(F.data == "unpack_url")
async def ask_url(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🔗 **URL Unpacker (Linkni yechish)**\n\n"
        "Qisqartirilgan havolani (`bit.ly`, `t.co` va h.k.) yuboring, men uning asl manzilini aniqlab beraman:"
    )
    await state.set_state(UrlUnpackState.waiting_for_url)
    await callback.answer()

@router.message(UrlUnpackState.waiting_for_url)
async def process_unpack(message: Message, state: FSMContext):
    short_url = message.text.strip()
    wait_msg = await message.answer("🔍 Havola manzili tekshirilmoqda...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(short_url, allow_redirects=True) as resp:
                final_url = str(resp.url)
        
        response = (
            f"🌐 **Link tahlili natijasi:**\n\n"
            f"📥 **Qisqartirilgan:** `{short_url}`\n"
            f"📤 **Asl manzil:** `{final_url}`\n\n"
            "⚠️ *Eslatma: Asl manzilni tekshirgandan so'nggina unga kiring!*"
        )
    except Exception:
        response = "❌ Havolani ochishda xatolik yuz berdi. To'g'ri link kiritganingizni tekshiring."

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")]]
    )
    await wait_msg.edit_text(response, reply_markup=keyboard, parse_mode="Markdown")
    await state.clear()


# Shaxsiy Xavfsizlik Bali (Security Score)
@router.callback_query(F.data == "security_score")
async def show_security_score(callback: CallbackQuery):
    user_id = callback.from_user.id

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT security_score, points FROM users WHERE user_id = ?;", (user_id,)) as cursor:
            res = await cursor.fetchone()
            score = res[0] if res else 50
            pts = res[1] if res else 0

    text = (
        f"🛡 **Sizning Raqamli Xavfsizlik Profilingiz**\n\n"
        f"📊 **Xavfsizlik Bali:** `{score} / 100`\n"
        f"🏆 **To'plagan ballaringiz:** `{pts}` ball\n\n"
        "💡 *Maslahat: Ballaringizni oshirish uchun Kiber-Maktab testlaridan o'ting!*"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")]]
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()