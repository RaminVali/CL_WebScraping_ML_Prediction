# Predicting champions league matches using web data

## Motivation
A sports TV channel has asked us to come up with predictions for upcoming UEFA Champions League matches. They would like to know if a team is favoured to win or lose, and what are the main factors associated with the prediction. 

## Goal
In this project we scrape statistics tables for each Champions League season and try to predict the results of the future games using ML.

## Running the Project

- The model can be run visa webapp written in streamlit. Here is the [link]().

- To make the model and load the data yourself:
    - Clone the repository
    - Run the get data, this will take a whe as it avoids being banned. You can change the date range for your scraping. The notebook will save all the data in "all_seasons.csv"
    - The clean_predict notebook will clean and construct the M model and the finalised predictors. These are then fed int ot he webapp. 

The get_data notebook will scrape all the web for th stats in the game. Timing measures are implemented to avoid being banned by the website

Note: The cleanest way of implementing the get_data stage i.e. playwright usage would be to use in in jupyter notebook. However, playwright async does not run on windows for the reasons mentioned [here](https://github.com/scrapy-plugins/scrapy-playwright#known-issues). As a result I implement the data scraping part in .py and then move to jupyter notebok for parsing and cleaning etc.