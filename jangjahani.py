import asyncio
import random
import json
import os
import time
import math
import re
import string
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from rubka import Robot, Message
from rubka.keypad import ChatKeypadBuilder

# ==================== تنظیمات اصلی ربات ====================
BOT_TOKEN = "bot_token"
OWNER_ID = "chat_id"

ADMIN_IDS = [
    "chat_id",
    "chat_id"
]

CHANNEL_ID = ""
CHANNEL_URL = ""

bot = Robot(BOT_TOKEN)

# ==================== سیستم سرورها ====================
SERVERS = {
    1: {"name": "سرور آسیا", "emoji": "🌏", "continents": ["asia"]},
    2: {"name": "سرور اروپا", "emoji": "🌍", "continents": ["europe"]},
    3: {"name": "سرور آمریکا", "emoji": "🌎", "continents": ["america"]},
    4: {"name": "سرور آفریقا", "emoji": "🌍", "continents": ["africa"]},
    5: {"name": "سرور اقیانوسیه", "emoji": "🌏", "continents": ["oceania"]},
    6: {"name": "سرور شرق میانه", "emoji": "🌏", "continents": ["asia"]},
    7: {"name": "سرور نوردیک", "emoji": "🌍", "continents": ["europe"]},
    8: {"name": "سرور مستعمرات", "emoji": "🌎", "continents": ["america", "africa"]},
    9: {"name": "سرور آسیای شرقی", "emoji": "🌏", "continents": ["asia"]},
    10: {"name": "سرور مدیترانه", "emoji": "🌍", "continents": ["europe", "africa"]}
}

# ==================== قاره‌ها و کشورهای واقعی ====================
CONTINENTS = {
    "asia": {
        "name": "آسیا", "emoji": "🌏",
        "countries": {
            "iran": {"name": "ایران", "emoji": "🇮🇷", "capital": "تهران", "population": 89, "gdp": 500, "army": 610000, "nuclear": False, "resources": {"oil": 155, "gas": 200, "iron": 80, "copper": 50, "gold": 30, "saffron": 90}},
            "china": {"name": "چین", "emoji": "🇨🇳", "capital": "پکن", "population": 1410, "gdp": 17700, "army": 2000000, "nuclear": True, "resources": {"iron": 300, "technology": 150, "gold": 200, "coal": 400, "rare_earth": 250, "electronics": 350}},
            "russia": {"name": "روسیه", "emoji": "🇷🇺", "capital": "مسکو", "population": 146, "gdp": 1800, "army": 1150000, "nuclear": True, "resources": {"oil": 300, "gas": 350, "uranium": 100, "iron": 200, "gold": 150, "timber": 200}},
            "japan": {"name": "ژاپن", "emoji": "🇯🇵", "capital": "توکیو", "population": 125, "gdp": 4900, "army": 247000, "nuclear": False, "resources": {"technology": 200, "iron": 100, "gold": 150, "electronics": 300, "robotics": 250, "automotive": 350}},
            "india": {"name": "هند", "emoji": "🇮🇳", "capital": "دهلی", "population": 1428, "gdp": 3700, "army": 1450000, "nuclear": True, "resources": {"iron": 150, "technology": 100, "food": 300, "textile": 200, "gold": 80, "spices": 150}},
            "turkey": {"name": "ترکیه", "emoji": "🇹🇷", "capital": "آنکارا", "population": 85, "gdp": 950, "army": 425000, "nuclear": False, "resources": {"iron": 90, "food": 150, "gold": 80, "textile": 180, "boron": 100, "tourism": 200}},
            "saudi": {"name": "عربستان", "emoji": "🇸🇦", "capital": "ریاض", "population": 36, "gdp": 1100, "army": 257000, "nuclear": False, "resources": {"oil": 500, "gas": 200, "gold": 100, "petrochemical": 300, "dates": 100}},
            "korea": {"name": "کره جنوبی", "emoji": "🇰🇷", "capital": "سئول", "population": 51, "gdp": 1800, "army": 555000, "nuclear": False, "resources": {"technology": 180, "iron": 100, "gold": 120, "electronics": 350, "shipbuilding": 200}},
            "pakistan": {"name": "پاکستان", "emoji": "🇵🇰", "capital": "اسلام‌آباد", "population": 231, "gdp": 380, "army": 654000, "nuclear": True, "resources": {"iron": 70, "food": 180, "textile": 200, "gold": 40, "cotton": 150}},
            "iraq": {"name": "عراق", "emoji": "🇮🇶", "capital": "بغداد", "population": 43, "gdp": 250, "army": 193000, "nuclear": False, "resources": {"oil": 400, "gas": 100, "gold": 30, "dates": 80}},
            "afghanistan": {"name": "افغانستان", "emoji": "🇦🇫", "capital": "کابل", "population": 41, "gdp": 20, "army": 175000, "nuclear": False, "resources": {"iron": 60, "copper": 40, "gold": 20, "lapis": 100, "saffron": 50}},
            "kazakhstan": {"name": "قزاقستان", "emoji": "🇰🇿", "capital": "آستانه", "population": 19, "gdp": 220, "army": 108000, "nuclear": False, "resources": {"oil": 180, "uranium": 120, "iron": 100, "gold": 60, "coal": 150}},
            "indonesia": {"name": "اندونزی", "emoji": "🇮🇩", "capital": "جاکارتا", "population": 277, "gdp": 1300, "army": 395000, "nuclear": False, "resources": {"oil": 100, "gas": 150, "coal": 250, "gold": 100, "timber": 200}},
            "vietnam": {"name": "ویتنام", "emoji": "🇻🇳", "capital": "هانوی", "population": 99, "gdp": 430, "army": 482000, "nuclear": False, "resources": {"oil": 60, "food": 250, "coffee": 200, "textile": 150}},
            "thailand": {"name": "تایلند", "emoji": "🇹🇭", "capital": "بانکوک", "population": 71, "gdp": 520, "army": 306000, "nuclear": False, "resources": {"food": 250, "tourism": 300, "electronics": 120, "rubber": 200}},
            "malaysia": {"name": "مالزی", "emoji": "🇲🇾", "capital": "کوالالامپور", "population": 33, "gdp": 430, "army": 113000, "nuclear": False, "resources": {"oil": 80, "gas": 100, "palm_oil": 250, "electronics": 200}},
            "philippines": {"name": "فیلیپین", "emoji": "🇵🇭", "capital": "مانیل", "population": 115, "gdp": 430, "army": 143000, "nuclear": False, "resources": {"gold": 50, "copper": 80, "electronics": 150, "food": 180}}
        }
    },
    "europe": {
        "name": "اروپا", "emoji": "🌍",
        "countries": {
            "germany": {"name": "آلمان", "emoji": "🇩🇪", "capital": "برلین", "population": 84, "gdp": 4400, "army": 183000, "nuclear": False, "resources": {"iron": 200, "technology": 180, "gold": 150, "automotive": 400, "machinery": 300}},
            "france": {"name": "فرانسه", "emoji": "🇫🇷", "capital": "پاریس", "population": 68, "gdp": 3000, "army": 208000, "nuclear": True, "resources": {"technology": 150, "food": 200, "gold": 120, "aerospace": 250, "wine": 300, "tourism": 350}},
            "uk": {"name": "انگلیس", "emoji": "🇬🇧", "capital": "لندن", "population": 68, "gdp": 3300, "army": 194000, "nuclear": True, "resources": {"technology": 160, "gold": 180, "oil": 80, "finance": 500, "pharma": 200}},
            "italy": {"name": "ایتالیا", "emoji": "🇮🇹", "capital": "رم", "population": 59, "gdp": 2100, "army": 165000, "nuclear": False, "resources": {"food": 250, "gold": 100, "iron": 70, "fashion": 400, "tourism": 350}},
            "spain": {"name": "اسپانیا", "emoji": "🇪🇸", "capital": "مادرید", "population": 47, "gdp": 1500, "army": 122000, "nuclear": False, "resources": {"food": 180, "gold": 90, "iron": 60, "tourism": 400, "olive_oil": 200}},
            "poland": {"name": "لهستان", "emoji": "🇵🇱", "capital": "ورشو", "population": 38, "gdp": 750, "army": 125000, "nuclear": False, "resources": {"iron": 100, "food": 150, "gold": 60, "coal": 200}},
            "ukraine": {"name": "اوکراین", "emoji": "🇺🇦", "capital": "کیف", "population": 37, "gdp": 180, "army": 300000, "nuclear": False, "resources": {"iron": 150, "food": 350, "coal": 150, "gold": 40}},
            "sweden": {"name": "سوئد", "emoji": "🇸🇪", "capital": "استکهلم", "population": 10, "gdp": 620, "army": 30000, "nuclear": False, "resources": {"iron": 120, "technology": 150, "gold": 80, "timber": 250}},
            "netherlands": {"name": "هلند", "emoji": "🇳🇱", "capital": "آمستردام", "population": 17, "gdp": 1100, "army": 41000, "nuclear": False, "resources": {"gas": 200, "food": 250, "technology": 120, "electronics": 180}},
            "greece": {"name": "یونان", "emoji": "🇬🇷", "capital": "آتن", "population": 10, "gdp": 240, "army": 142000, "nuclear": False, "resources": {"tourism": 400, "olive_oil": 250, "food": 150, "gold": 40}},
            "switzerland": {"name": "سوئیس", "emoji": "🇨🇭", "capital": "برن", "population": 8, "gdp": 870, "army": 20000, "nuclear": False, "resources": {"gold": 300, "finance": 500, "technology": 150, "pharma": 200}},
            "norway": {"name": "نروژ", "emoji": "🇳🇴", "capital": "اسلو", "population": 5, "gdp": 550, "army": 23000, "nuclear": False, "resources": {"oil": 250, "gas": 200, "fish": 300, "timber": 120}},
            "belgium": {"name": "بلژیک", "emoji": "🇧🇪", "capital": "بروکسل", "population": 11, "gdp": 620, "army": 25000, "nuclear": False, "resources": {"technology": 100, "gold": 80, "food": 120, "diamond": 150}},
            "austria": {"name": "اتریش", "emoji": "🇦🇹", "capital": "وین", "population": 9, "gdp": 520, "army": 22000, "nuclear": False, "resources": {"tourism": 300, "iron": 60, "gold": 70, "timber": 120}},
            "romania": {"name": "رومانی", "emoji": "🇷🇴", "capital": "بخارست", "population": 19, "gdp": 350, "army": 70000, "nuclear": False, "resources": {"oil": 100, "food": 150, "iron": 50, "timber": 100}}
        }
    },
    "america": {
        "name": "آمریکا", "emoji": "🌎",
        "countries": {
            "usa": {"name": "آمریکا", "emoji": "🇺🇸", "capital": "واشنگتن", "population": 336, "gdp": 26900, "army": 1390000, "nuclear": True, "resources": {"technology": 250, "gold": 300, "oil": 200, "iron": 150, "aerospace": 500}},
            "canada": {"name": "کانادا", "emoji": "🇨🇦", "capital": "اتاوا", "population": 40, "gdp": 2100, "army": 72000, "nuclear": False, "resources": {"oil": 200, "iron": 120, "gold": 100, "timber": 350, "uranium": 80}},
            "brazil": {"name": "برزیل", "emoji": "🇧🇷", "capital": "برازیلیا", "population": 216, "gdp": 2100, "army": 360000, "nuclear": False, "resources": {"food": 300, "iron": 150, "oil": 100, "timber": 350, "gold": 70}},
            "mexico": {"name": "مکزیک", "emoji": "🇲🇽", "capital": "مکزیکوسیتی", "population": 130, "gdp": 1500, "army": 280000, "nuclear": False, "resources": {"oil": 150, "food": 180, "gold": 70, "silver": 250}},
            "argentina": {"name": "آرژانتین", "emoji": "🇦🇷", "capital": "بوینس آیرس", "population": 46, "gdp": 640, "army": 103000, "nuclear": False, "resources": {"food": 250, "iron": 80, "gold": 60, "wine": 200}},
            "colombia": {"name": "کلمبیا", "emoji": "🇨🇴", "capital": "بوگوتا", "population": 52, "gdp": 360, "army": 293000, "nuclear": False, "resources": {"oil": 80, "gold": 100, "coffee": 300, "emerald": 150}},
            "chile": {"name": "شیلی", "emoji": "🇨🇱", "capital": "سانتیاگو", "population": 19, "gdp": 340, "army": 77000, "nuclear": False, "resources": {"copper": 300, "gold": 80, "iron": 60, "wine": 150}},
            "venezuela": {"name": "ونزوئلا", "emoji": "🇻🇪", "capital": "کاراکاس", "population": 28, "gdp": 100, "army": 123000, "nuclear": False, "resources": {"oil": 500, "gas": 150, "iron": 100, "gold": 80}},
            "peru": {"name": "پرو", "emoji": "🇵🇪", "capital": "لیما", "population": 34, "gdp": 260, "army": 81000, "nuclear": False, "resources": {"gold": 150, "copper": 200, "silver": 120, "food": 120}},
            "cuba": {"name": "کوبا", "emoji": "🇨🇺", "capital": "هاوانا", "population": 11, "gdp": 110, "army": 76000, "nuclear": False, "resources": {"sugar": 300, "nickel": 150, "tobacco": 200, "food": 80}}
        }
    },
    "africa": {
        "name": "آفریقا", "emoji": "🌍",
        "countries": {
            "egypt": {"name": "مصر", "emoji": "🇪🇬", "capital": "قاهره", "population": 111, "gdp": 470, "army": 450000, "nuclear": False, "resources": {"oil": 80, "food": 120, "gold": 100, "cotton": 200}},
            "nigeria": {"name": "نیجریه", "emoji": "🇳🇬", "capital": "آبوجا", "population": 223, "gdp": 510, "army": 215000, "nuclear": False, "resources": {"oil": 200, "food": 150, "iron": 60, "gold": 50}},
            "south_africa": {"name": "آفریقای جنوبی", "emoji": "🇿🇦", "capital": "پرتوریا", "population": 60, "gdp": 400, "army": 82000, "nuclear": False, "resources": {"gold": 200, "diamond": 150, "iron": 100, "platinum": 200}},
            "algeria": {"name": "الجزایر", "emoji": "🇩🇿", "capital": "الجزیره", "population": 45, "gdp": 220, "army": 130000, "nuclear": False, "resources": {"oil": 150, "gas": 250, "iron": 50, "gold": 30}},
            "morocco": {"name": "مراکش", "emoji": "🇲🇦", "capital": "رباط", "population": 37, "gdp": 140, "army": 198000, "nuclear": False, "resources": {"phosphate": 350, "food": 120, "gold": 40, "tourism": 200}},
            "ethiopia": {"name": "اتیوپی", "emoji": "🇪🇹", "capital": "آدیس آبابا", "population": 126, "gdp": 150, "army": 135000, "nuclear": False, "resources": {"coffee": 300, "food": 180, "gold": 60}},
            "kenya": {"name": "کنیا", "emoji": "🇰🇪", "capital": "نایروبی", "population": 55, "gdp": 120, "army": 24000, "nuclear": False, "resources": {"tea": 250, "coffee": 150, "tourism": 300, "food": 100}},
            "libya": {"name": "لیبی", "emoji": "🇱🇾", "capital": "طرابلس", "population": 7, "gdp": 50, "army": 35000, "nuclear": False, "resources": {"oil": 400, "gas": 100, "gold": 20}}
        }
    },
    "oceania": {
        "name": "اقیانوسیه", "emoji": "🌏",
        "countries": {
            "australia": {"name": "استرالیا", "emoji": "🇦🇺", "capital": "کانبرا", "population": 26, "gdp": 1700, "army": 60000, "nuclear": False, "resources": {"iron": 250, "gold": 150, "uranium": 80, "coal": 300, "gas": 100}},
            "new_zealand": {"name": "نیوزیلند", "emoji": "🇳🇿", "capital": "ولینگتون", "population": 5, "gdp": 250, "army": 9000, "nuclear": False, "resources": {"food": 200, "gold": 50, "iron": 40, "dairy": 250}},
            "fiji": {"name": "فیجی", "emoji": "🇫🇯", "capital": "سووا", "population": 1, "gdp": 5, "army": 3000, "nuclear": False, "resources": {"sugar": 150, "tourism": 200, "gold": 30, "fish": 100}}
        }
    }
}

# ==================== منابع و واحدهای نظامی ====================
RESOURCES = {
    "gold": {"name": "طلا", "emoji": "🥇", "base_price": 100},
    "oil": {"name": "نفت", "emoji": "🛢️", "base_price": 150},
    "iron": {"name": "آهن", "emoji": "⛓️", "base_price": 80},
    "food": {"name": "غذا", "emoji": "🍞", "base_price": 50},
    "uranium": {"name": "اورانیوم", "emoji": "☢️", "base_price": 500},
    "diamond": {"name": "الماس", "emoji": "💎", "base_price": 2000},
    "technology": {"name": "فناوری", "emoji": "🔬", "base_price": 1000},
    "gas": {"name": "گاز", "emoji": "🔥", "base_price": 120},
    "steel": {"name": "فولاد", "emoji": "🔩", "base_price": 200},
    "electronics": {"name": "الکترونیک", "emoji": "📱", "base_price": 800},
    "tourism": {"name": "گردشگری", "emoji": "✈️", "base_price": 400},
    "timber": {"name": "چوب", "emoji": "🪵", "base_price": 70},
    "copper": {"name": "مس", "emoji": "🟤", "base_price": 90},
    "silver": {"name": "نقره", "emoji": "⚪", "base_price": 300}
}

MILITARY_UNITS = {
    "infantry": {"name": "سرباز پیاده", "emoji": "💂", "cost": {"gold": 100, "food": 50}, "power": 10, "defense": 5},
    "tank": {"name": "تانک", "emoji": "🚜", "cost": {"gold": 500, "iron": 200, "steel": 50}, "power": 50, "defense": 20},
    "artillery": {"name": "توپخانه", "emoji": "💣", "cost": {"gold": 800, "iron": 300, "steel": 100}, "power": 80, "defense": 10},
    "jet": {"name": "جنگنده", "emoji": "✈️", "cost": {"gold": 1000, "iron": 300, "oil": 100}, "power": 100, "defense": 10},
    "bomber": {"name": "بمب‌افکن", "emoji": "🛩️", "cost": {"gold": 2000, "iron": 500, "oil": 200}, "power": 200, "defense": 15},
    "submarine": {"name": "زیردریایی", "emoji": "⚓", "cost": {"gold": 1500, "iron": 400, "steel": 200}, "power": 150, "defense": 50},
    "missile": {"name": "موشک", "emoji": "🚀", "cost": {"gold": 3000, "technology": 50, "uranium": 20}, "power": 300, "defense": 5},
    "nuke": {"name": "بمب اتمی", "emoji": "☢️", "cost": {"gold": 10000, "uranium": 100, "technology": 200}, "power": 2000, "defense": 0},
    "drone": {"name": "پهپاد", "emoji": "🛸", "cost": {"gold": 600, "technology": 30, "electronics": 80}, "power": 30, "defense": 5},
    "navy": {"name": "نیروی دریایی", "emoji": "🚢", "cost": {"gold": 2500, "iron": 500, "steel": 300}, "power": 180, "defense": 100},
    "air_defense": {"name": "پدافند هوایی", "emoji": "🎯", "cost": {"gold": 1200, "iron": 200, "electronics": 100}, "power": 40, "defense": 80},
    "special_forces": {"name": "نیروی ویژه", "emoji": "🦅", "cost": {"gold": 5000, "technology": 100, "food": 200}, "power": 250, "defense": 50}
}

BUILDINGS = {
    "barracks": {"name": "پادگان نظامی", "emoji": "🏚️", "cost": {"gold": 2000, "iron": 500}, "effect": "افزایش ۵٪ قدرت حمله به ازای هر سطح ارتقا", "max": 10},
    "wall": {"name": "دیوار دفاعی", "emoji": "🧱", "cost": {"gold": 3000, "iron": 1000, "steel": 500}, "effect": "افزایش ۱۰٪ قدرت دفاع به ازای هر سطح ارتقا", "max": 15},
    "mine": {"name": "معدن طلا", "emoji": "⛏️", "cost": {"gold": 1000}, "effect": "افزایش ۱۰۰ طلا درآمد در هر دوره ۳ دقیقه", "max": 20},
    "farm": {"name": "مزرعه گندم", "emoji": "🌾", "cost": {"gold": 500}, "effect": "افزایش ۵۰ غذا در هر دوره ۳ دقیقه", "max": 20},
    "oil_rig": {"name": "سکوی نفتی", "emoji": "🛢️", "cost": {"gold": 1500, "iron": 300}, "effect": "افزایش ۳۰ نفت در هر دوره ۳ دقیقه", "max": 15},
    "lab": {"name": "آزمایشگاه تحقیقاتی", "emoji": "🔬", "cost": {"gold": 5000, "technology": 100}, "effect": "تسریع پیشرفت فناوری و کاهش هزینه تحقیقات", "max": 10},
    "hospital": {"name": "بیمارستان صحرایی", "emoji": "🏥", "cost": {"gold": 2000, "food": 500}, "effect": "کاهش ۵٪ تلفات نظامی به ازای هر سطح", "max": 10},
    "bank": {"name": "بانک مرکزی", "emoji": "🏦", "cost": {"gold": 10000, "steel": 1000}, "effect": "افزایش ۵۰۰ طلا درآمد در هر دوره", "max": 5},
    "spy_agency": {"name": "سازمان جاسوسی", "emoji": "🕵️", "cost": {"gold": 8000, "technology": 100}, "effect": "افزایش شانس موفقیت در عملیات‌های جاسوسی و هک", "max": 5},
    "bunker": {"name": "پناهگاه هسته‌ای", "emoji": "🏰", "cost": {"gold": 15000, "steel": 3000}, "effect": "محافظت در برابر حملات اتمی و کاهش خسارت", "max": 3},
    "factory": {"name": "کارخانه اسلحه‌سازی", "emoji": "🏭", "cost": {"gold": 5000, "iron": 1000, "steel": 500}, "effect": "کاهش ۱۵٪ هزینه خرید واحدهای نظامی", "max": 10},
    "trade_center": {"name": "مرکز تجارت جهانی", "emoji": "🏪", "cost": {"gold": 8000, "steel": 500}, "effect": "کاهش کارمزد معاملات در بازار", "max": 5},
    "airport": {"name": "فرودگاه بین‌المللی", "emoji": "🛫", "cost": {"gold": 7000, "steel": 1000}, "effect": "افزایش سرعت استقرار نیروها", "max": 5},
    "port": {"name": "بندر تجاری", "emoji": "⚓", "cost": {"gold": 6000, "steel": 800}, "effect": "افزایش درآمد حاصل از تجارت دریایی", "max": 5},
    "university": {"name": "دانشگاه ملی", "emoji": "🎓", "cost": {"gold": 4000, "technology": 50}, "effect": "افزایش سرعت تحقیقات و کسب امتیاز", "max": 10}
}

ACHIEVEMENTS = {
    "first_blood": {"name": "اولین خون", "desc": "اولین نبرد خود را انجام دهید و طعم پیروزی یا شکست را بچشید", "icon": "⚔️", "score": 100, "gold": 1000},
    "victorious_10": {"name": "فاتح ۱۰", "desc": "در ۱۰ نبرد متوالی یا غیرمتوالی پیروز شوید و نام خود را در تاریخ ثبت کنید", "icon": "🏆", "score": 500, "gold": 5000},
    "victorious_50": {"name": "فاتح ۵۰", "desc": "۵۰ پیروزی درخشان در نبردها کسب کنید و به اسطوره جنگ تبدیل شوید", "icon": "👑", "score": 2000, "diamond": 10},
    "rich_100k": {"name": "ثروت افسانه‌ای", "desc": "۱۰۰,۰۰۰ طلا در خزانه کشور ذخیره کنید و به ثروتمندترین کشور جهان تبدیل شوید", "icon": "💰", "score": 300, "gold": 10000},
    "powerful_10k": {"name": "قدرت بی‌نظیر", "desc": "قدرت نظامی خود را به ۱۰,۰۰۰ واحد برسانید و به ارتشی شکست‌ناپذیر دست یابید", "icon": "💪", "score": 500, "steel": 500},
    "scientist": {"name": "دانشمند برجسته", "desc": "به سطح فناوری ۵ دست یابید و کشورتان را به قطب علمی جهان تبدیل کنید", "icon": "🔬", "score": 600, "technology": 200},
    "builder": {"name": "معمار بزرگ", "desc": "۱۰ ساختمان را به سطح ۵ ارتقا دهید و زیرساخت‌های کشورتان را مدرن کنید", "icon": "🏗️", "score": 800, "steel": 1000},
    "nuclear": {"name": "قدرت هسته‌ای", "desc": "بمب اتمی بسازید و به باشگاه قدرت‌های هسته‌ای جهان بپیوندید", "icon": "☢️", "score": 1500, "uranium": 50},
    "diplomat": {"name": "دیپلمات برتر", "desc": "با ۵ کشور مختلف پیمان اتحاد ببندید و شبکه دیپلماتیک قدرتمندی ایجاد کنید", "icon": "🤝", "score": 400, "gold": 5000},
    "spy_master": {"name": "استاد جاسوسی", "desc": "۲۰ عملیات جاسوسی یا هک موفقیت‌آمیز انجام دهید", "icon": "🕵️", "score": 700, "technology": 150},
    "trader": {"name": "تاجر ماهر", "desc": "۱۰۰ معامله در بازار جهانی انجام دهید و به قطب اقتصادی تبدیل شوید", "icon": "💱", "score": 500, "gold": 8000},
    "continent_ruler": {"name": "فاتح قاره", "desc": "به قدرتمندترین کشور قاره خود تبدیل شوید و بر منطقه حکومت کنید", "icon": "🌍", "score": 2000, "diamond": 20},
    "world_domination": {"name": "سلطه بر جهان", "desc": "قدرتمندترین کشور کل جهان شوید و به ابرقدرت بی‌رقیب تبدیل شوید", "icon": "🌐", "score": 5000, "diamond": 50},
    "statement_writer": {"name": "بیانیه‌نویس رسمی", "desc": "۵ بیانیه رسمی صادر کنید که توسط ادمین تأیید و در کانال منتشر شود", "icon": "📜", "score": 300, "gold": 3000}
}

LUCKY_WHEEL_PRIZES = [
    {"type": "gold", "amount": 5000, "name": "۵,۰۰۰ طلا", "emoji": "💰", "chance": 25},
    {"type": "gold", "amount": 10000, "name": "۱۰,۰۰۰ طلا", "emoji": "💰", "chance": 15},
    {"type": "gold", "amount": 25000, "name": "۲۵,۰۰۰ طلا", "emoji": "💰", "chance": 5},
    {"type": "oil", "amount": 2000, "name": "۲,۰۰۰ نفت", "emoji": "🛢️", "chance": 20},
    {"type": "oil", "amount": 5000, "name": "۵,۰۰۰ نفت", "emoji": "🛢️", "chance": 10},
    {"type": "xp", "amount": 100, "name": "۱۰۰ XP", "emoji": "🎯", "chance": 15},
    {"type": "xp", "amount": 250, "name": "۲۵۰ XP", "emoji": "🎯", "chance": 8},
    {"type": "vip", "amount": 7, "name": "عضویت VIP هفت روزه رایگان", "emoji": "💎", "chance": 3},
    {"type": "protection", "amount": 3, "name": "سپر محافظتی سه روزه", "emoji": "🛡️", "chance": 4},
    {"type": "nothing", "amount": 0, "name": "متأسفانه هیچ چیز", "emoji": "😢", "chance": 10}
]

# ==================== دیتابیس ====================
DATA_DIR = "war_game_v3"
os.makedirs(DATA_DIR, exist_ok=True)

def load_json(filename, default):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return default

def save_json(filename, data):
    with open(os.path.join(DATA_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_invite_code(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

class GameDB:
    def __init__(self):
        self.players = load_json("players.json", {})
        self.countries_taken = load_json("countries_taken.json", [])
        self.chat_ids = load_json("chat_ids.json", [])
        self.banned = load_json("banned.json", [])
        self.market_prices = load_json("market_prices.json", {})
        self.daily_bonuses = load_json("daily_bonuses.json", {})
        self.statements = load_json("statements.json", [])
        self.broadcast_history = load_json("broadcast_history.json", [])
        self.war_logs = load_json("war_logs.json", [])
        self.spy_reports = load_json("spy_reports.json", {})
        self.sanctions = load_json("sanctions.json", {})
        self.global_events = load_json("global_events.json", {"active": None, "until": 0, "history": []})
        self.admin_logs = load_json("admin_logs.json", [])
        self.achievements_data = load_json("achievements_data.json", {})
        self.trade_history = load_json("trade_history.json", [])
        self.vip_users = load_json("vip_users.json", {})
        self.alliance_requests = load_json("alliance_requests.json", {})
        self.war_declarations = load_json("war_declarations.json", {})
        self.trade_offers = load_json("trade_offers.json", {})
        self.ally_chat = load_json("ally_chat.json", {})
        self.invites = load_json("invites.json", {})
        self.invite_codes = load_json("invite_codes.json", {})
        self.server_players = load_json("server_players.json", {str(i): [] for i in range(1, 11)})
        self.un_data = load_json("un_data.json", {
            str(i): {"secretary_general": None, "members": [], "join_requests": [], "founded": datetime.now().isoformat()}
            for i in range(1, 11)
        })
        self.lucky_wheel = load_json("lucky_wheel.json", {})
        self.lucky_wheel_count = load_json("lucky_wheel_count.json", {})
    
    def save(self):
        for name in ["players", "countries_taken", "chat_ids", "banned", "market_prices",
                     "daily_bonuses", "statements", "broadcast_history", "war_logs",
                     "spy_reports", "sanctions", "global_events", "admin_logs",
                     "achievements_data", "trade_history", "vip_users", "alliance_requests",
                     "war_declarations", "trade_offers", "ally_chat", "invites", "invite_codes", "server_players",
                     "un_data", "lucky_wheel", "lucky_wheel_count"]:
            save_json(f"{name}.json", getattr(self, name))

db = GameDB()

def get_player(user_id):
    return db.players.get(user_id)

def find_country_by_name(name):
    name = name.strip().lower()
    for uid, p in db.players.items():
        if name == p.get("country_name", "").lower():
            return uid
    for uid, p in db.players.items():
        if name in p.get("country_name", "").lower():
            return uid
    return None

def find_country_smart(query):
    query = query.strip()
    result = find_country_by_name(query)
    if result:
        return result
    for uid in db.players:
        if uid[-4:] == query or uid == query or query in uid:
            return uid
    return None

def find_user_by_invite_code(code):
    code = code.strip().upper()
    for uid, c in db.invite_codes.items():
        if c == code:
            return uid
    return None

def create_player(user_id, server_id, continent_key, country_key, inviter_code=None):
    continent = CONTINENTS[continent_key]
    country = continent["countries"][country_key]
    
    initial_resources = country["resources"].copy()
    initial_resources["gold"] = initial_resources.get("gold", 0) + 5000
    initial_resources["food"] = initial_resources.get("food", 0) + 2000
    initial_resources["steel"] = 100
    initial_resources["diamond"] = 5
    initial_resources["uranium"] = 20 if country["nuclear"] else 5
    initial_resources["technology"] = 50 if country["nuclear"] else 10
    
    invite_code = generate_invite_code()
    while invite_code in db.invite_codes.values():
        invite_code = generate_invite_code()
    
    player = {
        "user_id": user_id, "server_id": server_id,
        "continent": continent_key, "continent_name": continent["name"], "continent_emoji": continent["emoji"],
        "country_key": country_key, "country_name": country["name"], "country_emoji": country["emoji"],
        "capital": country["capital"], "population": country["population"], "gdp": country["gdp"],
        "army_strength": country["army"], "nuclear_power": country["nuclear"],
        "resources": initial_resources,
        "military": {u: 0 for u in MILITARY_UNITS},
        "buildings": {b: (1 if b in ["barracks", "wall", "mine", "farm"] else 0) for b in BUILDINGS},
        "tech_level": 1, "score": 0, "xp": 0,
        "allies": [], "wars": [],
        "battles_won": 0, "battles_lost": 0, "total_battles": 0,
        "spy_missions": 0, "spy_success": 0, "trades_done": 0,
        "achievements": [],
        "joined_at": datetime.now().isoformat(), "last_active": int(time.time()), "online": True,
        "prestige": 0, "sanctioned_by": [], "statements_approved": 0,
        "is_vip": False, "vip_expire": 0, "title": "حاکم",
        "inviter": None, "invites_sent": 0, "invite_code": invite_code,
        "newbie_protection": int(time.time()) + 900,
        "last_war_time": 0, "last_hack_time": 0,
        "alliance_lock": {}, "war_cooldown": 10800, "hack_cooldown": 3600,
        "un_member": False, "protection_expire": 0
    }
    
    db.players[user_id] = player
    db.countries_taken.append(country_key)
    db.server_players[str(server_id)].append(user_id)
    db.invite_codes[user_id] = invite_code
    
    invite_bonus = 0
    if inviter_code:
        inviter_uid = find_user_by_invite_code(inviter_code)
        if inviter_uid and inviter_uid != user_id and inviter_uid in db.players:
            player["inviter"] = inviter_uid
            db.players[inviter_uid]["resources"]["gold"] = db.players[inviter_uid]["resources"].get("gold", 0) + 5000
            db.players[inviter_uid]["invites_sent"] = db.players[inviter_uid].get("invites_sent", 0) + 1
            player["resources"]["gold"] = player["resources"].get("gold", 0) + 5000
            invite_bonus = 5000
            db.save()
            check_achievements(db.players[inviter_uid], inviter_uid)
    
    db.save()
    return player, invite_bonus

def get_power(player):
    attack = 0
    defense = 0
    for unit, count in player.get("military", {}).items():
        if unit in MILITARY_UNITS and count > 0:
            attack += MILITARY_UNITS[unit]["power"] * count
            defense += MILITARY_UNITS[unit]["defense"] * count
    
    tech_bonus = 1 + (player.get("tech_level", 1) - 1) * 0.1
    barracks_bonus = 1 + player.get("buildings", {}).get("barracks", 0) * 0.05
    wall_bonus = 1 + player.get("buildings", {}).get("wall", 0) * 0.1
    bunker_bonus = 1 + player.get("buildings", {}).get("bunker", 0) * 0.3
    
    attack = int(attack * tech_bonus * barracks_bonus)
    defense = int(defense * tech_bonus * wall_bonus * bunker_bonus)
    
    return attack, defense

def is_admin(user_id):
    return str(user_id) in ADMIN_IDS

def is_protected(player):
    now = int(time.time())
    if player.get("newbie_protection", 0) > now:
        return True
    if player.get("protection_expire", 0) > now:
        return True
    return False

async def send_channel(text):
    try:
        await bot.send_message(CHANNEL_ID, text)
        return True
    except Exception as e:
        print(f"Error sending to channel: {e}")
        return False

def check_achievements(player, user_id):
    new_achs = []
    attack, _ = get_power(player)
    
    checks = {
        "first_blood": player.get("total_battles", 0) >= 1,
        "victorious_10": player.get("battles_won", 0) >= 10,
        "victorious_50": player.get("battles_won", 0) >= 50,
        "rich_100k": player["resources"].get("gold", 0) >= 100000,
        "powerful_10k": attack >= 10000,
        "scientist": player.get("tech_level", 0) >= 5,
        "nuclear": player["military"].get("nuke", 0) >= 1,
        "diplomat": len(player.get("allies", [])) >= 5,
        "spy_master": player.get("spy_success", 0) >= 20,
        "trader": player.get("trades_done", 0) >= 100,
        "statement_writer": player.get("statements_approved", 0) >= 5
    }
    
    for ach_id, condition in checks.items():
        if condition and ach_id not in player.get("achievements", []):
            player.setdefault("achievements", []).append(ach_id)
            player["score"] += ACHIEVEMENTS[ach_id]["score"]
            if "gold" in ACHIEVEMENTS[ach_id]:
                player["resources"]["gold"] = player["resources"].get("gold", 0) + ACHIEVEMENTS[ach_id]["gold"]
            if "diamond" in ACHIEVEMENTS[ach_id]:
                player["resources"]["diamond"] = player["resources"].get("diamond", 0) + ACHIEVEMENTS[ach_id]["diamond"]
            new_achs.append(ACHIEVEMENTS[ach_id])
    
    return new_achs

def get_un_data(server_id):
    return db.un_data.get(str(server_id), {"secretary_general": None, "members": [], "join_requests": []})

def get_un_secretary_general(server_id):
    un = get_un_data(server_id)
    sg_id = un.get("secretary_general")
    if sg_id and sg_id in db.players:
        return db.players[sg_id]
    return None

def auto_elect_secretary_general(server_id):
    un = get_un_data(server_id)
    members = un.get("members", [])
    if not members:
        un["secretary_general"] = None
    else:
        best = None
        best_score = -1
        for mid in members:
            if mid in db.players:
                score = db.players[mid].get("score", 0)
                if score > best_score:
                    best_score = score
                    best = mid
        un["secretary_general"] = best
        if best and best in db.players:
            check_achievements(db.players[best], best)
    db.un_data[str(server_id)] = un
    db.save()

def ensure_player_fields(player):
    """اطمینان از وجود تمام فیلدهای ضروری در بازیکن"""
    defaults = {
        "allies": [], "wars": [], "alliance_lock": {}, 
        "war_cooldown": 10800, "hack_cooldown": 3600,
        "last_war_time": 0, "last_hack_time": 0,
        "newbie_protection": 0, "protection_expire": 0,
        "is_vip": False, "vip_expire": 0,
        "un_member": False, "score": 0, "xp": 0,
        "battles_won": 0, "battles_lost": 0, "total_battles": 0,
        "spy_missions": 0, "spy_success": 0, "trades_done": 0,
        "statements_approved": 0, "invites_sent": 0,
        "achievements": [], "sanctioned_by": [],
        "prestige": 0, "online": False, "last_active": 0
    }
    for key, value in defaults.items():
        if key not in player:
            player[key] = value
    return player

# ==================== متغیرهای جوین اجباری فیک ====================
join_attempts = {}

async def check_forced_join(uid, cid, text, btn):
    """جوین اجباری فیک - کاربر باید ۳ بار دکمه عضو شدم را بزند"""
    
    if is_admin(uid):
        return True
    
    if join_attempts.get(uid, 0) >= 3:
        return True
    
    if btn == "joined_channel":
        join_attempts[uid] = join_attempts.get(uid, 0) + 1
        current = join_attempts[uid]
        
        if current == 1:
            kb = ChatKeypadBuilder()
            kb.row(kb.button("joined_channel", "✅ مطمئنم عضو شدم!"))
            kb.row(kb.button("check_again", "🔄 بررسی دوباره"))
            
            await bot.send_message(cid, f"""⚠️ **مطمئنی عضو کانال شدی؟**

هنوز توی لیست اعضای کانال نمی‌بینمت! 🤔

📢 **کانال رسمی:** {CHANNEL_ID}
🔗 **لینک مستقیم:** {CHANNEL_URL}

🔴 **حتماً باید عضو کانال باشی تا بتونی بازی کنی!**
✨ با عضویت در کانال از آخرین اخبار و رویدادهای جهان با خبر می‌شوی.

دوباره چک کن - شاید با اکانت دیگه عضو شدی!""", chat_keypad=kb.build())
            return False
            
        elif current == 2:
            kb = ChatKeypadBuilder()
            kb.row(kb.button("joined_channel", "✅ قسم می‌خورم عضو شدم!"))
            kb.row(kb.button("check_again", "🔄 چک کن ببینم"))
            
            await bot.send_message(cid, f"""🤨 **جدی میگی؟**

آخه من که نمی‌بینمت توی لیست اعضا... 
مطمئنی دکمه Join رو زدی؟

📢 **کانال:** {CHANNEL_ID}
🔗 **لینک:** {CHANNEL_URL}

💡 **راهنمایی:**
۱. از لینک بالا برو تو کانال
۲. دکمه Join (عضویت) رو بزن
۳. بعدش بیا اینجا دکمه «عضو شدم» رو بزن

الآن واقعاً عضو شدی؟ 🤔""", chat_keypad=kb.build())
            return False
            
        elif current >= 3:
            await bot.send_message(cid, f"""✅ **باشه قبول!**

خب خب... انگار واقعاً عضو شدی دیگه! 😅
ببخشید که اذیت کردم - امنیت بازی برامون مهمه!

🎮 **حالا می‌تونی آزادانه بازی کنی!**
یکی از گزینه‌های زیر رو انتخاب کن تا وارد دنیای جنگ جهانی بشی:

📢 راستی حواست به کانال {CHANNEL_ID} باشه:
• اعلام نتایج جنگ‌ها و نبردها
• خبرهای فوری و رویدادهای جهانی
• بیانیه‌های رسمی کشورها
• کدهای جایزه و تخفیف ویژه

🔥 **برو بازی کن و جهان رو فتح کن!**""", chat_keypad=start_keypad())
            return True
    
    if btn == "check_again":
        await bot.send_message(cid, f"""🔍 **در حال بررسی عضویت...**

📋 **نتیجه بررسی:** هنوز عضو کانال نشدی!

📢 **کانال:** {CHANNEL_ID}
🔗 **لینک عضویت:** {CHANNEL_URL}

⚠️ **توجه:** بدون عضویت در کانال رسمی نمی‌تونی از ربات استفاده کنی!
👆 اول عضو شو، بعد بیا دکمه «عضو شدم» رو بزن.""")
        return False
    
    if join_attempts.get(uid, 0) == 0:
        kb = ChatKeypadBuilder()
        kb.row(kb.button("joined_channel", "✅ عضو شدم"))
        
        await bot.send_message(cid, f"""🔒 **عضویت در کانال رسمی الزامیست!**

سلام فرمانده! 🖐️
برای استفاده از ربات و ورود به دنیای جنگ جهانی، باید عضو کانال رسمی ما باشید:

📢 **کانال رسمی:** {CHANNEL_ID}
🔗 **لینک عضویت:** {CHANNEL_URL}

✨ **مزایای عضویت در کانال:**
• 📡 اطلاع از آخرین اخبار و رویدادهای جهانی
• 📜 مشاهده بیانیه‌های رسمی کشورها
• ⚔️ آگاهی از جنگ‌ها و اتحادهای جدید
• 🎁 دریافت کدهای جایزه ویژه
• 🌍 تحلیل وضعیت جهان و قدرتمندترین کشورها

👆 **اول عضو شو، بعد بیا دکمه «عضو شدم» رو بزن!**
فقط چند ثانیه طول میکشه 😊""", chat_keypad=kb.build())
        return False
    
    return False

# ==================== کیپدها ====================
def main_keypad():
    b = ChatKeypadBuilder()
    b.row(b.button("country_info", "🏰 کشور من"), b.button("military_menu", "⚔️ ارتش"))
    b.row(b.button("buildings_menu", "🔨 ساختمان"), b.button("market_menu", "💹 بازار"))
    b.row(b.button("diplomacy_menu", "🤝 دیپلماسی"), b.button("attack_menu", "⚔️ حمله"))
    b.row(b.button("research_menu", "🔬 تحقیقات"), b.button("world_rank", "🌍 رتبه‌بندی"))
    b.row(b.button("spy_menu", "🕵️ جاسوسی"), b.button("statement_menu", "📜 بیانیه"))
    b.row(b.button("achievements_btn", "🏆 دستاوردها"), b.button("daily_bonus", "🎁 پاداش"))
    b.row(b.button("invite_menu", "👥 دعوت"), b.button("lucky_wheel", "🎡 گردونه"))
    b.row(b.button("un_menu", "🏛️ سازمان ملل"), b.button("enter_invite_code", "🔑 کد دعوت"))
    b.row(b.button("exchange_menu", "🔄 صرافی"), b.button("leave_country", "🚪 خروج"))
    return b.build()

def server_keypad():
    b = ChatKeypadBuilder()
    for i in range(1, 11):
        server = SERVERS[i]
        pc = len(db.server_players.get(str(i), []))
        b.row(b.button(f"server_{i}", f"{server['emoji']} {server['name']} ({pc}👤)"))
    return b.build()

def continent_keypad():
    b = ChatKeypadBuilder()
    for key, cont in CONTINENTS.items():
        b.row(b.button(f"cont_{key}", f"{cont['emoji']} {cont['name']}"))
    return b.build()

def country_keypad(cont_key):
    b = ChatKeypadBuilder()
    cont = CONTINENTS[cont_key]
    for key, country in cont["countries"].items():
        if key not in db.countries_taken:
            b.row(b.button(f"pick_{cont_key}_{key}", f"{country['emoji']} {country['name']}"))
    b.row(b.button("back_cont", "🔙 بازگشت"))
    return b.build()

def military_keypad():
    b = ChatKeypadBuilder()
    for key, unit in MILITARY_UNITS.items():
        b.row(b.button(f"buy_{key}", f"{unit['emoji']} {unit['name']}"))
    b.row(b.button("back", "🔙 بازگشت"))
    return b.build()

def building_keypad():
    b = ChatKeypadBuilder()
    for key, bld in BUILDINGS.items():
        b.row(b.button(f"upgrade_{key}", f"{bld['emoji']} {bld['name']}"))
    b.row(b.button("back", "🔙 بازگشت"))
    return b.build()

def statement_keypad():
    b = ChatKeypadBuilder()
    b.row(b.button("send_statement", "✍️ ارسال بیانیه"))
    b.row(b.button("my_statements", "📋 بیانیه‌های من"))
    b.row(b.button("back", "🔙 بازگشت"))
    return b.build()

def admin_keypad():
    b = ChatKeypadBuilder()
    b.row(b.button("adm_stats", "📊 آمار"), b.button("adm_players", "👥 بازیکنان"))
    b.row(b.button("adm_broadcast", "📢 پیام همگانی"), b.button("adm_channel", "📢 اعلامیه کانال"))
    b.row(b.button("adm_statements", "📜 بیانیه‌ها"), b.button("adm_ban", "🚫 مسدود"))
    b.row(b.button("adm_unban", "✅ رفع مسدود"), b.button("adm_give", "💰 طلا"))
    b.row(b.button("adm_reset", "🔄 ریست"), b.button("adm_give_all", "💰 طلا به همه"))
    b.row(b.button("adm_war", "⚔️ اعلام جنگ"), b.button("adm_peace", "🕊️ صلح اجباری"))
    b.row(b.button("adm_event", "🌍 رویداد"), b.button("adm_rich", "🏦 ثروتمندان"))
    b.row(b.button("adm_power", "💪 قدرتمندان"), b.button("adm_vip", "🌟 VIP"))
    b.row(b.button("adm_un", "🏛️ سازمان ملل"), b.button("adm_leave_requests", "🚪 درخواست خروج"))
    b.row(b.button("adm_logs", "📜 لاگ"), b.button("go_game", "🎮 بازی"))
    return b.build()

def statement_approve_keypad(stmt_id):
    b = ChatKeypadBuilder()
    b.row(b.button(f"appr_{stmt_id}", "✅ تایید و انتشار"), b.button(f"rej_{stmt_id}", "❌ رد"))
    return b.build()

def un_keypad():
    b = ChatKeypadBuilder()
    b.row(b.button("un_info", "🏛️ اطلاعات"), b.button("un_join", "📝 درخواست عضویت"))
    b.row(b.button("un_members", "👥 اعضا"), b.button("un_requests", "📋 درخواست‌ها"))
    b.row(b.button("back", "🔙 بازگشت"))
    return b.build()

def lucky_wheel_keypad():
    b = ChatKeypadBuilder()
    b.row(b.button("spin_wheel", "🎲 بچرخون!"), b.button("back", "🔙 بازگشت"))
    return b.build()

def start_keypad():
    b = ChatKeypadBuilder()
    b.row(b.button("enter_invite_code", "🔑 کد دعوت دارم"))
    b.row(b.button("start_game", "🎮 شروع بازی"))
    return b.build()

def attack_units_keypad(target_id):
    """کیپد انتخاب نوع نیرو برای حمله"""
    b = ChatKeypadBuilder()
    b.row(b.button(f"attack_infantry_{target_id}", "💂 سربازان پیاده"))
    b.row(b.button(f"attack_tank_{target_id}", "🚜 تانک‌ها و توپخانه"))
    b.row(b.button(f"attack_jet_{target_id}", "✈️ نیروی هوایی"))
    b.row(b.button(f"attack_special_{target_id}", "🦅 نیروهای ویژه"))
    b.row(b.button(f"attack_all_{target_id}", "⚔️ تمام نیروها"))
    b.row(b.button("back", "🔙 بازگشت"))
    return b.build()

def diplomacy_menu_keypad():
    """کیپد منوی دیپلماسی"""
    b = ChatKeypadBuilder()
    b.row(b.button("alliance_inbox", "📥 درخواست‌های اتحاد"))
    b.row(b.button("war_inbox", "⚔️ اعلام جنگ‌ها"))
    b.row(b.button("ally_chat_menu", "💬 چت با متحدان"))
    b.row(b.button("back", "🔙 بازگشت"))
    return b.build()

def exchange_keypad():
    """کیپد منوی صرافی"""
    b = ChatKeypadBuilder()
    b.row(b.button("create_trade_offer", "📤 ایجاد پیشنهاد"))
    b.row(b.button("view_trade_offers", "📥 پیشنهادات دیگران"))
    b.row(b.button("my_trade_offers", "📋 پیشنهادات من"))
    b.row(b.button("back", "🔙 بازگشت"))
    return b.build()

# ==================== متغیرهای موقت ====================
pending = {}
attack_pending = {}

# ==================== اعلامیه‌های کانال ====================
async def announce_new_country(p):
    message = f"""🌍 **یک کشور جدید به جهان پیوست!**

{'─'*40}
{p['country_emoji']} **{p['country_name']}**
📌 قاره: {p['continent_emoji']} {p['continent_name']}
🏛 پایتخت: {p['capital']}
🖥️ سرور {p.get('server_id', '?')}: {SERVERS.get(p.get('server_id', 1), {}).get('name', '')}
{'─'*40}

📊 **اطلاعات کشور:**
👥 جمعیت: {p['population']} میلیون نفر
💰 تولید ناخالص داخلی: {p['gdp']} میلیارد دلار
⚔️ قدرت ارتش ملی: {p['army_strength']:,} سرباز
☢️ قدرت هسته‌ای: {'✅ دارد' if p['nuclear_power'] else '❌ ندارد'}

🌐 این کشور اکنون بخشی از جامعه جهانی است و آماده فتح جهان!

#{p['country_name']} #NewCountry #Server{p.get('server_id', '?')}"""
    await send_channel(message)

async def announce_statement(country_name, country_emoji, text):
    message = f"""📜 **بیانیه رسمی**

{country_emoji} **{country_name}**

📝 متن بیانیه:
"{text}"

{'─'*40}
📢 این بیانیه از طرف دولت {country_name} صادر شده و در کانال رسمی منتشر گردیده است.

#Statement #{country_name}"""
    return await send_channel(message)

async def announce_war(att, defr):
    a_pwr, _ = get_power(att)
    d_pwr, _ = get_power(defr)
    message = f"""⚔️ **اعلام جنگ رسمی!**

{att['country_emoji']} **{att['country_name']}** به **{defr['country_name']}** {defr['country_emoji']} اعلام جنگ کرد!

📊 **مقایسه قدرت نظامی:**
⚔️ مهاجم: {att['country_emoji']} {att['country_name']} - قدرت {a_pwr:,}
🛡️ مدافع: {defr['country_emoji']} {defr['country_name']} - قدرت {d_pwr:,}

{'─'*40}
🔥 جهان در آستانه یک جنگ جدید است!

#War #{att['country_name']} #{defr['country_name']}"""
    await send_channel(message)

async def announce_victory(winner, loser, loot):
    message = f"""🏆 **پیروزی در نبرد!**

{winner['country_emoji']} **{winner['country_name']}** بر **{loser['country_name']}** {loser['country_emoji']} پیروز شد!

💰 **غنیمت جنگی:** {loot:,} طلا

{'─'*40}
⚔️ ارتش فاتح با غنیمت و افتخار به کشور باز می‌گردد!

#Victory #{winner['country_name']}"""
    await send_channel(message)

async def announce_defeat(attacker, defender):
    message = f"""💀 **شکست در حمله!**

{attacker['country_emoji']} **{attacker['country_name']}** در حمله به **{defender['country_name']}** {defender['country_emoji']} شکست خورد!

🛡️ **{defender['country_name']}** با موفقیت از خاک خود دفاع کرد.

#Defeat #{attacker['country_name']}"""
    await send_channel(message)

async def announce_alliance(p1, p2):
    message = f"""🤝 **اتحاد جدید!**

{p1['country_emoji']} **{p1['country_name']}** و **{p2['country_name']}** {p2['country_emoji']} متحد شدند!

🛡️ از این پس در نبردها ۱۵٪ از قدرت یکدیگر بهره‌مند خواهند شد.
🔒 این اتحاد تا ۲۴ ساعت قابل لغو نیست.

#Alliance #{p1['country_name']} #{p2['country_name']}"""
    await send_channel(message)

async def announce_peace(p1, p2):
    message = f"""🕊️ **صلح برقرار شد!**

{p1['country_emoji']} **{p1['country_name']}** و **{p2['country_name']}** {p2['country_emoji']} به جنگ پایان دادند!

☮️ صلح و آرامش بین دو کشور برقرار گردید.

#Peace #{p1['country_name']} #{p2['country_name']}"""
    await send_channel(message)

async def announce_un_member(p):
    message = f"""🏛️ **عضویت در سازمان ملل**

{p['country_emoji']} **{p['country_name']}** به سازمان ملل متحد پیوست!

🖥️ سرور {p.get('server_id', '?')}

#UnitedNations #{p['country_name']}"""
    await send_channel(message)

async def announce_country_leave(country_name, country_emoji):
    message = f"""🚪 **خروج از جهان!**

{country_emoji} **{country_name}** رهبر خود را از دست داد!
🔓 کشور آزاد شد.

#CountryLeft #{country_name}"""
    await send_channel(message)

async def announce_global_event(event_name, description):
    message = f"""🌍 **رویداد جهانی!**

📢 **{event_name}**

📝 **توضیحات:**
{description}

⏱️ این رویداد به مدت ۳۰ دقیقه بر تمام کشورهای جهان تأثیر می‌گذارد.

#GlobalEvent #WorldNews"""
    await send_channel(message)

# ==================== توضیحات رویدادهای جهانی ====================
GLOBAL_EVENTS = {
    "رونق اقتصادی": "بازارهای جهانی در وضعیت صعودی قرار گرفته‌اند! 📈\n\n• 💰 درآمد طلای تمام کشورها ۲ برابر می‌شود\n• 📊 قیمت منابع در بازار ۲۰٪ افزایش می‌یابد\n• 🏭 تولید کارخانه‌ها ۵۰٪ بیشتر می‌شود\n\n💡 فرصت عالی برای خرید و فروش در بازار!",
    "بحران نفتی": "ذخایر نفتی جهان با کاهش شدید مواجه شده است! 🛢️\n\n• 🛢️ تولید نفت تمام کشورها نصف می‌شود\n• ⛽ قیمت نفت در بازار ۳ برابر می‌شود\n• ✈️ هزینه نگهداری نیروی هوایی ۲ برابر\n\n💡 نفت خود را ذخیره کنید یا به قیمت بالا بفروشید!",
    "جنگ سرد": "تنش‌های سیاسی جهان را فرا گرفته است! 🥶\n\n• ⚔️ قدرت حمله تمام کشورها ۳۰٪ کاهش می‌یابد\n• 🛡️ قدرت دفاعی ۵۰٪ افزایش می‌یابد\n• 🤝 اتحادهای جدید ۲ برابر امتیاز دارند\n\n💡 زمان مناسبی برای دفاع و اتحاد است!",
    "انقلاب صنعتی": "فناوری‌های جدید جهان را متحول کرده است! 🏭\n\n• 🔬 سطح فناوری تمام کشورها +۱ می‌شود\n• 🏗️ هزینه ساخت ساختمان‌ها ۵۰٪ کاهش\n• ⚡ سرعت تحقیقات ۲ برابر می‌شود\n\n💡 بهترین زمان برای ارتقا و ساخت و ساز!",
    "تهدید هسته‌ای": "خطر جنگ هسته‌ای جهان را تهدید می‌کند! ☢️\n\n• ☢️ تمام کشورهای دارای بمب اتمی ۱۰۰۰ امتیاز می‌گیرند\n• 🏰 اهمیت پناهگاه‌های هسته‌ای ۳ برابر\n• ⚠️ هزینه ساخت بمب اتم ۵۰٪ کاهش\n\n💡 پناهگاه بسازید یا به باشگاه هسته‌ای بپیوندید!",
    "همه‌گیری جهانی": "بیماری مرموزی در حال گسترش است! 🦠\n\n• 🏥 اهمیت بیمارستان‌ها ۳ برابر می‌شود\n• 👥 جمعیت کشورها ۱۰٪ کاهش می‌یابد\n• 💊 قیمت غذا ۲ برابر می‌شود\n\n💡 بیمارستان بسازید و غذای خود را ذخیره کنید!",
    "عصر طلایی": "دوران شکوفایی و prosperity فرا رسیده! ✨\n\n• 💰 تمام کشورها ۱۰,۰۰۰ طلا هدیه می‌گیرند\n• 💎 تولید الماس ۲ برابر می‌شود\n• 🎁 شانس گردونه شانس ۲ برابر\n\n💡 گردونه رو بچرخون و طلاهات رو سرمایه‌گذاری کن!",
    "زمستان هسته‌ای": "آسمان جهان تاریک شده است! 🌑\n\n• 🌡️ تولید غذا ۸۰٪ کاهش می‌یابد\n• 🔥 اهمیت نفت و گاز ۳ برابر\n• ⚔️ تمام جنگ‌ها متوقف می‌شود\n\n💡 منابع انرژی خود را مدیریت کن!"
}

# ==================== تابع کمکی برای چت متحدان ====================
def get_ally_chat_key(uid, allies):
    all_members = sorted([uid] + allies)
    return "_".join(all_members)

# ==================== هندلر اصلی ====================
@bot.on_message_text()
async def handler(bot: Robot, msg: Message):
    try:
        uid = str(msg.sender_id)
        cid = str(msg.chat_id) if msg.chat_id else ""
        text = msg.text.strip() if msg.text else ""
        btn = msg.aux_data.button_id if msg.aux_data else None
        
        if not cid:
            return
        
        if cid not in db.chat_ids:
            db.chat_ids.append(cid)
            db.save()
        
        if uid in db.banned:
            return await bot.send_message(cid, "⛔ **دسترسی مسدود شد!**\n\nشما توسط مدیریت از بازی محروم شده‌اید و امکان استفاده از ربات را ندارید.")
        
        # ===== جوین اجباری فیک =====
        p = get_player(uid)
        if not p:
            can_enter = await check_forced_join(uid, cid, text, btn)
            if not can_enter:
                return
        
        now = int(time.time())
        
        # ⭐ اطمینان از وجود تمام فیلدهای ضروری
        if p:
            p = ensure_player_fields(p)
        
        # ===== پنل ادمین =====
        if text == "پنل":
            if is_admin(uid):
                return await bot.send_message(cid, """👑 **پنل مدیریت ربات**

به پنل مدیریت جنگ جهانی خوش آمدید!

از دکمه‌های زیر برای مدیریت بخش‌های مختلف ربات استفاده کنید:
• 📊 آمار - مشاهده آمار کلی بازیکنان و منابع
• 👥 بازیکنان - لیست تمام کشورهای ثبت‌نام شده
• 📢 پیام همگانی - ارسال پیام به تمام کاربران
• 📢 اعلامیه کانال - ارسال پیام به کانال رسمی
• 📜 بیانیه‌ها - بررسی و تأیید/رد بیانیه‌های ارسالی
• 🚫 مسدود/✅ رفع - مدیریت کاربران خاطی
• 💰 طلا - اهدای طلا به بازیکنان
• 🔄 ریست - حذف کامل یک بازیکن
• 🌟 VIP - مدیریت اشتراک ویژه
• ⚔️ اعلام جنگ/🕊️ صلح - مدیریت جنگ‌ها
• 🌍 رویداد - فعال‌سازی رویداد جهانی
• 🏛️ سازمان ملل - مدیریت عضویت‌ها
• 🚪 درخواست خروج - بررسی درخواست‌های ترک کشور""", chat_keypad=admin_keypad())
            else:
                return await bot.send_message(cid, "❌ **دسترسی غیرمجاز!**\n\nشما ادمین نیستید و نمی‌توانید به پنل مدیریت وارد شوید.")
        
        # ===== بخش ادمین - دکمه‌ها =====
        if is_admin(uid) and btn:
            if btn.startswith("appr_"):
                try:
                    stmt_id = int(btn.replace("appr_", ""))
                except:
                    return await bot.send_message(cid, "❌ خطا در شناسه بیانیه!", chat_keypad=admin_keypad())
                
                for stmt in db.statements:
                    if stmt.get("id") == stmt_id and stmt["status"] == "pending":
                        stmt["status"] = "approved"
                        stmt["approved_at"] = datetime.now().isoformat()
                        stmt["approved_by"] = uid
                        db.save()
                        
                        if stmt["user_id"] in db.players:
                            db.players[stmt["user_id"]]["statements_approved"] = db.players[stmt["user_id"]].get("statements_approved", 0) + 1
                            p_name = db.players[stmt["user_id"]]["country_name"]
                            p_emoji = db.players[stmt["user_id"]]["country_emoji"]
                            
                            channel_result = await announce_statement(p_name, p_emoji, stmt["text"])
                            
                            try:
                                if channel_result:
                                    await bot.send_message(stmt["user_id"], f"✅ **بیانیه شما تأیید و منتشر شد!**\n\n📢 بیانیه شما با موفقیت در کانال رسمی {CHANNEL_ID} منتشر گردید.\n\n📝 متن: {stmt['text'][:100]}...")
                                else:
                                    await bot.send_message(stmt["user_id"], f"✅ **بیانیه شما تأیید شد!**\n\n⚠️ اما خطایی در انتشار کانال رخ داد. لطفاً به ادمین اطلاع دهید.")
                            except:
                                pass
                            
                            check_achievements(db.players[stmt["user_id"]], stmt["user_id"])
                        
                        db.admin_logs.append({"action": "approve_statement", "stmt_id": stmt_id, "time": datetime.now().isoformat()})
                        db.save()
                        
                        return await bot.send_message(cid, f"✅ **بیانیه شماره {stmt_id} تأیید و در کانال منتشر شد!**\n\n📢 کانال: {CHANNEL_ID}\n📝 وضعیت: انتشار یافته", chat_keypad=admin_keypad())
                
                return await bot.send_message(cid, "❌ **بیانیه یافت نشد!**\n\nاین بیانیه قبلاً بررسی شده یا وجود ندارد.", chat_keypad=admin_keypad())
            
            if btn.startswith("rej_"):
                try:
                    stmt_id = int(btn.replace("rej_", ""))
                except:
                    return await bot.send_message(cid, "❌ خطا در شناسه بیانیه!", chat_keypad=admin_keypad())
                
                for stmt in db.statements:
                    if stmt.get("id") == stmt_id and stmt["status"] == "pending":
                        stmt["status"] = "rejected"
                        stmt["rejected_at"] = datetime.now().isoformat()
                        stmt["rejected_by"] = uid
                        db.save()
                        
                        try:
                            await bot.send_message(stmt["user_id"], "❌ **بیانیه شما رد شد.**\n\nمتأسفانه بیانیه شما مورد تأیید قرار نگرفت. می‌توانید متن را اصلاح کرده و دوباره ارسال کنید.")
                        except:
                            pass
                        
                        db.admin_logs.append({"action": "reject_statement", "stmt_id": stmt_id, "time": datetime.now().isoformat()})
                        db.save()
                        
                        return await bot.send_message(cid, f"❌ **بیانیه شماره {stmt_id} رد شد!**\n\n📝 وضعیت: رد شده", chat_keypad=admin_keypad())
                
                return await bot.send_message(cid, "❌ **بیانیه یافت نشد!**", chat_keypad=admin_keypad())
            
            if btn.startswith("approve_leave_"):
                target_uid = btn.replace("approve_leave_", "")
                if target_uid in db.players:
                    pl = db.players[target_uid]
                    country_name = pl.get("country_name", "نامشخص")
                    country_emoji = pl.get("country_emoji", "")
                    country_key = pl.get("country_key")
                    
                    if country_key and country_key in db.countries_taken:
                        db.countries_taken.remove(country_key)
                    
                    server_id = str(pl.get("server_id", 1))
                    if target_uid in db.server_players.get(server_id, []):
                        db.server_players[server_id].remove(target_uid)
                    
                    if target_uid in db.invite_codes:
                        del db.invite_codes[target_uid]
                    
                    del db.players[target_uid]
                    
                    try:
                        del pending[f"leave_{target_uid}"]
                    except:
                        pass
                    
                    db.admin_logs.append({"action": "approve_leave", "country": country_name, "time": datetime.now().isoformat()})
                    db.save()
                    
                    await announce_country_leave(country_name, country_emoji)
                    
                    try:
                        await bot.send_message(target_uid, f"✅ **درخواست خروج شما تأیید شد!**\n\nکشور {country_emoji} {country_name} آزاد شد.\n\n🎮 با /start می‌توانید دوباره ثبت‌نام کنید و کشور جدیدی انتخاب نمایید.")
                    except:
                        pass
                    
                    return await bot.send_message(cid, f"✅ **خروج بازیکن تأیید شد!**\n\n{country_emoji} **{country_name}** از کشورش خارج شد.\n🔓 کشور آزاد شد و بازیکنان جدید می‌توانند آن را انتخاب کنند.", chat_keypad=admin_keypad())
            
            if btn.startswith("reject_leave_"):
                target_uid = btn.replace("reject_leave_", "")
                try:
                    del pending[f"leave_{target_uid}"]
                except:
                    pass
                try:
                    await bot.send_message(target_uid, "❌ **درخواست خروج شما رد شد.**\n\nادمین با خروج شما از کشور موافقت نکرد. به بازی ادامه دهید!")
                except:
                    pass
                return await bot.send_message(cid, "❌ **درخواست خروج رد شد!**\n\nبازیکن به بازی ادامه خواهد داد.", chat_keypad=admin_keypad())
        
        # ===== کاربر ثبت‌نام نشده =====
        if not p:
            if text.startswith("/start"):
                parts = text.split()
                if len(parts) > 1:
                    code = parts[1].strip().upper()
                    if len(code) >= 4:
                        pending[f"{uid}_inviter_code"] = code
                try:
                    del pending[uid]
                except:
                    pass
            
            if btn == "start_game" or text == "/start":
                try:
                    del pending[uid]
                except:
                    pass
                pending[uid] = "wait_server"
                return await bot.send_message(cid, f"""🌍 **به دنیای جنگ جهانی خوش آمدید!** ⚔️

🎮 **Game War - نبرد فرماندهان**
"سرزمینت را بساز، ارتشت را تجهیز کن و جهان را فتح کن!"

{'─'*40}
✨ **امکانات بی‌نظیر بازی:**

🏰 **۱۰۰+ کشور واقعی** با پرچم، پایتخت و قدرت‌های متفاوت
🌍 **۱۰ سرور مجزا** با رتبه‌بندی مستقل از یکدیگر
⚔️ **جنگ‌های استراتژیک** با محاسبه دقیق قدرت نظامی و انتخاب نوع نیرو
🤝 **سیستم اتحاد دوطرفه** - درخواست اتحاد بفرستید و منتظر تأیید باشید
💬 **چت با متحدان** - با هم‌پیمانان خود گفتگو و هماهنگی کنید
💀 **عملیات هک و جاسوسی** - منابع دشمن را بدزدید و اطلاعات کسب کنید
☢️ **موشک هسته‌ای** - سلاح آخرالزمانی برای نابودی کامل دشمن
💎 **سیستم VIP** با بونوس‌های ویژه و درآمد بیشتر
🏗️ **۱۵ نوع ساختمان** با قابلیت ارتقا و اثرات متنوع
👥 **دعوت دوستان** - با کد دعوت ۵,۰۰۰ طلا جایزه بگیرید
🏛️ **سازمان ملل متحد** - عضو شوید، رأی دهید و دبیرکل شوید
🔄 **صرافی** - تبادل کالا با سایر بازیکنان
🎡 **گردونه شانس** - هر ۱۲ ساعت رایگان بچرخانید

{'─'*40}
📢 **کانال رسمی:** {CHANNEL_ID}
👑 **ادمین:** برای دسترسی به پنل مدیریت «پنل» را تایپ کنید

🎮 برای شروع، سرور خود را از بین ۱۰ سرور موجود انتخاب کنید:""", chat_keypad=server_keypad())
            
            if btn == "enter_invite_code":
                try:
                    del pending[uid]
                except:
                    pass
                pending[uid] = "wait_invite_code"
                return await bot.send_message(cid, """🔑 **وارد کردن کد دعوت**

کد دعوت ۶ رقمی دوست خود را وارد کنید تا هر دو نفر ۵,۰۰۰ طلا جایزه دریافت کنید!

📝 کد را دقیقاً مطابق با کدی که دوستتان به شما داده وارد کنید.
🔤 حروف بزرگ و کوچک مهم است.
💰 جایزه: ۵,۰۰۰ طلا برای هر دو طرف

💡 اگر کد دعوت ندارید، دکمه «شروع بدون کد» را بزنید.""", 
                    chat_keypad=ChatKeypadBuilder().row(ChatKeypadBuilder().button("start_game", "🎮 شروع بدون کد")).build())
            
            if btn and btn.startswith("server_"):
                server_id = int(btn.replace("server_", ""))
                if server_id in SERVERS:
                    pending[uid] = f"server_{server_id}"
                    return await bot.send_message(cid, f"""🖥️ **{SERVERS[server_id]['emoji']} {SERVERS[server_id]['name']}**

شما سرور {server_id} را برای بازی انتخاب کردید.
این سرور دارای رتبه‌بندی و آمار مستقل از سایر سرورهاست.

🌍 اکنون **قاره** مورد نظر خود را انتخاب کنید:""", chat_keypad=continent_keypad())
            
            if btn and btn.startswith("cont_"):
                cont_key = btn.replace("cont_", "")
                if cont_key in CONTINENTS:
                    return await bot.send_message(cid, f"""{CONTINENTS[cont_key]['emoji']} **قاره {CONTINENTS[cont_key]['name']}**

🎌 کشورهای آزاد این قاره را مشاهده می‌کنید.
هر کشور دارای منابع، قدرت نظامی و ویژگی‌های منحصر به فرد است.

کشوری را که می‌خواهید رهبری کنید با دقت انتخاب نمایید:""", chat_keypad=country_keypad(cont_key))
            
            if btn and btn.startswith("pick_"):
                parts = btn.split("_")
                cont_key = parts[1]
                country_key = "_".join(parts[2:])
                
                server_data = pending.get(uid, "")
                server_id = int(server_data.replace("server_", "")) if server_data.startswith("server_") else 1
                
                if cont_key in CONTINENTS and country_key in CONTINENTS[cont_key]["countries"]:
                    if country_key in db.countries_taken:
                        return await bot.send_message(cid, "❌ **این کشور قبلاً انتخاب شده است!**\n\nبازیکن دیگری این کشور را انتخاب کرده. لطفاً کشور دیگری برگزینید.", chat_keypad=continent_keypad())
                    
                    inviter_code = pending.get(f"{uid}_inviter_code")
                    p, invite_bonus = create_player(uid, server_id, cont_key, country_key, inviter_code)
                    
                    try:
                        del pending[uid]
                    except:
                        pass
                    try:
                        del pending[f"{uid}_inviter_code"]
                    except:
                        pass
                    
                    inviter_text = ""
                    if invite_bonus > 0:
                        inviter_text = f"\n\n👥 **کد دعوت فعال شد!**\n💰 ۵,۰۰۰ طلا جایزه به حساب شما و دعوت‌کننده واریز گردید!"
                        if p.get("inviter") and p["inviter"] in db.players:
                            try:
                                await bot.send_message(p["inviter"], f"🎉 **دعوت موفق!**\n\n{p['country_emoji']} **{p['country_name']}** با کد دعوت شما وارد بازی شد!\n\n💰 ۵,۰۰۰ طلا به حساب شما واریز شد.")
                            except:
                                pass
                    
                    await bot.send_message(cid, f"""🎉 **به دنیای جنگ جهانی خوش آمدید!**

{p['country_emoji']} **{p['country_name']}**
📌 قاره: {p['continent_emoji']} {p['continent_name']}
🏛 پایتخت: {p['capital']}
🖥️ سرور {server_id}: {SERVERS[server_id]['name']}

📊 **اطلاعات کشور شما:**
👥 جمعیت: {p['population']} میلیون نفر
💰 تولید ناخالص داخلی: {p['gdp']} میلیارد دلار
⚔️ قدرت ارتش ملی: {p['army_strength']:,} سرباز

📦 **منابع اولیه:**
🥇 طلا: {p['resources']['gold']:,}
🍞 غذا: {p['resources']['food']:,}
🛢️ نفت: {p['resources'].get('oil', 0):,}
💎 الماس: {p['resources'].get('diamond', 0)}

🛡️ **محافظت نوب:** ۱۵ دقیقه (هیچ کشوری نمی‌تواند به شما حمله کند)
🔑 **کد دعوت شما:** `{p['invite_code']}`
{inviter_text}

{'─'*40}
🎮 از دکمه‌های زیر برای مدیریت کشورتان استفاده کنید.
⚔️ ارتش بسازید، متحد شوید و جهان را فتح کنید!""", chat_keypad=main_keypad())
                    await announce_new_country(p)
                    return
            
            if btn == "back_cont":
                return await bot.send_message(cid, "🌍 **انتخاب قاره:**\n\nلطفاً قاره مورد نظر خود را انتخاب کنید:", chat_keypad=continent_keypad())
            
            if pending.get(uid) == "wait_invite_code" and text and not btn:
                code = text.strip().upper()
                if len(code) >= 4:
                    inviter_uid = find_user_by_invite_code(code)
                    if inviter_uid and inviter_uid in db.players:
                        pending[f"{uid}_inviter_code"] = code
                        try:
                            del pending[uid]
                        except:
                            pass
                        pending[uid] = "wait_server"
                        return await bot.send_message(cid, f"""✅ **کد دعوت معتبر است!**

👤 دعوت از طرف: {db.players[inviter_uid]['country_emoji']} **{db.players[inviter_uid]['country_name']}**

💰 پس از انتخاب کشور، ۵,۰۰۰ طلا جایزه دریافت خواهید کرد!

حالا سرور خود را انتخاب کنید:""", chat_keypad=server_keypad())
                    else:
                        return await bot.send_message(cid, "❌ **کد دعوت نامعتبر است!**\n\nاین کد در سیستم وجود ندارد. لطفاً دوباره تلاش کنید یا بدون کد ادامه دهید.", chat_keypad=start_keypad())
            
            if not btn:
                return await bot.send_message(cid, """🎮 **شما هنوز ثبت‌نام نکرده‌اید!**

برای ورود به دنیای جنگ جهانی، یکی از گزینه‌های زیر را انتخاب کنید:

🔑 **کد دعوت دارم** - اگر دوستتان شما را دعوت کرده، کد را وارد کنید تا ۵,۰۰۰ طلا جایزه بگیرید
🎮 **شروع بازی** - ورود مستقیم به بازی و انتخاب کشور""", chat_keypad=start_keypad())
            
            return
        
        # ===== کاربر ثبت‌نام شده =====
        p["online"] = True
        p["last_active"] = now
        
        if p.get("is_vip") and p.get("vip_expire", 0) > 0 and p["vip_expire"] < now:
            p["is_vip"] = False
            p["vip_expire"] = 0
            db.save()
        
        protection_msg = ""
        if is_protected(p):
            parts = []
            if p.get("newbie_protection", 0) > now:
                remaining_minutes = (p["newbie_protection"] - now) // 60
                parts.append(f"🛡️ محافظت نوب: {remaining_minutes} دقیقه دیگر")
            if p.get("protection_expire", 0) > now:
                remaining_hours = (p["protection_expire"] - now) // 3600
                parts.append(f"🛡️ محافظت ویژه: {remaining_hours} ساعت دیگر")
            if parts:
                protection_msg = "\n" + "\n".join(parts)
        
        if btn == "back":
            return await bot.send_message(cid, f"""🏰 **بازگشت به منوی اصلی**

{p['country_emoji']} **{p['country_name']}**
{protection_msg}

🔑 **کد دعوت شما:** `{p.get('invite_code', 'خطا در نمایش')}`
📋 این کد را به دوستان خود بدهید تا هر دو ۵,۰۰۰ طلا جایزه بگیرید!

از دکمه‌های زیر برای ادامه بازی استفاده کنید:""", chat_keypad=main_keypad())
        
        if btn == "go_game":
            atk, df = get_power(p)
            return await bot.send_message(cid, f"""{p['country_emoji']} **{p['country_name']}**

🖥️ سرور {p.get('server_id', '?')}: {SERVERS.get(p.get('server_id', 1), {}).get('name', '?')}

📊 **قدرت نظامی:**
⚔️ حمله: {atk:,}
🛡️ دفاع: {df:,}

🔑 کد دعوت: `{p.get('invite_code', 'N/A')}`
{protection_msg}

از دکمه‌های زیر استفاده کنید:""", chat_keypad=main_keypad())
        
        # ===== کد دعوت برای کاربران ثبت‌نام شده =====
        if btn == "enter_invite_code":
            pending[uid] = "wait_invite_code_registered"
            return await bot.send_message(cid, """🔑 **وارد کردن کد دعوت**

⚠️ شما قبلاً ثبت‌نام کرده‌اید!
اما اگر هنوز کد دعوت دوستتان را وارد نکرده‌اید، می‌توانید همین الان این کار را انجام دهید.

📝 **توجه:** اگر قبلاً با کد دعوت ثبت‌نام کرده‌اید، جایزه مجدد دریافت نمی‌کنید.

💰 **جایزه:** ۵,۰۰۰ طلا برای شما و دوستتان

کد ۶ رقمی را وارد کنید:""", 
                chat_keypad=ChatKeypadBuilder().row(ChatKeypadBuilder().button("back", "🔙 بازگشت")).build())
        
        if pending.get(uid) == "wait_invite_code_registered" and text and not btn:
            code = text.strip().upper()
            if len(code) >= 4:
                inviter_uid = find_user_by_invite_code(code)
                if inviter_uid and inviter_uid != uid and inviter_uid in db.players:
                    if p.get("inviter"):
                        pending.pop(uid, None)
                        return await bot.send_message(cid, "❌ **شما قبلاً با کد دعوت ثبت‌نام کرده‌اید!**\n\nجایزه دعوت فقط یک بار قابل دریافت است.", chat_keypad=main_keypad())
                    
                    p["inviter"] = inviter_uid
                    db.players[inviter_uid]["resources"]["gold"] = db.players[inviter_uid]["resources"].get("gold", 0) + 5000
                    db.players[inviter_uid]["invites_sent"] = db.players[inviter_uid].get("invites_sent", 0) + 1
                    p["resources"]["gold"] = p["resources"].get("gold", 0) + 5000
                    
                    pending.pop(uid, None)
                    db.save()
                    check_achievements(db.players[inviter_uid], inviter_uid)
                    
                    try:
                        await bot.send_message(inviter_uid, f"🎉 **دعوت جدید!**\n\n{p['country_emoji']} **{p['country_name']}** با کد شما جایزه گرفت!\n💰 +۵,۰۰۰ طلا به حساب شما واریز شد.")
                    except:
                        pass
                    
                    return await bot.send_message(cid, f"""✅ **کد دعوت فعال شد!**

👤 دعوت از: {db.players[inviter_uid]['country_emoji']} **{db.players[inviter_uid]['country_name']}**
💰 **جایزه:** ۵,۰۰۰ طلا به حساب شما و دعوت‌کننده واریز شد!""", chat_keypad=main_keypad())
                else:
                    pending.pop(uid, None)
                    return await bot.send_message(cid, "❌ **کد دعوت نامعتبر است!**\n\nاین کد در سیستم وجود ندارد. لطفاً دوباره تلاش کنید.", chat_keypad=main_keypad())
        
        # ===== خروج از کشور =====
        if btn == "leave_country" or text == "خروج":
            return await bot.send_message(cid, f"""🚪 **خروج از کشور**

⚠️ **هشدار جدی!** با خروج از کشور:

• 📦 تمام منابع ذخیره شده شما نابود می‌شود
• ⚔️ تمام نیروهای نظامی شما منهدم می‌گردد
• 🏗️ تمام ساختمان‌ها و پیشرفت‌های شما از بین می‌رود
• 🌍 کشور شما برای انتخاب سایر بازیکنان آزاد می‌شود
• 🎮 برای ادامه بازی باید دوباره ثبت‌نام کنید

📝 برای تأیید نهایی، بنویسید: `تایید خروج`
🔙 برای انصراف و بازگشت به بازی: `انصراف`""", 
                chat_keypad=ChatKeypadBuilder().row(ChatKeypadBuilder().button("back", "🔙 انصراف از خروج")).build())
        
        if text == "تایید خروج":
            pending[f"leave_{uid}"] = True
            
            for admin_id in ADMIN_IDS:
                try:
                    kb = ChatKeypadBuilder()
                    kb.row(
                        kb.button(f"approve_leave_{uid}", "✅ تایید خروج"),
                        kb.button(f"reject_leave_{uid}", "❌ رد خروج")
                    )
                    await bot.send_message(admin_id, f"""🚪 **درخواست خروج از کشور**

{p['country_emoji']} **{p['country_name']}**
🖥️ سرور {p.get('server_id', '?')}
⭐ امتیاز: {p.get('score', 0):,}
🥇 طلا: {p['resources'].get('gold', 0):,}
📅 تاریخ عضویت: {p.get('joined_at', 'نامشخص')[:10]}

👤 این بازیکن می‌خواهد کشورش را ترک کند و تمام دارایی‌هایش از بین می‌رود.
⏳ منتظر تصمیم شماست...""", chat_keypad=kb.build())
                except:
                    pass
            
            return await bot.send_message(cid, """✅ **درخواست خروج ثبت شد!**

درخواست شما برای ادمین ارسال گردید.
⏳ لطفاً منتظر تأیید ادمین باشید...

🔙 برای لغو درخواست، `انصراف` بنویسید.""", chat_keypad=main_keypad())
        
        if text == "انصراف":
            try:
                del pending[f"leave_{uid}"]
            except:
                pass
            return await bot.send_message(cid, "🔙 **درخواست خروج لغو شد.**\n\nشما همچنان رهبر کشورتان هستید. به بازی ادامه دهید و جهان را فتح کنید!", chat_keypad=main_keypad())
        
        # ===== سازمان ملل =====
        if btn == "un_menu":
            server_id = p.get("server_id", 1)
            un = get_un_data(server_id)
            sg = get_un_secretary_general(server_id)
            member_count = len(un.get("members", []))
            is_member = uid in un.get("members", [])
            
            sg_text = "ندارد"
            if sg:
                sg_text = f"{sg['country_emoji']} **{sg['country_name']}**"
            
            return await bot.send_message(cid, f"""🏛️ **سازمان ملل متحد - سرور {server_id}**

🌍 کشور شما: {p['country_emoji']} **{p['country_name']}**
📋 وضعیت عضویت: {'✅ عضو رسمی' if is_member else '❌ عضو نیستید'}

👑 **دبیرکل سازمان ملل:** 
   {sg_text}

📊 **اعضای سازمان ملل:** {member_count} کشور

{'─'*40}
🔹 **امکانات سازمان ملل:**
• 📝 درخواست عضویت - به جامعه جهانی بپیوندید
• 👥 مشاهده اعضا - کشورهای عضو را ببینید
• 📋 درخواست‌های عضویت - وضعیت درخواست‌ها""", chat_keypad=un_keypad())
        
        if btn == "un_join":
            server_id = p.get("server_id", 1)
            un = get_un_data(server_id)
            
            if uid in un.get("members", []):
                return await bot.send_message(cid, "✅ **شما قبلاً عضو سازمان ملل هستید!**\n\nبه عنوان عضو، از بونوس درآمد اضافی و حق رأی در تصمیم‌گیری‌ها بهره‌مند می‌شوید.", chat_keypad=un_keypad())
            
            if uid in un.get("join_requests", []):
                return await bot.send_message(cid, "⏳ **درخواست شما قبلاً ثبت شده است!**\n\nلطفاً منتظر تأیید دبیرکل سازمان ملل باشید.", chat_keypad=un_keypad())
            
            if p.get("score", 0) < 100:
                return await bot.send_message(cid, f"❌ **حداقل ۱۰۰ امتیاز نیاز است!**\n\nبرای عضویت در سازمان ملل باید حداقل ۱۰۰ امتیاز کسب کرده باشید.\n⭐ امتیاز فعلی شما: {p.get('score', 0)}", chat_keypad=un_keypad())
            
            un["join_requests"].append(uid)
            db.un_data[str(server_id)] = un
            db.save()
            
            return await bot.send_message(cid, """📝 **درخواست عضویت ثبت شد!**

درخواست شما برای عضویت در سازمان ملل متحد ثبت گردید.
👑 دبیرکل سازمان ملل درخواست شما را بررسی خواهد کرد.

✨ **مزایای عضویت:**
• 💰 درآمد طلای بیشتر در هر دوره
• 🎯 کسب امتیاز تجربه اضافی
• 🗳️ حق رأی در تصمیم‌گیری‌های جهانی
• 🛡️ اعتبار بین‌المللی

⏳ لطفاً منتظر تأیید باشید...""", chat_keypad=un_keypad())
        
        if btn == "un_members":
            server_id = p.get("server_id", 1)
            un = get_un_data(server_id)
            members = un.get("members", [])
            
            if not members:
                return await bot.send_message(cid, "👥 **هنوز کشوری عضو سازمان ملل نشده است!**\n\nشما می‌توانید اولین عضو باشید و در تاریخ ثبت شوید.", chat_keypad=un_keypad())
            
            msg = f"👥 **اعضای سازمان ملل متحد - سرور {server_id}:**\n\n"
            for i, mid in enumerate(members[:20], 1):
                if mid in db.players:
                    mp = db.players[mid]
                    is_sg = "👑 " if un.get("secretary_general") == mid else ""
                    msg += f"{i}. {is_sg}{mp['country_emoji']} **{mp['country_name']}** | ⭐{mp.get('score', 0):,} امتیاز\n"
            
            if len(members) > 20:
                msg += f"\n... و {len(members) - 20} کشور دیگر"
            
            return await bot.send_message(cid, msg, chat_keypad=un_keypad())
        
        if btn == "un_requests":
            server_id = p.get("server_id", 1)
            un = get_un_data(server_id)
            requests = un.get("join_requests", [])
            
            if not requests:
                return await bot.send_message(cid, "📋 **هیچ درخواست عضویتی در انتظار نیست!**", chat_keypad=un_keypad())
            
            msg = f"📋 **درخواست‌های عضویت در انتظار تأیید - سرور {server_id}:**\n\n"
            for i, req_uid in enumerate(requests[:15], 1):
                if req_uid in db.players:
                    rp = db.players[req_uid]
                    msg += f"{i}. {rp['country_emoji']} **{rp['country_name']}** | ⭐{rp.get('score', 0):,} امتیاز\n"
            
            if len(requests) > 15:
                msg += f"\n... و {len(requests) - 15} درخواست دیگر"
            
            msg += "\n\n👑 **دبیرکل** می‌تواند با دستور زیر درخواست‌ها را تأیید کند:\n`تایید_عضویت [نام کشور] [شماره سرور]`"
            
            return await bot.send_message(cid, msg, chat_keypad=un_keypad())
        
        # ===== گردونه شانس =====
        if btn == "lucky_wheel":
            last = db.lucky_wheel.get(uid, 0)
            cd = 12*3600
            if now - last >= cd:
                rem = "✅ **آماده چرخوندن!**"
                can = True
            else:
                r = cd - (now - last)
                rem = f"⏳ **{r//3600} ساعت و {(r%3600)//60} دقیقه دیگر**"
                can = False
            
            msg = f"""🎡 **گردونه شانس**

🎁 **جوایز احتمالی گردونه:**

{'─'*20} 💰 طلا {'─'*20}
💰 ۵,۰۰۰ طلا
💰 ۱۰,۰۰۰ طلا
💰 ۲۵,۰۰۰ طلا

{'─'*20} 🛢️ نفت {'─'*20}
🛢️ ۲,۰۰۰ نفت
🛢️ ۵,۰۰۰ نفت

{'─'*20} 🎯 تجربه {'─'*20}
🎯 ۱۰۰ XP
🎯 ۲۵۰ XP

{'─'*20} ✨ ویژه {'─'*20}
💎 VIP ۷ روز رایگان
🛡️ محافظت ۳ روزه
😢 متأسفانه چیزی نبردی!

⏱️ **هر ۱۲ ساعت یکبار**
🆓 **کاملاً رایگان!**

{'─'*40}
⏰ وضعیت: {rem}"""
            
            return await bot.send_message(cid, msg, chat_keypad=lucky_wheel_keypad() if can else main_keypad())
        
        if btn == "spin_wheel":
            last = db.lucky_wheel.get(uid, 0)
            if now - last < 12*3600:
                remaining = 12*3600 - (now - last)
                return await bot.send_message(cid, f"⏳ **{remaining//3600} ساعت دیگر** می‌توانید گردونه را بچرخانید!", chat_keypad=main_keypad())
            
            total_chance = sum(p["chance"] for p in LUCKY_WHEEL_PRIZES)
            roll = random.randint(1, total_chance)
            cum = 0
            selected = LUCKY_WHEEL_PRIZES[-1]
            for prize in LUCKY_WHEEL_PRIZES:
                cum += prize["chance"]
                if roll <= cum:
                    selected = prize
                    break
            
            if selected["type"] == "gold":
                p["resources"]["gold"] += selected["amount"]
                res = f"💰 **{selected['amount']:,} طلا** به حساب شما واریز شد!"
            elif selected["type"] == "oil":
                p["resources"]["oil"] = p["resources"].get("oil",0) + selected["amount"]
                res = f"🛢️ **{selected['amount']:,} نفت** به منابع شما اضافه شد!"
            elif selected["type"] == "xp":
                p["xp"] = p.get("xp",0) + selected["amount"]
                p["score"] += selected["amount"]
                res = f"🎯 **{selected['amount']} امتیاز تجربه** کسب کردید!"
            elif selected["type"] == "vip":
                p["is_vip"] = True
                p["vip_expire"] = now + selected["amount"]*86400
                res = f"💎 **عضویت VIP {selected['amount']} روزه** برای شما فعال شد!"
            elif selected["type"] == "protection":
                p["protection_expire"] = now + selected["amount"]*86400
                res = f"🛡️ **محافظت {selected['amount']} روزه** فعال شد! هیچکس نمی‌تواند به شما حمله کند."
            else:
                res = "😢 **متأسفانه این دفعه چیزی نبردی!** شانس خود را ۱۲ ساعت دیگر دوباره امتحان کن."
            
            db.lucky_wheel[uid] = now
            db.lucky_wheel_count[uid] = db.lucky_wheel_count.get(uid,0) + 1
            db.save()
            check_achievements(p, uid)
            
            return await bot.send_message(cid, f"""🎲 **نتیجه قرعه‌کشی گردونه شانس:**

✨ {selected['emoji']} **{selected['name']}**

{res}

{'─'*40}
⏳ ۱۲ ساعت دیگر می‌توانید دوباره شانس خود را امتحان کنید!""", chat_keypad=main_keypad())
        
        # ===== دعوت =====
        if btn == "invite_menu":
            return await bot.send_message(cid, f"""🎁 **سیستم دعوت دوستان**

📋 **کد دعوت شما:**
`{p.get('invite_code','N/A')}`

👥 **تعداد دعوت‌های موفق:** {p.get('invites_sent',0)} نفر
💰 **جایزه هر دعوت:** ۵,۰۰۰ طلا (برای هر دو نفر)

{'─'*40}
✨ **روش استفاده:**
۱. کد بالا را برای دوستانتان بفرستید
۲. دوست شما هنگام ثبت‌نام گزینه «🔑 کد دعوت دارم» را بزند
۳. کد شما را وارد کند
۴. پس از انتخاب کشور، هر دو ۵,۰۰۰ طلا جایزه می‌گیرید!

💡 **نکته:** دوست شما باید هنوز ثبت‌نام نکرده باشد.""", chat_keypad=main_keypad())
        
        # ===== کشور من =====
        if btn == "country_info":
            atk, df = get_power(p)
            vip_status = "🌟 فعال" if p.get("is_vip") else "❌ غیرفعال"
            un_status = "✅ عضو" if p.get("un_member") else "❌ غیرعضو"
            
            msg = f"""{p['country_emoji']} **{p['country_name']}**

📌 قاره: {p['continent_emoji']} {p['continent_name']}
🏛 پایتخت: {p['capital']}
🖥️ سرور {p.get('server_id', '?')}

📊 **اطلاعات کلی:**
👥 جمعیت: {p['population']}M
💰 GDP: {p['gdp']}B
⚔️ ارتش ملی: {p['army_strength']:,}
🛡️ محافظت: {'✅ فعال' if is_protected(p) else '❌ پایان یافته'}
🌟 VIP: {vip_status}
🏛️ سازمان ملل: {un_status}

{'─'*40}
📦 **منابع:**\n"""
            for r, a in p["resources"].items():
                if a > 0 and r in RESOURCES:
                    msg += f"{RESOURCES[r]['emoji']} {RESOURCES[r]['name']}: {a:,}\n"
            
            msg += f"""
{'─'*40}
⚔️ قدرت حمله: {atk:,}
🛡️ قدرت دفاع: {df:,}
🔬 سطح فناوری: {p['tech_level']}
⭐ امتیاز: {p['score']:,}
🎯 تجربه: {p.get('xp', 0)} XP
🏆 پیروزی: {p['battles_won']} | 💀 شکست: {p['battles_lost']}

🔑 کد دعوت: `{p.get('invite_code', 'خطا')}`"""
            
            return await bot.send_message(cid, msg, chat_keypad=main_keypad())
        
        # ===== منوی حمله =====
        if btn == "attack_menu":
            server_list = [(pl, get_power(pl)) for uid_pl, pl in db.players.items() if uid_pl != uid and pl.get("server_id") == p.get("server_id")]
            cd = (p.get('last_war_time',0) + p.get('war_cooldown',10800)) - now
            cd_text = '✅ **آماده حمله**' if cd <= 0 else f'⏳ **{cd//60} دقیقه دیگر**'
            
            msg = "⚔️ **اهداف در سرور شما:**\n\n"
            if server_list:
                for pl, (atk, df) in server_list[:10]:
                    prot = " 🛡️" if is_protected(pl) else ""
                    on = "🟢 آنلاین" if pl.get("online") else "⚪ آفلاین"
                    msg += f"{pl['country_emoji']} **{pl['country_name']}**{prot}\n"
                    msg += f"   وضعیت: {on}\n"
                    msg += f"   💪 حمله: {atk:,} | 🛡️ دفاع: {df:,} | ⭐ امتیاز: {pl.get('score', 0):,}\n\n"
            else:
                msg += "هیچ هدفی در سرور شما وجود ندارد!\nمنتظر بمانید تا بازیکنان جدید ثبت‌نام کنند.\n"
            
            msg += f"""{'─'*40}
⏳ **کول‌داون جنگ:** {cd_text}

📝 **نحوه حمله:**
برای حمله به یک کشور، نام آن را بنویسید:
`حمله ایران` یا `حمله آلمان`

⚔️ پس از زدن اسم کشور، می‌توانید نوع نیروهای اعزامی را انتخاب کنید:
• 💂 سربازان پیاده
• 🚜 تانک‌ها و توپخانه
• ✈️ نیروی هوایی
• 🦅 نیروهای ویژه
• ⚔️ تمام نیروها

🛡️ کشورهای تحت محافظت قابل حمله نیستند."""
            return await bot.send_message(cid, msg)
        
        # ===== حمله با انتخاب نیرو =====
        if text.startswith("حمله "):
            target_name = text[5:].strip()
            target = find_country_smart(target_name)
            
            if not target or target not in db.players:
                server_list = [f"{pl['country_emoji']} {pl['country_name']}" for uid_pl, pl in db.players.items() if uid_pl != uid and pl.get("server_id") == p.get("server_id")]
                hint = "\n".join(server_list[:5]) if server_list else "هیچ کشوری در سرور شما وجود ندارد!"
                return await bot.send_message(cid, f"""❌ **کشور '{target_name}' یافت نشد!**

📋 **کشورهای موجود در سرور شما:**
{hint}

📝 **مثال صحیح:** `حمله ایران`""")
            
            if target == uid:
                return await bot.send_message(cid, "❌ **نمی‌توانید به خودتان حمله کنید!**\n\nکشور خودتان را نمی‌توانید مورد حمله قرار دهید.")
            
            tgt = db.players[target]
            
            if tgt.get("server_id") != p.get("server_id"):
                return await bot.send_message(cid, "❌ **این کشور در سرور دیگری است!**\n\nشما فقط می‌توانید به کشورهای هم‌سرور خود حمله کنید.")
            
            if is_protected(tgt):
                return await bot.send_message(cid, f"🛡️ **{tgt['country_emoji']} {tgt['country_name']} تحت محافظت است!**\n\nاین کشور در حال حاضر سپر محافظتی دارد و قابل حمله نیست.")
            
            if p.get("last_war_time", 0) + p.get("war_cooldown", 10800) > now:
                remaining = (p["last_war_time"] + p["war_cooldown"]) - now
                return await bot.send_message(cid, f"⏳ **خستگی جنگ!**\n\nارتش شما پس از نبرد قبلی هنوز آماده نیست. باید {remaining // 60} دقیقه دیگر صبر کنید.")
            
            attack_pending[uid] = target
            return await bot.send_message(cid, f"""⚔️ **حمله به {tgt['country_emoji']} {tgt['country_name']}**

📊 **قدرت دشمن:**
⚔️ حمله: {get_power(tgt)[0]:,}
🛡️ دفاع: {get_power(tgt)[1]:,}

🎯 **نوع نیروی اعزامی را انتخاب کنید:**
• 💂 سربازان پیاده - نیروهای زمینی سبک
• 🚜 تانک‌ها و توپخانه - نیروهای زرهی سنگین
• ✈️ نیروی هوایی - جنگنده‌ها و بمب‌افکن‌ها
• 🦅 نیروهای ویژه - کماندوهای زبده
• ⚔️ تمام نیروها - حمله همه‌جانبه""", chat_keypad=attack_units_keypad(target))
        
        # ===== هندلر انتخاب نیرو =====
        if btn and btn.startswith("attack_") and uid in attack_pending:
            parts = btn.split("_")
            unit_type = parts[1] if len(parts) > 1 else ""
            target_id = parts[2] if len(parts) > 2 else ""
            
            if target_id != attack_pending.get(uid):
                return
            
            target = target_id
            tgt = db.players[target]
            
            unit_map = {
                "infantry": ({"infantry": p["military"].get("infantry", 0)}, "سربازان پیاده"),
                "tank": ({"tank": p["military"].get("tank", 0), "artillery": p["military"].get("artillery", 0)}, "تانک‌ها و توپخانه"),
                "jet": ({"jet": p["military"].get("jet", 0), "bomber": p["military"].get("bomber", 0), "drone": p["military"].get("drone", 0)}, "نیروی هوایی"),
                "special": ({"special_forces": p["military"].get("special_forces", 0)}, "نیروهای ویژه"),
                "all": (p["military"].copy(), "تمام نیروها")
            }
            
            if unit_type not in unit_map:
                return
            
            use_units, unit_name = unit_map[unit_type]
            
            my_atk = sum(MILITARY_UNITS[u]["power"] * c for u, c in use_units.items() if u in MILITARY_UNITS and c > 0)
            tech_bonus = 1 + (p.get("tech_level", 1) - 1) * 0.1
            barracks_bonus = 1 + p.get("buildings", {}).get("barracks", 0) * 0.05
            my_atk = int(my_atk * tech_bonus * barracks_bonus)
            
            ally_bonus = 0
            for ally in p.get("allies", []):
                if ally in db.players:
                    ally_atk, _ = get_power(db.players[ally])
                    ally_bonus += int(ally_atk * 0.15)
            
            total_atk = my_atk + ally_bonus
            tgt_total = get_power(tgt)[0] + get_power(tgt)[1]
            
            p["last_war_time"] = now
            attack_pending.pop(uid, None)
            
            if total_atk > tgt_total * 1.3:
                loot = min(tgt["resources"].get("gold", 0), random.randint(500, 5000) * p["tech_level"])
                tgt["resources"]["gold"] = max(0, tgt["resources"].get("gold", 0) - loot)
                p["resources"]["gold"] += loot
                
                for u in use_units:
                    if u in p["military"]:
                        p["military"][u] = int(p["military"][u] * 0.85)
                for u in tgt["military"]:
                    tgt["military"][u] = int(tgt["military"][u] * 0.5)
                
                p["score"] += 200
                p["xp"] = p.get("xp", 0) + 50
                p["battles_won"] += 1
                p["total_battles"] += 1
                tgt["battles_lost"] += 1
                tgt["total_battles"] += 1
                
                db.save()
                db.war_logs.append({"type": "war", "attacker": p['country_name'], "defender": tgt['country_name'], "units": unit_name, "result": "victory", "loot": loot, "time": datetime.now().isoformat()})
                db.save()
                check_achievements(p, uid)
                
                await announce_victory(p, tgt, loot)
                
                try:
                    await bot.send_message(target, f"""⚠️ **کشور شما مورد حمله قرار گرفت!**

{p['country_emoji']} **{p['country_name']}** با {unit_name} به شما حمله کرد و پیروز شد!

💰 **خسارت:** {loot:,} طلا از خزانه شما به غارت رفت
💀 **تلفات ارتش:** ۵۰٪ از نیروهای شما نابود شدند

🛡️ برای دفاع بهتر در آینده، ارتش خود را تقویت کنید و با کشورهای دیگر متحد شوید.""")
                except:
                    pass
                
                return await bot.send_message(cid, f"""⚔️ **پیروزی قاطع با {unit_name}!**

💰 **غنیمت جنگی:** +{loot:,} طلا
⭐ **امتیاز:** +200
🎯 **تجربه:** +50 XP

💀 **تلفات شما:** ۱۵٪ (آسیب جزئی)
💀 **تلفات دشمن:** ۵۰٪ (شکست سنگین)

📢 نتیجه نبرد در کانال رسمی اعلام شد!""")
            
            elif total_atk > tgt_total * 0.9:
                loot = min(tgt["resources"].get("gold", 0), random.randint(200, 2000))
                tgt["resources"]["gold"] = max(0, tgt["resources"].get("gold", 0) - loot)
                p["resources"]["gold"] += loot
                
                for u in use_units:
                    if u in p["military"]:
                        p["military"][u] = int(p["military"][u] * 0.65)
                for u in tgt["military"]:
                    tgt["military"][u] = int(tgt["military"][u] * 0.7)
                
                p["score"] += 100
                p["xp"] = p.get("xp", 0) + 25
                p["battles_won"] += 1
                p["total_battles"] += 1
                tgt["battles_lost"] += 1
                tgt["total_battles"] += 1
                
                db.save()
                check_achievements(p, uid)
                
                await send_channel(f"""⚔️ **پیروزی نزدیک با {unit_name}!**

{p['country_emoji']} **{p['country_name']}** در نبردی سخت بر **{tgt['country_name']}** {tgt['country_emoji']} پیروز شد!
💰 غنیمت: {loot:,} طلا

#Victory #{p['country_name']}""")
                
                return await bot.send_message(cid, f"""⚔️ **پیروزی نزدیک با {unit_name}!**

💰 **غنیمت:** +{loot:,} طلا
⭐ **امتیاز:** +100
🎯 **تجربه:** +25 XP

⚠️ **تلفات شما:** ۳۵٪ (آسیب متوسط)
⚠️ **تلفات دشمن:** ۳۰٪

📢 نتیجه در کانال اعلام شد!""")
            
            else:
                for u in use_units:
                    if u in p["military"]:
                        p["military"][u] = int(p["military"][u] * 0.45)
                
                p["battles_lost"] += 1
                p["total_battles"] += 1
                tgt["battles_won"] += 1
                tgt["total_battles"] += 1
                tgt["score"] += 50
                
                db.save()
                
                await announce_defeat(p, tgt)
                
                try:
                    await bot.send_message(target, f"""🛡️ **دفاع موفق از کشور!**

{p['country_emoji']} **{p['country_name']}** با {unit_name} حمله کرد و شکست خورد!

⭐ **پاداش دفاع:** +۵۰ امتیاز
💀 **تلفات دشمن:** ۵۵٪ ارتش مهاجم نابود شد

🎉 به دفاع از کشورتان ادامه دهید!""")
                except:
                    pass
                
                return await bot.send_message(cid, f"""💀 **شکست در حمله با {unit_name}!**

🛡️ **{tgt['country_name']}** با موفقیت از کشورش دفاع کرد!

💀 **تلفات شما:** ۵۵٪ ارتش نابود شد
⭐ **امتیاز مدافع:** +۵۰

📢 نتیجه در کانال رسمی اعلام شد!

💡 **راهنمایی برای پیروزی در نبردهای آینده:**
• نیروهای نظامی بیشتری خریداری کنید
• سطح فناوری کشور را افزایش دهید
• با کشورهای قدرتمند متحد شوید
• قبل از حمله، از قدرت دشمن جاسوسی کنید""")
        
        # ===== هک =====
        if text.startswith("هک "):
            target = find_country_smart(text[4:].strip())
            if not target or target not in db.players or target == uid:
                return await bot.send_message(cid, "❌ **کشور مورد نظر یافت نشد!**\n\n📝 مثال صحیح: `هک آلمان`")
            
            tgt = db.players[target]
            if p.get("last_hack_time",0) + p.get("hack_cooldown",3600) > now:
                remaining = (p["last_hack_time"] + p["hack_cooldown"]) - now
                return await bot.send_message(cid, f"⏳ **زمان حمله سایبری فرا نرسیده!**\n\nتیم هکری شما به {remaining // 60} دقیقه استراحت نیاز دارد.")
            if p["resources"].get("gold",0) < 2000:
                return await bot.send_message(cid, "❌ **بودجه کافی نیست!**\n\nبرای عملیات هک به ۲,۰۰۰ طلا نیاز دارید. از بازار طلا بخرید یا منتظر درآمد دوره‌ای باشید.")
            
            p["resources"]["gold"] -= 2000
            p["last_hack_time"] = now
            p["spy_missions"] = p.get("spy_missions",0) + 1
            
            chance = 0.3 + p["buildings"].get("spy_agency",0)*0.1
            if random.random() < chance:
                res = random.choice(["gold","technology","uranium","diamond"])
                amt = int(tgt["resources"].get(res,0) * random.uniform(0.1,0.3))
                if amt > 0:
                    tgt["resources"][res] -= amt
                    p["resources"][res] = p["resources"].get(res,0) + amt
                p["spy_success"] = p.get("spy_success",0) + 1
                p["score"] += 100
                p["xp"] = p.get("xp",0) + 30
                db.save()
                check_achievements(p, uid)
                return await bot.send_message(cid, f"""💀 **عملیات هک موفقیت‌آمیز بود!**

💰 **منبع دزدیده شده:** {amt:,} {RESOURCES[res]['emoji']} {RESOURCES[res]['name']}
⭐ **امتیاز:** +100
🎯 **تجربه:** +30 XP

🔓 تیم هکری شما با موفقیت به سیستم‌های امنیتی دشمن نفوذ کرد و منابع ارزشمندی را به سرقت برد!""")
            db.save()
            return await bot.send_message(cid, """💀 **عملیات هک ناموفق بود!**

🔒 سیستم امنیتی دشمن قوی‌تر از آن بود که بتوانید نفوذ کنید.
💡 **راهنمایی:** سازمان جاسوسی خود را ارتقا دهید تا شانس موفقیت در عملیات‌های بعدی افزایش یابد.""")
        
        # ===== جاسوس =====
        if text.startswith("جاسوس "):
            target = find_country_smart(text[7:].strip())
            if not target or target not in db.players or target == uid:
                return await bot.send_message(cid, "❌ **کشور مورد نظر یافت نشد!**\n\n📝 مثال صحیح: `جاسوس آلمان`")
            
            tgt = db.players[target]
            atk, df = get_power(tgt)
            p["spy_missions"] = p.get("spy_missions",0) + 1
            
            if random.random() < 0.3 * (1 + p["buildings"].get("spy_agency",0)*0.3):
                p["spy_success"] = p.get("spy_success",0) + 1
                db.save()
                check_achievements(p, uid)
                return await bot.send_message(cid, f"""🕵️ **گزارش جاسوسی از {tgt['country_emoji']} {tgt['country_name']}:**

📊 **اطلاعات نظامی:**
⚔️ قدرت حمله: {atk:,}
🛡️ قدرت دفاع: {df:,}
👥 کل نیروها: {sum(tgt['military'].values())} واحد

💰 **منابع اقتصادی:**
🥇 طلا: {tgt['resources'].get('gold', 0):,}
🛢️ نفت: {tgt['resources'].get('oil', 0):,}
☢️ اورانیوم: {tgt['resources'].get('uranium', 0):,}

🔬 سطح فناوری: {tgt.get('tech_level', 1)}
⭐ امتیاز: {tgt.get('score', 0):,}

{'─'*40}
📋 این اطلاعات فوق‌محرمانه است! با آگاهی از قدرت دشمن، استراتژی حمله خود را تنظیم کنید.""")
            db.save()
            return await bot.send_message(cid, """❌ **جاسوس شما لو رفت!**

ماموریت جاسوسی با شکست مواجه شد و جاسوس شما توسط نیروهای امنیتی دشمن دستگیر شد.
💡 **راهنمایی:** سازمان جاسوسی خود را ارتقا دهید تا شانس موفقیت در ماموریت‌های بعدی افزایش یابد.""")

        # ===== منوی دیپلماسی =====
        if btn == "diplomacy_menu":
            allies = p.get("allies", [])
            ally_list = ""
            if allies:
                for ally_uid in allies[:4]:
                    if ally_uid in db.players:
                        ally = db.players[ally_uid]
                        on = "🟢" if ally.get("online") else "⚪"
                        lock = ""
                        if ally_uid in p.get("alliance_lock", {}) and p["alliance_lock"][ally_uid] > now:
                            remaining = (p["alliance_lock"][ally_uid] - now) // 3600
                            lock = f" 🔒{remaining}h"
                        ally_list += f"{ally['country_emoji']} {ally['country_name']} {on}{lock}\n"
            else:
                ally_list = "هیچ متحدی ندارید\n"
            
            return await bot.send_message(cid, f"""🤝 **دیپلماسی**

🤝 **متحدان ({len(allies)}/4):**
{ally_list}
⚔️ **جنگ‌های فعال:** {len(p.get('wars',[]))}

📥 **درخواست‌های دریافتی:**
• درخواست‌های اتحاد در انتظار تأیید
• اعلام جنگ‌های جدید

💬 **چت با متحدان** - گفتگو با هم‌پیمانان

📝 **دستورات دیپلماتیک:**
`اتحاد [نام]` - ارسال درخواست اتحاد
`لغو اتحاد [نام]` - پایان اتحاد (بعد از ۲۴h)
`جنگ [نام]` - اعلام جنگ رسمی
`صلح [نام]` - پایان جنگ""", chat_keypad=diplomacy_menu_keypad())
        
        # ===== چت با متحدان =====
        if btn == "ally_chat_menu":
            allies = p.get("allies", [])
            if not allies:
                return await bot.send_message(cid, """❌ **شما هیچ متحدی ندارید!**

برای استفاده از چت متحدان، ابتدا باید با کشورهای دیگر متحد شوید.

📝 برای اتحاد: `اتحاد [نام کشور]`
💡 پس از اتحاد، می‌توانید با متحدان خود چت کنید و استراتژی‌های مشترک طراحی کنید.""", chat_keypad=diplomacy_menu_keypad())
            
            ally_chat_key = get_ally_chat_key(uid, allies)
            chat_history = db.ally_chat.get(ally_chat_key, [])
            
            msg = f"💬 **چت با متحدان ({len(allies)} کشور)**\n\n"
            
            if chat_history:
                msg += "📜 **آخرین پیام‌ها:**\n\n"
                for msg_entry in chat_history[-10:]:
                    sender_emoji = msg_entry.get("emoji", "")
                    sender_name = msg_entry.get("name", "نامشخص")
                    msg_text = msg_entry.get("text", "")
                    msg_time = msg_entry.get("time", "")[:16]
                    msg += f"{sender_emoji} **{sender_name}**: {msg_text}\n🕐 {msg_time}\n\n"
            else:
                msg += "💬 **هنوز پیامی ارسال نشده!**\nاولین پیام را شما بفرستید و بحث را شروع کنید.\n\n"
            
            msg += """{'─'*40}
📝 **برای ارسال پیام:** `متحد [متن پیام]`
💡 **مثال:** `متحد سلام دوستان! آماده حمله هستید؟`
📋 **نکته:** پیام‌ها بین همه متحدان به اشتراک گذاشته می‌شود."""
            
            kb = ChatKeypadBuilder()
            kb.row(kb.button("back", "🔙 بازگشت"))
            return await bot.send_message(cid, msg, chat_keypad=kb.build())
        
        # ===== ارسال پیام به متحدان =====
        if text.startswith("متحد "):
            ally_msg = text[5:].strip()
            if len(ally_msg) > 300:
                return await bot.send_message(cid, "❌ **حداکثر ۳۰۰ کاراکتر!**\n\nپیام شما طولانی‌تر از حد مجاز است. لطفاً کوتاه‌تر بنویسید.")
            
            allies = p.get("allies", [])
            if not allies:
                return await bot.send_message(cid, "❌ **شما هیچ متحدی ندارید!**\n\nابتدا با کشورهای دیگر متحد شوید تا بتوانید از چت استفاده کنید.")
            
            # ذخیره پیام در تاریخچه
            ally_chat_key = get_ally_chat_key(uid, allies)
            if ally_chat_key not in db.ally_chat:
                db.ally_chat[ally_chat_key] = []
            
            msg_entry = {
                "user_id": uid,
                "emoji": p["country_emoji"],
                "name": p["country_name"],
                "text": ally_msg,
                "time": datetime.now().isoformat()
            }
            db.ally_chat[ally_chat_key].append(msg_entry)
            
            if len(db.ally_chat[ally_chat_key]) > 50:
                db.ally_chat[ally_chat_key] = db.ally_chat[ally_chat_key][-50:]
            
            db.save()
            
            # ارسال به متحدان
            sent = 0
            for ally_uid in allies:
                if ally_uid != uid:
                    try:
                        await bot.send_message(ally_uid, f"💬 **{p['country_emoji']} {p['country_name']}** (متحد):\n\n{ally_msg}\n\n{'─'*30}\n💡 پاسخ: `متحد [متن]`")
                        sent += 1
                    except Exception as e:
                        print(f"Cannot send to ally {ally_uid}: {e}")
            
            if sent == 0:
                note = "\n\n⚠️ **توجه:** هیچیک از متحدان شما در حال حاضر آنلاین نیستند یا ربات را استارت نکرده‌اند. پیام در تاریخچه ذخیره شد."
            else:
                note = ""
            
            return await bot.send_message(cid, f"✅ **پیام شما به {sent} متحد ارسال شد!**\n\n📝 پیام: {ally_msg[:50]}{'...' if len(ally_msg) > 50 else ''}{note}")
        
        # ===== درخواست‌های اتحاد =====
        if btn == "alliance_inbox":
            requests = db.alliance_requests.get(uid, [])
            if not requests:
                return await bot.send_message(cid, """📥 **هیچ درخواست اتحادی دریافت نکرده‌اید!**

برای اتحاد با یک کشور، از دستور `اتحاد [نام کشور]` استفاده کنید.
منتظر بمانید تا دیگران نیز به شما درخواست اتحاد بدهند.""", chat_keypad=diplomacy_menu_keypad())
            
            await bot.send_message(cid, f"📥 **{len(requests)} درخواست اتحاد دریافتی:**")
            
            for req_uid in requests[:5]:
                if req_uid in db.players:
                    req_p = db.players[req_uid]
                    kb = ChatKeypadBuilder()
                    kb.row(
                        kb.button(f"accept_alliance_{req_uid}", "✅ قبول اتحاد"),
                        kb.button(f"reject_alliance_{req_uid}", "❌ رد اتحاد")
                    )
                    await bot.send_message(cid, f"""🤝 **درخواست اتحاد جدید**

{req_p['country_emoji']} **{req_p['country_name']}** می‌خواهد با شما متحد شود!

📊 **اطلاعات کشور درخواست‌کننده:**
⭐ امتیاز: {req_p.get('score', 0):,}
⚔️ قدرت حمله: {get_power(req_p)[0]:,}
🛡️ قدرت دفاع: {get_power(req_p)[1]:,}
👥 متحدان فعلی: {len(req_p.get('allies', []))}/4

🤝 با پذیرش این اتحاد، در نبردها ۱۵٪ از قدرت یکدیگر بهره‌مند می‌شوید.
💬 امکان چت با متحدان نیز فعال خواهد شد.""", chat_keypad=kb.build())
            
            if len(requests) > 5:
                await bot.send_message(cid, f"... و {len(requests)-5} درخواست دیگر")
            return
        
        # ===== درخواست‌های جنگ =====
        if btn == "war_inbox":
            declarations = db.war_declarations.get(uid, [])
            if not declarations:
                return await bot.send_message(cid, """⚔️ **هیچ اعلام جنگی دریافت نکرده‌اید!**

برای اعلام جنگ به یک کشور، از دستور `جنگ [نام کشور]` استفاده کنید.
منتظر بمانید تا دیگران نیز به شما اعلام جنگ کنند.""", chat_keypad=diplomacy_menu_keypad())
            
            await bot.send_message(cid, f"⚔️ **{len(declarations)} اعلام جنگ دریافتی:**")
            
            for dec_uid in declarations[:5]:
                if dec_uid in db.players:
                    dec_p = db.players[dec_uid]
                    kb = ChatKeypadBuilder()
                    kb.row(
                        kb.button(f"accept_war_{dec_uid}", "⚔️ قبول جنگ"),
                        kb.button(f"reject_war_{dec_uid}", "🕊️ رد جنگ")
                    )
                    await bot.send_message(cid, f"""⚔️ **اعلام جنگ جدید**

{dec_p['country_emoji']} **{dec_p['country_name']}** به شما اعلام جنگ کرده است!

📊 **قدرت نظامی دشمن:**
⚔️ حمله: {get_power(dec_p)[0]:,}
🛡️ دفاع: {get_power(dec_p)[1]:,}
⭐ امتیاز: {dec_p.get('score', 0):,}

⚠️ با پذیرش جنگ، وارد نبرد رسمی با این کشور می‌شوید.""", chat_keypad=kb.build())
            
            if len(declarations) > 5:
                await bot.send_message(cid, f"... و {len(declarations)-5} اعلام جنگ دیگر")
            return
        
        # ===== اتحاد با نمایش لیست کشورها =====
        if text.startswith("اتحاد "):
            target_name = text[6:].strip()
            target = find_country_smart(target_name)
            
            if not target or target not in db.players:
                # ⭐ نمایش لیست کامل کشورهای هم‌سرور با وضعیت آنلاین
                server_list = []
                for uid_pl, pl in db.players.items():
                    if uid_pl != uid and pl.get("server_id") == p.get("server_id"):
                        on_status = "🟢 آنلاین" if pl.get("online") else "⚪ آفلاین"
                        prot_status = " 🛡️" if is_protected(pl) else ""
                        server_list.append(f"{pl['country_emoji']} **{pl['country_name']}** {on_status}{prot_status}")
                
                if server_list:
                    hint = "\n".join(server_list[:15])
                    msg = f"""❌ **کشور '{target_name}' یافت نشد!**

📋 **کشورهای قابل اتحاد در سرور شما ({len(server_list)} کشور):**

{hint}

📝 **برای اتحاد، نام کشور را دقیقاً بنویسید:**
`اتحاد ایران`"""
                    
                    if len(server_list) > 15:
                        msg += f"\n\n... و {len(server_list) - 15} کشور دیگر"
                else:
                    msg = f"❌ **کشور '{target_name}' یافت نشد!**\n\nهیچ کشور دیگری در سرور شما وجود ندارد."
                
                return await bot.send_message(cid, msg)
            
            if target == uid:
                return await bot.send_message(cid, "❌ **نمی‌توانید با خودتان متحد شوید!**")
            
            tgt = db.players[target]
            
            if len(p.get("allies",[])) >= 4:
                return await bot.send_message(cid, "❌ **حداکثر ۴ متحد!**\n\nشما در حال حاضر ۴ متحد دارید و نمی‌توانید متحد جدیدی اضافه کنید.")
            if len(tgt.get("allies",[])) >= 4:
                return await bot.send_message(cid, "❌ **طرف مقابل ۴ متحد دارد!**\n\nاین کشور در حال حاضر با ۴ کشور متحد است و نمی‌تواند متحد جدیدی بپذیرد.")
            if target in p.get("allies",[]):
                return await bot.send_message(cid, "❌ **شما قبلاً با این کشور متحد هستید!**")
            
            db.alliance_requests[target] = db.alliance_requests.get(target, [])
            if uid not in db.alliance_requests[target]:
                db.alliance_requests[target].append(uid)
                db.save()
                
                try:
                    await bot.send_message(target, f"""🤝 **درخواست اتحاد جدید!**

{p['country_emoji']} **{p['country_name']}** می‌خواهد با شما متحد شود!

📊 **اطلاعات کشور درخواست‌کننده:**
⭐ امتیاز: {p.get('score', 0):,}
⚔️ قدرت حمله: {get_power(p)[0]:,}
🛡️ قدرت دفاع: {get_power(p)[1]:,}
👥 متحدان فعلی: {len(p.get('allies', []))}/4

🤝 با پذیرش این اتحاد، در نبردها ۱۵٪ از قدرت یکدیگر بهره‌مند می‌شوید.
💬 امکان چت با متحدان نیز فعال خواهد شد.

📥 برای مشاهده و پاسخ: **منوی دیپلماسی → درخواست‌های اتحاد**""")
                except:
                    pass
                
                return await bot.send_message(cid, f"""📤 **درخواست اتحاد ارسال شد!**

درخواست اتحاد شما برای **{tgt['country_emoji']} {tgt['country_name']}** ارسال گردید.
⏳ منتظر تأیید طرف مقابل باشید...

💡 **نکته:** طرف مقابل باید از منوی دیپلماسی، درخواست شما را تأیید کند.""")
        
        # ===== لغو اتحاد =====
        if text.startswith("لغو اتحاد "):
            target_name = text[8:].strip()
            target = find_country_smart(target_name)
            
            if not target or target not in db.players:
                return await bot.send_message(cid, f"❌ **کشور '{target_name}' یافت نشد!**\n\n📝 مثال: `لغو اتحاد آلمان`")
            
            if target not in p.get("allies", []):
                return await bot.send_message(cid, "❌ **شما با این کشور متحد نیستید!**")
            
            tgt = db.players[target]
            
            # چک قفل اتحاد
            alliance_lock = p.get("alliance_lock", {})
            if target in alliance_lock:
                lock_time = alliance_lock[target]
                if lock_time > now:
                    remaining_hours = (lock_time - now) // 3600
                    remaining_minutes = ((lock_time - now) % 3600) // 60
                    return await bot.send_message(cid, f"🔒 **اتحاد قفل است!**\n\nشما باید {remaining_hours} ساعت و {remaining_minutes} دقیقه دیگر صبر کنید تا بتوانید این اتحاد را لغو کنید.\n\n⏰ زمان آزادسازی: {datetime.fromtimestamp(lock_time).strftime('%H:%M:%S')}")
            
            # لغو اتحاد
            p["allies"].remove(target)
            tgt["allies"].remove(uid)
            
            # پاک کردن قفل
            if target in p.get("alliance_lock", {}):
                del p["alliance_lock"][target]
            if uid in tgt.get("alliance_lock", {}):
                del tgt["alliance_lock"][uid]
            
            db.save()
            
            await send_channel(f"""💔 **اتحاد لغو شد!**

{p['country_emoji']} **{p['country_name']}** و **{tgt['country_name']}** {tgt['country_emoji']} به اتحاد خود پایان دادند!

⚔️ این دو کشور دیگر در نبردها از یکدیگر حمایت نخواهند کرد.

#BrokenAlliance #{p['country_name']} #{tgt['country_name']}""")
            
            try:
                await bot.send_message(target, f"""💔 **اتحاد لغو شد!**

{p['country_emoji']} **{p['country_name']}** اتحاد با شما را لغو کرد.

⚔️ شما دیگر در نبردها از این کشور حمایت دریافت نمی‌کنید.
💡 می‌توانید با کشورهای دیگر متحد شوید: `اتحاد [نام کشور]`""")
            except:
                pass
            
            return await bot.send_message(cid, f"""💔 **اتحاد با {tgt['country_name']} لغو شد!**

⚔️ شما دیگر در نبردها از این کشور حمایت دریافت نمی‌کنید.
📢 خبر لغو اتحاد در کانال منتشر شد.""")

        # ===== قبول اتحاد =====
        if btn and btn.startswith("accept_alliance_"):
            requester_uid = btn.replace("accept_alliance_", "")
            
            if uid not in db.alliance_requests or requester_uid not in db.alliance_requests.get(uid, []):
                return await bot.send_message(cid, "❌ **این درخواست اتحاد منقضی شده یا وجود ندارد!**", chat_keypad=diplomacy_menu_keypad())
            
            if requester_uid not in db.players:
                return await bot.send_message(cid, "❌ **کشور درخواست‌کننده دیگر وجود ندارد!**", chat_keypad=diplomacy_menu_keypad())
            
            requester = db.players[requester_uid]
            requester = ensure_player_fields(requester)
            
            if len(p.get("allies",[])) >= 4:
                return await bot.send_message(cid, "❌ **شما ۴ متحد دارید!**", chat_keypad=diplomacy_menu_keypad())
            if len(requester.get("allies",[])) >= 4:
                return await bot.send_message(cid, "❌ **طرف مقابل ۴ متحد دارد!**", chat_keypad=diplomacy_menu_keypad())
            
            p.setdefault("alliance_lock", {})
            requester.setdefault("alliance_lock", {})
            
            p.setdefault("allies",[]).append(requester_uid)
            requester.setdefault("allies",[]).append(uid)
            
            lock_time = now + 86400
            p["alliance_lock"][requester_uid] = lock_time
            requester["alliance_lock"][uid] = lock_time
            
            db.alliance_requests[uid].remove(requester_uid)
            
            db.save()
            await announce_alliance(p, requester)
            
            try:
                await bot.send_message(requester_uid, f"""🤝 **اتحاد پذیرفته شد!**

{p['country_emoji']} **{p['country_name']}** درخواست اتحاد شما را پذیرفت!

🎉 اکنون شما متحد یکدیگر هستید.
🛡️ در نبردهای آینده ۱۵٪ از قدرت متحدتان به شما اضافه می‌شود.
💬 چت با متحدان برای شما فعال شد.
🔒 این اتحاد تا ۲۴ ساعت قابل لغو نیست.

📢 خبر اتحاد در کانال رسمی منتشر شد!""")
            except:
                pass
            
            return await bot.send_message(cid, f"""🤝 **اتحاد برقرار شد!**

شما اکنون با {requester['country_emoji']} **{requester['country_name']}** متحد هستید.

🛡️ در نبردها ۱۵٪ از قدرت متحدتان به شما اضافه می‌شود.
💬 چت با متحدان برای شما فعال شد.
🔒 این اتحاد تا ۲۴ ساعت قابل لغو نیست.

📢 خبر اتحاد در کانال رسمی منتشر شد!""", chat_keypad=diplomacy_menu_keypad())
        
        # ===== رد اتحاد =====
        if btn and btn.startswith("reject_alliance_"):
            requester_uid = btn.replace("reject_alliance_", "")
            
            if uid in db.alliance_requests and requester_uid in db.alliance_requests[uid]:
                db.alliance_requests[uid].remove(requester_uid)
                db.save()
            
            if requester_uid in db.players:
                try:
                    await bot.send_message(requester_uid, f"""❌ **درخواست اتحاد رد شد.**

{p['country_emoji']} **{p['country_name']}** درخواست اتحاد شما را نپذیرفت.

💡 می‌توانید با کشورهای دیگر متحد شوید.""")
                except:
                    pass
            
            return await bot.send_message(cid, "❌ **درخواست اتحاد رد شد!**\n\nبه منوی دیپلماسی بازگردانده شدید.", chat_keypad=diplomacy_menu_keypad())
        
        # ===== جنگ =====
        if text.startswith("جنگ "):
            target_name = text[4:].strip()
            target = find_country_smart(target_name)
            
            if not target or target not in db.players or target == uid:
                return await bot.send_message(cid, f"❌ **کشور مورد نظر یافت نشد!**\n\n📝 مثال صحیح: `جنگ آلمان`")
            
            tgt = db.players[target]
            
            if target in p.get("wars",[]):
                return await bot.send_message(cid, "❌ **شما قبلاً با این کشور در جنگ هستید!**")
            
            db.war_declarations[target] = db.war_declarations.get(target, [])
            if uid not in db.war_declarations[target]:
                db.war_declarations[target].append(uid)
                db.save()
                
                try:
                    await bot.send_message(target, f"""⚔️ **اعلام جنگ جدید!**

{p['country_emoji']} **{p['country_name']}** به شما اعلام جنگ کرد!

📊 **قدرت نظامی دشمن:**
⚔️ حمله: {get_power(p)[0]:,}
🛡️ دفاع: {get_power(p)[1]:,}
⭐ امتیاز: {p.get('score', 0):,}

⚠️ با پذیرش جنگ، وارد نبرد رسمی با این کشور می‌شوید.

📥 **منوی دیپلماسی → اعلام جنگ‌های دریافتی**""")
                except:
                    pass
                
                return await bot.send_message(cid, f"""⚔️ **اعلام جنگ ارسال شد!**

اعلان جنگ شما به **{tgt['country_emoji']} {tgt['country_name']}** ارسال گردید.
⏳ منتظر پاسخ طرف مقابل باشید...

💡 طرف مقابل باید از منوی دیپلماسی پاسخ دهد.""")
        
        # ===== قبول جنگ =====
        if btn and btn.startswith("accept_war_"):
            declarer_uid = btn.replace("accept_war_", "")
            if declarer_uid in db.players and uid in db.players:
                declarer = db.players[declarer_uid]
                
                p.setdefault("wars",[]).append(declarer_uid)
                declarer.setdefault("wars",[]).append(uid)
                
                if uid in db.war_declarations and declarer_uid in db.war_declarations[uid]:
                    db.war_declarations[uid].remove(declarer_uid)
                
                db.save()
                await announce_war(declarer, p)
                
                try:
                    await bot.send_message(declarer_uid, f"""⚔️ **جنگ آغاز شد!**

{p['country_emoji']} **{p['country_name']}** اعلام جنگ شما را پذیرفت!

🔥 اکنون در وضعیت جنگی با این کشور هستید.
⚔️ می‌توانید با دستور `حمله {p['country_name']}` به آنها حمله کنید.

📢 خبر جنگ در کانال رسمی منتشر شد!""")
                except:
                    pass
                
                return await bot.send_message(cid, f"""⚔️ **جنگ با {declarer['country_name']} آغاز شد!**

🔥 شما اکنون در وضعیت جنگی با {declarer['country_emoji']} **{declarer['country_name']}** هستید.

⚔️ با دستور `حمله {declarer['country_name']}` می‌توانید حمله کنید.
📢 خبر جنگ در کانال رسمی منتشر شد!""", chat_keypad=diplomacy_menu_keypad())
        
        # ===== رد جنگ =====
        if btn and btn.startswith("reject_war_"):
            declarer_uid = btn.replace("reject_war_", "")
            if uid in db.war_declarations and declarer_uid in db.war_declarations[uid]:
                db.war_declarations[uid].remove(declarer_uid)
                db.save()
            
            if declarer_uid in db.players:
                try:
                    await bot.send_message(declarer_uid, f"""🕊️ **اعلام جنگ رد شد.**

{p['country_emoji']} **{p['country_name']}** اعلام جنگ شما را نپذیرفت و خواهان صلح است.""")
                except:
                    pass
            
            return await bot.send_message(cid, "🕊️ **اعلام جنگ رد شد!**\n\nشما این اعلام جنگ را نپذیرفتید و صلح را برگزیدید.", chat_keypad=diplomacy_menu_keypad())
        
        # ===== صلح =====
        if text.startswith("صلح "):
            target = find_country_smart(text[5:].strip())
            if target and target in db.players and target in p.get("wars",[]):
                p["wars"].remove(target)
                if uid in db.players[target].get("wars",[]):
                    db.players[target]["wars"].remove(uid)
                db.save()
                await announce_peace(p, db.players[target])
                return await bot.send_message(cid, f"""🕊️ **صلح برقرار شد!**

جنگ با {db.players[target]['country_emoji']} **{db.players[target]['country_name']}** پایان یافت.

☮️ صلح و آرامش بین دو کشور برقرار گردید.
📢 خبر صلح در کانال رسمی منتشر شد!""")
        
        # ===== صرافی =====
        if btn == "exchange_menu":
            return await bot.send_message(cid, """🔄 **صرافی بین‌المللی**

در صرافی می‌توانید منابع خود را با سایر بازیکنان تبادل کنید:

📤 **ایجاد پیشنهاد** - پیشنهاد تبادل جدید ایجاد کنید
📥 **پیشنهادات دیگران** - پیشنهادات فعال را ببینید
📋 **پیشنهادات من** - مدیریت پیشنهادات خودتان

💡 **نکته:** تبادل مستقیم با سایر بازیکنان، راهی عالی برای کسب منابع مورد نیاز است!""", chat_keypad=exchange_keypad())
        
        if btn == "create_trade_offer":
            pending[uid] = "wait_trade_offer"
            return await bot.send_message(cid, """📤 **ایجاد پیشنهاد تبادل**

فرمت: `[منبع_خودی] [مقدار] [منبع_مقابل] [مقدار]`

📝 **مثال‌ها:**
`نفت 100 طلا 5000` ← شما ۱۰۰ نفت می‌دهید، ۵۰۰۰ طلا می‌خواهید
`آهن 50 غذا 200` ← شما ۵۰ آهن می‌دهید، ۲۰۰ غذا می‌خواهید
`فولاد 20 الماس 2` ← شما ۲۰ فولاد می‌دهید، ۲ الماس می‌خواهید

📋 **منابع قابل تبادل:** طلا، نفت، آهن، غذا، فولاد، الماس، اورانیوم، فناوری""", 
                chat_keypad=ChatKeypadBuilder().row(ChatKeypadBuilder().button("back", "🔙")).build())
        
        if pending.get(uid) == "wait_trade_offer" and text and not btn:
            parts = text.strip().split()
            if len(parts) >= 4:
                res_map = {RESOURCES[r]["name"]: r for r in RESOURCES}
                res_map.update({"طلا": "gold"})
                
                give_res = res_map.get(parts[0])
                try: give_amt = int(parts[1])
                except: give_amt = 0
                want_res = res_map.get(parts[2])
                try: want_amt = int(parts[3])
                except: want_amt = 0
                
                if give_res and want_res and give_amt > 0 and want_amt > 0:
                    if p["resources"].get(give_res, 0) >= give_amt:
                        p["resources"][give_res] -= give_amt
                        
                        offer = {
                            "id": len(db.trade_offers) + 1,
                            "user_id": uid,
                            "country_name": p["country_name"],
                            "country_emoji": p["country_emoji"],
                            "give_res": give_res,
                            "give_amt": give_amt,
                            "want_res": want_res,
                            "want_amt": want_amt,
                            "status": "active",
                            "time": datetime.now().isoformat()
                        }
                        db.trade_offers[str(offer["id"])] = offer
                        pending.pop(uid)
                        db.save()
                        return await bot.send_message(cid, f"""✅ **پیشنهاد تبادل ثبت شد!**

📤 شما می‌دهید: {RESOURCES[give_res]['emoji']} {give_amt:,} {RESOURCES[give_res]['name']}
📥 شما می‌خواهید: {RESOURCES[want_res]['emoji']} {want_amt:,} {RESOURCES[want_res]['name']}

⏳ منتظر بمانید تا بازیکنی پیشنهاد شما را قبول کند.""", chat_keypad=exchange_keypad())
                    else:
                        return await bot.send_message(cid, f"❌ **منبع کافی نیست!**\n\n📦 {RESOURCES[give_res]['name']} موجود: {p['resources'].get(give_res, 0):,}\n📝 نیاز: {give_amt:,}")
            
            return await bot.send_message(cid, "❌ **فرمت نادرست!**\n\n📝 مثال: `نفت 100 طلا 5000`")
        
        if btn == "view_trade_offers":
            active_offers = {k: v for k, v in db.trade_offers.items() if v.get("status") == "active" and v.get("user_id") != uid}
            if not active_offers:
                return await bot.send_message(cid, "📥 **هیچ پیشنهاد فعالی وجود ندارد!**\n\nشما می‌توانید اولین پیشنهاد را ایجاد کنید.", chat_keypad=exchange_keypad())
            
            await bot.send_message(cid, f"📥 **{len(active_offers)} پیشنهاد فعال:**")
            
            for oid, offer in list(active_offers.items())[:5]:
                kb = ChatKeypadBuilder()
                kb.row(
                    kb.button(f"accept_trade_{oid}", "✅ قبول تبادل"),
                    kb.button(f"reject_trade_{oid}", "❌ رد تبادل")
                )
                await bot.send_message(cid, f"""📤 **پیشنهاد #{offer['id']}**
{offer['country_emoji']} **{offer['country_name']}**
📤 می‌دهد: {RESOURCES[offer['give_res']]['emoji']} {offer['give_amt']:,} {RESOURCES[offer['give_res']]['name']}
📥 می‌خواهد: {RESOURCES[offer['want_res']]['emoji']} {offer['want_amt']:,} {RESOURCES[offer['want_res']]['name']}
🕐 {offer.get('time','')[:16]}""", chat_keypad=kb.build())
            
            if len(active_offers) > 5:
                await bot.send_message(cid, f"... و {len(active_offers)-5} پیشنهاد دیگر")
            return
        
        if btn == "my_trade_offers":
            my_offers = {k: v for k, v in db.trade_offers.items() if v.get("user_id") == uid}
            if not my_offers:
                return await bot.send_message(cid, "📋 **پیشنهادی ندارید!**\n\nاز دکمه «ایجاد پیشنهاد» استفاده کنید.", chat_keypad=exchange_keypad())
            
            msg = f"📋 **پیشنهادات من ({len(my_offers)}):**\n\n"
            for oid, offer in list(my_offers.items())[:5]:
                status = "✅ فعال" if offer.get("status") == "active" else "❌ انجام شده"
                msg += f"#{offer['id']} | {status}\n📤 {RESOURCES[offer['give_res']]['emoji']} {offer['give_amt']:,} ↔ 📥 {RESOURCES[offer['want_res']]['emoji']} {offer['want_amt']:,}\n\n"
            
            if len(my_offers) > 5:
                msg += f"... و {len(my_offers)-5} پیشنهاد دیگر\n"
            
            kb = ChatKeypadBuilder()
            kb.row(kb.button("cancel_trade_offers", "🗑️ لغو همه"))
            kb.row(kb.button("back", "🔙 بازگشت"))
            return await bot.send_message(cid, msg, chat_keypad=kb.build())
        
        # ===== قبول تبادل =====
        if btn and btn.startswith("accept_trade_"):
            offer_id = btn.replace("accept_trade_", "")
            offer = db.trade_offers.get(offer_id)
            
            if not offer or offer.get("status") != "active":
                return await bot.send_message(cid, "❌ **این پیشنهاد منقضی شده یا دیگر فعال نیست!**", chat_keypad=exchange_keypad())
            
            if offer.get("user_id") == uid:
                return await bot.send_message(cid, "❌ **نمی‌توانید پیشنهاد خودتان را قبول کنید!**", chat_keypad=exchange_keypad())
            
            if p["resources"].get(offer["want_res"], 0) >= offer["want_amt"]:
                p["resources"][offer["want_res"]] -= offer["want_amt"]
                p["resources"][offer["give_res"]] = p["resources"].get(offer["give_res"], 0) + offer["give_amt"]
                
                if offer["user_id"] in db.players:
                    db.players[offer["user_id"]]["resources"][offer["want_res"]] = db.players[offer["user_id"]]["resources"].get(offer["want_res"], 0) + offer["want_amt"]
                
                offer["status"] = "completed"
                db.save()
                
                try:
                    await bot.send_message(offer["user_id"], f"""✅ **پیشنهاد شما قبول شد!**

{p['country_emoji']} **{p['country_name']}** پیشنهاد تبادل شما را پذیرفت!

📥 شما دریافت کردید: {offer['want_amt']:,} {RESOURCES[offer['want_res']]['name']}""")
                except:
                    pass
                
                return await bot.send_message(cid, f"""✅ **تبادل انجام شد!**

📥 شما دریافت کردید: {RESOURCES[offer['give_res']]['emoji']} {offer['give_amt']:,} {RESOURCES[offer['give_res']]['name']}
📤 شما پرداخت کردید: {RESOURCES[offer['want_res']]['emoji']} {offer['want_amt']:,} {RESOURCES[offer['want_res']]['name']}""", chat_keypad=exchange_keypad())
            else:
                return await bot.send_message(cid, f"❌ **منبع کافی نیست!**\n\n📦 نیاز: {offer['want_amt']:,} {RESOURCES[offer['want_res']]['name']}\n📝 موجودی شما: {p['resources'].get(offer['want_res'], 0):,}", chat_keypad=exchange_keypad())
        
        # ===== رد تبادل =====
        if btn and btn.startswith("reject_trade_"):
            offer_id = btn.replace("reject_trade_", "")
            return await bot.send_message(cid, "❌ **پیشنهاد تبادل را رد کردید.**\n\nبه لیست پیشنهادات بازگردانده شدید.", chat_keypad=exchange_keypad())
        
        if btn == "cancel_trade_offers":
            for oid, offer in list(db.trade_offers.items()):
                if offer.get("user_id") == uid and offer.get("status") == "active":
                    p["resources"][offer["give_res"]] = p["resources"].get(offer["give_res"], 0) + offer["give_amt"]
                    offer["status"] = "cancelled"
            db.save()
            return await bot.send_message(cid, "🗑️ **همه پیشنهادات فعال لغو شدند.**\n\nمنابع شما برگشت داده شد.", chat_keypad=exchange_keypad())
        
        # ===== رتبه‌بندی =====
        if btn == "world_rank":
            server_id = p.get("server_id", 1)
            srv_pls = sorted([pl for pl in db.players.values() if pl.get("server_id") == server_id], key=lambda x: x.get("score", 0), reverse=True)
            rank = next((i+1 for i, pl in enumerate(srv_pls) if pl["user_id"] == uid), "?")
            msg = f"{SERVERS[server_id]['emoji']} **رتبه‌بندی {SERVERS[server_id]['name']} (سرور {server_id})**\n\n"
            for i, pl in enumerate(srv_pls[:15], 1):
                m = "🥇" if i==1 else "🥈" if i==2 else "🥉" if i==3 else f"{i}."
                atk, _ = get_power(pl)
                msg += f"{m} {pl['country_emoji']} **{pl['country_name']}** {'🟢' if pl.get('online') else '⚪'}\n💪{atk:,} | ⭐{pl['score']:,} | 🎯{pl.get('xp',0)} XP\n"
            msg += f"\n🌍 **کل بازیکنان:** {len(srv_pls)} کشور\n📍 **رتبه شما:** {rank}"
            return await bot.send_message(cid, msg, chat_keypad=main_keypad())
        
        # ===== منوهای دیگر =====
        if btn == "military_menu":
            atk, df = get_power(p)
            msg = "⚔️ **ارتش شما:**\n\n"
            has_units = False
            for unit, count in p["military"].items():
                if count > 0 and unit in MILITARY_UNITS:
                    msg += f"{MILITARY_UNITS[unit]['emoji']} **{MILITARY_UNITS[unit]['name']}:** {count:,} واحد\n"
                    has_units = True
            if not has_units:
                msg += "❌ **ارتش شما خالی است!**\n\n💡 از دکمه‌های زیر واحد نظامی بخرید.\n"
            msg += f"\n{'─'*40}\n⚔️ قدرت حمله: {atk:,}\n🛡️ قدرت دفاع: {df:,}"
            return await bot.send_message(cid, msg, chat_keypad=military_keypad())
        
        if btn and btn.startswith("buy_"):
            unit = btn.replace("buy_", "")
            if unit in MILITARY_UNITS:
                info = MILITARY_UNITS[unit]
                cost = {r: int(a * (1 - p["buildings"].get("factory",0)*0.15)) for r, a in info["cost"].items()}
                can_afford = all(p["resources"].get(r,0) >= a for r, a in cost.items())
                
                if can_afford:
                    for r, a in cost.items():
                        p["resources"][r] -= a
                    p["military"][unit] = p["military"].get(unit,0) + 1
                    p["score"] += info["power"] // 10
                    p["xp"] = p.get("xp",0) + 5
                    db.save()
                    return await bot.send_message(cid, f"✅ {info['emoji']} **{info['name']}** خریداری شد!\n📊 موجودی: {p['military'][unit]} | 🎯 +5 XP", chat_keypad=military_keypad())
                msg = "❌ **منابع کافی نیست!**\n\nبرای خرید این واحد نیاز دارید:\n"
                for r, a in cost.items():
                    msg += f"{RESOURCES[r]['emoji']} {RESOURCES[r]['name']}: {p['resources'].get(r,0):,}/{a:,}\n"
                return await bot.send_message(cid, msg)
        
        if btn == "buildings_menu":
            msg = "🔨 **ساختمان‌های شما:**\n\n"
            has_buildings = False
            for bkey, bld in BUILDINGS.items():
                level = p["buildings"].get(bkey, 0)
                if level > 0:
                    msg += f"{bld['emoji']} **{bld['name']}:** سطح {level}/{bld['max']}\n"
                    msg += f"   └ {bld['effect']}\n"
                    has_buildings = True
            if not has_buildings:
                msg += "❌ **هیچ ساختمانی نساخته‌اید!**\n\n💡 از دکمه‌های زیر ساختمان بسازید.\n"
            return await bot.send_message(cid, msg, chat_keypad=building_keypad())
        
        if btn and btn.startswith("upgrade_"):
            bkey = btn.replace("upgrade_", "")
            if bkey in BUILDINGS:
                bld = BUILDINGS[bkey]
                cur = p["buildings"].get(bkey, 0)
                if cur >= bld["max"]:
                    return await bot.send_message(cid, f"❌ **{bld['name']} به حداکثر سطح رسیده!** ({cur}/{bld['max']})")
                cost = {r: int(a*(cur+1)*2) for r, a in bld["cost"].items()}
                if all(p["resources"].get(r,0) >= a for r, a in cost.items()):
                    for r, a in cost.items():
                        p["resources"][r] -= a
                    p["buildings"][bkey] = cur + 1
                    p["score"] += 50*(cur+1)
                    p["xp"] = p.get("xp",0) + 10
                    db.save()
                    return await bot.send_message(cid, f"✅ {bld['emoji']} **{bld['name']}** سطح {cur+1}!\n🎯 +10 XP")
                msg = "❌ **منابع کافی نیست!**\n\nنیاز:\n"
                for r, a in cost.items():
                    msg += f"{RESOURCES[r]['emoji']} {RESOURCES[r]['name']}: {p['resources'].get(r,0):,}/{a:,}\n"
                return await bot.send_message(cid, msg)
        
        if btn == "market_menu":
            if not db.market_prices:
                for res in RESOURCES:
                    db.market_prices[res] = RESOURCES[res]["base_price"]
                db.save()
            msg = "💹 **بازار جهانی:**\n\n📦 **منابع شما:**\n"
            for res, amt in p["resources"].items():
                if amt > 0 and res in RESOURCES:
                    msg += f"{RESOURCES[res]['emoji']} {RESOURCES[res]['name']}: {amt:,}\n"
            msg += "\n💵 **قیمت‌های بازار:**\n"
            for res, price in list(db.market_prices.items())[:8]:
                msg += f"{RESOURCES[res]['emoji']} {RESOURCES[res]['name']}: {price:,} طلا\n"
            msg += "\n━━━━━━━━━━━━━━━━━━━━\n📝 `خرید نفت 100` | `فروش آهن 50`"
            return await bot.send_message(cid, msg)
        
        if btn == "research_menu":
            cost = p["tech_level"]*5000 + p["tech_level"]*1000
            can = p["resources"].get("gold",0) >= cost
            if can:
                msg = f"🔬 **تحقیقات علمی**\n\n📊 سطح فعلی: {p['tech_level']}\n💰 هزینه ارتقا: {cost:,} طلا\n🥇 طلای شما: {p['resources'].get('gold',0):,}\n\n✅ می‌توانید ارتقا دهید!\n📝 دستور: `ارتقا`"
            else:
                lack = cost - p["resources"].get("gold",0)
                msg = f"🔬 **تحقیقات علمی**\n\n📊 سطح فعلی: {p['tech_level']}\n💰 هزینه ارتقا: {cost:,} طلا\n🥇 طلای شما: {p['resources'].get('gold',0):,}\n\n❌ {lack:,} طلا کم دارید"
            return await bot.send_message(cid, msg)
        
        if btn == "achievements_btn":
            msg = f"🏆 **دستاوردهای {p['country_name']}:**\n\n"
            for ach_id, ach in ACHIEVEMENTS.items():
                done = ach_id in p.get("achievements", [])
                msg += f"{ach['icon']} **{ach['name']}** {'✅' if done else '🔒'}\n└ {ach['desc']}\n\n"
            msg += f"📊 **پیشرفت:** {len(p.get('achievements',[]))}/{len(ACHIEVEMENTS)} دستاورد"
            return await bot.send_message(cid, msg, chat_keypad=main_keypad())
        
        if btn == "statement_menu":
            return await bot.send_message(cid, """📜 **بیانیه‌های رسمی**

در این بخش می‌توانید بیانیه رسمی کشورتان را صادر کنید.
پس از تأیید ادمین، بیانیه در کانال رسمی منتشر خواهد شد.

📝 بیانیه شما نشان‌دهنده موضع رسمی کشورتان در جهان است.""", chat_keypad=statement_keypad())
        
        if btn == "send_statement":
            pending[uid] = "wait_statement"
            return await bot.send_message(cid, """✍️ **ارسال بیانیه**

لطفاً متن بیانیه خود را بنویسید و ارسال کنید.

⚠️ **محدودیت:** حداکثر ۵۰۰ کاراکتر
📝 متن شما پس از تأیید ادمین در کانال منتشر می‌شود.""", 
                chat_keypad=ChatKeypadBuilder().row(ChatKeypadBuilder().button("back", "🔙 انصراف")).build())
        
        if btn == "my_statements":
            my_stmts = [s for s in db.statements if s.get("user_id") == uid]
            if not my_stmts:
                return await bot.send_message(cid, "📜 **بیانیه‌ای ندارید!**\n\nشما هنوز هیچ بیانیه‌ای ارسال نکرده‌اید.", chat_keypad=statement_keypad())
            msg = f"📋 **بیانیه‌های شما ({len(my_stmts)}):**\n\n"
            for s in my_stmts[-5:]:
                status = "⏳ در انتظار" if s["status"]=="pending" else "✅ تأیید" if s["status"]=="approved" else "❌ رد"
                msg += f"📝 {s['text'][:50]}...\n📊 {status}\n🕐 {s.get('time','')[:10]}\n\n"
            return await bot.send_message(cid, msg, chat_keypad=statement_keypad())
        
        if btn == "daily_bonus":
            today = datetime.now().strftime("%Y-%m-%d")
            if db.daily_bonuses.get(uid) == today:
                return await bot.send_message(cid, "🎁 **پاداش امروز را قبلاً دریافت کرده‌اید!**\n\n⏰ فردا دوباره تشریف بیاورید.", chat_keypad=main_keypad())
            
            streak = db.daily_bonuses.get(f"{uid}_streak",0) + 1
            reward = min(streak*200, 3000)
            if p.get("is_vip"):
                reward = int(reward*1.5)
            p["resources"]["gold"] += reward
            p["xp"] = p.get("xp",0) + 10
            db.daily_bonuses[uid] = today
            db.daily_bonuses[f"{uid}_streak"] = streak
            db.save()
            
            bonus = ""
            if streak >= 7:
                p["resources"]["diamond"] = p["resources"].get("diamond",0) + 2
                bonus = "\n💎 **+2 الماس** (پاداش روز هفتم)"
            if p.get("is_vip"):
                bonus += "\n🌟 **VIP:** +۵۰٪ طلای بیشتر"
            
            return await bot.send_message(cid, f"""🎁 **پاداش روزانه!**

💰 **طلا:** +{reward:,}
🎯 **تجربه:** +10 XP
🔥 **روز متوالی:** {streak}{bonus}

━━━━━━━━━━━━━━━━━━━━
⏰ فردا دوباره بیایید تا پاداش بیشتری بگیرید!""", chat_keypad=main_keypad())
        
        if btn == "spy_menu":
            hack_remaining = (p.get('last_hack_time', 0) + p.get('hack_cooldown', 3600)) - now
            hack_text = '✅ آماده' if hack_remaining <= 0 else f'⏳ {hack_remaining//60}دقیقه'
            return await bot.send_message(cid, f"🕵️ **جاسوسی و هک**\n📊 {p.get('spy_missions',0)} ماموریت | ✅ {p.get('spy_success',0)} موفق\n📝 `جاسوس ایران` | `هک آلمان`\n⏳ هک: {hack_text} | 💰 ۲,۰۰۰")
        
        # ===== خرید/فروش/ارتقا =====
        if text.startswith("خرید "):
            parts = text[5:].split()
            if len(parts) >= 2:
                res_map = {RESOURCES[r]["name"]: r for r in RESOURCES}
                res = res_map.get(parts[0])
                try: amt = int(parts[1])
                except: return await bot.send_message(cid, "❌ مقدار نامعتبر!")
                if res and res in RESOURCES:
                    price = db.market_prices.get(res, RESOURCES[res]["base_price"])
                    total = price * amt
                    if p["resources"].get("gold",0) >= total:
                        p["resources"]["gold"] -= total
                        p["resources"][res] = p["resources"].get(res,0) + amt
                        p["trades_done"] = p.get("trades_done",0) + 1
                        db.save()
                        return await bot.send_message(cid, f"✅ +{amt} {RESOURCES[res]['name']}\n💰 {total:,} طلا")
            return await bot.send_message(cid, "❌ طلا کافی نیست!")
        
        if text.startswith("فروش "):
            parts = text[5:].split()
            if len(parts) >= 2:
                res_map = {RESOURCES[r]["name"]: r for r in RESOURCES}
                res = res_map.get(parts[0])
                try: amt = int(parts[1])
                except: return await bot.send_message(cid, "❌ مقدار نامعتبر!")
                if res and res in RESOURCES and p["resources"].get(res,0) >= amt:
                    price = db.market_prices.get(res, RESOURCES[res]["base_price"])
                    total = int(price * amt * 0.8)
                    p["resources"][res] -= amt
                    p["resources"]["gold"] += total
                    p["trades_done"] = p.get("trades_done",0) + 1
                    db.save()
                    return await bot.send_message(cid, f"✅ +{total:,} طلا")
            return await bot.send_message(cid, "❌ منبع کافی نیست!")
        
        if text == "ارتقا":
            cost = p["tech_level"]*5000 + p["tech_level"]*1000
            if p["resources"].get("gold",0) >= cost:
                p["resources"]["gold"] -= cost
                p["tech_level"] += 1
                p["score"] += 200
                p["xp"] = p.get("xp",0) + 20
                db.save()
                check_achievements(p, uid)
                return await bot.send_message(cid, f"🔬 سطح {p['tech_level']}!")
            return await bot.send_message(cid, f"❌ {cost:,} طلا!")
        
        if text == "راهنما":
            return await bot.send_message(cid, """🌍 **راهنمای نبرد فرماندهان**

🎮 **حمله:** `حمله ایران` ← انتخاب نوع نیرو
💀 **هک:** `هک آلمان` (کول‌داون ۱h)
🕵️ **جاسوس:** `جاسوس چین` ← گزارش قدرت
🤝 **اتحاد:** `اتحاد آلمان` (دوطرفه - تأیید در دیپلماسی)
💔 **لغو اتحاد:** `لغو اتحاد آلمان` (بعد از ۲۴h قفل)
⚔️ **جنگ:** `جنگ روسیه` (دوطرفه)
🕊️ **صلح:** `صلح روسیه`
💬 **چت متحدان:** `متحد سلام` ← گفتگو با هم‌پیمانان
💰 **خرید/فروش:** `خرید نفت 100` | `فروش آهن 50`
🔬 **ارتقا:** `ارتقا` ← افزایش فناوری
🚪 **خروج:** `خروج` ← ترک کشور
🔄 **صرافی:** تبادل منابع با بازیکنان
👑 **ادمین:** «پنل»""", chat_keypad=main_keypad())
        
        # ===== پندینگ بیانیه =====
        if pending.get(uid) == "wait_statement" and text and not btn:
            if len(text) > 500:
                return await bot.send_message(cid, "❌ ۵۰۰ کاراکتر!")
            db.statements.append({"id": len(db.statements)+1, "user_id": uid, "text": text, "status": "pending", "time": datetime.now().isoformat()})
            pending.pop(uid)
            db.save()
            for aid in ADMIN_IDS:
                try:
                    await bot.send_message(aid, f"📜 بیانیه از {p['country_emoji']} {p['country_name']}\n«پنل»")
                except: pass
            return await bot.send_message(cid, "✅ ثبت شد!", chat_keypad=main_keypad())
        
        # ===== پنل ادمین =====
        if is_admin(uid) and btn and btn.startswith("adm_"):
            if btn == "adm_stats":
                total = len(db.players)
                online = sum(1 for pl in db.players.values() if pl.get("online"))
                total_gold = sum(pl["resources"].get("gold", 0) for pl in db.players.values())
                return await bot.send_message(cid, f"📊 **آمار**\n👥 {total} (🟢{online})\n💰 {total_gold:,}\n📜 {len(db.statements)}", chat_keypad=admin_keypad())
            
            if btn == "adm_broadcast":
                pending[uid] = "wait_bc"
                return await bot.send_message(cid, "📢 متن:", chat_keypad=admin_keypad())
            if btn == "adm_channel":
                pending[uid] = "wait_ch"
                return await bot.send_message(cid, "📢 کانال:", chat_keypad=admin_keypad())
            if btn == "adm_statements":
                stmts = [s for s in db.statements if s["status"]=="pending"]
                if not stmts:
                    return await bot.send_message(cid, "📜 خالی!", chat_keypad=admin_keypad())
                for s in stmts[:5]:
                    pn = db.players[s["user_id"]]["country_name"] if s["user_id"] in db.players else "?"
                    pe = db.players[s["user_id"]]["country_emoji"] if s["user_id"] in db.players else ""
                    await bot.send_message(cid, f"📜 #{s['id']} {pe} {pn}\n{s['text']}", chat_keypad=statement_approve_keypad(s["id"]))
                return
            
            if btn == "adm_leave_requests":
                reqs = [k.replace("leave_","") for k in pending if k.startswith("leave_") and k.replace("leave_","") in db.players]
                if not reqs:
                    return await bot.send_message(cid, "🚪 خالی!", chat_keypad=admin_keypad())
                for tuid in reqs[:5]:
                    pl = db.players[tuid]
                    kb = ChatKeypadBuilder()
                    kb.row(kb.button(f"approve_leave_{tuid}","✅"), kb.button(f"reject_leave_{tuid}","❌"))
                    await bot.send_message(cid, f"🚪 {pl['country_emoji']} {pl['country_name']}\n⭐{pl.get('score',0):,}", chat_keypad=kb.build())
                return
            
            if btn == "adm_ban":
                pending[uid] = "wait_ban"
                return await bot.send_message(cid, "🚫 کشور:")
            if btn == "adm_unban":
                pending[uid] = "wait_unban"
                return await bot.send_message(cid, "✅ کشور:")
            if btn == "adm_give":
                pending[uid] = "wait_give"
                return await bot.send_message(cid, "💰 کشور مقدار:")
            if btn == "adm_reset":
                pending[uid] = "wait_reset"
                return await bot.send_message(cid, "🔄 کشور:")
            if btn == "adm_vip":
                pending[uid] = "wait_vip"
                return await bot.send_message(cid, "🌟 کشور:")
            if btn == "adm_give_all":
                for pl in db.players.values():
                    pl["resources"]["gold"] = pl["resources"].get("gold",0) + 10000
                db.save()
                return await bot.send_message(cid, "✅ ۱۰K همه!", chat_keypad=admin_keypad())
            if btn == "adm_war":
                pending[uid] = "wait_adm_war"
                return await bot.send_message(cid, "⚔️ دو کشور: ایران آلمان")
            if btn == "adm_peace":
                pending[uid] = "wait_adm_peace"
                return await bot.send_message(cid, "🕊️ دو کشور: ایران آلمان")
            if btn == "adm_un":
                return await bot.send_message(cid, "🏛️ `تایید_عضویت نام سرور` | `حذف_عضویت` | `دبیرکل`")
            if btn == "adm_rich":
                rich = sorted(db.players.items(), key=lambda x: x[1]["resources"].get("gold", 0), reverse=True)[:10]
                msg = "🏦 **ثروتمندان:**\n\n" + "\n".join(f"{i}. {pl['country_emoji']} {pl['country_name']}: {pl['resources'].get('gold',0):,}" for i, (_,pl) in enumerate(rich,1))
                return await bot.send_message(cid, msg)
            if btn == "adm_power":
                pw = sorted(db.players.items(), key=lambda x: get_power(x[1])[0], reverse=True)[:10]
                msg = "💪 **قدرتمندان:**\n\n" + "\n".join(f"{i}. {pl['country_emoji']} {pl['country_name']}: {get_power(pl)[0]:,}" for i, (_,pl) in enumerate(pw,1))
                return await bot.send_message(cid, msg)
            if btn == "adm_logs":
                logs = db.admin_logs[-20:]
                if not logs:
                    return await bot.send_message(cid, "📜 خالی!")
                return await bot.send_message(cid, "📜 **لاگ:**\n\n" + "\n".join(f"• {l['action']} | {l['time'][:16]}" for l in logs))
            if btn == "adm_players":
                msg = f"👥 **{len(db.players)}:**\n\n"
                for uid_pl, pl in list(db.players.items())[:20]:
                    atk, _ = get_power(pl)
                    msg += f"{pl['country_emoji']} {pl['country_name']} | 💪{atk:,}\n"
                return await bot.send_message(cid, msg)
            if btn == "adm_event":
                event_name = random.choice(list(GLOBAL_EVENTS.keys()))
                event_desc = GLOBAL_EVENTS[event_name]
                db.global_events["active"] = event_name
                db.global_events["until"] = int(time.time()) + 1800
                db.save()
                await announce_global_event(event_name, event_desc)
                return await bot.send_message(cid, f"🌍 **{event_name}**\n\n{event_desc}", chat_keypad=admin_keypad())
        
        # ===== پندینگ‌های ادمین =====
        if is_admin(uid) and pending.get(uid) == "wait_bc" and text:
            pending.pop(uid)
            sent = 0
            for cid_s in db.chat_ids:
                try:
                    await bot.send_message(cid_s, f"📢 **مدیریت:**\n\n{text}")
                    sent += 1
                    await asyncio.sleep(0.3)
                except: pass
            return await bot.send_message(cid, f"✅ {sent} نفر")
        
        if is_admin(uid) and pending.get(uid) == "wait_ch" and text:
            pending.pop(uid)
            await send_channel(f"📢 **اعلامیه:**\n\n{text}")
            return await bot.send_message(cid, "✅ کانال")
        
        if is_admin(uid) and pending.get(uid) == "wait_adm_war" and text:
            parts = text.strip().split()
            if len(parts) >= 2:
                p1 = find_country_smart(parts[0])
                p2 = find_country_smart(parts[1])
                if p1 and p2 and p1 in db.players and p2 in db.players:
                    await announce_war(db.players[p1], db.players[p2])
                    pending.pop(uid)
                    return await bot.send_message(cid, f"⚔️ {db.players[p1]['country_name']} vs {db.players[p2]['country_name']}")
        
        if is_admin(uid) and pending.get(uid) == "wait_adm_peace" and text:
            parts = text.strip().split()
            if len(parts) >= 2:
                p1 = find_country_smart(parts[0])
                p2 = find_country_smart(parts[1])
                if p1 and p2 and p1 in db.players and p2 in db.players:
                    pl1, pl2 = db.players[p1], db.players[p2]
                    if p2 in pl1.get("wars",[]): pl1["wars"].remove(p2)
                    if p1 in pl2.get("wars",[]): pl2["wars"].remove(p1)
                    pending.pop(uid)
                    db.save()
                    return await bot.send_message(cid, f"🕊️ {pl1['country_name']} & {pl2['country_name']}")
        
        for act in ["wait_ban","wait_unban","wait_reset","wait_vip"]:
            if is_admin(uid) and pending.get(uid) == act and text:
                target = find_country_smart(text.strip())
                if target and target in db.players:
                    if act == "wait_ban" and target not in db.banned:
                        db.banned.append(target)
                    elif act == "wait_unban" and target in db.banned:
                        db.banned.remove(target)
                    elif act == "wait_reset":
                        del db.players[target]
                    elif act == "wait_vip":
                        db.players[target]["is_vip"] = not db.players[target].get("is_vip",False)
                        if db.players[target]["is_vip"]:
                            db.players[target]["vip_expire"] = now + 30*86400
                    pending.pop(uid)
                    db.save()
                    return await bot.send_message(cid, "✅")
                pending.pop(uid)
                return await bot.send_message(cid, "❌")
        
        if is_admin(uid) and pending.get(uid) == "wait_give" and text:
            parts = text.split()
            if len(parts) >= 2:
                target = find_country_smart(parts[0])
                try: amt = int(parts[1])
                except: amt = 10000
                if target and target in db.players:
                    db.players[target]["resources"]["gold"] += amt
                    pending.pop(uid)
                    db.save()
                    return await bot.send_message(cid, f"✅ {amt:,} به {db.players[target]['country_name']}")
        
        if is_admin(uid) and text.startswith("تایید_عضویت "):
            parts = text[12:].split()
            if len(parts) >= 2:
                target = find_country_smart(parts[0])
                sid = int(parts[1]) if parts[1].isdigit() else 1
                if target and target in db.players:
                    un = get_un_data(sid)
                    if target not in un["members"]:
                        un["members"].append(target)
                        if target in un["join_requests"]:
                            un["join_requests"].remove(target)
                        db.players[target]["un_member"] = True
                        if not un.get("secretary_general"):
                            auto_elect_secretary_general(sid)
                        db.un_data[str(sid)] = un
                        db.save()
                        check_achievements(db.players[target], target)
                        await announce_un_member(db.players[target])
                        await bot.send_message(cid, f"✅ {db.players[target]['country_name']}")
        
        if is_admin(uid) and text.startswith("حذف_عضویت "):
            parts = text[11:].split()
            if len(parts) >= 2:
                target = find_country_smart(parts[0])
                sid = int(parts[1]) if parts[1].isdigit() else 1
                if target and target in db.players:
                    un = get_un_data(sid)
                    if target in un["members"]:
                        un["members"].remove(target)
                        db.players[target]["un_member"] = False
                        if un.get("secretary_general") == target:
                            auto_elect_secretary_general(sid)
                        db.un_data[str(sid)] = un
                        db.save()
                        await bot.send_message(cid, f"✅ حذف شد!")
        
        if is_admin(uid) and text.startswith("دبیرکل "):
            parts = text[7:].split()
            if len(parts) >= 2:
                target = find_country_smart(parts[0])
                sid = int(parts[1]) if parts[1].isdigit() else 1
                if target and target in db.players:
                    un = get_un_data(sid)
                    un["secretary_general"] = target
                    db.un_data[str(sid)] = un
                    db.save()
                    check_achievements(db.players[target], target)
                    await bot.send_message(cid, f"👑 {db.players[target]['country_name']}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

# ==================== سیستم‌های خودکار ====================
async def income_system():
    while True:
        await asyncio.sleep(180)
        for uid, p in db.players.items():
            p["resources"]["gold"] = p["resources"].get("gold", 0) + 200 + p["buildings"].get("mine", 0) * 100 + p["buildings"].get("bank", 0) * 500
            p["resources"]["food"] = p["resources"].get("food", 0) + 100 + p["buildings"].get("farm", 0) * 50
            p["resources"]["oil"] = p["resources"].get("oil", 0) + p["buildings"].get("oil_rig", 0) * 30
            if p.get("is_vip"):
                p["resources"]["gold"] = int(p["resources"]["gold"] * 1.3)
                p["resources"]["food"] = int(p["resources"]["food"] * 1.3)
            if p.get("un_member"):
                p["resources"]["gold"] = p["resources"].get("gold", 0) + 100
                p["xp"] = p.get("xp", 0) + 5
            troops = sum(p["military"].values())
            food_need = int(troops * 3 * (1 - p["buildings"].get("hospital", 0) * 0.05))
            if p["resources"].get("food", 0) >= food_need:
                p["resources"]["food"] -= food_need
            else:
                p["resources"]["food"] = 0
                if troops > 0:
                    for u in p["military"]:
                        p["military"][u] = max(0, int(p["military"][u] * 0.9))
        db.save()

async def market_system():
    while True:
        await asyncio.sleep(120)
        for res in RESOURCES:
            db.market_prices[res] = max(1, int(RESOURCES[res]["base_price"] * random.uniform(0.7, 1.5)))
        db.save()

async def online_system():
    while True:
        await asyncio.sleep(300)
        now = int(time.time())
        for p in db.players.values():
            p["online"] = (now - p.get("last_active", 0)) < 600
        db.save()

async def protection_reminder():
    while True:
        await asyncio.sleep(60)
        now = int(time.time())
        for uid, p in db.players.items():
            if 0 < p.get("newbie_protection", 0) - now <= 60:
                try:
                    await bot.send_message(uid, "⚠️ محافظت نوب تا ۱ دقیقه دیگر تمام می‌شود!")
                except: pass

async def un_auto_manage():
    while True:
        await asyncio.sleep(3600)
        for sid_str, un in db.un_data.items():
            sid = int(sid_str)
            for req in un.get("join_requests", [])[:]:
                if req in db.players and db.players[req].get("score", 0) >= 500:
                    if req not in un["members"]:
                        un["members"].append(req)
                        db.players[req]["un_member"] = True
                        check_achievements(db.players[req], req)
                    un["join_requests"].remove(req)
            if not un.get("secretary_general") or un["secretary_general"] not in db.players:
                auto_elect_secretary_general(sid)
            db.un_data[sid_str] = un
        db.save()

# ==================== اجرا ====================
async def main():
    total = sum(len(c['countries']) for c in CONTINENTS.values())
    print("=" * 70)
    print("🌍 ربات جنگ جهانی - نبرد فرماندهان V4.4 Final Ultimate")
    print("=" * 70)
    print(f"📢 کانال: {CHANNEL_ID}")
    print(f"🌍 {len(CONTINENTS)} قاره | 🏳️ {total} کشور | 🖥️ {len(SERVERS)} سرور")
    print(f"👥 {len(db.players)} بازیکن | 👑 {len(ADMIN_IDS)} ادمین")
    print("=" * 70)
    print("✅ **V4.4 - تمام امکانات:**")
    print("  ✓ لغو اتحاد با دستور `لغو اتحاد [نام]`")
    print("  ✓ لیست کشورها با وضعیت آنلاین/آفلاین")
    print("  ✓ کیپد رد تبادل در صرافی")
    print("  ✓ پیام به متحدان با send_message مستقیم")
    print("  ✓ نمایش متحدان در منوی دیپلماسی")
    print("=" * 70)
    
    await send_channel("🔄 ربات V4.4 راه‌اندازی شد! ✅")
    
    asyncio.create_task(income_system())
    asyncio.create_task(market_system())
    asyncio.create_task(online_system())
    asyncio.create_task(protection_reminder())
    asyncio.create_task(un_auto_manage())
    
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())