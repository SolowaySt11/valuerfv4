from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

TOKEN = "8847119724:AAGudqiuhIdAoehPBwTCnJKywUmeoKxb7_E"

# ---------- Функция курсов валют (ExchangeRate-API) ----------
def get_currency_rate(currency_code):
    url = "https://api.exchangerate-api.com/v4/latest/RUB"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        rate = data['rates'][currency_code]
        return round(rate, 2)
    except:
        return None

# ---------- Функция цен металлов (MOEX) ----------
def get_metal_price(ticker):
    url = f"https://iss.moex.com/iss/engines/currency/markets/selt/boards/selt/securities/{ticker}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['marketdata']['data'][0][2]
        else:
            return None
    except:
        return None

# ---------- Главное меню ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🪙 Драгоценные металлы", callback_data="metals")],
        [InlineKeyboardButton("💵 Валюты", callback_data="currencies")],
        [InlineKeyboardButton("📈 Акции", callback_data="stocks")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🏭 *Инвестиционный дашборд*\n\n"
        "Здравствуй! Выбери категорию:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ---------- Меню драгметаллов ----------
async def metals_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text="🪙 Выбери драгоценный металл:"):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🥇 Золото", callback_data="gold")],
        [InlineKeyboardButton("🥈 Серебро", callback_data="silver")],
        [InlineKeyboardButton("💍 Платина", callback_data="PLAT")],
        [InlineKeyboardButton("🪨 Палладий", callback_data="PLD")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message_text, reply_markup=reply_markup)

# ---------- Меню валют ----------
async def currencies_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text="💵 Выбери валюту:"):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🇺🇸 Доллар", callback_data="USD")],
        [InlineKeyboardButton("🇪🇺 Евро", callback_data="EUR")],
        [InlineKeyboardButton("🇨🇳 Юань", callback_data="CNY")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message_text, reply_markup=reply_markup)

# ---------- Обработчик кнопок ----------
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Назад в главное меню
    if data == "main_menu":
        await start(update, context)
        return

    # Показать меню металлов
    if data == "metals":
        await metals_menu(update, context)
        return

    # Показать меню валют
    if data == "currencies":
        await currencies_menu(update, context)
        return

    # ========== МЕТАЛЛЫ ==========
    if data == "gold":
        price = get_metal_price("GOLD")
        text = f"🥇 Золото: {price} ₽" if price else "❌ Не удалось получить цену золота"
        await query.edit_message_text(text)
        return

    if data == "silver":
        price = get_metal_price("SILV")
        text = f"🥈 Серебро: {price} ₽" if price else "❌ Не удалось получить цену серебра"
        await query.edit_message_text(text)
        return

    if data == "PLAT":
        price = get_metal_price("PLAT")
        text = f"💍 Платина: {price} ₽" if price else "❌ Не удалось получить цену платины"
        await query.edit_message_text(text)
        return

    if data == "PLD":
        price = get_metal_price("PLD")
        text = f"🪨 Палладий: {price} ₽" if price else "❌ Не удалось получить цену палладия"
        await query.edit_message_text(text)
        return

    # ========== ВАЛЮТЫ ==========
    if data in ["USD", "EUR", "CNY"]:
        rate = get_currency_rate(data)
        if rate:
            if data == "USD":
                text = f"🇺🇸 Доллар США: {rate} ₽"
            elif data == "EUR":
                text = f"🇪🇺 Евро: {rate} ₽"
            else:
                text = f"🇨🇳 Китайский юань: {rate} ₽"
        else:
            text = "❌ Не удалось получить курс. Попробуй позже."
        await query.edit_message_text(text)
        return

    # Акции (заготовка)
    if data == "stocks":
        await query.edit_message_text("📈 Раздел с акциями в разработке. Скоро появится!")
        return

# ---------- Запасные команды ----------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Используй /start для начала работы.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()