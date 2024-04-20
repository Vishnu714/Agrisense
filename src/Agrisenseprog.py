import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
# Load your dataset
df = pd.read_csv('yield_df.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)

# Calculate yield per country
yield_per_country = df.groupby('Area')['hg/ha_yield'].sum()

# Calculate yield per item
yield_per_item = df.groupby('Item')['hg/ha_yield'].sum()

# Function to create interactive map for selected crop
def create_map_for_crop(crop):
    crop_df = df[df['Item'] == crop]
    
    fig = px.scatter_geo(crop_df, locations='Area', locationmode='country names', 
                         hover_name='Area',color='hg/ha_yield',
                         projection="mercator", size='hg/ha_yield')
    
    fig.update_geos(showcountries=True)
    fig.update_layout(title=f"Crop Distribution: {crop}", 
                      geo=dict(showland=True, landcolor="#B4CADE"),
                      width=1000,  # Adjust width
                      height=1000)  # Adjust height
    
    return fig

#ai ml
col=['Year','average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp', 'Area' , 'Item', 'hg/ha_yield']
df=df[col]
df.drop_duplicates(inplace=True)
X=df.drop('hg/ha_yield', axis=1)
y=df['hg/ha_yield']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)#20%data goes for test and 80% goes for train
ohe=OneHotEncoder(drop='first')
scaler=StandardScaler()
preprocessor=ColumnTransformer(
transformers=[
    ('onehotencoder', ohe,[4,5]),
    ('standardization', scaler, [0,1,2,3])
],
remainder='passthrough'
)
X_train_dummy=preprocessor.fit_transform(X_train)
X_test_dummy=preprocessor.transform(X_test)

dtr=DecisionTreeRegressor()
dtr.fit(X_train_dummy,y_train)
dtr.predict(X_test_dummy)

def prediction(Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area, Item):
    
    features=np.array([[Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area, Item]])
    transformed_features=preprocessor.transform(features)
    predicted_value=dtr.predict(transformed_features).reshape(1,-1)
    return predicted_value[0]

# Define main function
def main():
    st.title("AgriSense")
    st.sidebar.markdown('<h1 style="color: #71c33b;">Crop Selection</h1>', unsafe_allow_html=True)

    # Create crop selection dropdown in the sidebar
    selected_crop = st.sidebar.selectbox("Select Crop", df['Item'].unique())

    # Show map for selected crop
    fig = create_map_for_crop(selected_crop)
    st.plotly_chart(fig)
    
    st.sidebar.markdown('<h2 style="color: #71c33b;">Yield per Country</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Yield per Country"):
        st.bar_chart(yield_per_country)

    st.sidebar.markdown('<h2 style="color: #71c33b;">Yield per Item</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Yield per Item"):
        st.bar_chart(yield_per_item)

    st.sidebar.markdown('<h2 style="color: #71c33b;">Frequency of Area</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Frequency of Area"):
        st.bar_chart(df['Area'].value_counts())

    st.sidebar.markdown('<h2 style="color: #71c33b;">Frequency of Items</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Frequency of Items"):
        st.bar_chart(df['Item'].value_counts())

    st.markdown('<h2 style="color: #71c33b;">Yield Prediction</h2>', unsafe_allow_html=True)
    Year = st.number_input("Year", value=2000)
    average_rain_fall_mm_per_year = st.number_input("Average Rainfall (mm/year)")
    pesticides_tonnes = st.number_input("Pesticides (tonnes)")
    avg_temp = st.number_input("Average Temperature")
    Area = st.selectbox("Area", df['Area'].unique())
    print(type(Area))
    Item = st.selectbox("Item", df['Item'].unique())
    print(type(Item))
    if st.button("Predict Yield"):
        # Make prediction
        predicted_yield = prediction(Year,average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area, Item)
        st.title("Yield")
        st.markdown(f'<h3 style="color: #71c33b;">{predicted_yield}</h1>', unsafe_allow_html=True)
        

if __name__ == "__main__":
    main()
