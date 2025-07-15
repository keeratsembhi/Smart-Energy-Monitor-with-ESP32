import streamlit as st
import pandas as pd
import serial
import time
import os

st.set_page_config(page_title="ESP32 Energy Dashboard", layout="wide")
st.title("⚡ ESP32 Energy Monitor")

# Let user choose mode
mode = st.radio("Select data source:", ["Live from ESP32", "Read from CSV"])

if mode == "Live from ESP32":
    # live mode
    PORT = "/dev/cu.usbserial-210"
    BAUD = 115200

    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(2)  # allow reset
    except Exception as e:
        st.error(f"Could not connect to serial port: {e}")
        st.stop()

    st.success("Connected to ESP32 over serial")
    placeholder = st.empty()

    while True:
        line = ser.readline().decode().strip()
        if "Voltage RMS" in line:
            try:
                voltage = float(line.split(":")[1].strip())
                current = float(ser.readline().decode().split(":")[1].strip())
                power   = float(ser.readline().decode().split(":")[1].strip())
                _ = ser.readline()  # separator

                with placeholder.container():
                    st.metric("Voltage (V)", f"{voltage:.2f}")
                    st.metric("Current (A)", f"{current:.3f}")
                    st.metric("Power (W)", f"{power:.2f}")

            except Exception as e:
                st.warning(f"Parse error: {e}")

        time.sleep(1)
        st.experimental_rerun()

else:
    # csv mode
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Data preview:")
        st.dataframe(df.tail(20))

        st.subheader("Trends")
        st.line_chart(df[['Voltage (V)', 'Current (A)', 'Power (W)']])

        if df['Power (W)'].iloc[-1] > 100:
            st.error("OVERLOAD DETECTED!")
        else:
            st.success("Normal operation.")
