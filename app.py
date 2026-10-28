import requests
import streamlit as st

from database.db import (
    init_db,
    save_prediction,
    get_prediction_history,
)
from dashboard.api_client import check_api_health, predict_rul
from dashboard.components import (
    render_header,
    render_prediction_history,
    render_prediction_result,
    render_sensor_table,
)
from dashboard.config import (
    SENSOR_COLUMNS,
    SENSOR_DEFAULTS,
    SETTING_DEFAULTS,
)


st.set_page_config(
    page_title="Industrial Predictive Maintenance",
    page_icon="⚙️",
    layout="wide",
)


def initialize_session():
    """Menyiapkan state dashboard dan database."""
    init_db()

    if "latest_prediction" not in st.session_state:
        st.session_state.latest_prediction = None

    if "latest_sensor_data" not in st.session_state:
        st.session_state.latest_sensor_data = None


def render_sensor_form():
    """Menampilkan form input pengaturan dan sensor."""
    payload = {}

    with st.form("sensor_form"):
        st.subheader("Pengaturan Operasi")
        setting_columns = st.columns(3)

        for index, (name, default_value) in enumerate(
            SETTING_DEFAULTS.items()
        ):
            with setting_columns[index]:
                payload[name] = st.number_input(
                    name,
                    value=float(default_value),
                    format="%.6f",
                    key=f"input_{name}",
                )

        st.subheader("Input Sensor")
        sensor_columns = st.columns(3)

        for index, name in enumerate(SENSOR_COLUMNS):
            with sensor_columns[index % 3]:
                payload[name] = st.number_input(
                    name,
                    value=float(SENSOR_DEFAULTS[name]),
                    format="%.6f",
                    key=f"input_{name}",
                )

        submitted = st.form_submit_button(
            "Prediksi RUL",
            type="primary",
            use_container_width=True,
        )

    return submitted, payload


def render_history_filters():
    """Menampilkan filter dan mengambil riwayat dari SQLite."""
    st.subheader("Filter Riwayat Prediksi")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        search_query = st.text_input(
            "Cari ID atau waktu prediksi",
            placeholder="Contoh: 2026-10 atau 12",
            help="Cari berdasarkan ID catatan atau teks waktu prediksi.",
            key="history_search",
        )

    with filter_col2:
        history_limit = st.selectbox(
            "Jumlah maksimum catatan",
            options=[10, 25, 50, 100, 500, 1000],
            index=3,
            key="history_limit",
        )

    rul_col1, rul_col2 = st.columns(2)

    with rul_col1:
        min_rul = st.number_input(
            "RUL minimum",
            min_value=0.0,
            value=0.0,
            step=5.0,
            key="history_min_rul",
        )

    with rul_col2:
        max_rul = st.number_input(
            "RUL maksimum",
            min_value=0.0,
            value=125.0,
            step=5.0,
            key="history_max_rul",
        )

    if min_rul > max_rul:
        st.warning(
            "RUL minimum tidak boleh melebihi RUL maksimum."
        )
        return

    try:
        history = get_prediction_history(
            limit=history_limit,
            search=search_query.strip(),
            min_rul=min_rul,
            max_rul=max_rul,
        )

        render_prediction_history(history)

    except Exception as exc:
        st.error(
            f"Gagal membaca riwayat dari database: {exc}"
        )


def main():
    initialize_session()
    render_header()

    # Periksa koneksi backend dan status model.
    try:
        health = check_api_health()

        if health.get("model_loaded"):
            st.success("API terhubung · Model berhasil dimuat")
        else:
            st.warning(
                "API aktif, tetapi status model belum terkonfirmasi."
            )

    except requests.RequestException:
        st.error(
            "Dashboard tidak dapat terhubung ke FastAPI. "
            "Pastikan backend berjalan di port 8000."
        )
        st.stop()

    # Form prediksi.
    st.divider()
    st.subheader("Prediksi Kondisi Mesin")

    submitted, sensor_data = render_sensor_form()

    if submitted:
        try:
            prediction = predict_rul(sensor_data)
            rul = float(prediction["predicted_rul"])

            # Simpan hasil ke SQLite.
            save_prediction(
                predicted_rul=rul,
                sensor_data=sensor_data,
            )

            # Simpan hasil terbaru selama sesi aktif.
            st.session_state.latest_prediction = prediction
            st.session_state.latest_sensor_data = sensor_data.copy()

            st.toast("Prediksi berhasil dan riwayat tersimpan.")

        except requests.HTTPError as exc:
            status_code = (
                exc.response.status_code
                if exc.response is not None
                else "tidak diketahui"
            )

            st.error(f"API mengembalikan HTTP {status_code}.")

            if exc.response is not None:
                st.code(exc.response.text)

        except (requests.RequestException, KeyError, ValueError) as exc:
            st.error(f"Gagal memproses prediksi: {exc}")

        except Exception as exc:
            st.error(f"Gagal menyimpan hasil prediksi: {exc}")

    # Hasil prediksi terakhir.
    if st.session_state.latest_prediction is not None:
        st.divider()
        st.subheader("Hasil Prediksi Terbaru")

        render_prediction_result(
            st.session_state.latest_prediction
        )

        st.divider()
        st.subheader("Data Sensor Prediksi Terbaru")

        render_sensor_table(
            st.session_state.latest_sensor_data
        )

    # Riwayat prediksi dengan pencarian dan filter.
    st.divider()
    render_history_filters()

    st.caption(
        "Prototype edukasi berbasis NASA C-MAPSS FD001. "
        "Prediksi RUL merupakan estimasi model dan tidak "
        "menggantikan inspeksi atau sistem keselamatan industri."
    )


if __name__ == "__main__":
    main()