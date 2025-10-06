import streamlit as st
import pickle
import pandas as pd

# Load the trained GradientBoost model
with open("GradientBoost_model_new.pkl", "rb") as f:
    model = pickle.load(f)

# Ordinal encoding mappings using enumerate
Fuel_Type = dict(enumerate(['Cng', 'Diesel', 'Electric', 'Lpg', 'Petrol'], start=0))
Fuel_Type = {v: float(k) for k, v in Fuel_Type.items()}

Transmission_Type = dict(enumerate(['Automatic', 'Manual'], start=0))
Transmission_Type = {v: float(k) for k, v in Transmission_Type.items()}

Manufactured_By = dict(enumerate([
    'Audi', 'BMW', 'Chevrolet', 'Citroen', 'Datsun', 'Fiat', 'Ford',
    'Hindustan Motors', 'Honda', 'Hyundai', 'Isuzu', 'Jaguar', 'Jeep',
    'Kia', 'Land Rover', 'Lexus', 'MG', 'Mahindra', 'Mahindra Renault',
    'Mahindra Ssangyong', 'Maruti', 'Mercedes-Benz', 'Mini', 'Mitsubishi',
    'Nissan', 'Porsche', 'Renault', 'Skoda', 'Tata', 'Toyota', 'Volkswagen', 'Volvo'
], start=0))
Manufactured_By = {v: float(k) for k, v in Manufactured_By.items()}

Car_Model = dict(enumerate([
    'Ambassador', 'Audi A3', 'Audi A3 cabriolet', 'Audi A4', 'Audi A6',
    'Audi A8', 'Audi Q2', 'Audi Q3', 'Audi Q3 Sportback', 'Audi Q5',
    'Audi Q7', 'Audi S5 Sportback', 'BMW 1 Series', 'BMW 2 Series',
    'BMW 3 Series', 'BMW 3 Series GT', 'BMW 3 Series Gran Limousine',
    'BMW 5 Series', 'BMW 6 Series', 'BMW 7 Series', 'BMW X1', 'BMW X3',
    'BMW X4', 'BMW X5', 'BMW X7', 'Chevrolet Aveo', 'Chevrolet Beat',
    'Chevrolet Captiva', 'Chevrolet Cruze', 'Chevrolet Enjoy',
    'Chevrolet Optra', 'Chevrolet Sail', 'Chevrolet Spark',
    'Chevrolet Tavera', 'Citroen C3', 'Citroen C5 Aircross', 'Datsun GO',
    'Datsun GO Plus', 'Datsun RediGO', 'Fiat Abarth Avventura',
    'Fiat Avventura', 'Fiat Grande Punto', 'Fiat Linea', 'Fiat Palio',
    'Fiat Punto', 'Fiat Punto Abarth', 'Fiat Punto EVO', 'Fiat Punto Pure',
    'Ford Aspire', 'Ford Ecosport', 'Ford Endeavour', 'Ford Fiesta',
    'Ford Fiesta Classic', 'Ford Figo', 'Ford Freestyle', 'Ford Ikon',
    'Ford Mondeo', 'Hindustan Motors Contessa', 'Honda Amaze'
], start=0))
Car_Model = {v: float(k) for k, v in Car_Model.items()}

Location = dict(enumerate(['Bangalore', 'Chennai', 'Hyderabad', 'Jaipur', 'Kolkata', 'delhi'], start=0))
Location = {v: float(k) for k, v in Location.items()}

def inv_trans(x):
    return 1 / x if x != 0 else 0

# Streamlit UI
st.title("Car Price Prediction 🚗💰")
st.write("Enter car details below:")

kilometers_driven = st.number_input("Kilometers Driven", min_value=0)
transmission_type = st.selectbox("Transmission Type", list(Transmission_Type.keys()))
car_model = st.selectbox("Car Model", list(Car_Model.keys()))
car_produced_year = st.number_input("Car Produced Year", min_value=1900, max_value=2024, step=1)
engine_cc = st.number_input("Engine CC", min_value=0)
mileage_kmpl = st.number_input("Mileage (kmpl)", min_value=0.0)
location = st.selectbox("Location", list(Location.keys()))

if st.button("Predict Price"):
    # Preprocess the input data
    input_data = pd.DataFrame({
        'Kilometers_Driven': [inv_trans(kilometers_driven)],
        'Transmission_Type': [Transmission_Type[transmission_type]],
        'Car_Model': [Car_Model[car_model]],
        'Car_Produced_Year': [car_produced_year],
        'Engine_CC': [engine_cc],
        'Mileage(kmpl)': [mileage_kmpl],
        'Location': [Location[location]]
    })

    # Make prediction
    predicted_price = model.predict(input_data)[0]


    st.success(f"Predicted Car Price: ₹ {predicted_price:,.2f}")