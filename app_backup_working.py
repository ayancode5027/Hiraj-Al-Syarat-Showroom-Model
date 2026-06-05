import streamlit as st
from database import conn, cursor
from auth import login, create_default_users
from translations import LANG

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Hiraj Al Sayarat Al Jadeed",
    page_icon="🚗",
    layout="wide"
)
st.markdown("""
<style>

.main {
    background-color:#f5f5f5;
}

.hero{
    background:linear-gradient(135deg,#111,#222);
    padding:40px;
    border-radius:20px;
    color:white;
    text-align:center;
    margin-bottom:20px;
}

.hero-title{
    font-size:48px;
    font-weight:bold;
}

.hero-sub{
    font-size:20px;
}

.car-card{
    background:white;
    padding:15px;
    border-radius:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.1);
    margin-bottom:20px;
}

.gold{
    color:#D4AF37;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

create_default_users()

# =========================
# SESSION VARIABLES
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "lang" not in st.session_state:
    st.session_state.lang = "en"

# =========================
# LANGUAGE
# =========================
st.sidebar.title("🌐 Language")

language = st.sidebar.selectbox(
    "Select Language",
    ["en", "ar"]
)

st.session_state.lang = language
T = LANG[language]

# =========================
# SIDEBAR LOGIN
# =========================
st.sidebar.markdown("---")
st.sidebar.title("🔐 Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):

    role = login(username, password)

    if role:
        st.session_state.logged_in = True
        st.session_state.role = role
        st.sidebar.success(f"Logged in as {role}")

    else:
        st.sidebar.error("Invalid Username or Password")

# =========================
# SHOWROOM HEADER
# =========================
st.title("🚗 Hiraj Al Sayarat Al Jadeed")

st.markdown(
    """
    ### New & Used Cars in Makkah
    ### سيارات جديدة ومستعملة في مكة
    """
)

st.info(
    "📍 Wali Al Ahad Al Ukayshiyah, Makkah | "
    "📞 +966543346930"
)

# =========================
# MENU
# =========================
menu = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Inventory",
        "Compare Cars",
        "Finance Calculator",
        "Book Test Drive",
        "Contact"
    ]
)

if st.session_state.logged_in:

    if st.session_state.role == "admin":
        menu = st.sidebar.radio(
            "Navigation",
            [
                "Home",
                "Inventory",
                "Finance Calculator",
                "Book Test Drive",
                "Contact",
                "Admin Dashboard"
            ]
        )

    elif st.session_state.role == "sales":
        menu = st.sidebar.radio(
            "Navigation",
            [
                "Home",
                "Inventory",
                "Finance Calculator",
                "Book Test Drive",
                "Contact",
                "Sales Dashboard"
            ]
        )

# =========================
# HOME PAGE
# =========================
if menu == "Home":

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
# =========================
# INVENTORY
# =========================
elif menu == "Inventory":

    st.header("Vehicle Inventory")

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

                sst.markdown(
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
            # =========================
# COMPARE CARS
# =========================
elif menu == "Compare Cars":

    st.header("🚗 Compare Vehicles")

    cursor.execute(
        "SELECT id, brand, model FROM cars"
    )

    vehicle_list = cursor.fetchall()

    options = [
        f"{v[0]} - {v[1]} {v[2]}"
        for v in vehicle_list
    ]

    car1 = st.selectbox(
        "Select Vehicle 1",
        options,
        key="car1"
    )

    car2 = st.selectbox(
        "Select Vehicle 2",
        options,
        key="car2"
    )

    if st.button("Compare"):

        id1 = int(car1.split(" - ")[0])
        id2 = int(car2.split(" - ")[0])

        cursor.execute(
            "SELECT * FROM cars WHERE id=?",
            (id1,)
        )

        c1 = cursor.fetchone()

        cursor.execute(
            "SELECT * FROM cars WHERE id=?",
            (id2,)
        )

        c2 = cursor.fetchone()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                f"{c1[1]} {c1[2]}"
            )

            if c1[11]:
                st.image(
                    c1[11],
                    use_container_width=True
                )

            st.write(
                f"Price: {c1[5]:,} SAR"
            )

            st.write(
                f"Year: {c1[3]}"
            )

            st.write(
                f"Engine: {c1[6]}"
            )

            st.write(
                f"Fuel: {c1[8]}"
            )

        with col2:

            st.subheader(
                f"{c2[1]} {c2[2]}"
            )

            if c2[11]:
                st.image(
                    c2[11],
                    use_container_width=True
                )

            st.write(
                f"Price: {c2[5]:,} SAR"
            )

            st.write(
                f"Year: {c2[3]}"
            )

            st.write(
                f"Engine: {c2[6]}"
            )

            st.write(
                f"Fuel: {c2[8]}"
            )
# =========================
# FINANCE CALCULATOR
# =========================
elif menu == "Finance Calculator":

    st.header("Finance Calculator")

    price = st.number_input(
        "Vehicle Price (SAR)",
        min_value=0
    )

    down_payment = st.number_input(
        "Down Payment",
        min_value=0
    )

    months = st.number_input(
        "Months",
        min_value=1
    )

    if st.button("Calculate"):

        remaining = price - down_payment

        interest = remaining * 0.05

        monthly = (
            remaining + interest
        ) / months

        st.info(
            f"Total Finance Amount: "
            f"{remaining + interest:,.2f} SAR"
        )

        st.success(
            f"Monthly Payment: "
            f"{monthly:,.2f} SAR"
        )
# =========================
# TEST DRIVE
# =========================
elif menu == "Book Test Drive":

    st.header("Book Test Drive")

    name = st.text_input("Name")
    phone = st.text_input("Phone")

    cursor.execute(
        "SELECT brand, model FROM cars"
    )

    cars = cursor.fetchall()

    options = [
        f"{c[0]} {c[1]}"
        for c in cars
    ]

    selected_car = st.selectbox(
        "Vehicle",
        options
    )

    date = st.date_input("Date")
    time = st.time_input("Time")

    if st.button("Book Now"):

        cursor.execute(
            """
            INSERT INTO bookings
            (name,phone,car,date,time)
            VALUES (?,?,?,?,?)
            """,
            (
                name,
                phone,
                selected_car,
                str(date),
                str(time)
            )
        )

        conn.commit()

        st.success(
            "Test Drive Booked Successfully"
        )

# =========================
# CONTACT
# =========================
elif menu == "Contact":

    st.header("📞 Contact Us")

    st.success(
        "🚗 Hiraj Al Sayarat Al Jadeed"
    )

    st.write(
        "📍 Wali Al Ahad Al Ukayshiyah, Makkah"
    )

    st.write(
        "📞 +966543346930"
    )

    st.link_button(
        "📱 WhatsApp",
        "https://wa.me/966543346930"
    )
# =========================
# ADMIN DASHBOARD
# =========================
elif menu == "Admin Dashboard":

    st.header("🛠 Admin Dashboard")

    # Analytics
    cursor.execute("SELECT COUNT(*) FROM cars")
    total_cars = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    c1, c2 = st.columns(2)

    with c1:
        st.metric("🚗 Total Vehicles", total_cars)

    with c2:
        st.metric("📅 Total Bookings", total_bookings)

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ Add Vehicle",
            "🚗 Manage Vehicles",
            "📅 Bookings"
        ]
    )

    # =========================
    # ADD VEHICLE
    # =========================
    with tab1:

        st.subheader("Add New Vehicle")

        brand = st.text_input("Brand")

        model = st.text_input("Model")

        year = st.number_input(
            "Year",
            min_value=2000,
            max_value=2035,
            value=2025
        )

        condition = st.selectbox(
            "Condition",
            ["New", "Used"]
        )

        price = st.number_input(
            "Price (SAR)",
            min_value=0
        )

        engine = st.text_input(
            "Engine"
        )

        transmission = st.selectbox(
            "Transmission",
            [
                "Automatic",
                "Manual"
            ]
        )

        fuel = st.selectbox(
            "Fuel Type",
            [
                "Petrol",
                "Diesel",
                "Hybrid",
                "Electric"
            ]
        )

        color = st.text_input(
            "Color"
        )

        stock = st.number_input(
            "Stock",
            min_value=0,
            value=1
        )

        image_url = st.text_input(
            "Image URL"
        )

        description = st.text_area(
            "Description"
        )

        if st.button("Add Vehicle"):

            cursor.execute(
                """
                INSERT INTO cars
                (
                    brand,
                    model,
                    year,
                    condition,
                    price,
                    engine,
                    transmission,
                    fuel_type,
                    color,
                    stock,
                    image_url,
                    description
                )
                VALUES
                (
                    ?,?,?,?,?,?,?,?,?,?,?,?
                )
                """,
                (
                    brand,
                    model,
                    year,
                    condition,
                    price,
                    engine,
                    transmission,
                    fuel,
                    color,
                    stock,
                    image_url,
                    description
                )
            )

            conn.commit()

            st.success(
                "✅ Vehicle Added Successfully"
            )

            st.rerun()

    # =========================
    # MANAGE VEHICLES
    # =========================
    with tab2:

        st.subheader("Manage Vehicles")

        cursor.execute(
            "SELECT * FROM cars ORDER BY id DESC"
        )

        cars = cursor.fetchall()

        if not cars:
            st.info("No vehicles available.")

        for car in cars:

            col1, col2 = st.columns([5, 1])

            with col1:

                st.write(
                    f"""
                    ID: {car[0]}
                    | {car[1]} {car[2]}
                    | {car[5]:,} SAR
                    """
                )

            with col2:

                if st.button(
                    "❌ Delete",
                    key=f"delete_{car[0]}"
                ):

                    cursor.execute(
                        "DELETE FROM cars WHERE id=?",
                        (car[0],)
                    )

                    conn.commit()

                    st.success(
                        f"Vehicle {car[0]} deleted"
                    )

                    st.rerun()

    # =========================
    # BOOKINGS
    # =========================
    with tab3:

        st.subheader("Test Drive Bookings")

        cursor.execute(
            "SELECT * FROM bookings ORDER BY id DESC"
        )

        bookings = cursor.fetchall()

        if not bookings:
            st.info(
                "No bookings yet."
            )

        for booking in bookings:

            st.write(
                booking
            )

# =========================
# SALES DASHBOARD
# =========================
elif menu == "Sales Dashboard":

    st.header("Sales Dashboard")

    cursor.execute(
        "SELECT COUNT(*) FROM bookings"
    )

    bookings = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM cars"
    )

    cars = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Cars",
            cars
        )

    with col2:
        st.metric(
            "Bookings",
            bookings
        )
        st.markdown("""
<a href="https://wa.me/966543346930" target="_blank">
<button style="
position:fixed;
bottom:20px;
right:20px;
background:#25D366;
color:white;
padding:15px;
border:none;
border-radius:50px;
font-size:18px;
cursor:pointer;
z-index:999;">
WhatsApp
</button>
</a>
""", unsafe_allow_html=True)
        
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
WhatsApp
</div>
</a>
""", unsafe_allow_html=True)