# Listmonk Bülten Oluşturucu

RSS beslemelerinden Listmonk uyumlu e-posta bültenleri oluşturan Python aracı. Gelişmiş şablonlama, izleme özellikleri ve kişiselleştirilmiş içerik desteği ile profesyonel görünümlü bültenler hazırlayın.

![Listmonk Logo](https://listmonk.app/images/logo.svg)
![Thunderbird test](https://github.com/yuceltoluyag/listmonk-bulten-generator/blob/main/2025-04-12_06-35.png)

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
- Türkçe tarih formatı desteği

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

## Çıktı Dosyaları

Program çalıştırıldığında aşağıdaki dosyalar oluşturulur:

1. **aylik_bulten.html** - Listmonk'a yüklenebilecek ana HTML şablonu. İçerik için `{{ template "content" . }}` yer tutucusu içerir.

2. **bulten_content.html** - Gerçek içerik HTML'i. Kampanya içeriği olarak kullanılabilir.

3. **bulten_template.html** - İçerik şablonu. Listmonk'a yüklenip kampanya oluştururken seçilebilir.

## Listmonk Entegrasyonu

Bu oluşturucu, aşağıdaki Listmonk değişkenlerini ve işlevlerini destekler:

### Abone Alanları

| Değişken                      | Açıklama                                                      |
| ----------------------------- | ------------------------------------------------------------- |
| `{{ .Subscriber.UUID }}`      | Abonenin benzersiz kimliği                                    |
| `{{ .Subscriber.Email }}`     | Abone e-posta adresi                                          |
| `{{ .Subscriber.Name }}`      | Abonenin tam adı                                              |
| `{{ .Subscriber.FirstName }}` | Abonenin adı (isimden otomatik çıkarılır)                     |
| `{{ .Subscriber.LastName }}`  | Abonenin soyadı (isimden otomatik çıkarılır)                  |
| `{{ .Subscriber.Status }}`    | Abone durumu (etkin, devre dışı, kara listede)                |
| `{{ .Subscriber.Attribs }}`   | Özel nitelikler. `.Subscriber.Attribs.city` gibi erişilebilir |
| `{{ .Subscriber.CreatedAt }}` | Abonenin eklendiği zaman damgası                              |
| `{{ .Subscriber.UpdatedAt }}` | Abonenin güncellendiği zaman damgası                          |

### Kampanya Alanları

| Değişken                    | Açıklama                                |
| --------------------------- | --------------------------------------- |
| `{{ .Campaign.UUID }}`      | Kampanyanın benzersiz kimliği           |
| `{{ .Campaign.Name }}`      | Kampanyanın dahili adı                  |
| `{{ .Campaign.Subject }}`   | Kampanyanın e-posta konusu              |
| `{{ .Campaign.FromEmail }}` | Kampanyanın gönderildiği e-posta adresi |

### Fonksiyonlar

| Fonksiyon                            | Açıklama                                                                     |
| ------------------------------------ | ---------------------------------------------------------------------------- |
| `{{ Date "02 Ocak 2006" }}`          | Belirli bir format için geçerli tarih/saat yazdırır                          |
| `{{ TrackLink "https://link.com" }}` | Bir URL alır ve üzerinde bir izleme URL'si oluşturur                         |
| `https://link.com@TrackLink`         | TrackLink için kısayol. Örn: `<a href="https://link.com@TrackLink">Link</a>` |
| `{{ TrackView }}`                    | Tek bir izleme pikseli ekler                                                 |
| `{{ UnsubscribeURL }}`               | Abonelikten çıkma URL'si                                                     |
| `{{ MessageURL }}`                   | Mesajın barındırılan sürümünü görüntüleme URL'si                             |
| `{{ OptinURL }}`                     | Çift onay sayfasının URL'si                                                  |
| `{{ Safe "<!-- yorum -->" }}`        | HTML kodunu olduğu gibi ekler                                                |

## Lisans

MIT

## Yapımcı

[Yücel Toluyağ](https://yuceltoluyag.dev)
