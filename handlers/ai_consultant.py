# handlers/ai_consultant.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

class AIConsultantState(StatesGroup):
    waiting_for_question = State()

@router.callback_query(F.data == "ai_consultant")
async def ask_ai_question(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")]
        ]
    )
    await callback.message.answer(
        "🤖 **AI Kiber-Maslahatchi**\n\n"
        "Sizda kiberxavfsizlik, onlayn maxfiylik yoki shubhali vaziyatlar bo'yicha savol bormi?\n"
        "Savolingizni erkin matn ko'rinishida yozib yuboring va men sizga yordam beraman:\n\n"
        "*(Masalan: 'Parollarimni qanday xavfsiz saqlashim mumkin?' yoki 'Shubhali SMS kelsa nima qilish kerak?')*",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await state.set_state(AIConsultantState.waiting_for_question)
    await callback.answer()

@router.message(AIConsultantState.waiting_for_question)
async def process_ai_question(message: Message, state: FSMContext):
    user_question = message.text.strip()
    
    wait_msg = await message.answer("🧠 AI yordamchi savolingizni tahlil qilmoqda, iltimos kuting...")

    # AI Maslahatchining kiberxavfsizlik bo'yicha aqlli javob logikasi
    answer = generate_cyber_advice(user_question)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❓ Yana savol berish", callback_data="ai_consultant")],
            [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")]
        ]
    )

    await wait_msg.edit_text(
        f"💡 **AI Maslahatchi Javobi:**\n\n{answer}",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await state.clear()


def generate_cyber_advice(q: str) -> str:
    """Kiberxavfsizlik mavzusiga moslashgan ekspert javoblari generatori"""
    q_lower = q.lower()

    if "wifi" in q_lower or "wi-fi" in q_lower or "vafe" in q_lower:
        return (
            "🔒 **Wi-Fi xavfsizligi bo'yicha maslahatlar:**\n\n"
            "1. Jamoat joylaridagi ochiq Wi-Fi tarmoqlariga ulanganda **VPN** ishlating.\n"
            "2. Uy Wi-Fi parolini kamida WPA2/WPA3 standarti bilan va murakkab parol bilan himoyalang.\n"
            "3. Ochiq Wi-Fi orqali bank ilovalariga kirmang va xaridlarni amalga oshirmang."
        )
    elif "sms" in q_lower or "kod" in q_lower or "2fa" in q_lower:
        return (
            "📱 **SMS-kodlar va Tasdiqlash xavfsizligi:**\n\n"
            "1. **Hech qachon** Telefoningizga kelgan 4-6 xonali tasdiqlash kodini birovga bermang — hatto o'zini bank yoki operatordan deb tanishtirsa ham!\n"
            "2. Barcha ijtimoiy tarmoq va pochtalarda **Ikki bosqichli tasdiqlash (2FA)** funksiyasini yoqing."
        )
    elif "fishing" in q_lower or "phishing" in q_lower or "havola" in q_lower or "sayt" in q_lower:
        return (
            "🎣 **Fishing (Soxta saytlar)dan himoyalanish:**\n\n"
            "1. Sayt domenini diqqat bilan tekshiring (Masalan: `my.gov.uz` o'rniga `my-gov-uz.ru` bo'lsa, bu soxta).\n"
            "2. Botimizning **'🔍 Havolani tekshirish'** bo'limidan foydalanib linklarni VirusTotal orqali tekshirib oling."
        )
    elif "telegram" in q_lower or "instagram" in q_lower or "akkaunt" in q_lower or "profil" in q_lower:
        return (
            "🛡 **Ijtimoiy tarmoqlar maxfiyligi:**\n\n"
            "1. *Sozlamalar -> Maxfiylik va Xavfsizlik* bo'limidan **Faol seanslar**ni muntazam tekshirib turing.\n"
            "2. Notanish fayllar (`.apk`, `.exe`) yoki 'Sizga ovoz berdim' degan havolalarni ochmang."
        )
    else:
        return (
            f"🛡 **Kiberxavfsizlik bo'yicha umumiy maslahat:**\n\n"
            f"Sizning savolingiz: *\"{q}\"*\n\n"
            "1. **Shaxsiy ma'lumotlar:** Karta raqami amal qilish muddati va CVV kodingizni sir saqlang.\n"
            "2. **Parollar:** Har bir xizmat uchun alohida murakkab parol ishlating.\n"
            "3. **Hushyorlik:** Bepul yutuq, aksiya yoki shoshilinch pul o'tkazmasi haqidagi xabarlarga darhol ishonavermang!"
        )