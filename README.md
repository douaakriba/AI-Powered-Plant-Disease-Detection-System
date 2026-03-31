# 🌱 AI-Powered Plant Disease Detection System

An intelligent agricultural system that uses Artificial Intelligence and Computer Vision to detect plant diseases from images in real time.

---

## 📌 Overview

This project is designed to support phytosanitary inspection services and farmers by enabling fast and accurate detection of plant diseases.

Field agents can capture a photo of a plant (leaf, stem, or fruit), upload it to the system, and instantly receive a detailed phytosanitary report including:

* Disease name
* Confidence level
* Severity analysis
* Recommended treatment

---

## 🚀 Features

* 📸 Image-based plant disease detection
* 🤖 AI model for classification (Deep Learning)
* ⚡ Real-time analysis using FastAPI
* 📊 Confidence score & severity indicators
* 💊 Treatment recommendations
* 🌍 Designed for real agricultural environments

---

## 🧠 Technologies Used

### Backend

* Python
* FastAPI
* TensorFlow / Keras
* NumPy
* Pillow (Image Processing)

### Frontend

* HTML
* CSS (Modern UI Design)
* JavaScript (Fetch API)

---

## 🏗️ System Architecture

```
User → Upload Image → FastAPI Backend → AI Model → Prediction → Web Interface
```

---

## 📂 Project Structure

```
project/
│
├── main.py              # FastAPI backend
├──  model.h5            # Trained AI model
│   
├──  index.html          # User interface
│       
├──
└── README.md
```

---

## ⚙️ Installation & Setup


###  Install dependencies

```
pip install fastapi uvicorn tensorflow pillow numpy
```

---

###  Run the backend server

```
uvicorn main:app --reload
```

---

###  Open the API docs

```
http://127.0.0.1:8000/docs
```

You can test image upload directly from the browser.

---

###  Run the frontend

Open `index.html` in your browser.

---

## 🧪 How It Works

1. The user uploads a plant image
2. The backend processes the image
3. The AI model analyzes it
4. The system returns:

   * Predicted disease
   * Confidence score
   * Additional insights

---

## 📊 Future Improvements

* 📍 GPS-based disease tracking
* 🗺️ Interactive agricultural map
* 🔔 Early warning system (alerts)
* 🧠 Improved AI accuracy with local datasets
* ☁️ Cloud deployment (AWS / Vercel / Docker)
* 📱 Mobile application version


---

## 📄 License

This project is open-source .

---



This system aims to digitize and modernize phytosanitary inspection processes by leveraging AI, helping prevent crop diseases and improving agricultural productivity.

---
