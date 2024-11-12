import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


urls = [
    "https://garden.org/plants/view/799595/Tall-Bearded-Iris-Iris-Shout-it-Out-Loud/",
    "https://garden.org/plants/view/810771/Tall-Bearded-Iris-Iris-Show-Me-the-Money/",
    "https://garden.org/plants/view/812374/Miniature-Tall-Bearded-Iris-Iris-Silence-Please/",
    "https://garden.org/plants/view/93419/Intermediate-Bearded-Iris-Iris-Silent-Strings/",
    "https://garden.org/plants/view/785706/Tall-Bearded-Iris-Iris-Silver-Celebration/",
    "https://garden.org/plants/view/580461/Tall-Bearded-Iris-Iris-Silver-Creek/",
    "https://garden.org/plants/view/840185/Tall-Bearded-Iris-Iris-Simply-Said/",
    "https://garden.org/plants/view/553712/Tall-Bearded-Iris-Iris-Single-Malt/"
]


# Define the fields to scrape
fields = ["Name", "1-Class", "2-Hybridizer", "3-Year", "4-Height", "5-Season", "6-ReBloom", "7-Style", "8-Fragrant", "9-Link", "10-Color", "11-Description"]

# Function to scrape data from a single plant page
def scrape_plant_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": "https://americanenglishfordevs.com",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching {url}: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract each field from the HTML
    plant_data = {}

    def get_data_by_label(label):
        rows = soup.find_all("tr")
        for row in rows:
            tds = row.find_all("td")
            if len(tds) > 1 and label in tds[0].get_text(strip=True):
                formatted_value = tds[1].get_text(strip=True)
                if label == "Classification:":
                    start = formatted_value.find('(')
                    end = formatted_value.find(')')
                    if start != -1 and end != -1:
                        formatted_value = formatted_value[start+1:end]
                if (label == "Bloom Season:"):
                    formatted_value = ', '.join(tds[1].stripped_strings)
                if (label == "Fragrance:"):
                    formatted_value = ', '.join(tds[1].stripped_strings)
                if (label == "Flower Pattern:" or label == "Flower Form:"):
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
        time.sleep(3)  # Respectful delay between requests
    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Convert to DataFrame
df = pd.DataFrame(all_plants_data, columns=fields)

# Save to Excel
df.to_excel("iris_plants_data.xlsx", index=False)
