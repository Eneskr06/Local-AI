# Local AI 🤖

Local AI, tamamen yerel olarak çalışan ve web arayüzü üzerinden yapay zeka ile sohbet etmenizi sağlayan bir Python projesidir. İnternet bağlantısı gerektirmez ve tüm işlemler bilgisayarınızda gerçekleşir.

## ✨ Özellikler

- 🔒 **Tamamen Yerel**: Tüm işlemler bilgisayarınızda gerçekleşir
- 🌐 **Web Arayüzü**: Modern ve kullanıcı dostu web tabanlı sohbet arayüzü
- 🚀 **Kolay Kurulum**: Basit komutlarla hızlı kurulum
- 💬 **Gerçek Zamanlı Sohbet**: Anlık mesajlaşma deneyimi
- 🎨 **Responsive Tasarım**: Mobil ve masaüstü uyumlu
- 🔧 **Özelleştirilebilir**: Kendi modelinizi entegre edebilirsiniz

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- En az 4GB RAM (önerilen: 8GB+)

## 🚀 Kurulum

### 1. Projeyi İndirin

```bash
git clone https://github.com/Eneskr06/Local-AI.git
cd Local-AI
```

### 2. Sanal Ortam Oluşturun (Önerilen)

```bash
python -m venv venv

# Windows için:
venv\Scripts\activate

# macOS/Linux için:
source venv/bin/activate
```

### 3. Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Uygulamayı Başlatın

```bash
python app.py
```

Uygulama başlatıldıktan sonra tarayıcınızda `http://localhost:5000` adresine giderek Local AI'yi kullanabilirsiniz.

## 📁 Proje Yapısı

```
local-ai/
├── app.py                 # Ana uygulama dosyası
├── requirements.txt       # Python bağımlılıkları
├── script.js               # CSS, JS ve diğer statik dosyalar
├── style.css
├── index.html			  # HTML şablonları
├── models/               # AI modelleri
├── .env            # Yapılandırma ayarları
└── README.md
```

## ⚙️ Yapılandırma

### Temel Ayarlar

`.env` dosyasında aşağıdaki ayarları değiştirebilirsiniz:

```python
#API Ayarları
GROQ_API_KEY=your_api_key

# Sunucu ayarları
PORT = 5000
DEBUG = True
```

## 🖥️ Kullanım

1. Uygulamayı başlattıktan sonra `http://localhost:5000` adresine gidin
2. Sohbet arayüzünde mesajınızı yazın
3. Enter tuşuna basın veya "Gönder" butonuna tıklayın
4. AI'nin yanıtını bekleyin ve sohbete devam edin

### Kısayol Tuşları

- `Enter`: Mesaj gönder
- `Shift + Enter`: Yeni satıra geç

## 🔧 Sorun Giderme

### Sık Karşılaşılan Sorunlar

**Port zaten kullanımda hatası:**
```bash
# Farklı bir port kullanın
python app.py --port 8000
```

**Model yükleme hatası:**
- Model dosyalarının doğru konumda olduğundan emin olun
- Yeterli RAM olduğunu kontrol edin
- Model formatının desteklendiğini doğrulayın

**Bağımlılık hatası:**
```bash
# Paketleri yeniden yükleyin
pip install --upgrade -r requirements.txt
```

## 🤝 Katkıda Bulunma

Bu projeye katkıda bulunmak isterseniz:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'e push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📝 Değişiklik Geçmişi

### v1.0.0
- İlk sürüm
- Temel sohbet arayüzü
- Yerel model desteği

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - UI components
- [jQuery](https://jquery.com/) - JavaScript library

## 📞 İletişim

Proje Sahibi: [Adınız]
- GitHub: [@kullaniciadi](https://github.com/Eneskr06)
- Email: enescetinoglu130@hotmail.com

Proje Linki: [https://github.com/kullaniciadi/local-ai](https://github.com/Eneskr06/Local-AI)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!