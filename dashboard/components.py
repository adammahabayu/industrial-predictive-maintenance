import json

import pandas as pd
import streamlit as st


def render_header():
    st.title("Industrial Predictive Maintenance")
    st.caption(
        "Equipment monitoring and Remaining Useful Life (RUL) "
        "estimation powered by Random Forest."
    )


def render_prediction_result(prediction):
    rul = float(prediction["predicted_rul"])

    st.subheader("Hasil Prediksi")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Predicted RUL", f"{rul:.2f} siklus")

    with col2:
        if rul <= 20:
            status = "Perhatian tinggi"
        elif rul <= 50:
            status = "Perlu pemantauan"
        else:
            status = "Estimasi RUL relatif tinggi"

        st.metric("Indikator awal", status)

    st.info(
        "Indikator ini menggunakan ambang RUL sederhana untuk "
        "demonstrasi, bukan standar keselamatan industri."
    )

    interpretation = prediction.get("interpretation")
    if interpretation:
        st.caption(interpretation)


def render_sensor_table(sensor_data):
    st.subheader("Profil Input Sensor")

    sensor_frame = pd.DataFrame(
        [
            {"Fitur": name, "Nilai": value}
            for name, value in sensor_data.items()
        ]
    )

    st.dataframe(
        sensor_frame,
        use_container_width=True,
        hide_index=True,
    )


def render_prediction_history(history):
    st.subheader("Riwayat Prediksi")

    if not history:
        st.info("Tidak ada riwayat yang cocok dengan filter.")
        return

    # Ringkasan dari riwayat yang sedang ditampilkan.
    rul_values = [
        float(item["Predicted RUL"])
        for item in history
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric("Jumlah catatan", len(history))
    col2.metric(
        "Rata-rata RUL",
        f"{sum(rul_values) / len(rul_values):.2f} siklus",
    )
    col3.metric(
        "RUL terbaru",
        f"{float(history[0]['Predicted RUL']):.2f} siklus",
    )

    history_frame = pd.DataFrame(
        [
            {
                "ID": item["id"],
                "Waktu": item["Waktu"],
                "Predicted RUL": item["Predicted RUL"],
            }
            for item in history
        ]
    )

    # Data grafik disusun dari yang lama ke yang baru.
    chart_frame = history_frame.iloc[::-1].set_index("Waktu")

    st.markdown("#### Tren Prediksi RUL")

    st.line_chart(
        chart_frame["Predicted RUL"],
        y_label="RUL (siklus)",
    )

    st.markdown("#### Daftar Prediksi")

    st.dataframe(
        history_frame,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### Detail Input Sensor")

    selected_id = st.selectbox(
        "Pilih ID prediksi",
        options=[item["id"] for item in history],
        format_func=lambda record_id: (
            f"ID {record_id} — "
            f"{next(item['Waktu'] for item in history if item['id'] == record_id)}"
        ),
    )

    selected_record = next(
        item for item in history
        if item["id"] == selected_id
    )

    st.write(
        f"**Predicted RUL:** "
        f"{float(selected_record['Predicted RUL']):.2f} siklus"
    )

    sensor_frame = pd.DataFrame(
        [
            {"Fitur": name, "Nilai": value}
            for name, value in selected_record["Sensor"].items()
        ]
    )

    st.dataframe(
        sensor_frame,
        use_container_width=True,
        hide_index=True,
    )

    with st.expander("Lihat input sensor dalam format JSON"):
        st.code(
            json.dumps(
                selected_record["Sensor"],
                indent=2,
            ),
            language="json",
        )

    # Ekspor daftar riwayat beserta seluruh input sensor.
    export_records = []

    for item in history:
        record = {
            "id": item["id"],
            "Waktu": item["Waktu"],
            "Predicted RUL": item["Predicted RUL"],
        }
        record.update(item["Sensor"])
        export_records.append(record)

    export_frame = pd.DataFrame(export_records)

    st.download_button(
        label="Unduh riwayat lengkap (CSV)",
        data=export_frame.to_csv(index=False).encode("utf-8"),
        file_name="prediction_history.csv",
        mime="text/csv",
    )