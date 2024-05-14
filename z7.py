from function_read_json import *
import re

indexes = [49, 62, 151, 159, 160, 161, 189, 191, 227, 238, 241, 254, 257, 258, 259, 261, 267, 270, 272]

def clean_text(text):
    return re.sub(r'[^\w\s\u4e00-\u9fa5.,!?，。！？]', '', text)

data = read_json("concert_zh.json")
for index in indexes:
    print(index, [data[index]['int']])
    print(index, [clean_text(data[index]['int'])])
    print(data[index]['web'])
    print('---')
# for i in range(len(data)):

# from googletrans import Translator
# translator = Translator()
# import re
# import requests
# from urllib.parse import quote
#
#
# def clean_text(text):
#     # 只保留英文、數字、中文和常見中文標點符號
#     return re.sub(r'[^\w\s\u4e00-\u9fa5.,!?，。！？]', '', text)
#
#
# def translate_text(text, source_lang='zh-TW', target_lang='en'):
#     cleaned_text = clean_text(text)
#     url_encoded_text = quote(cleaned_text)
#     api_url = f"https://translation.googleapis.com/language/translate/v2?q={url_encoded_text}&source={source_lang}&target={target_lang}&key=YOUR_API_KEY"
#
#     response = requests.get(api_url)
#     if response.status_code == 200:
#         translated_text = response.json()['data']['translations'][0]['translatedText']
#         return translated_text
#     else:
#         return "Error: Unable to translate text"
#
#
# # 範例文章
# article = f"""2024 ISLANDs Music Festival\n\n 𝐍𝐨𝐯 𝟎𝟐  𝟎𝟑 , 𝐊𝐀𝐎𝐇𝐒𝐈𝐔𝐍𝐆 𝟐𝟎𝟐𝟒 𝐈𝐒𝐋𝐀𝐍𝐃𝐬𝐍𝐎𝐖 𝐎𝐍 𝐒𝐀𝐋𝐄 ! \n\n\xa0\n\n以音樂表演和市集為主軸，在為期兩天的大人慶典中\n打造民眾能悠遊其中的生活步調，與創作者們盡情展現自我的可能性的所在\n兩者至此交會，延展出無窮的生命力\n\n\xa0\n\n相關活動訊息請鎖定LA RUE 文創設計臉書粉絲專頁。\n 𝘓𝘐𝘕𝘒  httpswww.facebook.comdepuis2017\n\n\xa0\n\n節目資訊\n\n 活動名稱2024 ISLANDs Music Festival\n\n 演出日期20241102 Sat.  1103Sun.\n\n 活動地點高雄市輕軌夢時代站旁\n\n 啟售時間20240405 Fri.\n\n 主辦單位LA RUE 文創設計\n\n 購票方式KKTIX全家便利商店 FamiPort\n\xa0\n\n活動票價\n\n 單人雙日盲鳥票 NT2,600元\n\n 單人雙日早鳥票 NT2,800元\n\n 單人雙日預售票 NT3,100元\n\n 單人雙日愛心票 NT1,550元\n\n 11月02日單人單日票\xa0 NT1,800元\n\n 11月03日單人單日票\xa0 NT1,800元\n\xa0\n\n雙日票購票說明\n\n 雙日票2張為一組單人使用\n\n每按1次會顯示2張1位雙日票按2次會顯示4張2位雙日票。\n每筆訂單限購4張每位會員不限訂單數量可重複下單購買。\n2張雙日票限同1人使用，第1日入場時需出示2張票才能兌換雙日活動手環1個活動第2日憑配戴雙日手環入場即可雙日手環不得拆卸轉讓他人，請於2日活動期間妥善保管並在結束後自行拆除，若活動期間經工作人員辨識手環有明顯拆卸破壞痕跡，將禁止入場。\n\n 愛心雙日票2張為一組單人使用\n\n須具備身心障礙身份方可購買，購票前24小時請先至會員進行身份認證。\n通過身份認證之帳號，僅可購買身心障礙證明有效期限晚於活動日之票券。\n票價雙日愛心票 NT 775單日 一組為 NT1,550兩日，身心障礙者本人\n如需購買陪同票，請先線上購買雙日愛心票後，再以人工方式加購陪同票例先在KKTIX購買雙日愛心票後，再以人工方式，於上班日時間聯繫KKTIX客服告知訂單編號及要加購陪同票\n入場時需出示有效期限內之身心障礙證明正本核對，若有必要陪伴者，須一同入場恕無法單獨持票進場，以利查驗。\n進場時敬請攜帶有效證件，若有未帶證件資格不符者，屆時需以預售票價補差額入場，如非本人者等不合規定之事宜，視同放棄入場資格，不得要求退款變更。\n\n\xa0\n\n購票方式\n\nKKTIX網站購票購票流程圖示說明 請點我\n全家便利商店FamiPort購票購票流程圖示說明 請點我\n\n\xa0\n\n付款方式及期限\n\n線上信用卡刷卡\nATM虛擬帳號付款\n全家便利商店FamiPort購票付款\n\n\xa0\xa0\xa0\xa0\xa0\xa0\xa0\n\n取票方式\n\n電子票卷\n電子票券 QRCode 在哪裡？該如何使用？詳情 請點選此處\n電子票券可前往 App Store  Google Play 下載KKTIX app，入場時以行動裝置秀出QR Code或直接列印QR Code 作為入場票券掃描入場。\n全家Famiport取票手續費每筆30每次4張為限\n全家便利商店FamiPort取票說明 請點我\n選擇全家便利商店FamiPort取票請留意請勿在啟售當天於網站訂購完成後馬上至全家便利商店取票，極有可能因系統繁忙無法馬上取票，只要訂購成功票券在演出前皆可取票，請擇日再至全家便利商店取票。\n\n\xa0\n\n退票方式及規定\n根據文化部訂定藝文表演票券定型化契約應記載及不得記載事項第六項退換票機制之規定共有四種方案之退換票規定，本節目採用方案二消費者請求退換票之時限為購買票券後3日內不含購票日，購買票券後第4日起不接受退換票申請，請求退換票日期以寄達日為準，退票需酌收票面金額5手續費。\n退票規定範例如下\n202445購買，退票截止日為202448\xa0含，202449\xa0含起的郵戳退票不再受理\n若購買任何雙日票，退換票亦需將2張或4張票券辦理退票，恕不受理單張退票。\n電子票券如欲辦理退票請於退票期限內至以下連結填寫表單\n信用卡 退票申請書 _ 電子票券\n匯款 退票申請書 _ 電子票券\n實體票券退票皆需以郵寄方式退回票券，請將票券及KKTIX退票申請書以掛號方式郵寄至KKTIX票務組收  105039 臺北體育場郵局第060號信箱。\nKKTIX退票申請書信用卡刷退\nKKTIX退票申請書現金匯款\n退票方式及退款時間請詳閱\xa0KKTIX退換票規定\n\xa0\n購票方式說明\n本節目僅限已完成電子郵件地址及手機號碼驗證的KKTIX會員才能進行購票流程，且至少於啟售日前一天前完成驗證手續，請至httpskktix.comusersedit 確認是否您的電子郵件及手機號碼已經認證完畢。提醒您請勿使用YahooHotmail信箱註冊及驗證，以避免驗證信未能寄達。\n本節目網站購票僅接受已完成手機號碼及電子郵件地址驗證之會員購買，購票前請先加入會員並盡早完成"""
# translate_text(article)