
import streamlit as st
from database import cursor

def show_inventory():

    st.header("🚗 Vehicle Inventory")

    search = st.text_input(
        "🔍 Search Vehicle"
    )

    brand_filter = st.selectbox(
        "Brand",
        [
            "All",
            "Toyota",
            "Hyundai",
            "Kia",
            "Nissan",
            "BMW",
            "Mercedes"
        ]
    )

    query = "SELECT * FROM cars WHERE 1=1"
    params = []

    if brand_filter != "All":
        query += " AND brand=?"
        params.append(brand_filter)

    if search:
        query += " AND (brand LIKE ? OR model LIKE ?)"
        params.extend([
            f"%{search}%",
            f"%{search}%"
        ])

    cursor.execute(query, params)
    cars = cursor.fetchall()

    for car in cars:

        with st.container():

            col1, col2 = st.columns([1, 2])

            with col1:

                if car[11]:
                    st.image(
                        car[11],
                        use_container_width=True
                    )

            with col2:

                st.markdown(
                    f"## 🚗 {car[1]} {car[2]}"
                )
                
                
                st.success(
                f"{car[5]:,.0f} SAR"
                )

                st.write(
                    f"📅 Year: {car[3]}"
                )

                st.write(
                    f"🚘 Transmission: {car[7]}"
                )

                st.write(
                    f"⛽ Fuel: {car[8]}"
                )

                st.write(
                    f"📦 Stock: {car[10]}"
                )

                whatsapp_message = (
                    f"Hello, I am interested in "
                    f"{car[1]} {car[2]}"
                )

                whatsapp_url = (
                    "https://wa.me/966543346930"
                    f"?text={whatsapp_message}"
                )

                st.markdown(
                    f"[📱 WhatsApp Inquiry]({whatsapp_url})"
                )

            st.divider()