import streamlit as st
from database import cursor

def show_home():
# all home page code here
# =========================
# HOME PAGE
# ========================

    st.header("⭐ Featured Vehicles")

    cursor.execute(
        "SELECT * FROM cars ORDER BY id DESC LIMIT 6"
    )

    cars = cursor.fetchall()

    cols = st.columns(3)

    for i, car in enumerate(cars):

        with cols[i % 3]:

            if car[11]:
                st.image(
                    car[11],
                    use_container_width=True
                )

            st.markdown(
                f"### 🚗 {car[1]} {car[2]}"
            )

            st.write(
                f"📅 Year: {car[3]}"
            )

            st.success(
                f"{car[5]:,.0f} SAR"
            )

            st.write(
                f"⚙️ Engine: {car[6]}"
            )

            st.write(
                f"🚘 Transmission: {car[7]}"
            )

            st.write(
                f"⛽ Fuel: {car[8]}"
            )

            whatsapp_url = (
                f"https://wa.me/966543346930?text="
                f"I am interested in {car[1]} {car[2]}"
            )

            st.link_button(
                "📱 WhatsApp Inquiry",
                whatsapp_url
            )