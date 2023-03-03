import pandas as pd
import pickle
import streamlit as st
from PIL import Image

from sklearn.ensemble import RandomForestClassifier


[predictors3, df_rolling, rf] = pickle.load(open('appData.pkl', 'rb'))




col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image('CL.png')

with col3:
    st.write('')



st.title('Champions League Match Prediction')

st.markdown("""
This app is developed for a **hypothetical** sports channel that will use the predictions in their sports programme.

This app uses a trained random forrest model to predict champions league matches. The features used to make
this prediction are engineered from statistics available before the match. 

- Data Source: All data is scrapped from [FBref](https://fbref.com/en/comps/8/Champions-League-Stats)

""")

st.sidebar.header('User Input Features')


selected_team = st.sidebar.selectbox('Team',df_rolling["team"].unique())

selected_opponent = st.sidebar.selectbox('Opponent', df_rolling["team"].unique())


if selected_team == selected_opponent:
    st.sidebar.markdown("**Team and opponent must be DIFFERENT**")


selected_venue = st.sidebar.selectbox('Venue', df_rolling["venue"].unique())
if selected_venue == 'home':
    v_code = 1
else:
    v_code = 0


# selected_hour = st.sidebar.selectbox('Match Hour', df_rolling["hour"].unique())
# selected_day = st.sidebar.selectbox('Match Day', df_rolling["day"].unique())


st.table (predictors3)


# tm_df = df_rolling[df_rolling['team'] == selected_team][predictors3].tail(1)



# predictions = rf.predict(test[predictors])







# importance = pd.Series(data=rf.feature_importances_
#                         index=  predictors+new_cols)
# # Sort importances
# importances_sorted = importance.sort_values()
# # Draw a horizontal barplot of importances_sorted
# importances_sorted.plot(kind='barh', color='blue')
# plt.title('Features Importances')
# plt.show()