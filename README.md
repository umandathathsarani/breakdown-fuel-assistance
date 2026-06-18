# RescueRoute Pro 🚗💨📌

## Project Overview

**RescueRoute Pro** is a full-stack web application built to modernize roadside assistance. Instead of drivers guessing what is wrong with their vehicle, this platform leverages a custom-trained Convolutional Neural Network (CNN) to automatically identify dashboard warning lights, gauge the severity, and seamlessly dispatch local service providers.

This project demonstrates the end-to-end integration of a PyTorch machine learning model into an asynchronous FastAPI and Vanilla JavaScript ecosystem.

---

## ✨ Key Features

### 🤖 AI Computer Vision Diagnosis

Drivers upload a photo of their dashboard. The system utilizes a custom PyTorch CNN to identify critical warnings (Engine, Battery, Oil, Fuel) in real-time.

### 🔄 Dual-Service Workflows

Dynamic frontend routing allows users to seamlessly switch between AI Breakdown Diagnosis and Emergency Fuel Delivery requests.

### 📊 Operator Dispatch Dashboard

A dedicated real-time portal for service providers. It uses asynchronous polling to instantly display incoming emergencies, the exact AI confidence threshold, and the driver's location.

### ⚡ In-Memory Queue System

High-performance, lightweight ticket management built directly into the FastAPI backend state.

### 📱 Responsive Architecture

A polished **Slate & Emerald** interface built with CSS Flexbox, ensuring accessibility across both desktop monitors and mobile devices.

### 🧭 Integrated Navigation

Core headers feature role-switching buttons to allow seamless shifting between the Driver App and Provider Portal views during evaluation.

---

# 📂 Repository Structure

```plaintext
breakdown-fuel-assistance/
├── ai_vision/               # Machine Learning Engine
│   ├── dataset/             # Curated training images (Golden Batch)
│   ├── model.py             # PyTorch CNN Architecture definition
│   ├── train.py             # Training loop & dataset generation
│   └── dashboard_cnn.pt     # Compiled model weights (Saved State)
│
├── backend/                 # FastAPI Server
│   ├── main.py              # Routing, State Management, Inference Pipeline
│   └── requirements.txt     # Python environment dependencies
│
└── frontend/                # Client & Provider UI
    ├── assets/              # Icons and images (Favicons)
    ├── css/                 # Styling (Forms, Modals, Layout)
    ├── js/                  # Vanilla JS DOM manipulation & Fetch API
    ├── index.html           # Driver Assistance Request Portal
    └── provider.html        # Operator Dispatch Dashboard
```

---

# 🛠️ Technology Stack

## Frontend

**Core Technologies**

* HTML5
* CSS3
* JavaScript (ES6+)

**Architecture**

* Modular file structure
* Separation of API logic
* DOM manipulation via `ui.js`
* Global layout styling

**Communication**

* Fetch API
* Multipart form-data processing

---

## Backend

**Framework**

* Python
* FastAPI

**Server**

* Uvicorn (ASGI)

**Data Flow**

* RESTful API architecture
* CORS-enabled communication

---

## Artificial Intelligence

**Core Frameworks**

* PyTorch
* Torchvision

**CNN Architecture**

* Conv2D
* MaxPool2D
* Fully Connected Layers

**Optimization**

* Adam Optimizer
* Cross-Entropy Loss Function

**Preprocessing**

* PIL Image Processing
* Tensor Normalization Pipelines

---

# 📡 API Endpoints

| Method | Endpoint                     | Description                            | Payload / Parameters                          |
| ------ | ---------------------------- | -------------------------------------- | --------------------------------------------- |
| POST   | `/api/diagnose`              | Processes dashboard images via PyTorch | Multipart Form Data (`image`, `location`)     |
| POST   | `/api/fuel`                  | Creates a fuel delivery request        | Form Data (`location`, `fuel_type`, `amount`) |
| GET    | `/api/providers/requests`    | Retrieves active dispatch queue        | None                                          |
| POST   | `/api/providers/accept/{id}` | Marks a request as dispatched          | Path Parameter (`ticket_id`)                  |

---

# 🚀 Getting Started

## 1. Prerequisites

Ensure Python 3.8 or higher is installed.

```bash
python --version
```

---

## 2. Installation & Setup

Clone the repository and create a virtual environment.

```bash
git clone https://github.com/YOUR_USERNAME/breakdown-fuel-assistance.git

cd breakdown-fuel-assistance

python -m venv venv
```

### Activate the Environment

#### Windows

```bash
.\venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install -r backend/requirements.txt
```

---

## 3. Running the Platform

Start the FastAPI backend server.

```bash
python backend/main.py
```

Once the terminal displays:

```plaintext
AI Model loaded into FastAPI server successfully
```

Open the frontend interfaces:

### Driver Interface

```plaintext
frontend/index.html
```

### Provider Dashboard

```plaintext
frontend/provider.html
```

Open the provider dashboard in a separate browser tab or window.

---

# 🧠 Model Training Details

The proprietary CNN model (`dashboard_cnn.pt`) was trained using a curated **Golden Mini-Batch Dataset**.

### Model Characteristics

* Input Size: 128 × 128 RGB Images
* Architecture: 3-Layer Convolutional Neural Network
* Feature Extraction: Convolution + Pooling Layers
* Classification: Fully Connected Layers
* Output Classes:

  * Engine Warning
  * Battery Warning
  * Oil Warning
  * Fuel Warning

Training scripts and dataset structures are retained within the `ai_vision/` directory for future experimentation and model improvement.

---

# 🗺️ Future Roadmap

### 🗄️ Database Persistence

Replace in-memory queues with MongoDB for persistent storage and historical ticket tracking.

### 📍 Geolocation Integration

Integrate Google Maps APIs for accurate GPS coordinates and route planning.

### 🧠 Model Expansion

Expand CNN recognition capabilities to support 20+ dashboard indicators.

### 🔐 Authentication & Security

Implement JWT-based authentication for service providers and administrators.

### 📈 Analytics Dashboard

Provide statistics on ticket volume, response times, and service provider performance.

---

# 🙏 Acknowledgments

Developed as a specialized project for the **Artificial Intelligence and Software Engineering curriculum**.

Special thanks to the open-source communities behind:

* FastAPI
* PyTorch
* Torchvision
* Uvicorn

whose documentation and community support greatly contributed to the development of this platform.

---

# 📜 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute this software in accordance with the terms of the license.
