# 🌿 PhytoSentinel
### Système Intelligent de Détection et de Suivi des Maladies des Plantes

> Developed at the **Direction des Services Agricoles (DSA) de Guelma**, Algeria  




<!-- SCREENSHOT BANNER -->
<!-- Replace with your actual screenshot -->
<!-- ![PhytoSentinel Dashboard](screenshots/dashboard.png) -->



---

## 🔍 About

**PhytoSentinel** is an intelligent web platform for **plant disease detection and monitoring**, built to assist Algerian farmers and phytosanitary inspectors. It uses deep learning (DenseNet121 + Transfer Learning) to analyze leaf images and deliver real-time diagnoses with confidence scores.

The system was developed as a practical solution to the limitations of manual plant disease diagnosis — slow, non-standardized, and difficult to trace — by providing a digital tool that is fast, accurate, and centralized.

---

## ✨ Features

### 🧑‍🌾 Farmer Interface
| Feature | Description |
|---|---|
| 🔬 AI Detection | Upload a leaf photo → instant disease diagnosis with confidence score |
| 📊 Analysis History | Full log of past analyses stored in SQLite |
| 🗺️ Geo-localization | Each analysis tagged with commune & coordinates |
| 🔔 Smart Alerts | Weather-based disease risk alerts via expert rules engine |
| 📅 Agri Calendar | Intelligent planning calendar for interventions |
| 📤 Share with Admin | Send analysis results to the administrator |

### 🛡️ Admin Interface
| Feature | Description |
|---|---|
| 👥 User Management | View all users, assign roles, deactivate accounts |
| 📋 All Analyses | Supervise every analysis submitted across the platform |
| 🗺️ Sanitary Map | Geographic heatmap of diseases across Wilaya de Guelma (38 communes) |
| 📈 Statistics | Platform-wide health metrics and disease trends |
| 🔔 Alerts Panel | Receive and manage phytosanitary alerts |

---

## 🤖 AI Models

PhytoSentinel integrates **9 specialized DenseNet121 models**, one per crop, trained via Transfer Learning on PlantVillage.

### 📥 Model Source

The pre-trained models used in this project are sourced from Kaggle:

> **[Plant Disease Detection Model — mgmitesh](https://www.kaggle.com/models/mgmitesh/plant-disease-detection-model)**

To use the project, download the `.h5` model files from the link above and place them in the `models/` folder:

```
models/
├── apple_model.h5
├── cherry_model.h5
├── corn_model.h5
├── grape_model.h5
├── peach_model.h5
├── pepper_model.h5
├── potato_model.h5
├── strawberry_model.h5
└── tomato_model.h5
```

### Covered Crops & Diseases

| Crop | Classes | Diseases Detected | Task |
|---|---|---|---|
| 🍅 Tomato | 4 | Bacterial Spot, Early Blight, Late Blight, Healthy | Multi-class |
| 🍎 Apple | 4 | Apple Scab, Black Rot, Cedar Apple Rust, Healthy | Multi-class |
| 🍇 Grape | 4 | Black Rot, Esca (Black Measles), Leaf Blight, Healthy | Multi-class |
| 🌽 Corn | 4 | Common Rust, Gray Leaf Spot, Northern Leaf Blight, Healthy | Multi-class |
| 🥔 Potato | 3 | Early Blight, Late Blight, Healthy | Multi-class |
| 🍒 Cherry | 2 | Powdery Mildew, Healthy | Binary |
| 🍑 Peach | 2 | Bacterial Spot, Healthy | Binary |
| 🫑 Pepper | 2 | Bacterial Spot, Healthy | Binary |
| 🍓 Strawberry | 2 | Leaf Scorch, Healthy | Binary |

### Performance (averaged across 9 models)

| Metric | Score |
|---|---|
| Accuracy | **98.20%** |
| Precision | **98.30%** |
| Recall | **98.10%** |
| F1-Score | **98.20%** |

### Training Parameters

| Parameter | Value |
|---|---|
| Base Architecture | DenseNet121 (pre-trained on ImageNet) |
| Approach | Transfer Learning (fine-tuning) |
| Input Size | 256×256 px (RGB), normalized [0,1] |
| Optimizer | Adam — lr = 1×10⁻⁴ |
| Loss Function | Categorical Crossentropy |
| Batch Size | 32 |
| Data Split | 80% Train / 10% Val / 10% Test |
| Model Size | ~33 MB per model (~7M parameters) |
| Inference Latency | ~50 ms/image (GPU) |

<!-- Add your performance chart here -->
<!-- ![Model Accuracy Chart](screenshots/model_accuracy.png) -->

---

## 🛠 Tech Stack

| Layer | Technology | Role |
|---|---|---|
| Backend | Python 3.x + Flask 3.0.3 | REST API, routing |
| Cross-Origin | Flask-CORS | Cross-origin request handling |
| AI Engine | TensorFlow 2.10 + tf_keras | CNN disease detection |
| Image Processing | Pillow (PIL) + NumPy | Preprocessing to 224×224 px |
| Auth | PyJWT + hashlib + secrets | JWT tokens, password hashing |
| Database | SQLite | Embedded, serverless DB |
| Frontend | HTML / CSS / JavaScript | Two user interfaces |

---

## 🏗 Architecture

The system follows a **4-layer architecture**:

```
┌─────────────────────────────────────────────────────┐
│         Layer 1 — Presentation (HTML/CSS/JS)         │
│    Interface Agriculteur  |  Interface Admin          │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP REST
┌──────────────────▼──────────────────────────────────┐
│         Layer 2 — Business Logic (Flask)             │
│   Auth/JWT  |  REST Routes  |  Services  |  Images   │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│         Layer 3 — Intelligence & Persistence         │
│     TensorFlow Models        |      SQLite DB         │
│  (DenseNet121 × 9 crops)     |  users/analyses/alerts │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│         Layer 4 — Infrastructure                     │
│   Flask Dev Server  |  Static Files  |  JWT Security  │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
PhytoSentinel/
│
├── app.py                    # Main Flask backend — REST API
├── database.py               # SQLite database manager (RBAC, users, analyses)
├── expert_alerts.py          # Rule-based expert system for weather alerts
├── disease_information.py    # Disease catalogue & treatment recommendations
│
├── admin.html                # Admin dashboard interface
├── agriculteur.html          # Farmer interface
│
├── models/                   # Pre-trained .h5 model files (not included in repo)
│   ├── apple_model.h5
│   ├── cherry_model.h5
│   ├── corn_model.h5
│   ├── grape_model.h5
│   ├── peach_model.h5
│   ├── pepper_model.h5
│   ├── potato_model.h5
│   ├── strawberry_model.h5
│   └── tomato_model.h5
│
├── uploads/                  # User-uploaded images (auto-created)
├── phytosentinel.db          # SQLite database (auto-created on first run)
│
└── README.md
```

> ⚠️ **Note:** Model `.h5` files are not included in the repository due to their size (~33 MB each). Download instructions below.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip





### Default Admin Credentials
```
Username: admin
Password: PhytoAdmin2024!
```

> 🔐 Change these in `app.py` before any production deployment.

---

## 📸 Screenshots

![Screenshot 348](Screenshot%20(348).png)
![Screenshot 349](Screenshot%20(349).png)
![Screenshot 350](Screenshot%20(350).png)
![Screenshot 351](Screenshot%20(351).png)
![Screenshot 352](Screenshot%20(352).png)
![Screenshot 353](Screenshot%20(353).png)
![Screenshot 354](Screenshot%20(354).png)
![Screenshot 355](Screenshot%20(355).png)
![Screenshot 356](Screenshot%20(356).png)
![Screenshot 357](Screenshot%20(357).png)
![Screenshot 358](Screenshot%20(358).png)
![Screenshot 359](Screenshot%20(359).png)
![Screenshot 360](Screenshot%20(360).png)
![Screenshot 361](Screenshot%20(361).png)
![Screenshot 362](Screenshot%20(362).png)
![Screenshot 363](Screenshot%20(363).png)
![Screenshot 364](Screenshot%20(364).png)
![Screenshot 365](Screenshot%20(365).png)

---


## 📄 License

This project was developed as an academic internship project. All rights reserved © 2025/2026.

---

<p align="center">
  Made with 🌿 for Algerian Agriculture
</p>
