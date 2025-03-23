import sqlite3
import pytest
from project import has_voted_today, save_vote, get_mood_keyboard
@pytest.fixture
def test_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE votes (
        user_id INTEGER PRIMARY KEY, 
        vote TEXT, 
        date TEXT
    )''')
    conn.commit()
    return conn
def test_save_vote(test_db):
    save_vote(12345, "happy", test_db)
    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM votes WHERE user_id=12345")
    assert cursor.fetchone() is not None

# تست بررسی رأی کاربر
def test_has_voted_today(test_db):
    """بررسی اینکه آیا تابع has_voted_today می‌تواند تشخیص دهد که کاربر امروز رأی داده یا نه"""
    cursor = test_db.cursor()
    cursor.execute("INSERT INTO votes (user_id, vote, date) VALUES (?, ?, ?)", (67890, "sad", "2025-03-22"))
    test_db.commit()

    assert has_voted_today(67890, test_db) == True  # کاربر 67890 باید قبلاً رأی داده باشد.
    assert has_voted_today(99999, test_db) == False  # کاربر 99999 نباید رأی داده باشد.

# تست دکمه‌های کیبورد
def test_get_mood_keyboard():
    """بررسی اینکه آیا تابع get_mood_keyboard دکمه‌های مناسب ایجاد می‌کند؟"""
    keyboard = get_mood_keyboard()
    buttons = [btn.text for row in keyboard.inline_keyboard for btn in row]  # استخراج متن دکمه‌ها

    assert len(buttons) == 5  # باید ۵ دکمه وجود داشته باشد.
    assert "😄" in buttons  # اطمینان از وجود استیکرهای حالت روحی
    assert "😀" in buttons
    assert "🙂" in buttons
    assert "😞" in buttons
    assert "😔" in buttons
