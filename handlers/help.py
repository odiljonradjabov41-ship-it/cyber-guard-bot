# handlers/help.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.callback_query(F.data == "help_advice")
async def help_main_menu(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Kartadan pul yechib olinsa...", callback_data="help_card")],
            [InlineKeyboardButton(text="📱 Telegram akkaunt o'g'irlansa...", callback_data="help_telegram")],
            [InlineKeyboardButton(text="📸 Instagram akkaunt buzilsa...", callback_data="help_instagram")],
            [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")]
        ]
    )
    await callback.message.edit_text(
        "💡 **Favqulodda Yordam & Maslahat**\n\n"
        "Agar siz yoki tanishlaringiz kiber-firibgarlar qurboni bo'lgan bo'lsa, quyidagi vaziyatlardan birini tanlang va zudlik bilan ko'rsatmalarga amal qiling:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "help_card")
async def help_card_scam(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Orqaga", callback_data="help_advice")]]
    )
    text = (
        "💳 **Bank kartasidan pul yechib olinsa nima qilish kerak?**\n\n"
        "1. **Zudlik bilan kartani bloklang:** Bank ilovasi (Payme, Uzum, Click) orqali yoki bankning qisqa raqamiga qo'ng'iroq qilib kartani vaqtincha bloklang.\n"
        "2. **Bankka murojaat qiling:** Bankning ishonch telefoniga qo'ng'iroq qilib, o'tkazma bo'yicha e'tiroz bildiring (chargeback).\n"
        "3. **Ichki ishlar organlariga xabar bering:** 102 raqamiga yoki hududiy ichki ishlar bo'limiga ariza yozing."
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "help_telegram")
async def help_telegram_scam(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Orqaga", callback_data="help_advice")]]
    )
    text = (
        "📱 **Telegram akkaunt o'g'irilsa nima qilish kerak?**\n\n"
        "1. **Seanslarni yopish:** Agar boshqa qurilmada hali ham ochiq bo'lsa: *Sozlamalar -> Maxfiylik va xavfsizlik -> Faol seanslar -> Barcha boshqa seanslarni yakunlash* tugmasini bosing.\n"
        "2. **Ikki bosqichli tasdiqlash (2FA):** Agar parolingiz o'zgargan bo'lsa, Telegram'ga SMS orqali qayta kirishga harakat qiling va zudlik bulant 2 bosqichli parolni o'rnating."
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "help_instagram")
async def help_instagram_scam(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Orqaga", callback_data="help_advice")]]
    )
    text = (
        "📸 **Instagram akkaunt buzilsa nima qilish kerak?**\n\n"
        "1. **Pochtani tekshiring:** Instagram'dan kelgan xatda «Email manzilingiz o'zgartirildi» degan xabar bo'lsa, xatdagi **«Secure my account»** havolasini bosing.\n"
        "2. **Qo'llab-quvvatlash xizmati:** Kirish oynasidan *«Get help logging in»* orqali shaxsingizni tasdiqlovchi selfie-video yuborish orqali akkauntni tiklang."
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

# Asosiy menyuga qaytish uchun umumiy handler
@router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery):
    from handlers.start import get_main_menu
    user_name = callback.from_user.first_name
    welcome_text = (
        f"Assalomu alaykum, **{user_name}**! 🛡\n\n"
        "Men **CyberGuard Uzbekistan** — kiberxavfsizlik va onlayn firibgarlikdan himoya qiluvchi yordamchingizman.\n\n"
        "Quyidagi xizmatlardan birini tanlang:"
    )
    await callback.message.edit_text(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await callback.answer()