import pandas as pd
import pickle
import streamlit as st
from PIL import Image

from sklearn.ensemble import RandomForestClassifier


[predictors, df, rf_bal_sub] = pickle.load(open('appData.pkl', 'rb'))


image = Image.open('CL.png')



st.image(image, width=10)

st.title('Champions League')