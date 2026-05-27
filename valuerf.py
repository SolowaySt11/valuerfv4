from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

TOKEN = "8847119724:AAGudqiuhIdAoehPBwTCnJKywUmeoKxb7_E"

# ---------- Функция получения курса валют ----------
def get_cbr_currency(currency_code):
    url = url = "https://www.cbr.ru/scripts/XML_daily.asp"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")
        valute = soup.find("CharCode", text=currency_code)
        if valute:
            valute_tag = valute.find_parent("Valute")
            nominal = int(valute_tag.find("Nominal").text)
            value = float(valute_tag.find("Value").text.replace(',', '.'))
            return round(value / nominal, 2)
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
async def metals_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🥇 Золото", callback_data="gold")],
        [InlineKeyboardButton("🥈 Серебро", callback_data="silver")],
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

    # Возврат в главное меню
    if data == "main_menu":
        await start(update, context)
        return

    # Драгоценные металлы
    if data == "metals":
        await metals_menu(update, context)
        return

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
        # Возвращаем меню металлов
        await metals_menu(update, context)
        return
    if data == "SILV":
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
        # Возвращаем меню металлов
        await metals_menu(update, context)
        return
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
    # Валюты 
    if data == "currencies":
        await currencies_menu(update, context)
        return

    if data in ["USD", "EUR", "CNY"]:
        rate = get_cbr_currency(data)
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
        # Возвращаем меню валют
        await currencies_menu(update, context)
        return

    # Акции (заготовка)
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