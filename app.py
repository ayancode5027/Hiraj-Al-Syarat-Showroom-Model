import streamlit as st
from database import conn, cursor
from auth import login, create_default_users
from pages.compare import show_compare
from translations import LANG
from pages.home import show_home
from pages.inventory import show_inventory
from pages.finance import show_finance
from pages.admin import show_admin
from pages.salesperson import show_salesperson


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Hiraj Al Sayarat Al Jadeed",
    page_icon="🚗",
    layout="wide"
)
# =========================
# GOLD + SILVER THEME
# =========================
st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #f5f5f5,
        #e8e8e8
    );
}

h1,h2,h3{
    color:#1a1a1a;
}

div[data-testid="stMetric"]{
    background:white;
    border:2px solid #D4AF37;
    border-radius:15px;
    padding:15px;
}

.stButton>button{
    background:#D4AF37;
    color:black;
    border:none;
    border-radius:10px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#C0C0C0;
    color:black;
}

div[data-testid="stImage"] img{
    border-radius:15px;
    border:3px solid #D4AF37;
}

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
   show_home()
# =========================
# INVENTORY
# =========================
elif menu == "Inventory":
     show_inventory()
# =========================
# COMPARE CARS
# =========================
elif menu == "Compare Cars":
     show_compare()
# =========================
# FINANCE CALCULATOR
# =========================
elif menu == "Finance Calculator":
     show_finance()
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

    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#D4AF37,#C0C0C0);
        padding:30px;
        border-radius:20px;
        text-align:center;
        color:black;
        font-weight:bold;
        box-shadow:0 4px 15px rgba(0,0,0,0.2);
    ">
        <h1>🚗 Hiraj Al Sayarat Al Jadeed</h1>
        <h3>Premium New & Used Cars in Makkah</h3>
        <h3>سيارات جديدة ومستعملة في مكة</h3>
        <hr>
        <h3>📍 Wali Al Ahad Al Ukayshiyah, Makkah</h3>
        <h3>📞 +966543346930</h3>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.link_button(
        "📱 Contact on WhatsApp",
        "https://wa.me/966543346930"
    )

    st.write("")

    st.success(
        "We are available for new cars, used cars, financing assistance, and test drives."
    )

    st.success(
        "نحن متاحون للسيارات الجديدة والمستعملة وخدمات التمويل وحجوزات التجربة."
    )
# =========================
# ADMIN DASHBOARD
# =========================
elif menu == "Admin Dashboard":
     show_admin()

# =========================
# SALES DASHBOARD
# =========================
elif menu == "Sales Dashboard":
     show_salesperson()