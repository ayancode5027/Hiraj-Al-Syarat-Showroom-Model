import streamlit as st
from database import cursor


def show_salesperson():

    st.header("📊 Sales Dashboard")

    # =========================
    # METRICS
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
        st.metric(
            "🚗 Cars In Stock",
            total_cars
        )

    with c2:
        st.metric(
            "📅 Bookings",
            total_bookings
        )

    with c3:
        st.metric(
            "💰 Cars Sold",
            total_sales
        )

    c4, c5 = st.columns(2)

    with c4:
        st.metric(
            "💵 Revenue",
            f"{total_revenue:,.0f} SAR"
        )

    with c5:
        st.metric(
            "📈 Profit",
            f"{total_profit:,.0f} SAR"
        )

    st.divider()

    # =========================
    # RECENT SALES
    # =========================

    st.subheader("💰 Recent Sales")

    cursor.execute("""
        SELECT
        brand,
        model,
        sale_price,
        profit,
        customer_name,
        sale_date
        FROM sales
        ORDER BY id DESC
        LIMIT 20
    """)

    sales = cursor.fetchall()

    if not sales:
        st.info("No sales recorded yet.")

    else:

        for sale in sales:

            st.write(
                f"""
                🚗 {sale[0]} {sale[1]}
                | Sold: {sale[2]:,.0f} SAR
                | Profit: {sale[3]:,.0f} SAR
                | Customer: {sale[4]}
                | Date: {sale[5]}
                """
            )

    st.divider()

    # =========================
    # BOOKINGS
    # =========================

    st.subheader("📅 Recent Bookings")

    cursor.execute("""
        SELECT *
        FROM bookings
        ORDER BY id DESC
        LIMIT 10
    """)

    bookings = cursor.fetchall()

    if not bookings:
        st.info("No bookings yet.")

    else:
        for booking in bookings:
            st.write(booking)

    # =========================
    # WHATSAPP BUTTON
    # =========================

    st.markdown("""
    <a href="https://wa.me/966543346930" target="_blank">
    <div style="
    position:fixed;
    bottom:20px;
    right:20px;
    background:#25D366;
    color:white;
    padding:15px 25px;
    border-radius:50px;
    font-weight:bold;
    z-index:999;">
    📱 WhatsApp
    </div>
    </a>
    """, unsafe_allow_html=True)