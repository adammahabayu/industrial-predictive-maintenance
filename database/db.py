import json
import sqlite3
from datetime import datetime
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "predictions.db"


def get_connection():
    """Membuka koneksi database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Membuat tabel jika belum tersedia."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS prediction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                predicted_at TEXT NOT NULL,
                predicted_rul REAL NOT NULL,
                sensor_data TEXT NOT NULL
            )
            """
        )


def save_prediction(predicted_rul, sensor_data):
    """Menyimpan prediksi dan input sensor."""
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO prediction_history
                (predicted_at, predicted_rul, sensor_data)
            VALUES (?, ?, ?)
            """,
            (
                datetime.now().astimezone().isoformat(
                    timespec="seconds"
                ),
                float(predicted_rul),
                json.dumps(sensor_data),
            ),
        )

        return cursor.lastrowid


def get_prediction_history(
    limit=100,
    search="",
    min_rul=None,
    max_rul=None,
):
    """Mengambil riwayat dengan filter opsional."""
    limit = max(1, min(int(limit), 1000))

    query = """
        SELECT id, predicted_at, predicted_rul, sensor_data
        FROM prediction_history
        WHERE 1 = 1
    """
    parameters = []

    if search.strip():
        query += " AND (CAST(id AS TEXT) LIKE ? OR predicted_at LIKE ?)"
        keyword = f"%{search.strip()}%"
        parameters.extend([keyword, keyword])

    if min_rul is not None:
        query += " AND predicted_rul >= ?"
        parameters.append(float(min_rul))

    if max_rul is not None:
        query += " AND predicted_rul <= ?"
        parameters.append(float(max_rul))

    query += " ORDER BY id DESC LIMIT ?"
    parameters.append(limit)

    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()

    return [
        {
            "id": row["id"],
            "Waktu": row["predicted_at"],
            "Predicted RUL": row["predicted_rul"],
            "Sensor": json.loads(row["sensor_data"]),
        }
        for row in rows
    ]