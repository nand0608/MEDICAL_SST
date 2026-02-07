# 🩺 Medical Speech-to-Text Prescription System (Offline)

An **offline, real-time medical speech-to-text prescription system** built using **Python** and **Vosk**.  
This project helps doctors and healthcare professionals **dictate prescriptions by voice** and automatically converts spoken medical instructions into **standard medical abbreviations and structured text**.

The system works completely **offline**, ensures **patient data privacy**, accurately converts **spoken numbers into digits**, and applies **medical rules** such as dosage, frequency, timing, and food instructions.

---

## 📌 Project Highlights

- 🎙️ Real-time offline speech recognition
- 🧠 Medical phrase normalization (BF, AF, BD, TDS, SOS, etc.)
- 🔢 Accurate spoken number conversion
  - five hundred → 500
  - one thousand → 1000
- 💊 Dosage form and unit handling
  - tablet, capsule, syrup, injection
  - mg, ml, IU
- 📋 Grammar-based recognition for higher accuracy
- 🔒 Privacy-safe (no internet, no cloud)
- 💻 Can run on any local machine or laptop

---

## 🧠 Example Output

| Spoken Input                      | Output            |
| --------------------------------- | ----------------- |
| five hundred milligram after food | `500 mg AF`       |
| tablet twice daily                | `tab BD`          |
| one thousand units injection      | `1000 IU inj`     |
| syrup ten milliliter at night     | `syp 10 ml night` |

---

## 🛠️ Technologies Used

- Python 3.8+
- Vosk Speech Recognition
- PyAudio
- Regex-based NLP normalization
- JSON-based medical grammar

---
## 🔽 Installation & Setup

### 1. Install Python
```bash
python --version
```
### 2. Clone Repository
```bash
git clone https://github.com/nand0608/medical-speech-to-text.git
cd medical-speech-to-text
```
### 3. Create Virtual Environment
```bash
python -m venv venv
```
Activate:
-Windows: venv\Scripts\activate
-Linux/macOS: source venv/bin/activate

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
### 5. Download Vosk Model
Download from https://alphacephei.com/vosk/models
Extract to:
```bash
model/vosk-model-small-en-us-0.15/
```
### 6.Run code
```bash
python stt_prescription.py
```





