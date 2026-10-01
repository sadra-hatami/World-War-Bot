<div align="center">

# ربات جنگ جهانی
# 🌍⚔️

### یک بازی استراتژی فارسی برای روبیکا

ربات ناهمگام استراتژی برای روبیکا: بازیکن کشور انتخاب می‌کند، اقتصاد می‌سازد، ارتش بالا می‌آورد، تجارت می‌کند، اتحاد می‌بندد و روی یک صفحهٔ مشترک رقابت می‌کند — با ذخیرهٔ JSON و رابط دکمه‌ای.

<br>

# 👨‍💻 **صدرا حاتمی**

### *توسعه‌دهنده • مهندس نرم‌افزار • سازنده*

<br>

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Rubka](https://img.shields.io/badge/Rubka-Rubika%20Bot-8E44AD?style=for-the-badge)](https://pypi.org/)
[![AsyncIO](https://img.shields.io/badge/AsyncIO-Asynchronous-2C3E50?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/asyncio.html)
[![JSON](https://img.shields.io/badge/Storage-JSON-003B57?style=for-the-badge)](#-معماری)
[![Strategy](https://img.shields.io/badge/Genre-Strategy-C0392B?style=for-the-badge)](#-قابلیتها)
[![Persian](https://img.shields.io/badge/Language-Persian-success?style=for-the-badge)](https://en.wikipedia.org/wiki/Persian_language)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
![Open Source](https://img.shields.io/badge/Open_Source-Project-black?style=for-the-badge&logo=github)
[![Stars](https://img.shields.io/github/stars/sadra-hatami/World-War-Bot?style=for-the-badge)](https://github.com/sadra-hatami/World-War-Bot/stargazers)

<br>

[🌐 پروفایل گیت‌هاب](https://github.com/sadra-hatami)
•
[📘 English README](README.md)
•
[📧 ایمیل](mailto:sadra.hatami.1732@gmail.com)

</div>

---

# 📑 فهرست

- [درباره](#-درباره)
- [مخازن مرتبط](#-مخازن-مرتبط)
- [چرا این پروژه](#-چرا-این-پروژه)
- [قابلیت‌ها](#-قابلیتها)
- [معماری](#-معماری)
- [ساختار](#-ساختار)
- [فناوری‌ها](#-فناوریها)
- [نصب](#-نصب)
- [پیکربندی](#-پیکربندی)
- [استفاده](#-استفاده)
- [مخاطب](#-مخاطب)
- [نقشه راه](#-نقشه-راه)
- [پرسش‌ها](#-پرسشها)
- [امنیت](#-امنیت)
- [مشارکت](#-مشارکت)
- [تماس](#-تماس)
- [مجوز](#-مجوز)
- [حق نشر](#-حق-نشر)
- [حمایت](#-حمایت)

---

# 📖 درباره

**World War Bot** یک بازی استراتژی فارسی برای روبیکا است.

بازیکن سرور، قاره و کشور را انتخاب می‌کند. بعد از کیپد منابع، ساختمان، تحقیق و ارتش را مدیریت می‌کند و با بقیه از راه دیپلماسی، تجارت، اتحاد و جدول رتبه روبه‌رو می‌شود. پاداش روزانه، دعوت، بیانیه و گردونه شانس جلسه را بین بازدیدها زنده نگه می‌دارند.

برنامه یک فایل ناهمگام است: `bot.py` با کتابخانهٔ `rubka`. وضعیت بازی لایهٔ `GameDB` است که فایل‌های JSON را از پوشهٔ `war_game_v3/` می‌خواند و می‌نویسد.

> **جمله کوتاه:** *ربات استراتژی روبیکا که در آن بازیکن یک کشور را اداره می‌کند، اقتصاد می‌سازد و در یک دنیای مشترک رقابت می‌کند.*

---

# 🔗 مخازن مرتبط

| مخزن | نقش |
|------|------|
| **[World War Bot](https://github.com/sadra-hatami/World-War-Bot)** | بازی استراتژی جهانی (همین مخزن) |
| **[Countries War Bot](https://github.com/sadra-hatami/Countries-War-Bot)** | بازی استراتژی کشورها، نسخهٔ قبلی |
| **[Rubika Group Bot](https://github.com/sadra-hatami/Rubika-Group-Bot)** | پلتفرم کامل گروه |
| **[Rubika Advanced Group Bot](https://github.com/sadra-hatami/Rubika-Advanced-Group-Bot)** | جدیدترین و بزرگ‌تر پلتفرم گروه |
| **[Telegram Rubika Account Panel](https://github.com/sadra-hatami/Telegram-Rubika-Account-Panel)** | پنل تلگرام برای حساب کاربری روبیکا |

این مخزن برای بازی استراتژی جهانی است.  
**Countries War Bot** بازی کشوری قبلی است.  
ربات‌های گروه برای نظارت و اتوماسیون هستند.  
**Account Panel** فقط کنترل حساب کاربری از تلگرام است.

---

# 🚀 چرا این پروژه

ربات چت می‌تواند یک دستور را جواب بدهد. ربات استراتژی باید کشور را به خاطر بسپارد.

اینجا یک دنیای مشترک می‌ماند:

- هر بازیکن کشور نام‌دار دارد
- اقتصاد، ساختمان و تحقیق در زمان عوض می‌شوند
- دیپلماسی، تجارت و اتحاد بازیکن‌ها را به هم وصل می‌کند
- رتبه و پاداش روزانه برمی‌گرداند
- ذخیرهٔ JSON بعد از ری‌استارت می‌ماند

---

# ✨ قابلیت‌ها

- 🌍 انتخاب سرور، قاره و کشور
- 🏛️ پروفایل کشور و منابع
- ⚔️ منوی ارتش و اقدام نظامی
- 🏗️ ساختمان و ارتقا
- 🛒 بازار، صرافی و پیشنهاد تجارت
- 🤝 دیپلماسی، اتحاد و گفتگوی متحدان
- 🔬 تحقیق
- 🕵️ اقدام اطلاعاتی
- 🏆 رتبه جهانی
- 🎖️ دستاورد
- 🎁 پاداش روزانه و کد دعوت
- 🎲 گردونه شانس
- 🌐 نهاد مشترک و بیانیه
- 🎛️ رابط فارسی دکمه‌ای
- 🛡️ پنل اپراتور
- 💾 پوشهٔ ذخیرهٔ `war_game_v3/`

---

# 🏗️ معماری

```text
بازیکن
 └─ چت روبیکا + کیپد
     └─ bot.py
         └─ GameDB
             └─ war_game_v3/*.json
```

شناسه دکمه‌ها به جریان کشور، ارتش، بازار، دیپلماسی، تحقیق و رتبه می‌روند. `GameDB.save()` دنیای حافظه را روی دیسک می‌نویسد. توکن باید در محیط باشد، نه داخل فایل.

---

# 📁 ساختار

```text
World-War-Bot/
├── bot.py
├── war_game_v3/     # هنگام اجرا ساخته می‌شود — commit نکنید
└── README.md
```

`bot.py` خود برنامه است. پوشهٔ JSON بازیکن‌ها، کشورهای گرفته‌شده، قیمت بازار، اتحاد، تجارت، بیانیه، دعوت و گزارش را نگه می‌دارد.

---

# 🛠️ فناوری‌ها

- Python 3.8+
- `rubka`
- asyncio
- ذخیرهٔ JSON

---

# 🚀 نصب

```bash
git clone https://github.com/sadra-hatami/World-War-Bot.git
cd World-War-Bot
pip install rubka
python bot.py
```

---

# ⚙️ پیکربندی

```text
RUBIKA_BOT_TOKEN
RUBIKA_ADMIN_IDS
```

`.gitignore`:

```text
.env
war_game_v3/
__pycache__/
```

---

# ▶️ استفاده

1. توکن را در محیط بگذار.
2. `bot.py` را اجرا کن.
3. ربات را در روبیکا باز کن.
4. سرور و کشور را انتخاب کن.
5. از کیپد برای ارتش، بازار، دیپلماسی، تحقیق و رتبه استفاده کن.

پنل اپراتور با دستور خصوصی `پنل` باز می‌شود.

---

# 🎓 مخاطب

- جامعه‌های روبیکا که بازی استراتژی طولانی می‌خواهند
- توسعه‌دهندگانی که ربات بزرگ کیپد محور می‌خوانند
- کسانی که نمونه کار بازی می‌سازند

---

# 🗺️ نقشه راه

- جدا کردن سیستم‌ها به بسته
- توضیح واضح‌تر هر منو
- پیکربندی امن‌تر
- پایگاه دادهٔ اختیاری

---

# ❓ پرسش‌ها

### آیا این ربات قفل گروه است؟

نه. ابزار گروه در [Rubika Group Bot](https://github.com/sadra-hatami/Rubika-Group-Bot) و [Rubika Advanced Group Bot](https://github.com/sadra-hatami/Rubika-Advanced-Group-Bot) است.

### تفاوت با Countries War Bot چیست؟

آن مخزن بازی کشوری قبلی است. این مخزن ساخت استراتژی جهانی است: سرور، قاره، بازار، دیپلماسی، تحقیق، دعوت و صفحهٔ مشترک.

### آیا پیشرفت بعد از ری‌استارت می‌ماند؟

بله، اگر پوشهٔ `war_game_v3/` روی دیسک بماند.

### آیا توکن را منتشر کنم؟

نه. فقط متغیر محیطی.

---

# 🔐 امنیت

توکن زنده، شناسه ادمین و شناسه کانال را commit نکن. اگر هنوز داخل `bot.py` هستند، قبل از پوش عمومی عوضشان کن. پوشهٔ `war_game_v3/` را هم خصوصی نگه دار.

---

# 🤝 مشارکت

گزارش باگ، صیقل منو و پیکربندی امن‌تر خوش‌آمد است.

---

# 📬 تماس

### صدرا حاتمی

📧 [ایمیل](mailto:sadra.hatami.1732@gmail.com)

🌐 [گیت‌هاب](https://github.com/sadra-hatami)

---

# 📄 مجوز

این پروژه تحت مجوز **MIT** است.

---

# © حق نشر

© ۲۰۲۶ **صدرا حاتمی**

---

# ⭐ حمایت

اگر این ربات در نمونه کار یا جامعه جا دارد، به مخزن ستاره بده.

---

<div align="center">

## طراحی و توسعه با ❤️ برای جامعهٔ برنامه‌نویسان ایران و جهان توسط **صدرا حاتمی**

</div>
