# handlers/admin.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import aiosqlite
from config import ADMIN_IDS, DB_NAME

router = Router()

class BroadcastState(StatesGroup):
    waiting_for_message = State()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Sizda bu buyruqdan foydalanish huquqi yo'q.")
        return

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM users;") as cursor:
            users_count = (await cursor.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM scam_reports;") as cursor:
            reports_count = (await cursor.fetchone())[0]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Barchaga xabar tarqatish", callback_data="start_broadcast")],
            [InlineKeyboardButton(text="📋 So'nggi xabarlarni ko'rish", callback_data="view_reports")]
        ]
    )

    admin_text = (
        "🛠 **Admin Panel / Statistika**\n\n"
        f"👥 Jami foydalanuvchilar: `{users_count}` ta\n"
        f"🚨 Kelib tushgan kiber-xabarlar: `{reports_count}` ta\n\n"
        "Quyidagi boshqaruv elementlaridan birini tanlang:"
    )
    await message.answer(admin_text, reply_markup=keyboard, parse_mode="Markdown")

@router.callback_query(F.data == "view_reports")
async def view_scam_reports(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("Huquqingiz yo'q!", show_alert=True)
        return

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT report_text, created_at FROM scam_reports ORDER BY id DESC LIMIT 5;") as cursor:
            reports = await cursor.fetchall()

    if not reports:
        await callback.message.answer("📭 Hozircha hech qanday kiber-xabar kelib tushmagan.")
        await callback.answer()
        return

    reports_text = "📋 **So'nggi kelib tushgan 5 ta xabar:**\n\n"
    for idx, (text, date) in enumerate(reports, 1):
        reports_text += f"{idx}. 🕒 `{date}`\n💬 `{text}`\n\n-------------------\n"

    await callback.message.answer(reports_text, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "start_broadcast")
async def ask_broadcast_message(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("Huquqingiz yo'q!", show_alert=True)
        return

    await callback.message.answer(
        "📢 **Xabar tarqatish rejimi**\n\n"
        "Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni (matn, rasm yoki video) yuboring:"
    )
    await state.set_state(BroadcastState.waiting_for_message)
    await callback.answer()

@router.message(BroadcastState.waiting_for_message)
async def send_broadcast(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id FROM users;") as cursor:
            users = await cursor.fetchall()

    success_count = 0
    fail_count = 0

    status_msg = await message.answer("⏳ Xabar tarqatilmoqda, iltimos kuting...")

    for (user_id,) in users:
        try:
            await message.send_copy(chat_id=user_id)
            success_count += 1
        except Exception:
            fail_count += 1

    await status_msg.edit_text(
        f"✅ **Xabar tarqatish yakunlandi!**\n\n"
        f"• Muvaffaqiyatli yuborildi: `{success_count}` ta\n"
        f"• Xatoliklar (bloklaganlar): `{fail_count}` ta",
        parse_mode="Markdown"
    )
    await state.clear()