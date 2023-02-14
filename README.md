# Predicting champions league matches using web data

In this project we scrape statistics tables for each Champions League seasons and try to predict the results of the future games using ML.

Note: The cleanest way of implementing the get_dat stage i.e. playwright usage would be to use in in jupyter notebook. However, playwright async does not run on windows for the reasons mentioned [here](https://github.com/scrapy-plugins/scrapy-playwright#known-issues). As a result I implement the data scraping part in .py and then move to jupyter notebok for parsing and cleaning etc.