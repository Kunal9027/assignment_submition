import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of event URLs
event_urls = ["https://www.eventbrite.com/e/bengaluru-business-networking-tickets-913820249967",
              "https://www.eventbrite.com/e/wofx-world-furniture-expo-tickets-813706727727",
              "https://www.eventbrite.com/e/exclusive-launch-event-of-royal-gateway-in-delhi-tickets-922719608187",
              "https://www.eventbrite.at/e/red-bull-bc-one-cypher-india-tickets-910465897007",
              "https://www.eventbrite.com/e/global-startups-club-l-startup-networking-tickets-913808073547"
              ]
    

def scrape_event(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    event_data = {}
    
    try:
        event_data['Event Name'] = soup.find("h1", class_ = "event-title css-0").text
    except:
        event_data['Event Name'] = "N/A"
    
    try:
        event_data['Event Date & time'] = soup.find("time" , class_ = "start-date").text
    except:
        event_data['Event Date(s)'] = "N/A"

    try:
        event_data['Location'] =   soup.find("div", class_ = "location-info__address").text
    except:
        event_data['Location'] = "N/A"
    
    event_data['Website URL'] = url
    
    try:
        event_data['Description'] = event_Desc = soup.find('div', class_ = "eds-text--left").text
    except:
        event_data['Description'] = "N/A"

    try:
      event_data['Pricing'] = soup.find("div", class_ = "ticket-card-compact-size__price-container").text
    except:
      event_data['Pricing'] = "N/A"
  
    try:
      box = soup.find("div", class_ = "Layout-module__module___2eUcs Layout-module__tags___3ORp2")
      event_UL = box.find("ul")
      event_LI = event_UL.find_all("li")
      event_data['Tags'] = []
      for i in event_LI:
        event_data['Tags'].append(i.text)
    except:
      event_data['Tags'] = "N/A"

    try:
      event_data['Organizer'] = soup.find("strong", class_ = "organizer-listing-info-variant-b__name-link").text
    except:
      event_data['Organizer'] = "N/A"

    try:
      event_data['Agenda/Schedule'] = soup.find("span", class_ = "date-info__full-datetime").text
    except:
      event_data['Agenda/Schedule'] = "N/A"

    return event_data

# Scrape data for all events
events_data = []
for url in event_urls:
    event_data = scrape_event(url)
    events_data.append(event_data)


# Convert scraped data to pandas DataFrame
df = pd.DataFrame(events_data)


# Save DataFrame to CSV
df.to_csv('events_data.csv', index=False, encoding='utf-8')

# Save DataFrame to JSON
df.to_json('events_data.json', orient='records', lines=True)