import pandas as pd
import pickle
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier

import plotly.graph_objects as go
import plotly.offline as pyo

[predictors3, df_rolling, rf, importances,dfd_rolling] = pickle.load(open('appData.pkl', 'rb'))



st.title('Champions League Match Prediction')
st.image('image.jpg')
st.caption('Photo by Timothy Tan on Unsplash', unsafe_allow_html=False)

st.markdown("""
This app is developed for a **hypothetical** sports channel that will use the predictions in their sports programme.

This app uses a trained random forrest model to predict champions league matches. The features used to make
this prediction are engineered from statistics available before the match. 

- Data Source: All data is scrapped from [FBref](https://fbref.com/en/comps/8/Champions-League-Stats)

""")

# Side bar stuff

st.sidebar.header('User Input Features')
selected_team = st.sidebar.selectbox('Team',df_rolling [df_rolling['season']=='2022-2023']['team'].unique()) # select your team

selected_opponent = st.sidebar.selectbox('Opponent', df_rolling [df_rolling['season']=='2022-2023']['team'].unique()) # Select opponent (not any opponent but Champions League opponent)

if selected_team == selected_opponent:
    st.sidebar.markdown("**Team and opponent must be DIFFERENT!**") # Selection check
selected_venue = st.sidebar.selectbox('Venue', df_rolling["venue"].unique()) # choose home or away
if selected_venue == 'home':
    v_code = 1
else:
    v_code = 0


selected_columns = ['team','venue','opponent','venue_code','opp_code','hour','day_code',
 'gf_rolling','gls_rolling','sh_rolling','sot_rolling','sot%_rolling','g/sh_rolling',
 'pk_rolling','pkatt_rolling','gf_opp_rolling','gls_opp_rolling','sh_opp_rolling','sot_opp_rolling',
 'sot%_opp_rolling','g/sh_opp_rolling','pk_opp_rolling','pkatt_opp_rolling','sota_rolling',
 'saves_rolling','cs_rolling','pka_rolling','pksv_rolling','pkm_rolling','sota_opp_rolling',
 'saves_opp_rolling','save%_opp_rolling','cs_opp_rolling','pka_opp_rolling','pksv_opp_rolling',
 'pkm_opp_rolling','ast_rolling','ast_opp_rolling','crs_rolling','crs_opp_rolling','tklw_rolling',
 'int_rolling','tkl+int_rolling','tklw_opp_rolling','int_opp_rolling','tkl+int_opp_rolling',
 'poss_x_rolling','poss_opp_rolling','crdy_rolling','crdr_rolling','2crdy_rolling', 'fls_rolling',
 'og_rolling','crdy_opp_rolling','crdr_opp_rolling','2crdy_opp_rolling','fls_opp_rolling',
 'og_opp_rolling','fls_rolling+sot%_rolling']

# Construct the dataframe to be fed into the model. 

tm_df = df_rolling[df_rolling['team'] == selected_team].tail(1) # get the last game row for the team. has the latest rolling stats.
tm_df = tm_df[selected_columns]

tm_df['opp_code'] = int(df_rolling[df_rolling['opponent']==selected_opponent]['opp_code'].head(1))
tm_df['opponent'] = selected_opponent
tm_df['venue'] = selected_venue
tm_df['venue_code'] = v_code

# st.table (tm_df['opp_code'])

# st.dataframe (tm_df)


# importance = pd.Series(data=importances, index=  predictors3)
# # Sort importances
# importances_sorted = importance.sort_values()
# st.table(importances_sorted)


if st.button('Predict Match'):
    if selected_team == selected_opponent:
        st.markdown("**Team and opponent must be DIFFERENT!**") # Selection check
    else:
        prediction = rf.predict(tm_df[predictors3])
        if prediction == 1:
            st.markdown(""" The selected team will **WIN** the match""")
        else:
            st.markdown(""" The selected team will **NOT WIN** the match""")

        st.markdown(""" A trained random forrest model is used to make this prediction, and rolling averages for 
                        the performance in past five games for each of the teams have been considered.""")

## DISPLAYNG STATS

shooting = ["gls_rolling", "sh_rolling","sot_rolling","dist_rolling",'xg_x_rolling']
shooting = [*shooting, shooting[0]]

st.table(dfd_rolling)
dfd_rolling['team']

tm_dfd = dfd_rolling[dfd_rolling['team'] == selected_team].tail(1) # get the last game row for the team. has the latest rolling stats.

opp_dfd = dfd_rolling[dfd_rolling['team'] == selected_opponent].tail(1)



if st.button("Compare Teams"):

    fig = go.Figure(
        data=[
            go.Scatterpolar(r=tm_dfd[shooting], theta=shooting, name= selected_team),
            go.Scatterpolar(r=opp_dfd[shooting], theta=shooting, name= selected_opponent),

        ],
        layout=go.Layout(
            title=go.layout.Title(text='team comparison'),
            polar={'radialaxis': {'visible': False}},
            showlegend=True
        )
    )

    pyo.plot(fig)









        #col1, col2, col3 = st.columns(3)
        # plt.figure(figsize=(5,20))
        # plt.subplots_adjust(top = 1, bottom = 0)
        # importances_sorted.plot(kind='barh', color='red')
        # col1.pyplot(plt)



        # st.table(importance)




        # importances_sorted.plot(kind='barh', color='blue')



# selected_hour = st.sidebar.selectbox('Match Hour', df_rolling["hour"].unique())
# selected_day = st.sidebar.selectbox('Match Day', df_rolling["day"].unique())



# with col1:
#     st.write(' ')

# with col2:
#     st.image('CL.png')

# with col3:
#     st.write('')