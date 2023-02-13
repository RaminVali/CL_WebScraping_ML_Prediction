
import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout #alternative to selenium
from bs4 import BeautifulSoup



DATA_DIR = "data"

SCORES_DIR = os.path.join(DATA_DIR, "scores_stats") #scores and fixtures data
LEAGUE_DIR = os.path.join(DATA_DIR, "league_stats") #squad standard stats
MISC_DIR = os.path.join(DATA_DIR, "misc_stats")     #miscellaneous stats
PLAYING_DIR = os.path.join(DATA_DIR, "playing_stats")#playing time stats
KEEPER_DIR = os.path.join(DATA_DIR, "keeper_stats")  #keepers stats
SHOOTING_DIR = os.path.join(DATA_DIR, "shootig_stats") #shooting stats


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



year = 2010
url = f"https://fbref.com/en/comps/8/{year}-{year+1}/schedule/{year}-{year+1}-Champions-League-Scores-and-Fixtures.html"
selector = "#div_sched_all"


html =  get_html(url,selector)

save_path = os.path.join(SCORES_DIR, url.split("schedule/")[-1]) # you ned to save your data to disk to process later, so create a path to the directory you want to save it, and the file nam eis going to be the end of the url, so we split towards the forwrad slash to give us the end bit of the url as the file name for each file
if os.path.exists(save_path):
    pass
else:
    with open(save_path, "w+", encoding="utf-8") as f: # open the saved path in write mode
        f.write(html)