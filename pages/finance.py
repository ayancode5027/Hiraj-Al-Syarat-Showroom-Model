
import streamlit as st
from database import cursor


def show_finance():

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
