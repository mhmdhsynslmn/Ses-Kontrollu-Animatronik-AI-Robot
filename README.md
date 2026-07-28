# Cezeri - AI Powered Interactive Animatronic Robot

Cezeri, Raspberry Pi tabanlı, yapay zeka ve yerel ses işleme altyapısıyla entegre çalışan, sesli komutları gerçek zamanlı işleyerek yanıt veren ve animasyonel göz/kapak hareketleriyle etkileşim sağlayan interaktif bir robot asistan projesidir.

---

## 🚀 Proje Amacı ve Kapsamı

Bu proje; gömülü sistemler, gerçek zamanlı ses işleme ve yapay zeka tabanlı etkileşimleri bir araya getirerek fiziksel bir robot asistan deneyimi yaratmayı amaçlar. Sistem, kullanıcının sesli komutlarını mikrofon aracılığıyla algılar, metne dönüştürür, uygun yanıtı sesli olarak üretir ve robotun görsel durumunu asenkron bir şekilde günceller.

---

## 🛠️ Kullanılan Teknolojiler ve Donanımlar

### Donanım Bileşenleri
- Raspberry Pi: Ana kontrolcü ve işlem birimi
- PCA9685: Servo motor sürücü kartı
- Servo motorlar: Göz ve kapak hareketleri için mekanik aktüatörler
- Mikrofon: Ses giriş cihazı
- Hoparlör: Ses çıkış cihazı

### Yazılım ve Kütüphaneler
- Python
- Vosk: Yerel ses tanıma altyapısı
- gTTS: Metin tabanlı ses üretimi
- PyAudio: Ses akışı yönetimi
- FFmpeg: Ses formatı dönüşümü

---

## ⚙️ Ses Mimarisi ve Optimizasyonlar

Projede donanımsal uyumsuzlukları ve ses gecikmelerini azaltmak amacıyla hibrit bir ses yapılandırması kullanılmıştır:
- Giriş sesi: 44100 Hz örnekleme hızında yapılandırılmıştır
- Çıkış sesi: 48000 Hz örnekleme hızında çalışmaktadır
- FFmpeg aracılığıyla ses dosyaları hedef donanım hızına dönüştürülerek uyumsuzluklar azaltılmıştır

---

## 📂 Proje Yapısı

```text
Ses-Kontrollu-Animatronik-AI-Robot/
├── app.py
├── eye.py
└── README.md
```

### Ana Dosyalar
- app.py: Ses tanıma, komut işleme ve ses üretimi mantığının bulunduğu ana dosya
- eye.py: Robotun göz/kapak hareketlerini yöneten animasyon mantığı

---

## 🔧 Kullanım Mantığı

Uygulama çalıştırıldığında:
- mikrofon aracılığıyla ses kayıt almaya başlar,
- algılanan metin işlenir,
- uygun yanıt sesli olarak üretilir,
- robotun durumu göz/kapak hareketleriyle görsel olarak yansıtılır.

---

## 📌 Notlar

- Bu proje şu an temel sesli etkileşim ve animasyon mantığı üzerine kuruludur.
- İleride kamera, daha gelişmiş yapay zeka karar mekanizmaları ve daha kapsamlı robot hareket kontrolü eklenebilir.
