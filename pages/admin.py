import streamlit as st
from database import cursor, conn
from datetime import date


def show_admin():

    st.header("🛠 Admin Dashboard")

    # =========================
    # ANALYTICS
    # =========================
    cursor.execute("SELECT COUNT(*) FROM cars")
    total_cars = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sales")
    total_sales = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(sale_price) FROM sales")
    total_revenue = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(profit) FROM sales")
    total_profit = cursor.fetchone()[0] or 0

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("🚗 Total Vehicles", total_cars)

    with c2:
        st.metric("📅 Bookings", total_bookings)

    with c3:
        st.metric("💰 Cars Sold", total_sales)

    c4, c5 = st.columns(2)

    with c4:
        st.metric("💵 Revenue", f"{total_revenue:,.0f} SAR")

    with c5:
        st.metric("📈 Profit", f"{total_profit:,.0f} SAR")

    st.divider()

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Add Vehicle",
        "🚗 Manage Vehicles",
        "📅 Bookings",
        "💰 Sales History"
    ])

    # =========================
    # ADD VEHICLE
    # =========================
    with tab1:

        st.subheader("Add New Vehicle")

        brand = st.text_input("Brand")
        model = st.text_input("Model")

        year = st.number_input("Year", 2000, 2035, 2025)

        condition = st.selectbox("Condition", ["New", "Used"])

        purchase_price = st.number_input("Purchase Price (Cost)", min_value=0)

        price = st.number_input("Selling Price", min_value=0)

        engine = st.text_input("Engine")

        transmission = st.selectbox("Transmission", ["Automatic", "Manual"])

        fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid", "Electric"])

        color = st.text_input("Color")

        stock = st.number_input("Stock", min_value=0, value=1)

        image_url = st.text_input("Image URL")

        description = st.text_area("Description")

        if st.button("Add Vehicle"):

            cursor.execute("""
                INSERT INTO cars (
                    brand, model, year, condition,
                    purchase_price, price,
                    engine, transmission, fuel_type,
                    color, stock, image_url, description
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                brand, model, year, condition,
                purchase_price, price,
                engine, transmission, fuel,
                color, stock, image_url, description
            ))

            conn.commit()
            st.success("Vehicle Added Successfully")
            st.rerun()

    # =========================
    # MANAGE VEHICLES
    # =========================
    with tab2:

        st.subheader("Manage Vehicles")

        cursor.execute("SELECT * FROM cars ORDER BY id DESC")
        cars = cursor.fetchall()

        if not cars:
            st.info("No vehicles available.")

        for car in cars:

            col1, col2, col3 = st.columns([4, 2, 2])

            with col1:
                st.write(f"🚗 {car[1]} {car[2]} | {car[5]:,} SAR")

            with col2:
                if st.button("💰 Sell", key=f"sell_{car[0]}"):
                    st.session_state["sell_car"] = car[0]

            with col3:
                if st.button("❌ Delete", key=f"del_{car[0]}"):

                    cursor.execute("DELETE FROM cars WHERE id=?", (car[0],))
                    conn.commit()
                    st.rerun()

        # =========================
        # SELL CAR FORM
        # =========================
        if "sell_car" in st.session_state:

            st.divider()
            st.subheader("Sell Vehicle")

            customer_name = st.text_input("Customer Name")
            customer_phone = st.text_input("Customer Phone")
            sale_price = st.number_input("Final Sale Price", min_value=0)

            if st.button("Confirm Sale"):

                car_id = st.session_state["sell_car"]

                cursor.execute("SELECT * FROM cars WHERE id=?", (car_id,))
                car = cursor.fetchone()

                purchase_price = car[5]
                profit = sale_price - purchase_price

                cursor.execute("""
                    INSERT INTO sales (
                        car_id, brand, model,
                        purchase_price, sale_price,
                        customer_name, customer_phone,
                        sale_date, profit
                    )
                    VALUES (?,?,?,?,?,?,?,?,?)
                """, (
                    car[0], car[1], car[2],
                    purchase_price, sale_price,
                    customer_name, customer_phone,
                    str(date.today()), profit
                ))

                cursor.execute("DELETE FROM cars WHERE id=?", (car_id,))

                conn.commit()

                del st.session_state["sell_car"]

                st.success(f"Sold Successfully! Profit: {profit:,.0f} SAR")
                st.rerun()

    # =========================
    # BOOKINGS
    # =========================
    with tab3:

        st.subheader("Test Drive Bookings")

        cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
        bookings = cursor.fetchall()

        if not bookings:
            st.info("No bookings yet.")

        for b in bookings:
            st.write(b)

    # =========================
    # SALES HISTORY
    # =========================
    with tab4:

        st.subheader("Sales History")

        cursor.execute("SELECT * FROM sales ORDER BY id DESC")
        sales = cursor.fetchall()

        if not sales:
            st.info("No sales yet.")

        for s in sales:

            st.write(
             f"🚗 {s[2]} {s[3]} | "
             f"Sold: {s[5]:,.0f} SAR | "
             f"Profit: {s[9]:,.0f} SAR | "
             f"Customer: {s[6]} | "
             f"Date: {s[8]}"
)