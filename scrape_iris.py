import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

urls = [
    "https://garden.org/plants/view/845627/Tall-Bearded-Iris-Iris-Hot-Granny/",
    "https://garden.org/plants/view/757826/Tall-Bearded-Iris-Iris-Hottie/",
    "https://garden.org/plants/view/810703/Tall-Bearded-Iris-Iris-House-of-Light/",
    "https://garden.org/plants/view/778218/Tall-Bearded-Iris-Iris-Hung-Up-On-You/",
    "https://garden.org/plants/view/839944/Border-Bearded-Iris-Iris-I-Believe/",
    "https://garden.org/plants/view/845638/Tall-Bearded-Iris-Iris-I-Love-Popcorn/",
    "https://garden.org/plants/view/751966/Tall-Bearded-Iris-Iris-Ice-Cream-Sundae/",
    "https://garden.org/plants/view/833810/Tall-Bearded-Iris-Iris-If-You-Come-Softly/",
    "https://garden.org/plants/view/840209/Tall-Bearded-Iris-Iris-Ill-Be-The-One/",
    "https://garden.org/plants/view/93279/Intermediate-Bearded-Iris-Iris-Imperative/",
    "https://garden.org/plants/view/840140/Tall-Bearded-Iris-Iris-Indiscriminate/",
    "https://garden.org/plants/view/799601/Tall-Bearded-Iris-Iris-Instant-Message/",
    "https://garden.org/plants/view/845648/Tall-Bearded-Iris-Iris-Iridescent/",
    "",
    "https://garden.org/plants/view/715114/Tall-Bearded-Iris-Iris-Irish-Jester/",
    "https://garden.org/plants/view/73881/Tall-Bearded-Iris-Iris-Iron-Eagle/",
    "https://garden.org/plants/view/789696/Tall-Bearded-Iris-Iris-Its-Me-Again/",
    "https://garden.org/plants/view/133509/Tall-Bearded-Iris-Iris-Jaunty-Dancer/",
    "https://garden.org/plants/view/568235/Tall-Bearded-Iris-Iris-Java-Bleue/",
    "https://garden.org/plants/view/801629/Tall-Bearded-Iris-Iris-Javalanche/",
    "https://garden.org/plants/view/229751/Tall-Bearded-Iris-Iris-Jennifer-Stout/",
    "https://garden.org/plants/view/840294/Tall-Bearded-Iris-Iris-Jimmys-Jam/",
    "https://garden.org/plants/view/73905/Tall-Bearded-Iris-Iris-Jimmys-Smile/",
    "https://garden.org/plants/view/568719/Standard-Dwarf-Bearded-Iris-Iris-Just-a-Flirt/",
    "https://garden.org/plants/view/714558/Tall-Bearded-Iris-Iris-Just-a-Touch/",
    "https://garden.org/plants/view/810705/Tall-Bearded-Iris-Iris-Just-Curious/",
    "https://garden.org/plants/view/817375/Tall-Bearded-Iris-Iris-Just-for-Ken/",
    "https://garden.org/plants/view/785415/Standard-Dwarf-Bearded-Iris-Iris-Just-Mist/",
    "https://garden.org/plants/view/228326/Tall-Bearded-Iris-Iris-Just-Witchery/",
    "https://garden.org/plants/view/801647/Tall-Bearded-Iris-Iris-Kays-Kakes/",
    "https://garden.org/plants/view/825336/Tall-Bearded-Iris-Iris-Keep-Calm-Grow-Iris/",
    "https://garden.org/plants/view/93288/Intermediate-Bearded-Iris-Iris-Kermit/",
    "https://garden.org/plants/view/73923/Tall-Bearded-Iris-Iris-Kinkajou-Shrew/",
    "https://garden.org/plants/view/778016/Tall-Bearded-Iris-Iris-Kiss-the-Night/",
    "https://garden.org/plants/view/569483/Tall-Bearded-Iris-Iris-Kristen-Faith/",
    "https://garden.org/plants/view/810768/Tall-Bearded-Iris-Iris-Lace-and-Promises/",
    "https://garden.org/plants/view/569722/Tall-Bearded-Iris-Iris-Lady-in-Purple/",
    "https://garden.org/plants/view/833879/Tall-Bearded-Iris-Iris-Lake-Mendota/",
    "https://garden.org/plants/view/714508/Tall-Bearded-Iris-Iris-Last-Tango-in-Paris/",
    "https://garden.org/plants/view/810769/Tall-Bearded-Iris-Iris-Later-Alligator/",
    "https://garden.org/plants/view/789601/Tall-Bearded-Iris-Iris-Law-and-Order/",
    "https://garden.org/plants/view/570162/Tall-Bearded-Iris-Iris-Lemon-Berry-Burst/",
    "https://garden.org/plants/view/840139/Tall-Bearded-Iris-Iris-Lemon-Peel/",
    "https://garden.org/plants/view/840207/Tall-Bearded-Iris-Iris-Like-a-Dream/",
    "https://garden.org/plants/view/845752/Tall-Bearded-Iris-Iris-Little-Licious/",
    "https://garden.org/plants/view/570760/Standard-Dwarf-Bearded-Iris-Iris-Little-Lighthouse/",
    "",
    "https://garden.org/plants/view/554472/Tall-Bearded-Iris-Iris-Love-is-Pink/",
    "https://garden.org/plants/view/840167/Intermediate-Bearded-Iris-Iris-Love-Life/",
    "https://garden.org/plants/view/810710/Tall-Bearded-Iris-Iris-Lovers-Kiss/",
    "",
    "https://garden.org/plants/view/122756/Tall-Bearded-Iris-Iris-Lucky-Stripes/",
    "https://garden.org/plants/view/812363/Intermediate-Bearded-Iris-Iris-Lumistreak/",
    "https://garden.org/plants/view/796959/Tall-Bearded-Iris-Iris-Lunar-Ring/",
    "https://garden.org/plants/view/840138/Tall-Bearded-Iris-Iris-Magic-Blue/",
    "https://garden.org/plants/view/670331/Intermediate-Bearded-Iris-Iris-Magical-Times/",
    "",
    "https://garden.org/plants/view/840206/Tall-Bearded-Iris-Iris-Major-Impact/",
    "https://garden.org/plants/view/840205/Tall-Bearded-Iris-Iris-Major-News/",
    "https://garden.org/plants/view/840204/Tall-Bearded-Iris-Iris-Make-a-Move/",
    "https://garden.org/plants/view/840137/Tall-Bearded-Iris-Iris-Make-Up-Your-Mind/",
    "",
    "https://garden.org/plants/view/772943/Tall-Bearded-Iris-Iris-Margin-Trader/",
    "https://garden.org/plants/view/840203/Tall-Bearded-Iris-Iris-Mark-My-Words/",
    "https://garden.org/plants/view/186495/Tall-Bearded-Iris-Iris-May-Debut/",
    "https://garden.org/plants/view/572131/Tall-Bearded-Iris-Iris-Meadowgaze/",
    "https://garden.org/plants/view/777944/Border-Bearded-Iris-Iris-Merry-Mulberry/",
    "https://garden.org/plants/view/572344/Intermediate-Bearded-Iris-Iris-Mescalero/",
    "https://garden.org/plants/view/744103/Tall-Bearded-Iris-Iris-Mezzo-Forte/",
    "",
    "https://garden.org/plants/view/801750/Tall-Bearded-Iris-Iris-Mind-Blowing/",
    "https://garden.org/plants/view/572552/Tall-Bearded-Iris-Iris-Mindy-Pink/",
    "https://garden.org/plants/view/527200/Standard-Dwarf-Bearded-Iris-Iris-Mini-Mouse/",
    "https://garden.org/plants/view/840056/Tall-Bearded-Iris-Iris-Misplaced-Dots/",
    "https://garden.org/plants/view/772977/Tall-Bearded-Iris-Iris-Misty-Sunlight/",
    "https://garden.org/plants/view/801765/Arilbred-Iris-Iris-Moment-in-the-Sun/",
    "https://garden.org/plants/view/840202/Tall-Bearded-Iris-Iris-Moment-of-Reflection/",
    "",
    "https://garden.org/plants/view/73000/Tall-Bearded-Iris-Iris-Money-in-Your-Pocket/",
    "https://garden.org/plants/view/95805/Tall-Bearded-Iris-Iris-Montevideo/",
    "https://garden.org/plants/view/789704/Tall-Bearded-Iris-Iris-More-than-Ruffles/",
    "https://garden.org/plants/view/707382/Standard-Dwarf-Bearded-Iris-Iris-Morning-Hues/",
    "https://garden.org/plants/view/839889/Tall-Bearded-Iris-Iris-Moving-On/",
    "https://garden.org/plants/view/642827/Tall-Bearded-Iris-Iris-Multnomah-Falls/",
    "https://garden.org/plants/view/778254/Tall-Bearded-Iris-Iris-Musicality/",
    "https://garden.org/plants/view/799911/Border-Bearded-Iris-Iris-My-Gal/",
    "https://garden.org/plants/view/573567/Miniature-Dwarf-Bearded-Iris-Iris-My-Huckleberry-Friend/",
    "https://garden.org/plants/view/546456/Tall-Bearded-Iris-Iris-My-Ladys-Manor/",
    "https://garden.org/plants/view/801777/Tall-Bearded-Iris-Iris-Myers-Mansion/",
    "https://garden.org/plants/view/799599/Tall-Bearded-Iris-Iris-Mystery-Lady/",
    "https://garden.org/plants/view/777808/Border-Bearded-Iris-Iris-Mystic-Siren/",
    "https://garden.org/plants/view/810976/Tall-Bearded-Iris-Iris-Mystify/",
    "https://garden.org/plants/view/840201/Tall-Bearded-Iris-Iris-Natural-Choice/",
    "https://garden.org/plants/view/840200/Tall-Bearded-Iris-Iris-Neapolitan-Delight/",
    "https://garden.org/plants/view/757184/Tall-Bearded-Iris-Iris-Need-You-Now/",
    "https://garden.org/plants/view/181308/Tall-Bearded-Iris-Iris-New-Age-Dawning/",
    "",
    "https://garden.org/plants/view/801790/Border-Bearded-Iris-Iris-Next-Up/",
    "https://garden.org/plants/view/834014/Tall-Bearded-Iris-Iris-Niagara-Mist/",
    "https://garden.org/plants/view/574038/Tall-Bearded-Iris-Iris-Nice-Shot/",
    "https://garden.org/plants/view/777806/Intermediate-Bearded-Iris-Iris-Nickels-Worth/",
    "https://garden.org/plants/view/789592/Tall-Bearded-Iris-Iris-Night-Whispers/",
    "https://garden.org/plants/view/834020/Tall-Bearded-Iris-Iris-None-of-Your-Beeswax/",
    "https://garden.org/plants/view/752284/Tall-Bearded-Iris-Iris-North-Rim/",
    "https://garden.org/plants/view/801795/Arilbred-Iris-Iris-Not-of-This-World/",
    "https://garden.org/plants/view/541888/Tall-Bearded-Iris-Iris-Notta-Lemon/",
    "https://garden.org/plants/view/166419/Tall-Bearded-Iris-Iris-Oasis-Sydney/",
    "https://garden.org/plants/view/123922/Tall-Bearded-Iris-Iris-Oaxaca/",
    "https://garden.org/plants/view/656365/Tall-Bearded-Iris-Iris-October-Dreaming/",
    "https://garden.org/plants/view/574645/Tall-Bearded-Iris-Iris-Olympic-Return/",
    "https://garden.org/plants/view/74034/Tall-Bearded-Iris-Iris-Ominous-Stranger/",
    "https://garden.org/plants/view/840199/Tall-Bearded-Iris-Iris-On-Angel-Wings/",
    "https://garden.org/plants/view/840198/Tall-Bearded-Iris-Iris-On-My-Way/",
    "https://garden.org/plants/view/645148/Tall-Bearded-Iris-Iris-One-Step-Beyond/",
    "",
    "https://garden.org/plants/view/810712/Tall-Bearded-Iris-Iris-One-Step-Closer/",
    "https://garden.org/plants/view/714835/Tall-Bearded-Iris-Iris-One-Wild-Child/",
    "https://garden.org/plants/view/840134/Tall-Bearded-Iris-Iris-Orange-Blast/",
    "https://garden.org/plants/view/834041/Tall-Bearded-Iris-Iris-Orange-Crush-Cocktail/",
    "https://garden.org/plants/view/95945/Tall-Bearded-Iris-Iris-Orange-Harvest/",
    "https://garden.org/plants/view/789588/Tall-Bearded-Iris-Iris-Orange-Temptation/",
    "https://garden.org/plants/view/609611/Tall-Bearded-Iris-Iris-Oro-Valley-Sunshine/",
    "https://garden.org/plants/view/840196/Tall-Bearded-Iris-Iris-Out-of-Character/",
    "https://garden.org/plants/view/715156/Tall-Bearded-Iris-Iris-Over-Drinks/",
    "https://garden.org/plants/view/773030/Tall-Bearded-Iris-Iris-Over-Heated/",
    "https://garden.org/plants/view/702351/Tall-Bearded-Iris-Iris-Painted-Words/",
    "https://garden.org/plants/view/95997/Tall-Bearded-Iris-Iris-Panama-Hattie/",
    "https://garden.org/plants/view/845901/Tall-Bearded-Iris-Iris-Papal-Slippers/",
    "https://garden.org/plants/view/773035/Border-Bearded-Iris-Iris-Papaya/",
    "https://garden.org/plants/view/799941/Miniature-Tall-Bearded-Iris-Iris-Paper-Tiger/",
    "https://garden.org/plants/view/840195/Tall-Bearded-Iris-Iris-Parade-of-Stars/",
    "https://garden.org/plants/view/575413/Tall-Bearded-Iris-Iris-Paris-Romance/",
    "https://garden.org/plants/view/789584/Tall-Bearded-Iris-Iris-Party-City/",
    "",
    "https://garden.org/plants/view/840026/Border-Bearded-Iris-Iris-Patriotic/",
    "https://garden.org/plants/view/712778/Tall-Bearded-Iris-Iris-Pattern-Play/",
    "https://garden.org/plants/view/96017/Tall-Bearded-Iris-Iris-Patterns/",
    "https://garden.org/plants/view/845912/Tall-Bearded-Iris-Iris-Pawnee-Buttes/",
    "https://garden.org/plants/view/96024/Tall-Bearded-Iris-Iris-Peach-Brandy/",
    "https://garden.org/plants/view/575650/Border-Bearded-Iris-Iris-Peach-Ice-Cream/",
    "https://garden.org/plants/view/642987/Tall-Bearded-Iris-Iris-Peach-Pearl/",
    "",
    "https://garden.org/plants/view/706904/Tall-Bearded-Iris-Iris-Peggy-Day/",
    "https://garden.org/plants/view/73204/Tall-Bearded-Iris-Iris-Penguin-Party/",
    "https://garden.org/plants/view/778234/Tall-Bearded-Iris-Iris-Perihelion-Pass/",
    "",
    "https://garden.org/plants/view/778127/Tall-Bearded-Iris-Iris-Pharaohs-Poet/",
    "https://garden.org/plants/view/700067/Tall-Bearded-Iris-Iris-Phasers-on-Stun/",
    "https://garden.org/plants/view/785604/Tall-Bearded-Iris-Iris-Picked-for-Pat/",
    "https://garden.org/plants/view/799580/Tall-Bearded-Iris-Iris-Piece-by-Piece/",
    "https://garden.org/plants/view/744211/Intermediate-Bearded-Iris-Iris-Pink-Blitz/",
    "https://garden.org/plants/view/845927/Tall-Bearded-Iris-Iris-Pitch-a-Fit/",
    "https://garden.org/plants/view/96093/Tall-Bearded-Iris-Iris-Platinum/",
    "https://garden.org/plants/view/799888/Tall-Bearded-Iris-Iris-Plic-Symphony/",
    "https://garden.org/plants/view/840194/Tall-Bearded-Iris-Iris-Plot-Thickens/",
    "https://garden.org/plants/view/840193/Tall-Bearded-Iris-Iris-Plot-Twist/",
    "https://garden.org/plants/view/800428/Tall-Bearded-Iris-Iris-Poetic-Dream/",
    "https://garden.org/plants/view/576628/Intermediate-Bearded-Iris-Iris-Point-the-Way/",
    "https://garden.org/plants/view/576642/Tall-Bearded-Iris-Iris-Pokin-Around/",
    "https://garden.org/plants/view/115318/Tall-Bearded-Iris-Iris-Polished-Amber/",
    "https://garden.org/plants/view/810770/Tall-Bearded-Iris-Iris-Politely-Pink/",
    "",
    "https://garden.org/plants/view/527207/Intermediate-Bearded-Iris-Iris-Pop-Culture/",
    "https://garden.org/plants/view/655960/Tall-Bearded-Iris-Iris-Power-Lines/",
    "https://garden.org/plants/view/840191/Tall-Bearded-Iris-Iris-Pretty-Rich/",
    "https://garden.org/plants/view/840133/Tall-Bearded-Iris-Iris-Pretty-Sight/",
    "https://garden.org/plants/view/181280/Tall-Bearded-Iris-Iris-Prime-Power/",
    "https://garden.org/plants/view/96129/Tall-Bearded-Iris-Iris-Prince-Charming/",
    "https://garden.org/plants/view/655974/Tall-Bearded-Iris-Iris-Prissy-Christy/",
    "https://garden.org/plants/view/845953/Tall-Bearded-Iris-Iris-Prom-Dance/",
    "https://garden.org/plants/view/769039/Standard-Dwarf-Bearded-Iris-Iris-Psychedelic-Dreams/",
    "https://garden.org/plants/view/810716/Tall-Bearded-Iris-Iris-Pull-Me-Close/",
    "https://garden.org/plants/view/72728/Tall-Bearded-Iris-Iris-Pure-as-Gold/",
    "https://garden.org/plants/view/845959/Tall-Bearded-Iris-Iris-Purplicious/",
    "https://garden.org/plants/view/554660/Tall-Bearded-Iris-Iris-Purr-Form-Mints/",
    "https://garden.org/plants/view/577534/Standard-Dwarf-Bearded-Iris-Iris-Quote/",
    "https://garden.org/plants/view/73063/Tall-Bearded-Iris-Iris-Raven-Girl/",
    "https://garden.org/plants/view/777385/Tall-Bearded-Iris-Iris-Reality-Check/",
    "https://garden.org/plants/view/849822/Tall-Bearded-Iris-Iris-Red-Frog-Flyin/",
    "https://garden.org/plants/view/72297/Standard-Dwarf-Bearded-Iris-Iris-Red-Heart/",
    "https://garden.org/plants/view/74105/Intermediate-Bearded-Iris-Iris-Red-Zinger/",
    "https://garden.org/plants/view/801885/Tall-Bearded-Iris-Iris-Reina/",
    "https://garden.org/plants/view/232773/Tall-Bearded-Iris-Iris-Reversi/",
    "https://garden.org/plants/view/120594/Intermediate-Bearded-Iris-Iris-Rikki-Tiki/",
    "https://garden.org/plants/view/578280/Standard-Dwarf-Bearded-Iris-Iris-Rings/",
    "https://garden.org/plants/view/715180/Tall-Bearded-Iris-Iris-Rise-Like-a-Phoenix/",
    "https://garden.org/plants/view/845983/Tall-Bearded-Iris-Iris-River-Runs-Through/",
    "https://garden.org/plants/view/74338/Standard-Dwarf-Bearded-Iris-Iris-Riveting/",
    "https://garden.org/plants/view/845984/Tall-Bearded-Iris-Iris-Road-Home/",
    "https://garden.org/plants/view/789571/Tall-Bearded-Iris-Iris-Rodeo-Cowboy/",
    "https://garden.org/plants/view/839890/Tall-Bearded-Iris-Iris-Romany-Rogue/",
    "https://garden.org/plants/view/796963/Tall-Bearded-Iris-Iris-Royal-Academy/",
    "https://garden.org/plants/view/94214/Standard-Dwarf-Bearded-Iris-Iris-Ruby-Eruption/",
    "https://garden.org/plants/view/810719/Tall-Bearded-Iris-Iris-Runaround/",
    "https://garden.org/plants/view/609657/Intermediate-Bearded-Iris-Iris-Rust-Never-Sleeps/",
    "https://garden.org/plants/view/840131/Tall-Bearded-Iris-Iris-Sack-of-Sunshine/",
    "https://garden.org/plants/view/186450/Tall-Bearded-Iris-Iris-Saffron-Drift/",
    "https://garden.org/plants/view/834158/Intermediate-Bearded-Iris-Iris-Sassy-Li-l-Brat/",
    "https://garden.org/plants/view/839891/Tall-Bearded-Iris-Iris-Satin-Ruffles/",
    "https://garden.org/plants/view/799577/Tall-Bearded-Iris-Iris-Say-the-Word/",
    "https://garden.org/plants/view/801922/Tall-Bearded-Iris-Iris-Scattergram/"
]

# Define the fields to scrape
fields = ["Name", "1-Class", "2-Hybridizer", "3-Year", "4-Height", "5-Season", "6-ReBloom", "7-Style", "8-Fragrant", "9-Link", "10-Color", "11-Description"]

# user_agents_list = [
#     'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
# ]


# "User-Agent":  random.choice(user_agents_list),

# Function to scrape data from a single plant page
def scrape_plant_data(url):
    # headers = {
    #     "User-Agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    #     "Accept-Language": "en-US,en;q=0.9",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Connection": "keep-alive",
    # }
    # headers = {
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Accept-Language": "en-US,en;q=0.5",
    #     "Cache-Control": "max-age=0",
    #     "Priority": "u=0, i",
    #     "Referer": "https://garden.org/plants/search/text.php?ppid=181474&q=Scattergram",
    #     "Sec-Fetch-Dest": "document",
    #     "Sec-Fetch-Mode": "navigate",
    #     "Sec-Fetch-Site": "same-origin",
    #     "Sec-Fetch-User": "?1",
    #     "Upgrade-insecure-requests": "1",
    #     "User-Agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    # }


    # session = requests.Session()
    # session.headers.update(headers)  # Use headers from the previous example

    # response = session.get(url)

    # response = requests.get(url, headers=headers)

    # if response.status_code == 403:
    #     print(f"Access forbidden for {url}: {response.status_code}")
    #     sys.exit(1)

    # if response.status_code != 200:
    #     print(f"Error fetching {url}: {response.status_code}")
    #     return None

    # soup = BeautifulSoup(response.content, 'html.parser')

    # tables = soup.find_all("table", "table")
    # print('tables:', tables)
    # df1 = pd.read_html(str(tables[0]))[0]
    # print(df1)

    options = Options()
    # options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Get the window size
    window_size = driver.get_window_size()
    width = window_size['width']
    height = window_size['height']

    print(window_size)
    print(f"Window size: {width} x {height}")

    # Move the cursor around for a few seconds
    action = ActionChains(driver)
    for _ in range(5):
        # Reset cursor position to the top-left corner before each move
        action.move_to_element_with_offset(driver.find_element(By.TAG_NAME, 'body'), 0, 0).perform()
        x_offset = random.randint(0, width - 1)
        y_offset = random.randint(0, height - 1)
        action.move_by_offset(x_offset, y_offset).perform()
        print(f"Cursor moved to: ({x_offset}, {y_offset})")
        time.sleep(1)
    time.sleep(random.uniform(2, 5))

    random_number = random.randint(1000, 9999)
    screenshot_path = f"screenshot_{random_number}.png"
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')



    # Extract each field from the HTML
    plant_data = {}

    def get_data_by_label(label):
        rows = soup.find_all("tr")
        print('rows:', rows);
        for row in rows:
            tds = row.find_all("td")
            if len(tds) > 1 and label in tds[0].get_text(strip=True):
                formatted_value = tds[1].get_text(strip=True)
                if label == "Classification:":
                    start = formatted_value.find('(')
                    end = formatted_value.find(')')
                    if start != -1 and end != -1:
                        formatted_value = formatted_value[start+1:end]
                if (label == "Registered Height:"):
                    start = formatted_value.find(' ')
                    if start != -1:
                        formatted_value = formatted_value[:start]
                if (label == "Bloom Season:"):
                    formatted_value = ', '.join(tds[1].stripped_strings)
                if (label == "Fragrance:"):
                    formatted_value = ', '.join(tds[1].stripped_strings)
                if (label == "Flower Patterns:" or label == "Flower Form:"):
                    formatted_value = ', '.join(tds[1].stripped_strings)
                if (label == "Bloom Color Classification:"):
                    formatted_value = ', '.join(tds[1].stripped_strings)
                if (label == "Awards:"):
                    formatted_value = ', '.join(tds[1].stripped_strings)
                return formatted_value
        return "N/A"

    plant_data["1-Class"] = get_data_by_label("Classification:")
    plant_data["2-Hybridizer"] = get_data_by_label("Hybridizer:")
    plant_data["3-Year"] = get_data_by_label("Year Of Introduction (May Differ From Registry):")
    if plant_data["3-Year"] == "N/A":
        plant_data["3-Year"] = get_data_by_label("Year Of Registration:")
    plant_data["4-Height"] = get_data_by_label("Registered Height:")
    plant_data["5-Season"] = get_data_by_label("Bloom Season:")
    plant_data["6-ReBloom"] = get_data_by_label("Rebloom:")
    if plant_data["6-ReBloom"] == "N/A":
        plant_data["6-ReBloom"] = "No"
    else:
        plant_data["6-ReBloom"] = "Yes"
    plant_data["7-Style"] = get_data_by_label("Flower Pattern:")
    if plant_data["7-Style"] == "N/A":
        plant_data["7-Style"] = get_data_by_label("Flower Form:")
    plant_data["8-Fragrant"] = get_data_by_label("Fragrance:")
    if plant_data["8-Fragrant"] == "N/A":
        plant_data["8-Fragrant"] = "No"
    else:
        plant_data["8-Fragrant"] = "Yes - " + get_data_by_label("Fragrance:")
    plant_data["9-Link"] = url
    plant_data["10-Color"] = get_data_by_label("Bloom Color Classification:")


    def format_description():
        bloom_color_description_string = ""
        if get_data_by_label("Bloom Color Description:") != "N/A":
            bloom_color_description_string = "Bloom Color Description: " + get_data_by_label("Bloom Color Description:")  + "\n"

        beard_color_string = ""
        if get_data_by_label("Beard Color:") != "N/A":
            beard_color_string = "Beard Color: " + get_data_by_label("Beard Color:")

        awards_string = ""
        if get_data_by_label("Awards:") != "N/A":
            awards_string = "\n" + get_data_by_label("Awards:")

        get_data_by_label("Bloom Color Description:")

        description = bloom_color_description_string + beard_color_string + awards_string;

        return description

    if plant_data["2-Hybridizer"] == "Lynda Miller" or plant_data["2-Hybridizer"] == "Keith Keppel" or plant_data["2-Hybridizer"] == "Thomas Johnson" or plant_data["2-Hybridizer"] == "Paul Black":
        plant_data["11-Description"] = format_description()
    else:
        plant_data["11-Description"] = ""

    return plant_data

# Initialize an empty list to store plant data
all_plants_data = []

for url in urls:
    try:
        plant_data = scrape_plant_data(url)
        all_plants_data.append(plant_data)
        time.sleep(5)  # Respectful delay between requests
    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Convert to DataFrame
df = pd.DataFrame(all_plants_data, columns=fields)

# Save to Excel
df.to_excel("iris_plants_data.xlsx", index=False)
