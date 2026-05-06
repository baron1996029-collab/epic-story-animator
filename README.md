````markdown name=README.md url=https://github.com/baron1996029-collab/epic-story-animator/blob/main/README.md
# 🎬 Epic Story Animator

**تحويل القصص التاريخية إلى فيديوهات أنيميشن سينمائية احترافية**

Convert historical stories to cinematic animated videos automatically using AI, Manim animations, and historical images.

---

## ✨ الميزات الرئيسية

- 🤖 **Ollama AI** - معالجة النص العربي وتقسيم القصة إلى مشاهد
- 🎨 **Manim** - أنيميشن رياضي واحترافي سينمائي
- 🖼️ **Wikimedia** - صور تاريخية حقيقية عالية الجودة
- 🎬 **MoviePy** - دمج احترافي مع ترانزيشنات سينمائية
- ⚡ **مجاني بالكامل** - بدون subscriptions أو APIs مدفوعة
- 🌍 **دعم عربي كامل** - معالجة النصوص والواجهات بالعربية

---

## 📋 المتطلبات

### التثبيتات الأساسية

```bash
# 1. Python 3.8+
python --version

# 2. Ollama (للذكاء الاصطناعي المحلي)
# Download from: https://ollama.ai
# بعد التثبيت:
ollama pull llama2  # أو mistral لأداء أفضل
ollama serve  # تشغيل الـ server
```

### تثبيت المشروع

```bash
# Clone the repo
git clone https://github.com/baron1996029-collab/epic-story-animator.git
cd epic-story-animator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Manim (قد يأخذ وقتاً - لازم LaTeX و FFmpeg)
# تأكد أن عندك:
# - FFmpeg: https://ffmpeg.org/download.html
# - LaTeX/MiKTeX (Windows) أو texlive (Linux/Mac)
```

---

## 🚀 طريقة الاستخدام

### البدء السريع

```bash
# تأكد أن Ollama شغال
ollama serve  # في نافذة terminal منفصلة

# بعدها، شغل البرنامج مع قصتك
python main.py "القصة اللي بدك تحولها لفيديو"
```

### مثال

```bash
python main.py "في سنة 1492، اكتشف كولومبس أمريكا. كان عنده ثلاث سفن وطاقم شجاع..."
```

### الإدخال التفاعلي

```bash
# أو بدون argument
python main.py

# بعدها أدخل القصة واضغط Enter مرتين للانتهاء
```

---

## 📁 هيكل المشروع

```
epic-story-animator/
├── main.py                 # البرنامج الرئيسي
├── config.py              # الإعدادات
├── requirements.txt       # المكتبات المطلوبة
├── modules/
│   ├── __init__.py
│   ├── ollama_processor.py    # معالجة النص مع Ollama
│   ├── scene_generator.py     # توليد الأنيميشن (Manim)
│   ├── image_processor.py     # جلب الصور التاريخية
│   └── video_composer.py      # دمج الفيديو النهائي
├── output/                # الفيديوهات المُنتجة
└── temp/                  # ملفات مؤقتة
```

---

## ⚙️ تخصيص الإعدادات

عدّل `config.py` لتغيير:

```python
# نوع النموذج (llama2, mistral, etc)
OLLAMA_MODEL = "llama2"

# جودة الفيديو
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30

# مدة الفيديو الأقصى
MAX_VIDEO_DURATION = 120  # 2 دقائق

# عدد المشاهد الأقصى
MAX_SCENES = 5

# الألوان السينمائية
PRIMARY_COLOR = "#FFD700"     # ذهبي
SECONDARY_COLOR = "#DC143C"   # قاني
ACCENT_COLOR = "#1E90FF"      # أزرق
BACKGROUND_COLOR = "#0B0014"  # بنفسجي غامق
```

---

## 🔄 خط العمل (Pipeline)

```
1️⃣ القصة النصية
        ↓
2️⃣ Ollama - تحليل وتقسيم لمشاهد
        ↓
3️⃣ Manim - توليد أنيميشنات احترافية
        ↓
4️⃣ Wikimedia - جلب صور تاريخية
        ↓
5️⃣ ImageProcessor - تحسين الصور
        ↓
6️⃣ MoviePy - دمج وإضافة ترانزيشنات
        ↓
7️⃣ الفيديو النهائي (16:9 HD)
```

---

## 🎯 أنواع الأنيميشنات المدعومة

- **historical_map** - خريطة تاريخية مع علامات
- **timeline** - خط زمني للأحداث
- **graph** - رسوم بيانية ومخططات
- **text_reveal** - عرض تدريجي للنصوص
- **image_zoom** - تكبير الصور بتأثيرات
- **transition** - انتقالات سينمائية

---

## ⚠️ استكشاف الأخطاء

### Ollama لا يعمل
```bash
# تأكد أنه شغال:
curl http://localhost:11434/api/tags

# أو شغله يدويّاً:
ollama serve
```

### Manim لا يرسم
```bash
# تأكد من LaTeX:
which pdflatex  # Linux/Mac
where pdflatex  # Windows

# أو ثبت MiKTeX/texlive
```

### FFmpeg مفقود
```bash
# Windows
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

---

## 📊 أداء متوقع

| العنصر | الوقت |
|------|------|
| معالجة النص (Ollama) | 30-60s |
| توليد مشهد واحد (Manim) | 2-5 دقائق |
| جلب الصور | 10-20s |
| دمج الفيديو | 1-3 دقائق |
| **المجموع** | **~10-20 دقيقة** |

---

## 🤝 المساهمة

Pull requests مرحب بها! للتحسينات الكبيرة، افتح issue أولاً.

---

## 📄 الترخيص

MIT License - استخدم حراً كما تشاء!

---

## 🌟 شكراً لـ

- [Ollama](https://ollama.ai) - نماذج AI محلية
- [Manim](https://github.com/3b1b/manim) - أنيميشن الرياضيات
- [MoviePy](https://zulko.github.io/moviepy/) - معالجة الفيديو
- [Wikimedia Commons](https://commons.wikimedia.org) - الصور التاريخية

---

## 💬 أسئلة شائعة

**س: هل يدعم اللغات الأخرى؟**
ج: نعم! Ollama يدعم معظم اللغات. عدّل الـ prompt في `ollama_processor.py`

**س: كم الحد الأدنى للمواصفات؟**
ج: 8GB RAM على الأقل، و GPU اختياري لكن يسرع المعالجة

**س: هل يمكن استخدام نموذج AI أخر؟**
ج: نعم! غير `OLLAMA_MODEL` في `config.py` إلى أي نموذج متاح

---

**استمتع بـ إنشاء فيديوهات مذهلة! 🎬✨**
````
