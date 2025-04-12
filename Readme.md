# Listmonk Bülten Oluşturucu

RSS beslemelerinden Listmonk uyumlu e-posta bültenleri oluşturan Python aracı. Gelişmiş şablonlama, izleme özellikleri ve kişiselleştirilmiş içerik desteği ile profesyonel görünümlü bültenler hazırlayın.

## Özellikler

- RSS beslemelerinden otomatik içerik çekme
- Son 30 gün içindeki yazıları tarih sırasına göre listeleme
- Listmonk uyumlu şablonlar ve değişkenler
- Çekici butonlar ve modern tasarım
- Abonelere özel kişiselleştirme desteği
- Link tıklama takibi (`@TrackLink`)
- E-posta açılma takibi (`TrackView`)
- Abonelikten çıkma bağlantıları
- Tarayıcıda görüntüleme desteği

## Kullanım

1. Projeyi klonlayın:

   ```
   git clone https://github.com/yuceltoluyag/listmonk-bulten-generator.git
   cd listmonk-bulten-generator
   ```

2. Gerekli bağımlılıkları yükleyin:

   ```
   pip install feedparser python-dateutil
   ```

3. RSS URL'nizi ayarlayın:

   ```python
   # main.py dosyasında
   rss_url = "https://sizin-siteniz.com/feed.xml"
   ```

4. Programı çalıştırın:

   ```
   python main.py
   ```

5. Oluşturulan dosyaları Listmonk'a yükleyin:
   - `aylik_bulten.html` - Ana e-posta şablonu olarak
   - `bulten_content.html` - Bir kampanya içeriği olarak
   - `bulten_template.html` - İçerik şablonu olarak

## Listmonk Entegrasyonu

Bu oluşturucu, aşağıdaki Listmonk değişkenlerini ve işlevlerini destekler:

- `{{ .Subscriber.FirstName }}`, `{{ .Subscriber.LastName }}` - Kişiselleştirme
- `{{ .Subscriber.Email }}` - Abone e-posta adresi
- `{{ .Campaign.Name }}` - Kampanya adı
- `@TrackLink` - Link tıklama takibi
- `{{ TrackView }}` - E-posta açılma takibi
- `{{ UnsubscribeURL }}` - Abonelikten çıkma bağlantısı
- `{{ MessageURL }}` - Tarayıcıda görüntüleme bağlantısı
- `{{ Date "02 Ocak 2006" }}` - Tarih formatı

## Lisans

MIT
