import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define the fields to scrape
fields = ["Name", "1-Class", "2-Hybridizer", "3-Year", "4-Height", "5-Season", "6-ReBloom", "7-Style", "8-Fragrant", "10-Color", "11-Description"]

# Function to scrape data from a single plant page
def scrape_plant_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching {url}: {response.status_code}")
        return None

    print('response: ')
    print(response);

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract each field from the HTML
    plant_data = {}
    # plant_data["Name"] = soup.find("h1").text.strip()  # Assuming name is in <h1> tag

    # Define a helper function to get text from the second <td> based on a label in the first <td>
    def get_data_by_label(label):
        print('label: ' + label)

        row = soup.find("tr", string=lambda text: text and label in text)  # Find the <tr> containing the label
        print(row)
        if row:
            data_td = row.find_all("td")  # Find all <td> in the row
            if len(data_td) > 1:
                return data_td[1].text.strip()  # Return text from the second <td>
        return "N/A"  # Return "N/A" if not found or no data

    # Now use this helper function to populate your dictionary fields
    plant_data["1-Class"] = get_data_by_label("Classification:")
    print(plant_data["1-Class"])
    # plant_data["2-Hybridizer"] = get_data_by_label("Hybridizer:")
    # plant_data["3-Year"] = get_data_by_label("Year Of Registration:")

    

    # Customize these selectors based on the actual structure of each field on garden.org
    # plant_data["1-Class"] = soup.find("div", {"data-label": "Classification:"}).text.strip()
    # plant_data["2-Hybridizer"] = soup.find("div", {"data-label": "Hybridizer:"}).text.strip()
    # plant_data["3-Year"] = soup.find("div", {"data-label": "Year Of Registration:"}).text.strip()
    # plant_data["4-Height"] = soup.find("div", {"data-label": "Height"}).text.strip()
    # plant_data["5-Season"] = soup.find("div", {"data-label": "Season"}).text.strip()
    # plant_data["6-ReBloom"] = soup.find("div", {"data-label": "ReBloom"}).text.strip()
    # plant_data["7-Style"] = soup.find("div", {"data-label": "Style"}).text.strip()
    # plant_data["8-Fragrant"] = soup.find("div", {"data-label": "Fragrant"}).text.strip()
    # plant_data["10-Color"] = soup.find("div", {"data-label": "Color"}).text.strip()
    # plant_data["11-Description"] = soup.find("div", {"data-label": "Description"}).text.strip()

    return plant_data

# List of URLs to scrape (for the full 1000, you’d add all URLs here)
urls = [
    "https://garden.org/plants/view/810722/Tall-Bearded-Iris-Iris-Shadowboxer/",
    # Add more URLs here...
]

# Initialize an empty list to store plant data
all_plants_data = []

# Loop through each URL and scrape data
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
