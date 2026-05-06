# 🛠️ التثبيت خطوة بخطوة

دليل شامل لتثبيت Epic Story Animator على جميع الأنظمة.

---

## المتطلبات الأساسية

### 1. Python 3.8+

**Windows:**
```bash
# Download from https://www.python.org/downloads/
# أثناء التثبيت، تأكد من تفعيل "Add Python to PATH"

python --version
```

**macOS:**
```bash
brew install python3
python3 --version
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
python3 --version
```

---

### 2. FFmpeg

**Windows:**
```bash
# الطريقة 1: مع Chocolatey
choco install ffmpeg

# الطريقة 2: يدويّاً من https://ffmpeg.org/download.html
# ثم أضف المسار للـ PATH

ffmpeg -version
```

**macOS:**
```bash
brew install ffmpeg
ffmpeg -version
```

**Linux:**
```bash
sudo apt-get install ffmpeg
ffmpeg -version
```

---

### 3. LaTeX/TeX (ضروري لـ Manim)

**Windows:**
```bash
# Download MiKTeX من https://miktex.org/download
# أو استخدم Chocolatey:
choco install miktex
```

**macOS:**
```bash
brew install --cask mactex
# أو أصغر:
brew install basictex
```

**Linux:**
```bash
sudo apt-get install texlive texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra
```

**تحقق من التثبيت:**
```bash
pdflatex --version
```

---

### 4. Ollama (الذكاء الاصطناعي المحلي)

**Windows & macOS:**
1. اذهب إلى https://ollama.ai
2. Download و Install
3. شغّل الـ Application

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

**تحميل نموذج:**
```bash
# Terminal منفصل
ollama pull llama2

# أو نموذج أسرع:
ollama pull mistral

# شغّل الـ server:
ollama serve
```

---

## تثبيت المشروع

### 1. Clone المستودع

```bash
git clone https://github.com/baron1996029-collab/epic-story-animator.git
cd epic-story-animator
```

### 2. إنشاء Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. تثبيت المكتبات

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**إذا حدثت مشاكل:**
```bash
# جرب التثبيت الفردي:
pip install ollama==0.1.32
pip install requests==2.31.0
pip install Pillow==10.1.0
pip install opencv-python==4.8.1.78
pip install moviepy==1.0.3
pip install numpy==1.24.3
pip install scipy==1.11.4
pip install beautifulsoup4==4.12.2
pip install lxml==4.9.3

# Manim (قد يأخذ وقتاً):
pip install manim==0.18.0
```

### 4. تحقق من التثبيت

```bash
python -c "import manim; print('✅ Manim OK')"
python -c "import moviepy; print('✅ MoviePy OK')"
python -c "import PIL; print('✅ Pillow OK')"
python -c "import requests; print('✅ Requests OK')"
```

---

## التشغيل الأول

### في نافذتي Terminal منفصلتين:

**النافذة الأولى: شغّل Ollama**
```bash
ollama serve
# يجب تشوف: Listening on 127.0.0.1:11434
```

**النافذة الثانية: شغّل البرنامج**
```bash
cd epic-story-animator
source venv/bin/activate  # أو venv\Scripts\activate على Windows
python main.py "قصة تاريخية قصيرة"
```

---

## حل المشاكل الشائعة

### ❌ `ollama: command not found`
```bash
# تأكد من التثبيت وأضف للـ PATH
# أو شغّل الـ Application GUI مباشرة
```

### ❌ `pdflatex not found`
```bash
# تثبيت LaTeX مجدداً:
# Windows: MiKTeX
# macOS: brew install basictex
# Linux: sudo apt-get install texlive-latex-extra
```

### ❌ `FFmpeg not found`
```bash
# أضفه للـ PATH أو ثبته مجدداً
ffmpeg -version  # تحقق
```

### ❌ `ConnectionError: Cannot connect to Ollama`
```bash
# تأكد أن Ollama شغال:
curl http://localhost:11434/api/tags

# إذا ما اشتغل:
ollama serve
```

### ❌ `manim: command not found`
```bash
# قد تحتاج لإعادة تشغيل terminal بعد التثبيت
# أو ثبت يدويّاً:
pip install manim --no-cache-dir
```

### ⚠️ بطء المعالجة
```bash
# جرب نموذج أخف:
ollama pull mistral  # أسرع من llama2
# وعدّل config.py:
OLLAMA_MODEL = "mistral"
```

---

## التحديثات

```bash
# لتحديث المكتبات:
pip install --upgrade -r requirements.txt

# أو مكتبة محددة:
pip install --upgrade manim
```

---

## الإزالة

```bash
# احذف المجلد:
rm -rf epic-story-animator  # macOS/Linux
rmdir /s epic-story-animator  # Windows

# أو احذف الـ virtual environment فقط:
rm -rf venv
```

---

## نصائح الأداء

1. **استخدم GPU** (إذا كان متوفراً)
   ```bash
   # NVIDIA
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

2. **قلل جودة الفيديو في التطوير**
   ```python
   # في config.py:
   MANIM_QUALITY = "low_quality"  # بدلاً من high_quality
   ```

3. **استخدم نموذج أخف**
   ```bash
   ollama pull orca-mini  # نموذج خفيف جداً
   ```

---

**استمتع بـ إنشاء الفيديوهات! 🎬**
