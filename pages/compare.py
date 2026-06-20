import streamlit as st
from database import cursor

def show_compare():
   
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