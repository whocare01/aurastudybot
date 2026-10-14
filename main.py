import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==========================================
# ⚙️ বটের মূল তথ্য ও কনফিগারেশন
# ==========================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8618161307:AAEu8BTLq4hQkriopoYkV0FL56Z-xIW_i7w") # 👈 এখানে আপনার বটের টোকেন দিন

# 👈 এখানে আপনার চ্যানেল দুটির ইউজারনেম দিন (@ সহ)
CHANNEL_1 = "@aurastudyhscshop"
CHANNEL_2 = "@aurastudyfreeshop"

bot = telebot.TeleBot(BOT_TOKEN)

# ইউজার উভয় চ্যানেলে জয়েন করেছে কিনা তা চেক করার ফাংশন
def is_user_joined(user_id):
    try:
        member1 = bot.get_chat_member(CHANNEL_1, user_id)
        status1 = member1.status in ['creator', 'administrator', 'member']
        
        member2 = bot.get_chat_member(CHANNEL_2, user_id)
        status2 = member2.status in ['creator', 'administrator', 'member']
        
        return status1 and status2
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

# দুটি চ্যানেলের জন্য জয়েন বাটন তৈরি
def get_join_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("✨ Join Aura Study HSC PAID", url=f"https://t.me/{CHANNEL_1.replace('@', '')}")
    btn2 = InlineKeyboardButton("✨ Join Aura Study HSC FREE", url=f"https://t.me/{CHANNEL_2.replace('@', '')}")
    btn3 = InlineKeyboardButton("✅ Joined Both Check Now", callback_data="check_membership")
    
    markup.add(btn1, btn2, btn3)
    return markup

# জয়েন করার পর সাকসেস মেসেজ
SUCCESS_MESSAGE = (
    "💖 আমাদের AURA STUDY পরিবারের সাথে যুক্ত হওয়ার জন্য আপনাকে ধন্যবাদ। "
    "এখন আপনার যদি কোনো প্রশ্ন থেকে থাকে আপনি আমাদের এখানে জিজ্ঞাসা করতে পারেন। "
    "আমাদের কোনো অ্যাডমিন আপনাকে শীঘ্রই উত্তর দেবে। 💖"
)

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_user_joined(user_id):
        bot.send_message(message.chat.id, SUCCESS_MESSAGE)
    else:
        bot.send_message(
            message.chat.id,
            "⚠️ আপনি আমাদের চ্যানেলে যুক্ত হননি। বটটি ব্যবহার করার জন্য আপনাকে আমাদের নিচের দুটি চ্যানেলেই অবশ্যই জয়েন করতে হবে :\n\n"
            "👉 চ্যানেলে জয়েন করা শেষ হলে নিচের 'Joined Both Check Now' বাটনে ক্লিক করুন।",
            reply_markup=get_join_keyboard()
        )

# বাটন ক্লিক ভেরিফিকেশন
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def verify_button(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)

    if is_user_joined(user_id):
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=SUCCESS_MESSAGE
        )
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="❌ আপনি এখনো দুটি চ্যানেলে সম্পূর্ণভাবে জয়েন করেননি! ❌\n\n"
                 "⚠️ ওপরের লিংকে গিয়ে উভয় চ্যানেলে জয়েন করুন, তারপর আবার \"Joined Both Check Now\" বাটনে চাপ দিন। ⚠️",
            reply_markup=get_join_keyboard()
        )

# ইউজার মেসেজ পাঠালে সিম্পল একটা রিসিভ মেসেজ দেওয়ার অপশন (চাইলে রাখতে পারেন বা বাদ দিতে পারেন)
@bot.message_handler(func=lambda message: message.chat.type == 'private' and not message.text.startswith('/'))
def handle_user_message(message):
    user_id = message.from_user.id
    
    if not is_user_joined(user_id):
        bot.send_message(
            message.chat.id,
            "⚠️ আপনি আমাদের চ্যানেলে যুক্ত হননি। মেসেজ পাঠাতে আগে চ্যানেলে জয়েন করুন!",
            reply_markup=get_join_keyboard()
        )
        return

    # ইউজার মেসেজ পাঠালে এখানে আপনার ইচ্ছামমতো রেসপন্স দিতে পারবেন
    bot.send_message(message.chat.id, "✅ আপনার মেসেজটি আমরা পেয়েছি। খুব শীঘ্রই উত্তর দেওয়া হবে।")

if __name__ == '__main__':
    print("🚀 Aura Study Bot is running smoothly...")
    bot.infinity_polling()
