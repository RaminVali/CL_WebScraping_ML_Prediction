import pandas as pd
import pickle
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go
import plotly.offline as pyo

# Loading the model and the associated data
[predictors3, df_rolling, rf, importances,dfd_rolling] = pickle.load(open('appData.pkl', 'rb'))

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



# Title, title image and introductory explanation
st.title('Champions League Match Prediction')
st.image('image.jpg')
st.caption('Photo by Timothy Tan on Unsplash', unsafe_allow_html=False)

st.markdown("""
A **hypothetical** sports channel has asked us to develop a webapp that they can refer to during their broadcasts. The
brief includes using the statistics obtained in the previous matches and predict weather a team will win a future match given a certain opponent.

This app uses a trained [random forrest model](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) to predict champions league matches. The features used to make
this prediction are engineered from statistics available before the match. 

After the prediction some handy comparison between the selected team and opponent are given using normalised team statistics.""")

st.caption('Data Source: All data is scraped from [FBref](https://fbref.com/en/comps/8/Champions-League-Stats)', unsafe_allow_html=True)



# Sidebar
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

## Setting up the data to be fed into the model.
tm_df = df_rolling[df_rolling['team'] == selected_team].tail(1) # get the last game row for the team. It has the latest rolling stats.
tm_df = tm_df[selected_columns]

tm_df['opp_code'] = int(df_rolling[df_rolling['opponent']==selected_opponent]['opp_code'].head(1))
tm_df['opponent'] = selected_opponent
tm_df['venue'] = selected_venue
tm_df['venue_code'] = v_code

#Preparing the comparative data for display 
tm_dfd = dfd_rolling[dfd_rolling['team'] == selected_team].tail(1) # get the last game row for the team. has the latest rolling stats.
opp_dfd = dfd_rolling[dfd_rolling['team'] == selected_opponent].tail(1)


shooting = ["gls_rolling", "sh_rolling","sot_rolling","dist_rolling",'xg_x_rolling','fk_rolling']
shooting = [*shooting, shooting[0]]

goalkeeping = ['sota_rolling','saves_rolling','cs_rolling','cmp%_rolling','pksv_rolling','#opa_rolling']
goalkeeping = [*goalkeeping, goalkeeping[0]]

passing = ['totdist_rolling', 'prgdist_rolling', 'kp_rolling','ppa_rolling','crspa_rolling','prgp_rolling']
passing = [*passing, passing[0]]


goal_and_shot = ['sca_rolling','passlive_rolling','fld_rolling', 'to_opp_rolling', 'def_rolling','passdead_rolling']
goal_and_shot = [*goal_and_shot, goal_and_shot[0]]

defence = ['tklw_rolling','def 3rd_rolling','mid 3rd_rolling','att 3rd_rolling','tkl%_rolling','lost_rolling']
defence = [*defence, defence[0]]

possession = ['poss_x_rolling','touches_rolling','succ%_rolling','tkld%_rolling','prgc_rolling','prgr_rolling']
possession = [*possession, possession[0]]



# Function to plot the radar plots
def plot_comparison(tm_dfd,opp_dfd,metric,selected_team, selected_opponent, metric_name):
    fig = go.Figure(
    data=[
        go.Scatterpolar(r=tm_dfd[metric].values[0], theta=metric, name= selected_team, line=dict(color="blue", width = 4) ),
        go.Scatterpolar(r=opp_dfd[metric].values[0], theta=metric, name= selected_opponent, line=dict(color="red", width = 4)),
        ],

    layout=go.Layout(height = 600, width = 800,
        title=go.layout.Title(text=f'{metric_name} Stats Comparison'),
        polar={'radialaxis': {'visible': True}, 'angularaxis':{'tickfont':{'size':15}}},

        showlegend=True
                    )
                    )
    st.plotly_chart(fig)


# Pressing the Predict button both prediction as well as the plots are shown
if st.sidebar.button('Predict Match'):
    if selected_team == selected_opponent:
        st.markdown("**Team and opponent must be DIFFERENT!**") # Selection check
    else:
        st.header("Game Prediction")
        prediction = rf.predict(tm_df[predictors3])
        if prediction == 1:
            st.write(selected_team ,""" will **WIN** the match""")
        else:
            st.write(selected_team ,"""  will **NOT WIN** the match""")

        st.markdown(""" A trained random forrest model is used to make this prediction, and rolling averages for 
                        the performance in past five games for each of the teams have been considered.""")
        
        st.header("Comparative Statistics")
        st.write("""This section presents a comprehensive comparison between the performance statistics between the teams.
        the presented data is averaged oer the last 3 games for each team and normalised""")

# Plotting the Shooting Comparison

        plot_comparison(tm_dfd,opp_dfd,shooting,selected_team, selected_opponent, 'Shooting')
        expander = st.expander("**Glossary**")
        expander.markdown('''**gls-rolling** -- Rolling average of goals score\n
**sh-rolling** -- Rolling average of total shots\n
**sot-rolling** -- Rolling average of shots on target\n
**dist-rolling** -- Rolling average of shot distance\n
**xg-x-rolling** -- Rolling average of expected goals\n
**fk_rolling** -- Rolling average of free kicks
''')

# Plotting the Goal Keeping Comparison

        plot_comparison(tm_dfd,opp_dfd,goalkeeping,selected_team, selected_opponent, 'Gaol Keeping')
        expander = st.expander("**Glossary**")
        expander.markdown('''**#OPA-rolling** -- Rolling average of the number of defensive actions outside of penalty area\n
**sota-rolling** -- Rolling average of shots on target against\n
**saves-rolling** -- Rolling average of saves\n
**cs-rolling** -- Rolling average of clean sheets\n
**cmp%-rolling** -- Rolling average of pass completion percentage\n
**pksv_rolling** -- Rolling average of saved penalty kicks
''')


# Plotting the Passing Comparison 

        plot_comparison(tm_dfd,opp_dfd,passing,selected_team, selected_opponent, 'Passing')
        expander = st.expander("**Glossary**")
        expander.markdown('''
TotDist -- Total Passing Distance\n
PrgDist -- Progressive Passing Distance\n
KP -- Key Passes Passes that directly lead to a shot (assisted shots)\n
PPA -- Passes into Penalty Area Completed passes into the 18-yard box Not including set pieces\n
CrsPA -- Crosses into Penalty Area Completed crosses into the 18-yard box Not including set pieces\n
PrgP -- Progressive Passes
''')


# Plotting the Goal and Shot Creation
        plot_comparison(tm_dfd,opp_dfd,goal_and_shot,selected_team, selected_opponent, 'Goal and Shot Creation')
        expander = st.expander("**Glossary**")
        expander.markdown('''
SCA -- Shot-Creating Actions\n
PassLive -- SCA (PassLive) Completed live-ball passes that lead to a shot attempt\n
Fld -- SCA (Fld) Fouls drawn that lead to a shot attempt\n
TO -- GCA (TO) Successful take-ons that lead to a goal\n
Def -- SCA (Def) Defensive actions that lead to a shot attempt\n
PassDead -- SCA (PassDead) Completed dead-ball passes that lead to a shot attempt.\n
''')


#Plotting Defensive Action
        plot_comparison(tm_dfd,opp_dfd,defence,selected_team, selected_opponent, 'Defensive Actions')
        expander = st.expander("**Glossary**")
        expander.markdown('''
TklW -- Tackles Won Tackles in which the tackler's team won possession of the ball\n
Def 3rd -- Tackles (Def 3rd) Tackles in defensive 1/3\n
Mid 3rd -- Tackles (Mid 3rd) Tackles in middle 1/3\n
Att 3rd -- Tackles (Att 3rd) Tackles in attacking 1/3\n
Tkl% -- % of dribblers tackled Percentage of dribblers tackled Dribblers tackled divided by number of attempts to challenge an opposing dribbler\n
Lost -- Challenges Lost Number of unsucessful attempts to challenge a dribbling player
''')


#Plotting Possession

        plot_comparison(tm_dfd,opp_dfd,defence,selected_team, selected_opponent, 'Possession')
        expander = st.expander("**Glossary**")
        expander.markdown('''
Poss -- Possession Calculated as the percentage of passes attempted
Touches -- Number of times a player touched the ball.
Succ% -- Successful Take-On %Percentage of Take-Ons Completed Successfully
Tkld% -- Tackled During Take-On Percentage Percentage of time tackled by a defender during a take-on attempt Minimum .5 take-ons per squad game to qualify as a leader
rgC -- Progressive Carries Carries that move the ball towards the opponent's goal line at least 10 yards from its furthest point in the last six passes, or any carry into the penalty area. Excludes carries which end in the defending 50% of the pitch
PrgR -- Progressive Passes Rec
Progressive Passes Received Completed passes that move the ball towards the opponent's goal line at least 10 yards from its furthest point in the last six passes, or any completed pass into the penalty area. Excludes passes from the defending 40% of the pitch
''')

# To be implemented later

# importance = pd.Series(data=importances, index=  predictors3)
# # Sort importances
# importances_sorted = importance.sort_values()
# st.table(importances_sorted)

# plt.figure(figsize=(5,20))
# plt.subplots_adjust(top = 1, bottom = 0)
# importances_sorted.plot(kind='barh', color='red')
# col1.pyplot(plt)
# st.table(importance)

# importances_sorted.plot(kind='barh', color='blue')









