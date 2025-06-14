import os
import requests
from telegram.ext import Updater, CommandHandler

# --- CẤU HÌNH ---
API_TOKEN = os.environ.get("API_TOKEN")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ALLOWED_USER_ID = 7984610063

# --- HÀM GỌI API 1688 ---
def get_trending_items(keyword, days):
    url = "https://tmapi.top/api/ali/item-list/search"
    headers = {"Authorization": API_TOKEN}
    params = {
        "keyword": keyword,
        "sortType": "salesVolumeDesc",
        "pageSize": 50,
        "days": days,
        "page": 1
    }
    res = requests.get(url, headers=headers, params=params)
    print("Status code:", res.status_code)
    print("Content:", res.text)

    try:
        items = res.json().get("data", [])
    except Exception as e:
        print("Lỗi parse JSON:", e)
        return []

    results = []
    for item in items:
        if item.get("salesVolume", 0) >= 5000 and all(x not in item.get("title", "") for x in ["内裤", "胸罩", "袜子"]):
            results.append(item)
        if len(results) >= 10:
            break
    return results

# --- GỬI KẾT QUẢ VỀ TELEGRAM ---
def send_results(update, items):
    for item in items:
        title = item.get("title", "")
        link = item.get("itemUrl")
        img = item.get("imageList", [""])[0]
        volume = item.get("salesVolume", 0)
        price = item.get("price", "")
        msg = f"👗 <b>{title}</b>\n💰 Giá: ¥{price}\n📦 Đơn bán: {volume}\n🔗 <a href='{link}'>Xem sản phẩm</a>"
        update.message.bot.send_photo(chat_id=update.effective_chat.id, photo=img, caption=msg, parse_mode='HTML')

# --- XỬ LÝ LỆNH ---
def handle_command(keyword, days):
    def handler(update, context):
        if update.effective_user.id != ALLOWED_USER_ID:
            return update.message.reply_text("Access Denied")
        update.message.reply_text("⏳ Đang lọc sản phẩm hot...")
        items = get_trending_items(keyword, days)
        if not items:
            return update.message.reply_text("Không tìm thấy sản phẩm phù hợp.")
        send_results(update, items)
    return handler

# --- MAIN ---
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("trendhan10", handle_command("韩版 女装", 10)))
    dp.add_handler(CommandHandler("trendhan20", handle_command("韩版 女装", 20)))
    dp.add_handler(CommandHandler("trendhan30", handle_command("韩版 女装", 30)))
    dp.add_handler(CommandHandler("trendtrung10", handle_command("女装", 10)))
    dp.add_handler(CommandHandler("trendtrung20", handle_command("女装", 20)))
    dp.add_handler(CommandHandler("trendtrung30", handle_command("女装", 30)))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
