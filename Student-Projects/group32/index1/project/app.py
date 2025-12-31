from flask import Flask, render_template, request, jsonify
import re
import random   # برای انتخاب رندوم

app = Flask(__name__)

# دیتابیس کتاب‌ها با لینک اختصاصی طاقچه
books = [
    # کلاسیک‌ها
    {"title": "غرور و تعصب", "author": "جین آستین", "year": 1813, "genre": "عاشقانه", "buy_link": "https://taaghche.com/book/70634"},
    {"title": "دراکولا", "author": "برام استوکر", "year": 1897, "genre": "ترسناک", "buy_link": "https://taaghche.com/book/63945"},
    {"title": "شازده کوچولو", "author": "آنتوان دو سنت اگزوپری", "year": 1943, "genre": "کودک", "buy_link": "https://taaghche.com/book/70633"},
    {"title": "1984", "author": "جورج اورول", "year": 1949, "genre": "سیاسی", "buy_link": "https://taaghche.com/book/63946"},
    {"title": "صد سال تنهایی", "author": "گابریل گارسیا مارکز", "year": 1967, "genre": "رمان", "buy_link": "https://taaghche.com/book/63947"},
    {"title": "تاریخچه زمان", "author": "استیون هاوکینگ", "year": 1988, "genre": "علمی", "buy_link": "https://taaghche.com/book/56321"},
    {"title": "هفت عادت مردمان موثر", "author": "استفان کاوی", "year": 1989, "genre": "توسعه فردی", "buy_link": "https://taaghche.com/book/11223"},
    {"title": "بیندیشید و ثروتمند شوید", "author": "ناپلئون هیل", "year": 1937, "genre": "توسعه فردی", "buy_link": "https://taaghche.com/book/67891"},

    # کتاب‌های جدیدتر (۲۰۰۰ تا ۲۰۲۵) 
    {"title": "هری پاتر و یادگاران مرگ", "author": "جی. کی. رولینگ", "year": 2007, "genre": "فانتزی", "buy_link": "https://taaghche.com/book/12345"},
    {"title": "مردی به نام اوه", "author": "فردریک بکمن", "year": 2012, "genre": "رمان", "buy_link": "https://taaghche.com/book/70515"},
    {"title": "هنر شفاف اندیشیدن", "author": "رولف دوبلی", "year": 2013, "genre": "توسعه فردی", "buy_link": "https://taaghche.com/book/63948"},
    {"title": "سیر عشق", "author": "آلن دوباتن", "year": 2016, "genre": "عاشقانه", "buy_link": "https://taaghche.com/book/12348"},
    {"title": "Educated", "author": "تارا وستوور", "year": 2018, "genre": "زندگینامه", "buy_link": "https://taaghche.com/book/12349"},
    {"title": "Where the Crawdads Sing", "author": "دلیا اوونز", "year": 2018, "genre": "رمان", "buy_link": "https://taaghche.com/book/12350"},
    {"title": "Project Hail Mary", "author": "اندی وییر", "year": 2021, "genre": "علمی-تخیلی", "buy_link": "https://taaghche.com/book/12351"},
    {"title": "Tomorrow, and Tomorrow, and Tomorrow", "author": "گابریلا زوین", "year": 2022, "genre": "رمان", "buy_link": "https://taaghche.com/book/12352"},
    {"title": "Fourth Wing", "author": "ربکا یاروس", "year": 2023, "genre": "فانتزی", "buy_link": "https://taaghche.com/book/12353"},
    {"title": "House of Flame and Shadow", "author": "سارا جی. ماس", "year": 2025, "genre": "فانتزی", "buy_link": "https://taaghche.com/book/12354"},
]

@app.route("/")
def home():
    return render_template("index.html")

def year_range(message):
    try:
        if message.isdigit():
            y = int(message)
        else:
            match = re.search(r"\d{3,4}", message)
            if match:
                y = int(match.group())
            else:
                return None
        start = y - 20
        end = y + 20
        return start, end
    except:
        return None

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    results = []

    # --- ژانر ---
    if user_message == "ژانر":
        reply = "سلام 📚 می‌تونی ژانر مورد علاقه‌ت رو انتخاب کنی:<br>"
        reply += "از بین اسامی زیر انتخاب کن:<br>"
        genres = list(set([book["genre"] for book in books]))
        for g in genres:
            reply += f"- {g}<br>"
        return jsonify({"reply": reply})

    # --- نویسنده ---
    if user_message == "نویسنده":
        reply = "سلام دوست من ✍️ این لیست نویسنده‌هاست:<br>"
        reply += "از بین اسامی زیر انتخاب کن:<br>"
        authors = list(set([book["author"] for book in books]))
        for a in authors:
            reply += f"- {a}<br>"
        return jsonify({"reply": reply})

    # --- سال انتشار ---
    if user_message == "سال انتشار":
        reply = "سلام رفیق 📅 سال مورد نظرتو وارد کن تا کتاب‌های نزدیک به اون سال رو پیدا کنم"
        return jsonify({"reply": reply})

    # --- کتاب رندوم ---
    if "یه کتاب دیگه معرفی کن" in user_message:
        book = random.choice(books)
        reply = f"📚 پیشنهاد رندوم:<br>- {book['title']} ({book['author']}, {book['year']})<br>"
        reply += f"<a href='{book['buy_link']}' target='_blank'>{book['buy_link']}</a><br><br>"
        return jsonify({"reply": reply})

    # --- جستجو بر اساس ژانر ---
    for book in books:
        if book["genre"] == user_message:
            results.append(book)

    # --- جستجو بر اساس نویسنده ---
    for book in books:
        if book["author"] == user_message:
            results.append(book)

    # --- جستجو بر اساس سال ---
    yr = year_range(user_message)
    if yr:
        start, end = yr
        for book in books:
            if start <= book["year"] <= end:
                results.append(book)

    # --- نمایش نتایج ---
    if results:
        reply = "📚 پیشنهادها:<br>"
        for b in results[:5]:
            reply += f"- {b['title']} ({b['author']}, {b['year']})<br>"
            reply += f"<a href='{b['buy_link']}' target='_blank'>{b['buy_link']}</a><br><br>"
    else:
        reply = "  متاسفم کتابت پیدا نشد،میتونی یه کتاب دیگه انتخاب کنی"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
