import requests
from telegram.ext import Updater, CommandHandler

# --- CẤU HÌNH ---
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VybmFtZSI6InVnenVpOTkiLCJDb21pZCI6bnVsbCwiUm9sZWlkIjpudWxsLCJpc3MiOiJ0bWFwaSIsInN1YiI6InVnenVpOTkiLCJhdWQiOlsiIl0sImlhdCI6MTc0OTgzODcwNn0.GQcqv2-ZrFmpyTSqoCvIA0BLJYuhp7-h0Ogsl7foIWs"
BOT_TOKEN = "7914664676:AAHz5a375rhGzPoxsO5VH5_Qqyz9CbKjIBg"
ALLOWED_USER_ID = 7984610063

# --- GỌI API ---
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
    try:
        res = requests.get(url, headers=headers, params=params, timeout=30)
        res.raise_for_status()
        items = res.json().get("data", [])
        results = []
        for item in items:
            if item.get("salesVolume", 0) >= 5000 and all(x not in item.get("title", "") for x in ["内裤", "胸罩", "袜子"]):
                results.append(item)
            if len(results) >= 10:
                break
        return results
    except Exception as e:
        print("Lỗi API:", e)
        return []

# --- GỬI TEXT ---
def send_results(update, items):
    for item in items:
        title = item.get("title", "Không có tiêu đề")
        link = item.get("itemUrl", "#")
        volume = item.get("salesVolume", 0)
        price = item.get("price", "N/A")
        msg = f"👗 <b>{title}</b>\n💰 Giá: ¥{price}\n📦 Đơn bán: {volume}\n🔗 <a href='{link}'>Xem sản phẩm</a>"
        try:
            update.message.reply_text(msg, parse_mode='HTML', disable_web_page_preview=True)
        except Exception as e:
            print("Lỗi gửi tin nhắn:", e)

# --- LỆNH ---
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
