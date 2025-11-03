# Auto-Translation Feature - ArtScope

## 🌍 Overview
Museum staff only needs to upload descriptions in **English**. The system automatically translates to **13 languages** including Kannada, Hindi, Tamil, Telugu, and more!

---

## ✨ Supported Languages

### European Languages
- 🇬🇧 **English** (Source)
- 🇪🇸 **Spanish** (Español)
- 🇫🇷 **French** (Français)
- 🇩🇪 **German** (Deutsch)
- 🇮🇹 **Italian** (Italiano)
- 🇵🇹 **Portuguese** (Português)

### Asian Languages
- 🇨🇳 **Chinese** (中文)
- 🇯🇵 **Japanese** (日本語)
- 🇸🇦 **Arabic** (العربية)

### Indian Languages
- 🇮🇳 **Hindi** (हिंदी)
- 🇮🇳 **Kannada** (ಕನ್ನಡ)
- 🇮🇳 **Tamil** (தமிழ்)
- 🇮🇳 **Telugu** (తెలుగు)
- 🇮🇳 **Malayalam** (മലയാളം)

---

## 🚀 How It Works

### **Step 1: Museum Uploads Artifact (English Only)**
```
Museum Staff Dashboard → Add Artifact
- Name: "Vijayanagara Empire Sculpture"
- Description: "This sculpture depicts..."
- Upload Image
- Auto-capture GPS location
- Submit
```

### **Step 2: System Auto-Translates**
When artifact is saved, Django signals trigger:
1. ✅ Translate title to all 13 languages
2. ✅ Translate description to all 13 languages
3. ✅ Translate historical context
4. ✅ Generate audio narration (Text-to-Speech) for each language
5. ✅ Generate QR code
6. ✅ Store GPS coordinates

**Example Output:**
- English: "This sculpture depicts..."
- Kannada: "ಈ ಶಿಲ್ಪವು ಚಿತ್ರಿಸುತ್ತದೆ..."
- Hindi: "यह मूर्ति चित्रित करती है..."
- Tamil: "இந்த சிற்பம் சித்தரிக்கிறது..."

### **Step 3: Visitor Scans Artifact**
1. Visitor opens ArtScope scanner
2. Selects language (e.g., Kannada)
3. Scans artifact with camera
4. **Geofencing validates location** (must be inside museum)
5. AR description appears in Kannada
6. Audio narration plays in Kannada

---

## 🔧 Technical Implementation

### **Translation Engine**
- **Library**: `deep-translator` (Google Translate API)
- **Speed**: ~2 seconds per language
- **Quality**: Professional-grade translation
- **Cost**: FREE (no API key needed)

### **Text-to-Speech**
- **Library**: `gTTS` (Google Text-to-Speech)
- **Voices**: Native language speakers
- **Format**: MP3 audio files
- **Storage**: Automatic S3/Media upload

### **Auto-Trigger**
```python
# Django Signal (core/signals.py)
@receiver(post_save, sender=Artwork)
def auto_translate_description(sender, instance, created, **kwargs):
    if created:
        # Translate to all languages
        auto_translate_artwork(instance)
        
        # Generate QR code
        generate_qr_code(instance)
```

---

## 📊 Database Structure

### **Artwork Model**
```python
- id
- title (English)
- description (English)
- historical_context (English)
- image
- latitude, longitude
- qr_code
```

### **ArtworkTranslation Model** (Auto-created)
```python
- artwork (Foreign Key)
- language (kn, hi, ta, te, ml, es, fr, de, etc.)
- title (Translated)
- description (Translated)
- historical_context (Translated)
- audio_narration (MP3 file)
```

---

## 🎯 User Experience

### **For Museum Staff**
1. Login to dashboard
2. Click "Add Artifact"
3. Fill form **in English only**:
   - Artifact name
   - Description
   - Upload image
4. Allow GPS location (auto-captured)
5. Click "Save"
6. ✨ **System auto-translates to 13 languages!**

### **For Visitors**
1. Open ArtScope scanner
2. Select preferred language (e.g., Kannada)
3. Point camera at artwork
4. **Geofence check** (must be inside museum)
5. AR description appears in Kannada
6. Click "🔊 Play Audio" for Kannada narration
7. Click "📌 Capture" to lock view while walking

---

## 🔐 Geofencing

### **Location Validation**
- Captured during artifact upload
- 100m radius default (configurable)
- Blocks scanning outside museum

### **User Experience**
```
✅ Inside Museum (0-100m): "Access granted"
⚠️ Nearby (100-500m): "You're 250m away. Walk closer."
❌ Far Away (>500m): "You're 2.5km away. Head to the museum."
```

---

## 🎨 Features Summary

| Feature | Status |
|---------|--------|
| Auto-translate from English | ✅ |
| 14 languages supported | ✅ |
| Audio narration (TTS) | ✅ |
| GPS auto-capture | ✅ |
| Geofencing validation | ✅ |
| QR code generation | ✅ |
| AR description overlay | ✅ |
| Capture/Lock view | ✅ |
| Language switcher | ✅ |

---

## 📝 Example Workflow

### **Museum: "Bangalore Palace"**
```
Staff uploads in English:
- Name: "Raja's Throne Room"
- Description: "This ornate throne room was built in 1887..."
- Image: throne_room.jpg
- GPS: Auto-captured (12.9981° N, 77.5920° E)
```

### **System Auto-Creates 13 Translations:**
```
Spanish: "Salón del Trono del Raja"
Kannada: "ರಾಜನ ಸಿಂಹಾಸನ ಕೋಣೆ"
Hindi: "राजा का सिंहासन कक्ष"
Tamil: "ராஜாவின் சிங்காசனம் அறை"
+ 10 more languages...
```

### **Visitor Experience:**
```
1. Tourist from Karnataka opens app
2. Selects "ಕನ್ನಡ (Kannada)"
3. Scans throne room
4. Geofence: ✅ 45m from artifact
5. AR overlay shows description in Kannada
6. Audio narration plays in Kannada voice
7. Tourist clicks "Capture" to read while walking
```

---

## 🚀 Benefits

### **For Museums**
- ✅ Upload once in English
- ✅ Reach international visitors
- ✅ No translation cost
- ✅ Professional quality
- ✅ Automatic audio narration

### **For Visitors**
- ✅ Read in native language
- ✅ Listen while exploring
- ✅ AR immersive experience
- ✅ Works only inside museum (geofenced)
- ✅ No app download needed

---

## 💡 Future Enhancements

- [ ] Add more Indian languages (Marathi, Bengali, etc.)
- [ ] Human review of translations
- [ ] Custom voice recordings
- [ ] Offline translation support
- [ ] Real-time translation from visitors' questions

---

## 🛠️ Installation

```bash
pip install deep-translator gtts geopy qrcode
```

No API keys required! Everything works out of the box.

---

**🎉 Result: Museum uploads in English, visitors experience in 13+ languages!**
