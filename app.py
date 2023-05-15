import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import pickle
import xgboost as xgb
from sklearn.metrics import precision_score
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import accuracy_score
import pickle
import plotly.express as px
import plotly.graph_objects as go
import base64
import streamlit as st
from PIL import Image



# Loading the model and the associated data
dfd_rolling = pd.read_csv('data/dfd_rolling.csv')

[combined, precision_weight, precision_raw, XGB_model, trim_features, df_rolling] = pickle.load(open('data/appData.pkl', 'rb'))

selected_columns = ['team','venue','opponent','venue_code','opp_code','hour','day_code',
 'gls_rolling','sh_rolling','sot_rolling','sot%_rolling','g/sh_rolling',
 'pk_rolling','pkatt_rolling','gls_opp_rolling','sh_opp_rolling','sot_opp_rolling',
 'sot%_opp_rolling','g/sh_opp_rolling','pk_opp_rolling','pkatt_opp_rolling','sota_rolling',
 'saves_rolling','cs_rolling','pka_rolling','pksv_rolling','pkm_rolling','sota_opp_rolling',
 'saves_opp_rolling','save%_opp_rolling','cs_opp_rolling','pka_opp_rolling','pksv_opp_rolling',
 'pkm_opp_rolling','ast_rolling','ast_opp_rolling','crs_rolling','crs_opp_rolling','tklw_rolling',
 'int_rolling','tkl+int_rolling','tklw_opp_rolling','int_opp_rolling','tkl+int_opp_rolling',
 'poss_x_rolling','poss_opp_rolling','crdy_rolling','crdr_rolling','2crdy_rolling', 'fls_rolling',
 'og_rolling','crdy_opp_rolling','crdr_opp_rolling','2crdy_opp_rolling','fls_opp_rolling',
 'og_opp_rolling','gf_rolling', 'gf_opp_rolling', 'round_code', 'comp_code']


########### TITLE PART ############################
# Title, title image and introductory explanation
st.title('Champions League Match Prediction')
# resizing gif
file_ = open("img/animation2.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="football gif">',unsafe_allow_html=True,)
st.caption('Animation curtsey of [mplsoccer](https://mplsoccer.readthedocs.io/en/latest/index.html) and [metrica-sports](https://metrica-sports.com/)', unsafe_allow_html=False)
st.markdown("""
A **hypothetical** sports channel has asked us to develop a webapp that they can refer to during their broadcasts. The
brief includes using the statistics obtained in the previous matches and predict weather a team will win a future match given a certain opponent.

This app uses a trained [random forrest model](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) to predict champions league matches. The features used to make
this prediction are engineered from statistics available before the match. 

To operate, choose the team and the opponent as well as the venue form the side bar. Then hit the "Predict Match" button.

Before the prediction some handy comparison between the selected team and opponent are given using normalised team statistics.""")

st.caption('Data Source: All data is scraped from [FBref](https://fbref.com/en/comps/8/Champions-League-Stats)', unsafe_allow_html=True)


###################### SIDEBAR##############################
st.sidebar.header('User Input Features')
selected_team = st.sidebar.selectbox('Team',dfd_rolling [dfd_rolling['season']=='2022-2023']['team'].unique()) # select your team

selected_opponent = st.sidebar.selectbox('Opponent', dfd_rolling [dfd_rolling['season']=='2022-2023']['team'].unique()) # Select opponent (not any opponent but Champions League opponent)

if selected_team == selected_opponent:
    st.sidebar.markdown("**Team and opponent must be DIFFERENT!**") # Selection check
selected_venue = st.sidebar.selectbox('Venue', dfd_rolling["venue"].unique()) # choose home or away
if selected_venue == 'home':
    v_code = 1
else:
    v_code = 0
# Pressing the Predict button both prediction as well as the plots are shown
if st.sidebar.button('Predict Match'):
    if selected_team == selected_opponent:
        st.markdown("**Team and opponent must be DIFFERENT!**") # Selection check
    else:
        st.header("Comparative Statistics")
        st.write("""This section presents a comprehensive comparison between the performance statistics between the teams.
        the presented data is averaged over the last 3 games for each team and normalised""")
        ########### DISPLAY PART ###################
        #Preparing the comparative data for display 
        tm_dfd = dfd_rolling[dfd_rolling['team'] == selected_team].tail(1) # get the last game row for the team. has the latest rolling stats.
        opp_dfd = dfd_rolling[dfd_rolling['team'] == selected_opponent].tail(1)
        # Setting up Display metrics
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
        #Function to plot the radar plots
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
TotDist-rolling -- Rolling average of total Passing Distance\n
PrgDist-rolling -- Rolling average of progressive Passing Distance\n
KP-rolling -- Rolling average of key Passes that directly lead to a shot (assisted shots)\n
PPA-rolling -- Rolling average of passes into Penalty Area Completed passes into the 18-yard box Not including set pieces\n
CrsPA-rolling -- Rolling average of crosses into Penalty Area Completed crosses into the 18-yard box Not including set pieces\n
PrgP-rolling -- Rolling average of progressive Passes
''')

# Plotting the Goal and Shot Creation
        plot_comparison(tm_dfd,opp_dfd,goal_and_shot,selected_team, selected_opponent, 'Goal and Shot Creation')
        expander = st.expander("**Glossary**")
        expander.markdown('''
SCA-rolling -- Rolling average of Shot-Creating Actions\n
PassLive-rolling -- SCA (PassLive) Rolling average of Completed live-ball passes that lead to a shot attempt\n
Fld-rolling -- SCA (Fld) Rolling average of Fouls drawn that lead to a shot attempt\n
TO-rolling -- GCA (TO) Rolling average of Successful take-ons that lead to a goal\n
Def-rolling -- SCA (Def) Rolling average of Defensive actions that lead to a shot attempt\n
PassDead-rolling -- SCA (PassDead) Rolling average of Completed dead-ball passes that lead to a shot attempt.\n
''')

#Plotting Defensive Action
        plot_comparison(tm_dfd,opp_dfd,defence,selected_team, selected_opponent, 'Defensive Actions')
        expander = st.expander("**Glossary**")
        expander.markdown('''
TklW-rolling -- Rolling average of Tackles Won Tackles in which the tackler's team won possession of the ball\n
Def 3rd-rolling -- Rolling average of Tackles (Def 3rd) Tackles in defensive 1/3\n
Mid 3rd-rolling -- Rolling average of Tackles (Mid 3rd) Tackles in middle 1/3\n
Att 3rd-rolling -- Rolling average of Tackles (Att 3rd) Tackles in attacking 1/3\n
Tkl%-rolling -- Rolling average of % of dribblers tackled Percentage of dribblers tackled Dribblers tackled divided by number of attempts to challenge an opposing dribbler\n
Lost-rolling -- Rolling average of Challenges Lost Number of unsuccessful attempts to challenge a dribbling player
''')

#Plotting Possession
        plot_comparison(tm_dfd,opp_dfd,possession,selected_team, selected_opponent, 'Possession')
        expander = st.expander("**Glossary**")
        expander.markdown('''
Poss-rolling -- Rolling average of Possession Calculated as the percentage of passes attempted\n
Touches-rolling -- Rolling average of Number of times a player touched the ball.\n
Succ%-rolling -- Rolling average of Successful Take-On %Percentage of Take-Ons Completed Successfully\n
Tkld%-rolling -- Rolling average of Tackled During Take-On Percentage Percentage of time tackled by a defender during a take-on attempt Minimum .5 take-ons per squad game to qualify as a leader\n
rgC-rolling -- Rolling average of Progressive Carries Carries that move the ball towards the opponent's goal line at least 10 yards from its furthest point in the last six passes, or any carry into the penalty area. Excludes carries which end in the defending 50% of the pitch\n
PrgR-rolling -- Rolling average of Progressive Passes Rec Progressive Passes Received Completed passes that move the ball towards the opponent's goal line at least 10 yards from its furthest point in the last six passes, or any completed pass into the penalty area. Excludes passes from the defending 40% of the pitch
''')
############### PREDICTION ##############################################
        def infer(selected_team,selected_opponent, v_code, data, model,features): #inference function, returns 0, 1, 2 for loss, win and draw
            '''Procedure for inference:
                - Get the features and split in two based on if they are for the home team or opposing team (f_h and f_opp)
                - Get the latest match of the team in the dataframe, and select the features orm the hoe team.
                - We need ot construct th eopposing team sub-dataframe to feed for inference. We need to now select the opposing team as home team (like above), change the feature names and take the "_opp" out, and find out the features for the opposing team. We then need to add those in the place of the opposing team features. 
                - This way when we flip the teams, the opposing and home teams will be flipped and we would not make a mistake again. 
            '''
            # split the features to home and opposing
            f_h = [f for f in features if "_opp" not in f] #Home team features
            f_opp = [f for f in features if "_opp" in f] #Opposing team features
            # Note that the opposing team features, for inference have to be the team features where the team is the opposing team.
            f_opp_p = [s.replace('_opp','') for s in f_opp] #opposing team features processed.
            ## Setting up the data to be fed into the model.
            hm_df = data[data['team'] == selected_team].tail(1) # get the last game row for the home team. It has the latest rolling stats.
            hm_df = hm_df[f_h].copy()
            # Get the stats for th eopposing team
            op_df = data[data['team'] == selected_opponent].tail(1) # Get the last game for the selected opponent, latest rolling stats
            op_df = op_df[f_opp_p].copy()
            # construcing the inference dataframe
            infer_df = hm_df
            infer_df[f_opp] = op_df.values #Placing the values we extracted for the opposing team under the correct column names in the infer dataframe
            infer_df['opp_code'] = int(data[data['opponent']==selected_opponent]['opp_code'].head(1)) # Adding the correct opp_code 
            infer_df['venue_code'] = v_code # adding the correct venue code (home away, 1,0)
            print(infer_df)
            inference = model.predict(infer_df[features])
            return inference   

        ## Prediction Display
        st.header("Game Prediction")
        inference = infer(selected_team,selected_opponent, v_code,df_rolling, XGB_model, trim_features)
        if inference == 1:
            st.write(selected_team ,""" will **WIN** the match""")
        else:
            st.write(selected_team ,"""  will **NOT WIN** the match""")

        st.markdown(""" A trained XGBoot model is used to make this prediction, and rolling averages for 
                        the performance in past five games for each of the teams have been considered.""")


        # Plotting Fature Importances
        fig, ax = plt.subplots()
        xgb_imp = pd.Series(XGB_model.get_booster().get_score(importance_type= 'gain'))
        xgb_imp = xgb_imp/len(trim_features)
        # Sort importances
        xgb_imp_sorted = xgb_imp.sort_values()
        # Draw a horizontal barplot of importances_sorted
        xgb_imp_sorted.plot(kind='barh', color='blue', figsize = (5,10), grid = True, xlabel = 'Feature Importances')
        plt.title('Feature Importance for XGBoost Algorithem')
        st.pyplot(fig)

        '''The glossary for the top 5 most important parameters are given below:'''
        expander = st.expander("**Glossary**")
        expander.markdown('''
        sota_rolling -- Rolling average of shots on target against\n
        gls_rolling -- Rolling average of goals\n
        poss_opp_rolling -- Rolling average of opposition possesion\n
        sot_rolling	-- Rolling average of shots on target\n
        poss_x_rolling-- ROlling average of posession\n
        ''')
        
        '''Here is the trained model confusion matrix:'''
        # plotting Confusion Matrix
        table = pd.crosstab(index=combined["actual"], columns=combined["predicted"])
        #Have to divide by the sum of each row to maintain consistancy with the random forrest confusion matrix plots. 
        table = table.div(table.sum(axis=1), axis = 0)
        fig = px.imshow(table, color_continuous_scale='blues', text_auto=True, x = ['won', 'not won'], y = ['won','not won'])
        st.plotly_chart(fig)

        '''We can also get a graph representation of the XGBtree:'''
        image = Image.open('img/XGBoost_Tree.jpg')
        st.image(image, caption='XGBoost Tree')