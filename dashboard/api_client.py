import requests

from dashboard.config import API_URL


def check_api_health():
    """Memeriksa koneksi API dan status model."""
    response = requests.get(
        f"{API_URL}/health",
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def predict_rul(sensor_data):
    """Mengirim data sensor dan mengambil prediksi RUL."""
    response = requests.post(
        f"{API_URL}/predict",
        json=sensor_data,
        timeout=15,
    )
    response.raise_for_status()
    return response.json()