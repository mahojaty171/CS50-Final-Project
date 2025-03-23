import sqlite3, datetime, matplotlib.pyplot as plt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
EXCLUDED_USER_ID = 5838692281
MOOD_LIST = {"smile": "😄", "grin": "😀", "neutral": "🙂", "sad": "😞", "pensive": "😔"}
MOOD_MSG = {
    "smile": "😊 The world is happy!", "grin": "😃 The world is in a great mood!", 
    "neutral": "🤔 The world feels neutral.", "sad": "😞 The world is feeling down.", 
    "pensive": "😔 The world is in deep thought."}
def init_db():
    with sqlite3.connect("votes.db") as db:
        db.execute("CREATE TABLE IF NOT EXISTS votes (user_id INTEGER, vote TEXT, date TEXT)")
def create_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton(MOOD_LIST[key], callback_data=key)] for key in MOOD_LIST])
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_chart(update)
    await update.message.reply_text("How are you feeling today?", reply_markup=create_keyboard())
def get_top_mood():
    with sqlite3.connect("votes.db") as db:
        mood = db.execute("SELECT vote FROM votes GROUP BY vote ORDER BY COUNT(*) DESC LIMIT 1").fetchone()
    return MOOD_MSG.get(mood[0], "No mood data yet.") if mood else "No votes recorded yet."
async def send_chart(update: Update):
    with sqlite3.connect("votes.db") as db:
        records = db.execute("SELECT date, vote, COUNT(*) FROM votes GROUP BY date, vote").fetchall()
    if not records:
        await update.message.reply_text("No voting data available yet!")
        return
    dates = sorted(set(row[0] for row in records))
    vote_counts = {mood: [0] * len(dates) for mood in MOOD_LIST}
    for date, vote, count in records:
        vote_counts[vote][dates.index(date)] = count
    plt.figure(figsize=(8, 5))
    for mood, counts in vote_counts.items():
        plt.plot(dates, counts, marker="o", label=MOOD_LIST[mood])
    plt.xlabel("Date"), plt.ylabel("Vote Count"), plt.title("Mood Poll Stats")
    plt.legend(), plt.xticks(rotation=45), plt.tight_layout(), plt.savefig("stats.png"), plt.close()
    mood_msg = get_top_mood()
    if update.message:
        await update.message.reply_photo(photo=open("stats.png", "rb"), caption=mood_msg)
    elif update.callback_query:
        await update.callback_query.message.reply_photo(photo=open("stats.png", "rb"), caption=mood_msg)
async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query, user_id, mood = update.callback_query, update.callback_query.from_user.id, update.callback_query.data
    today = str(datetime.date.today())
    if user_id == EXCLUDED_USER_ID:
        return await query.answer("❌ You are not allowed to vote!")
    with sqlite3.connect("votes.db") as db:
        if db.execute("SELECT 1 FROM votes WHERE user_id = ? AND date = ?", (user_id, today)).fetchone():
            return await query.answer("You have already voted today! 😊")
        db.execute("INSERT INTO votes (user_id, vote, date) VALUES (?, ?, ?)", (user_id, mood, today))
    await query.answer("Your vote has been recorded! 📊")
    await send_chart(query.message)
async def get_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your Telegram ID: {update.message.from_user.id}")
def main():
    TOKEN = "7798189595:AAF79ChRLikdUrveIXJ_zVJ3URDhe9k7wSg"
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(vote))
    app.add_handler(CommandHandler("stats", send_chart))
    app.add_handler(CommandHandler("id", get_user_id))
    app.run_polling()
if __name__ == "__main__":
    main()