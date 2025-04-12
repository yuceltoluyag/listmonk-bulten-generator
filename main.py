import feedparser
from datetime import datetime, timedelta
import locale
from dateutil import parser

# Türkçe tarih biçimi için locale ayarını yapalım (gerekirse)
try:
    locale.setlocale(locale.LC_TIME, "tr_TR.UTF-8")
except locale.Error:
    try:
        # Windows sistemlerde farklı kodlama gerekebilir
        locale.setlocale(locale.LC_TIME, "turkish")
    except locale.Error:
        print(
            "Türkçe locale ayarı yapılamadı. Tarihler İngilizce görüntülenebilir."
        )

# Türkçe ay isimleri
TURKCE_AYLAR = {
    "January": "Ocak",
    "February": "Şubat",
    "March": "Mart",
    "April": "Nisan",
    "May": "Mayıs",
    "June": "Haziran",
    "July": "Temmuz",
    "August": "Ağustos",
    "September": "Eylül",
    "October": "Ekim",
    "November": "Kasım",
    "December": "Aralık",
}


def turkce_tarih_formatla(tarih):
    """İngilizce tarih stringini Türkçe'ye çevirir"""
    if not tarih:
        return "Tarih bilgisi bulunmuyor."

    try:
        ingilizce_tarih = tarih.strftime("%d %B %Y %H:%M")

        # Ayı Türkçe'ye çevirme
        for ing_ay, tr_ay in TURKCE_AYLAR.items():
            ingilizce_tarih = ingilizce_tarih.replace(ing_ay, tr_ay)

        return ingilizce_tarih
    except:
        return tarih  # Hata durumunda orijinali döndür


def haftalik_bulten_olustur(rss_url):
    """
    Verilen RSS URL'sinden son haftanın gönderilerini çekerek haftalık bülten oluşturur.

    Args:
        rss_url (str): RSS feed'inin URL'si.

    Returns:
        str: Haftalık bültenin metin formatındaki içeriği.
    """
    feed = feedparser.parse(rss_url)
    if feed.bozo == 1:
        return (
            f"RSS feed'i ayrıştırılırken bir hata oluştu: {feed.bozo_exception}"
        )

    # Saat dilimi bilgisi olmayan (naive) bir datetime nesnesi oluştur
    hafta_once = datetime.now().replace(tzinfo=None) - timedelta(
        days=30
    )  # 7 günden 30 güne değiştirildi

    # HTML formatında içerik oluşturmaya başlıyoruz
    bulten_icerigi = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Aylık Bülten</title>
    <style>
      body {
        background: #eee;
        font-family: Arial, sans-serif;
        font-size: 16px;
        color: #111;
      }
      header {
        border-bottom: 1px solid #ddd;
        padding-bottom: 30px;
        margin-bottom: 30px;
        text-align: center;
      }
      .container {
        background: #fff;
        width: 600px;
        margin: 0 auto;
        padding: 30px;
      }
      .content {
        padding: 10px 0;
      }
      .post {
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 1px solid #eee;
      }
      .post h2 {
        margin-top: 0;
        color: #333;
      }
      .post-meta {
        color: #777;
        font-size: 14px;
        margin-bottom: 10px;
      }
      .post-link {
        margin-bottom: 10px;
      }
      .post-summary {
        line-height: 1.6;
      }
      .btn {
        display: inline-block;
        background: #4a6fa5;
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 10px;
      }
      .btn:hover {
        background: #245091;
      }
      .subscriber-details {
        margin-top: 30px;
        padding: 15px;
        background: #f9f9f9;
        border-radius: 5px;
      }
      footer {
        text-align: center;
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #ddd;
        font-size: 14px;
        color: #777;
      }
    </style>
  </head>
  <body>
    <section class="container">
      <header>
        <h1>Aylık Bülten</h1>
        <p>{{ Date "02 January 2006" }} tarihli bülten</p>
        <!-- Listmonk şablonunda burada abonelerin ismi görünebilir -->
        <p>Merhaba {{ .Subscriber.FirstName }}!</p>
      </header>

      <div class="content">
        {{ template "content" . }}
"""

    son_haftanin_gonderileri = []
    for entry in feed.entries:
        tarih = None
        if hasattr(entry, "published"):
            tarih = parser.parse(entry.published)
        elif hasattr(entry, "updated"):
            tarih = parser.parse(entry.updated)
        elif hasattr(entry, "date"):
            tarih = parser.parse(entry.date)

        # Saat dilimi bilgisini kaldırarak karşılaştırma yapabilir hale getir
        if tarih:
            tarih = tarih.replace(tzinfo=None)

        if tarih and tarih > hafta_once:
            son_haftanin_gonderileri.append(entry)

    if not son_haftanin_gonderileri:
        return "Son bir ay içinde yeni gönderi bulunamadı."

    def tarihe_gore_sirala(gonderi):
        tarih_str = getattr(
            gonderi,
            "published",
            getattr(
                gonderi,
                "updated",
                getattr(gonderi, "date", datetime.min.isoformat()),
            ),
        )
        try:
            tarih = parser.parse(tarih_str)
            if tarih.tzinfo:  # Timezone bilgisi varsa kaldır
                tarih = tarih.replace(tzinfo=None)
            return tarih
        except:
            return datetime.min  # Hata durumunda en eski tarih

    # İçerik kısmını oluşturuyoruz
    content = ""

    for gonderi in sorted(
        son_haftanin_gonderileri, key=tarihe_gore_sirala, reverse=True
    ):
        baslik = gonderi.title
        link = gonderi.link
        ozet = getattr(gonderi, "summary", "Özet bulunmuyor.")

        tarih_bilgisi = None
        if hasattr(gonderi, "published"):
            tarih = parser.parse(gonderi.published)
            tarih_bilgisi = turkce_tarih_formatla(tarih)
        elif hasattr(gonderi, "updated"):
            tarih = parser.parse(gonderi.updated)
            tarih_bilgisi = turkce_tarih_formatla(tarih)
        elif hasattr(gonderi, "date"):
            tarih = parser.parse(gonderi.date)
            tarih_bilgisi = turkce_tarih_formatla(tarih)
        else:
            tarih_bilgisi = "Tarih bilgisi bulunmuyor."

        content += f"""
        <div class="post">
          <h2>{baslik}</h2>
          <div class="post-meta">Yayın Tarihi: {tarih_bilgisi}</div>
          <div class="post-link">Link: <a href="{{ TrackLink \"{link}\" }}">{link}</a></div>
          <div class="post-summary">{ozet}</div>
        </div>
"""

    # Şablonu tamamlayalım
    bulten_icerigi_sonu = """
      </div>

      <footer>
        <p>Bu bülten <a href="https://yuceltoluyag.dev">Yücel Toluyağ</a> tarafından gönderilmiştir.</p>
        <p>Aboneliğinizi yönetmek için <a href="{{ UnsubscribeURL }}">buraya tıklayın</a>.</p>
        {{ TrackView }}
      </footer>
    </section>
  </body>
</html>
"""

    # "content" bölümü için Listmonk şablonu
    content_template = f"""
<!-- Bülten içeriği başlangıcı -->
{content}
<!-- Bülten içeriği sonu -->
"""

    # Tam şablonu döndür
    full_template = bulten_icerigi + bulten_icerigi_sonu

    return full_template


if __name__ == "__main__":
    rss_url = "https://yuceltoluyag.dev/feeds/all.atom.xml"  # Kendi RSS URL'nizi buraya yapıştırın
    haftalik_bulten = haftalik_bulten_olustur(rss_url)

    # Listmonk şablonu içerik bölümü için ayrı bir dosya
    content_template = """
<!-- Bülten içeriği buraya gelecek -->
{% for gonderi in gonderi_listesi %}
<div class="post">
  <h2>{{ gonderi.baslik }}</h2>
  <div class="post-meta">Yayın Tarihi: {{ gonderi.tarih }}</div>
  <div class="post-link">Link: <a href="{{ TrackLink \"{{ gonderi.link }}\" }}">{{ gonderi.link }}</a></div>
  <div class="post-summary">{{ gonderi.ozet }}</div>
</div>
{% endfor %}
"""

    # Gerçek gönderilerle dolu içerik şablonu oluşturma
    real_content = ""
    son_haftanin_gonderileri = []
    feed = feedparser.parse(rss_url)
    hafta_once = datetime.now().replace(tzinfo=None) - timedelta(days=30)

    # Sıralama fonksiyonu
    def tarihe_gore_sirala(gonderi):
        tarih_str = getattr(
            gonderi,
            "published",
            getattr(
                gonderi,
                "updated",
                getattr(gonderi, "date", datetime.min.isoformat()),
            ),
        )
        try:
            tarih = parser.parse(tarih_str)
            if tarih.tzinfo:  # Timezone bilgisi varsa kaldır
                tarih = tarih.replace(tzinfo=None)
            return tarih
        except:
            return datetime.min  # Hata durumunda en eski tarih

    # Gönderileri topla
    for entry in feed.entries:
        tarih = None
        if hasattr(entry, "published"):
            tarih = parser.parse(entry.published)
        elif hasattr(entry, "updated"):
            tarih = parser.parse(entry.updated)
        elif hasattr(entry, "date"):
            tarih = parser.parse(entry.date)

        if tarih:
            tarih = tarih.replace(tzinfo=None)

        if tarih and tarih > hafta_once:
            son_haftanin_gonderileri.append(entry)

    # İçerik oluştur
    for gonderi in sorted(
        son_haftanin_gonderileri, key=tarihe_gore_sirala, reverse=True
    ):
        baslik = gonderi.title
        link = gonderi.link
        ozet = getattr(gonderi, "summary", "Özet bulunmuyor.")

        tarih_bilgisi = None
        if hasattr(gonderi, "published"):
            tarih = parser.parse(gonderi.published)
            tarih_bilgisi = turkce_tarih_formatla(tarih)
        elif hasattr(gonderi, "updated"):
            tarih = parser.parse(gonderi.updated)
            tarih_bilgisi = turkce_tarih_formatla(tarih)
        elif hasattr(gonderi, "date"):
            tarih = parser.parse(gonderi.date)
            tarih_bilgisi = turkce_tarih_formatla(tarih)
        else:
            tarih_bilgisi = "Tarih bilgisi bulunmuyor."

        real_content += f"""
<div class="post">
  <h2>{baslik}</h2>
  <div class="post-meta">Yayın Tarihi: {tarih_bilgisi}</div>
  <div class="post-summary">{ozet}</div>
  <a href="{link}@TrackLink" class="btn">Devamını Oku</a>
</div>
"""

    # Abone bilgileri bölümü ekleyelim
    real_content += """
<!-- Abone bilgileri örneği - Listmonk ile çalışacak -->
<div class="subscriber-details">
  <h3>Sevgili {{ .Subscriber.FirstName }} {{ .Subscriber.LastName }},</h3>
  <p>Bu bülteni {{ .Subscriber.Email }} adresine gönderiyoruz.</p>
  <p>{{ Date "02 Ocak 2006" }} tarihinde güncellenmiştir.</p>
  
  <p><a href="{{ MessageURL }}" style="color:#4a6fa5;">Tarayıcıda görüntüle</a> | 
  <a href="{{ UnsubscribeURL }}" style="color:#4a6fa5;">Aboneliği yönet</a></p>
</div>
"""

    # İçerik dosyasını da kaydet
    with open("bulten_content.html", "w", encoding="utf-8") as dosya:
        dosya.write(real_content)
    print("Gerçek içerik 'bulten_content.html' dosyasına kaydedildi.")

    # HTML formatında bülteni kaydet
    with open("aylik_bulten.html", "w", encoding="utf-8") as dosya:
        dosya.write(haftalik_bulten)
    print(
        "\nAylık bülten 'aylik_bulten.html' dosyasına Listmonk uyumlu şablon olarak kaydedildi."
    )

    # İsterseniz Listmonk'a yükleyebileceğiniz içerik şablonunu da kaydetmek için:
    with open("bulten_template.html", "w", encoding="utf-8") as dosya:
        dosya.write(content_template)
    print("Bülten içerik şablonu 'bulten_template.html' dosyasına kaydedildi.")
