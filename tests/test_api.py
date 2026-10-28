from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def valid_sensor_payload():
    """Membuat payload sensor yang valid untuk pengujian."""
    return {
        "setting_1": -0.0006,
        "setting_2": 0.0004,
        "setting_3": 100.0,
        "sensor_1": 518.67,
        "sensor_2": 642.58,
        "sensor_3": 1581.22,
        "sensor_4": 1398.91,
        "sensor_5": 14.62,
        "sensor_6": 21.61,
        "sensor_7": 554.42,
        "sensor_8": 2388.08,
        "sensor_9": 9056.4,
        "sensor_10": 1.3,
        "sensor_11": 47.23,
        "sensor_12": 521.79,
        "sensor_13": 2388.06,
        "sensor_14": 8130.11,
        "sensor_15": 8.4024,
        "sensor_16": 0.03,
        "sensor_17": 393.0,
        "sensor_18": 2388.0,
        "sensor_19": 100.0,
        "sensor_20": 38.81,
        "sensor_21": 23.3552,
    }


def test_root_endpoint():
    """Memastikan endpoint utama API tersedia."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()


def test_health_endpoint():
    """Memastikan API aktif dan model berhasil dimuat."""
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data.get("model_loaded") is True


def test_predict_with_valid_payload():
    """Memastikan prediksi menghasilkan RUL yang valid."""
    response = client.post(
        "/predict",
        json=valid_sensor_payload(),
    )

    assert response.status_code == 200

    data = response.json()

    assert "predicted_rul" in data
    assert isinstance(data["predicted_rul"], (int, float))
    assert 0 <= data["predicted_rul"] <= 125


def test_predict_with_missing_sensor():
    """Memastikan API menolak payload dengan sensor yang hilang."""
    payload = valid_sensor_payload()
    payload.pop("sensor_1")

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_with_invalid_sensor_type():
    """Memastikan API menolak nilai sensor yang bukan angka."""
    payload = valid_sensor_payload()
    payload["sensor_1"] = "bukan-angka"

    response = client.post("/predict", json=payload)

    assert response.status_code == 422