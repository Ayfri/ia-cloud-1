import streamlit as st
import joblib

model = joblib.load("output/regression.joblib")

def display_3_forms():
    size = st.number_input("Size of the house (in sqft):", min_value=100, max_value=10000, value=1500, step=50)
    nb_rooms = st.number_input("Number of rooms:", min_value=1, max_value=20, value=3, step=1)
    garden = st.selectbox("Garden (1 for Yes, 0 for No):", options=[0, 1], index=1)

    if st.button("Predict Price"):
        input_data = [[size, nb_rooms, garden]]
        predicted_price = model.predict(input_data)
        st.success(f"The predicted price of the house is: ${predicted_price[0]:,.2f}")

st.title("House Price Prediction")
st.write("Enter the details of the house below to predict its price.")
display_3_forms()
