import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

logging.basicConfig(level=logging.INFO)

# ========== НОВЫЙ ТОКЕН ==========
BOT_TOKEN = "8507342702:AAF6mFeR25bxXUUS1qYbzF3H3G_7cp8UP_0"

# Твой HTTP прокси
PROXY_URL = "http://modeler_QAv4mN:kPWXfPcIVHSs@45.86.163.132:16216"

CHANNEL_ID = "-1003545128797"
CHANNEL_LINK = "https://t.me/+jsNubEq-f7U2ZjE0"
# ================================

dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
        is_subscribed = member.status in ["member", "administrator", "creator"]
    except:
        is_subscribed = False

    if is_subscribed:
        await message.answer(
            "✅ Вы уже подписаны на канал!\n\n"
            "🎉 2000 робуксов уже начислены на ваш аккаунт!\n"
            "Спасибо, что с нами! ❤️"
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="📢 Получить доступ",
                    callback_data="get_access"
                )]
            ]
        )
        await message.answer(
            "👋 Привет! Сердечко ❤️\n\n"
            "Чтобы начать пользоваться ботом и получить 2000 робуксов БЕСПЛАТНО, "
            "вам нужно подписаться на мой канал!\n\n"
            "📌 После подписки робуксы будут выданы автоматически.",
            reply_markup=keyboard
        )


@dp.callback_query(F.data == "get_access")
async def get_access_callback(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="📢 Подать заявку в канал",
                url=CHANNEL_LINK
            )],
            [InlineKeyboardButton(
                text="✅ Проверить подписку",
                callback_data="check_subscription"
            )]
        ]
    )
    await callback.message.edit_text(
        "👋 Привет! Сердечко ❤️\n\n"
        "Чтобы начать пользоваться ботом и получить 2000 робуксов БЕСПЛАТНО, "
        "вам нужно подписаться на мой канал!\n\n"
        "📌 Нажмите кнопку ниже, чтобы подать заявку, "
        "а затем нажмите «Проверить подписку»",
        reply_markup=keyboard
    )
    await callback.answer("Нажмите «Подать заявку», чтобы вступить в канал")


@dp.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback.from_user.id)
        is_subscribed = member.status in ["member", "administrator", "creator"]

        if is_subscribed:
            await callback.message.edit_reply_markup(reply_markup=None)
            await callback.message.edit_text(
                "✅ Успех! Почти готово! 🟢\n\n"
                "🎉 Вы успешно подписались на канал!\n"
                "2000 робуксов уже начислены на ваш аккаунт!\n"
                "Спасибо, что с нами! ❤️"
            )
            await callback.answer("Подписка подтверждена! 🎉")
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="📢 Подать заявку в канал",
                        url=CHANNEL_LINK
                    )],
                    [InlineKeyboardButton(
                        text="🔄 Проверить еще раз",
                        callback_data="check_subscription"
                    )]
                ]
            )
            await callback.message.edit_reply_markup(reply_markup=keyboard)
            await callback.answer(
                "❌ Вы ещё не подали заявку или не вступили в канал!",
                show_alert=True
            )
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        await callback.answer(
            "❌ Произошла ошибка. Попробуйте позже.",
            show_alert=True
        )


async def main():
    global bot
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    print("🚀 Бот запущен через HTTP прокси!")
    print(f"📡 Прокси: {PROXY_URL}")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
