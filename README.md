# DYNAMIC-EVENT-ATTENDANCE-PREDICTOR

The **Dynamic Event Attendance Prediction System** is a Machine Learning–based web application that predicts the expected number of attendees for events by analyzing factors such as event type, venue capacity, ticket pricing, season, weather, and past attendance records.  
The system is deployed using **Flask** with a user-friendly interface built using **HTML, CSS, and JavaScript**, enabling real-time predictions for event organizers.

---

## 👨‍💻 Team Members

### 🧠 Data Science Team
| Name |
|------|
| Bharath Kumar Barre |
| Ravi Kumar Penumajji |
| Varsha Bandari |

### 💻 Full Stack Team
| Name |
|------|
| Sai Surya Chekuri |
| Venkata Naga Satya Saiesh M |
| Maneesha Pulakanti |

---

## 📌 Table of Contents

- [Abstract](#-abstract)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Dataset Description](#-dataset-description)
- [Model Development & Evaluation](#-model-development--evaluation)
- [Project Workflow](#-project-workflow)
- [Installation & Setup](#-installation--setup)
- [Screenshots](#-screenshots)
- [Results & Insights](#-results--insights)
- [Conclusion & Future Scope](#-conclusion--future-scope)

---

## 📄 Abstract

Event attendance prediction is crucial for efficient event planning, resource allocation, and profit optimization.  
This project develops a **Machine Learning-based prediction system** using a synthetic event dataset. It evaluates multiple models and integrates the best-performing one (Random Forest) into a Flask-based web application.

The system allows users to enter event details and get real-time attendance predictions along with analytical insights.

---

## 🛠 Tech Stack

| Category | Technologies Used |
|----------|-------------------|
| Programming | Python 3.x |
| ML & Data Science | Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn |
| Web Framework | Flask |
| Frontend | HTML5, CSS3, JavaScript |
| Development Tools | Jupyter Notebook, VS Code |

---

## 🧬 Dataset Description

The dataset consists of **13 features** including:

| Feature | Description |
|--------|-------------|
| event_type | Category of event (Concert, Sports, etc.) |
| sub_event_type | Specific event type (e.g., IPL, Dussehra, Rock Show) |
| venue_city | City where the event is held |
| venue_capacity | Capacity of the venue |
| season | Season of the event |
| weather | Weather condition on event day |
| ticket_price | Average price of entry |
| avg_past_attendance | Audience count of similar past events |
| death_count | Safety metric |
| actual_attend (Target) | True attendance count |

---

## 📊 Model Development & Evaluation

Multiple Regression models were trained and tested.  
**Random Forest Regressor** achieved the best performance.

| Model | R² Score | RMSE |
|-------|----------|--------|
| Linear Regression | 0.9098 | 3092.64 |
| Ridge Regression | 0.9098 | 3092.50 |
| Elastic Net | 0.9098 | 3092.22 |
| Decision Tree | 0.8522 | 3958.71 |
| **Random Forest (Best)** | **0.9231** | **2855.46** |
| Gradient Boosting | 0.9221 | 2873.60 |
| KNN Regression | 0.4356 | 7737.47 |

✅ **Random Forest selected for deployment**

---

## 🚀 System Architecture

**System Workflow:**

1. Data Collection & Preprocessing  
2. Feature Engineering & One-Hot Encoding  
3. Model Training & Evaluation  
4. Model Selection & Saving (.pkl)  
5. Flask Backend Integration  
6. Frontend UI for User Input  
7. Live Attendance Prediction Display  

---

## 🔥 Features

✔ Real-time attendance prediction  
✔ User-friendly web interface  
✔ Model insights provided for decision-making  
✔ Supports multiple event types (Concerts, Sports, Political, Traditional, etc.)  
✔ Displays summary + prediction analysis  

---

## 📥 Installation & Setup

Clone this repository:

```bash
git clone <repo-link>
cd <project-folder>
