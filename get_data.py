
# Python file to extract useful tables form the various statistics tables for Champion League. 

import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout #alternative to selenium



DATA_DIR = "data"

SCORES_DIR = os.path.join(DATA_DIR, "scores_stats") #scores and fixtures data
LEAGUE_DIR = os.path.join(DATA_DIR, "league_stats") #squad standard stats
MISC_DIR = os.path.join(DATA_DIR, "misc_stats")     #miscellaneous stats
PLAYING_DIR = os.path.join(DATA_DIR, "playing_stats")#playing time stats
KEEPER_DIR = os.path.join(DATA_DIR, "keeper_stats")  #keepers stats
SHOOTING_DIR = os.path.join(DATA_DIR, "shooting_stats") #shooting stats

years = list(range(2010,2022))



# function to get html
def get_html(url, selector, sleep = 5, retries = 3):
    """
    :param url: url to download html from
    :type url: string
    :param selector: webpage CSS selector used to locate the required html section
    :type selector: string

    Downloads html for a certain url and retries in case of a timeout. 
    Incorporating progressive sleep times to avoid being banned by the site
    """

    html = None
    for i in range(1,retries+1):
        time.sleep(sleep*i)
        try:
            with sync_playwright() as p:
                browser = p.firefox.launch()
                page = browser.new_page()
                page.goto(url)
                print(page.title())
                html = page.inner_html(selector)
        except PlaywrightTimeout:
            print(f"Timeout on {url}")
            continue
        else: #else block is run when "try" is run successfully.
            break #break if getting html successful.
    return html

# Writing similar functions to get the data from  various pages and store them in the appropriate directories.

def get_score(year, url, selector):
    save_path = os.path.join(SCORES_DIR, url.split("schedule/")[-1]) 
    if os.path.exists(save_path):
        pass
    else:
        html =  get_html(url,selector)
        with open(save_path, "w+", encoding="utf-8") as f: 
            f.write(html)
######################
def get_keeper(year, url, selector):
    save_path = os.path.join(KEEPER_DIR, url.split('keepers/')[-1]) 
    if os.path.exists(save_path):
        pass
    else:
        html =  get_html(url,selector)
        with open(save_path, "w+", encoding="utf-8") as f:
            f.write(html)
######################
def get_league(year, url, selector):
    save_path = os.path.join(LEAGUE_DIR, url.split('stats/')[-1])
    if os.path.exists(save_path):
        pass
    else:
        html =  get_html(url,selector)
        with open(save_path, "w+", encoding="utf-8") as f: 
            f.write(html)
######################
def get_misc(year, url, selector):
    save_path = os.path.join(MISC_DIR, url.split('misc/')[-1])
    if os.path.exists(save_path):
        pass
    else:
        html =  get_html(url,selector)
        with open(save_path, "w+", encoding="utf-8") as f: 
            f.write(html)
######################
def get_shooting(year, url, selector):
    save_path = os.path.join(SHOOTING_DIR, url.split('shooting/')[-1])
    if os.path.exists(save_path):
        pass
    else:
        html =  get_html(url,selector)
        with open(save_path, "w+", encoding="utf-8") as f: 
            f.write(html)
######################
def get_playing(year, url, selector):
    save_path = os.path.join(PLAYING_DIR, url.split('playingtime/')[-1])
    if os.path.exists(save_path):
        pass
    else:
        html =  get_html(url,selector)
        with open(save_path, "w+", encoding="utf-8") as f: 
            f.write(html)


# Main loop to scrape and store

for year in years:
    
    score_url = f"https://fbref.com/en/comps/8/{year}-{year+1}/schedule/{year}-{year+1}-Champions-League-Scores-and-Fixtures.html"
    score_selector = "#div_sched_all"
    get_score(year, score_url, score_selector)

    keeper_url = f"https://fbref.com/en/comps/8/{year}-{year+1}/keepers/{year}-{year+1}-Champions-League-Stats.html"
    keeper_selector = "#div_stats_squads_keeper_for"
    get_keeper(year, keeper_url, keeper_selector)

    league_url = f"https://fbref.com/en/comps/8/{year}-{year+1}/stats/{year}-{year+1}-Champions-League-Stats.html"
    league_selector = "#switcher_stats_squads_standard"
    get_league(year, league_url, league_selector)

    misc_url = f"https://fbref.com/en/comps/8/{year}-{year+1}/misc/{year}-{year+1}-Champions-League-Stats.html"
    misc_selector = "#switcher_stats_squads_misc"
    get_misc(year, misc_url, misc_selector)

    shooting_url = f"https://fbref.com/en/comps/8/{year}-{year+1}/shooting/{year}-{year+1}-Champions-League-Stats.html"
    shooting_selector = "#switcher_stats_squads_shooting"
    get_shooting(year, shooting_url,shooting_selector)

    playing_url = f"https://fbref.com/en/comps/8/{year}-{year+1}/playingtime/{year}-{year+1}-Champions-League-Stats.html"
    playing_selector = "#switcher_stats_squads_playing_time"
    get_playing(year, playing_url, playing_selector)