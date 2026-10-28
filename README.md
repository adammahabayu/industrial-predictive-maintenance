# Industrial Predictive Maintenance & Equipment Monitoring Platform

A machine learning-based predictive maintenance prototype that estimates the Remaining Useful Life (RUL) of turbofan engines using sensor measurements from the NASA C-MAPSS FD001 dataset.

The project combines a machine learning model, a FastAPI prediction service, a Streamlit dashboard, and an SQLite database for prediction history.

## Project Overview

Unexpected equipment failure can lead to downtime, increased maintenance costs, and operational disruption. Predictive maintenance uses equipment data to estimate degradation and support maintenance planning.

This project demonstrates an end-to-end predictive maintenance workflow:

- Explore and preprocess turbofan engine sensor data.
- Train and evaluate a machine learning regression model.
- Serve RUL predictions through a REST API.
- Display predictions and sensor inputs in a dashboard.
- Store prediction history in SQLite.
- Test API endpoints and input validation automatically.

> This is an educational prototype. Predictions are not intended for real industrial safety decisions.

## Features

- RUL prediction using a Random Forest regression model.
- FastAPI endpoints for health checks and predictions.
- Streamlit dashboard for sensor input and prediction results.
- SQLite storage for prediction history.
- Search and filtering for historical predictions.
- CSV export for prediction history.
- Automated API tests with pytest.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Machine learning | scikit-learn |
| Model persistence | Joblib |
| Data processing | pandas |
| Backend API | FastAPI |
| API server | Uvicorn |
| Dashboard | Streamlit |
| Database | SQLite |
| Testing | pytest, FastAPI TestClient |

## Dataset

This project uses the NASA Commercial Modular Aero-Propulsion System Simulation (C-MAPSS) dataset, specifically the FD001 subset.

The dataset contains simulated turbofan engine degradation trajectories, operational settings, and sensor measurements.

Dataset source: [NASA Prognostics Center of Excellence Data Repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)

### Target Variable

Remaining Useful Life (RUL) represents the estimated number of operating cycles remaining before the defined end-of-life condition.

For the capped RUL experiment, target values are limited to a maximum of 125 cycles.

## Model Evaluation

The current model is a Random Forest Regressor trained with capped RUL labels.

Reported results from the project experiments:

| Evaluation | MAE | RMSE |
|---|---:|---:|
| Validation | 12.36 | 17.08 |
| Official test RUL | 12.14 | 17.23 |

- **MAE** measures the average absolute difference between predicted and actual RUL.
- **RMSE** penalizes larger prediction errors more strongly.

Lower values generally indicate better predictive performance.

These metrics are from the current project experiments and should be interpreted in the context of the FD001 dataset and its evaluation setup.

## System Architecture

```text
NASA C-MAPSS FD001
        |
        v
Data Exploration & Model Training
        |
        v
Random Forest Model
        |
        v
FastAPI Prediction Service
        |
        v
Streamlit Dashboard
        |
        +------> SQLite Prediction History
```

## Project Structure

```text
industrial-predictive-maintenance/
├── dashboard/
│   ├── __init__.py
│   ├── api_client.py
│   ├── components.py
│   └── config.py
├── database/
│   ├── __init__.py
│   └── db.py
├── tests/
│   └── test_api.py
├── app.py
├── main.py
├── feature_columns.json
├── random_forest_rul_capped.joblib
├── requirements.txt
├── requirements-lock.txt
└── README.md
```

The SQLite database is generated locally when the dashboard initializes. The trained model and feature configuration must be available before starting the API.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/adammahabayu/industrial-predictive-maintenance.git
cd industrial-predictive-maintenance
```

Replace `YOUR_USERNAME` with your GitHub username and update the repository URL after publishing the project.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Running the Application

Run the backend and dashboard in separate terminals.

### Terminal 1 — FastAPI

Activate the virtual environment, navigate to the project directory, and run:

```powershell
python -m uvicorn main:app --reload
```

API base URL: `http://127.0.0.1:8000`

Interactive API documentation: `http://127.0.0.1:8000/docs`

### Terminal 2 — Streamlit

Activate the virtual environment and run:

```powershell
python -m streamlit run app.py
```

Dashboard URL: `http://localhost:8501`

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check the root endpoint |
| GET | `/health` | Check API and model status |
| POST | `/predict` | Predict RUL from operational settings and sensor values |

The prediction endpoint expects the operational settings and sensor features required by the trained model.

## Running Tests

With the virtual environment activated:

```powershell
python -m pytest tests/test_api.py -v
```

The API test suite covers:

- Root endpoint availability.
- Health endpoint and model loading.
- Prediction with valid sensor input.
- Rejection of missing sensor fields.
- Rejection of non-numeric sensor values.

## Limitations

- The model is trained on simulated turbofan engine data, not live industrial equipment.
- Results depend on the dataset, preprocessing, feature selection, and evaluation methodology.
- A predicted RUL is an estimate and includes uncertainty.
- The prototype does not include live sensor integration, industrial control, or production-grade authentication.
- It must not be used as the sole basis for maintenance or safety decisions.

## Future Improvements

- Add model comparison and explainability.
- Improve validation and monitoring of prediction quality.
- Add trend analysis and more detailed historical reporting.
- Package the application for easier deployment.
- Integrate a suitable real-world equipment dataset when available.

## Author

**Adam Mahabayu Muhibbulloh**

GitHub: [adammahabayu](https://github.com/adammahabayu)