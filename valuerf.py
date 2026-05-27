from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

TOKEN = "8847119724:AAGudqiuhIdAoehPBwTCnJKywUmeoKxb7_E"

# ---------- Функция получения курса валют (ExchangeRate-API) ----------
def get_currency_rate(currency_code):
    """Возвращает курс валюты к рублю (USD, EUR, CNY)."""
    url = "https://api.exchangerate-api.com/v4/latest/RUB"
    try:
        response = requests.get(url)
        data = response.json()
        rate = data['rates'][currency_code]
        return round(rate, 2)
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
async def metals_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🥇 Золото", callback_data="gold")],
        [InlineKeyboardButton("🥈 Серебро", callback_data="silver")],
        [InlineKeyboardButton("💍 Платина", callback_data="PLAT")],
        [InlineKeyboardButton("🪨 Палладий", callback_data="PLD")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "🪙 Выбери драгоценный металл:",
        reply_markup=reply_markup
    )

# ---------- Меню валют ----------
async def currencies_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🇺🇸 Доллар", callback_data="USD")],
        [InlineKeyboardButton("🇪🇺 Евро", callback_data="EUR")],
        [InlineKeyboardButton("🇨🇳 Юань", callback_data="CNY")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "💵 Выбери валюту:",
        reply_markup=reply_markup
    )

# ---------- Обработка всех кнопок ----------
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await start(update, context)
        return

    # ========== ДРАГОЦЕННЫЕ МЕТАЛЛЫ ==========
    if data == "metals":
        await metals_menu(update, context)
        return

    # Золото
    if data == "gold":
        url = "https://iss.moex.com/iss/engines/currency/markets/selt/boards/selt/securities/GOLD.json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data_json = response.json()
                last_price = data_json['marketdata']['data'][0][2]
                text = f"🥇 Золото: {last_price} ₽"
            else:
                text = "❌ Ошибка при получении данных"
        except:
            text = "❌ Не удалось подключиться к серверу"
        await query.edit_message_text(text)
        await metals_menu(update, context)
        return

    # Серебро
    if data == "silver":
        url = "https://iss.moex.com/iss/engines/currency/markets/selt/boards/selt/securities/SILV.json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data_json = response.json()
                last_price = data_json['marketdata']['data'][0][2]
                text = f"🥈 Серебро: {last_price} ₽"
            else:
                text = "❌ Ошибка при получении данных"
        except:
            text = "❌ Не удалось подключиться к серверу"
        await query.edit_message_text(text)
        await metals_menu(update, context)
        return

    # Платина
    if data == "PLAT":
        url = "https://iss.moex.com/iss/engines/currency/markets/selt/boards/selt/securities/PLAT.json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data_json = response.json()
                last_price = data_json['marketdata']['data'][0][2]
                text = f"💍 Платина: {last_price} ₽"
            else:
                text = "❌ Ошибка при получении данных"
        except:
            text = "❌ Не удалось подключиться к серверу"
        await query.edit_message_text(text)
        await metals_menu(update, context)
        return

    # Палладий
    if data == "PLD":
        url = "https://iss.moex.com/iss/engines/currency/markets/selt/boards/selt/securities/PLD.json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data_json = response.json()
                last_price = data_json['marketdata']['data'][0][2]
                text = f"🪨 Палладий: {last_price} ₽"
            else:
                text = "❌ Ошибка при получении данных"
        except:
            text = "❌ Не удалось подключиться к серверу"
        await query.edit_message_text(text)
        await metals_menu(update, context)
        return

    # ========== ВАЛЮТЫ ==========
    if data == "currencies":
        await currencies_menu(update, context)
        return

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
        await currencies_menu(update, context)
        return

    # ========== АКЦИИ (ЗАГОТОВКА) ==========
    if data == "stocks":
        await query.edit_message_text("📈 Раздел с акциями в разработке. Скоро появится!")
        await start(update, context)
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