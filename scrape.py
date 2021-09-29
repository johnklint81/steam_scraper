import requests
import lxml.html
import json

# Open up Steam and pass the response to the lxml.html.fromstrings method
html = requests.get('https://store.steampowered.com/explore/new/')
doc = lxml.html.fromstring(html.content)

# Return a list of all the divs in the html page which have an id of 'tab_newreleases_content'.
new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]

# Retrieve titles and prices
titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')
prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')

# Extract the divs containing the tags for the games.
tags_divs = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
tags = []

for div in tags_divs:
    tags.append(div.text_content())

# Separate the tags so that each tag i a separate element.
tags = [tag.split(', ') for tag in tags]

# Extract the platforms associated with each game. The code first extracts the divs
# with the tab_item_details class, then the spans containing the platform_img class
# and finally the second class name which is the platform.
platforms_div = new_releases.xpath('.//div[@class="tab_item_details"]')
total_platforms = []

for game in platforms_div:
    temp = game.xpath('.//span[contains(@class, "platform_img")]')
    platforms = [t.get('class').split(' ')[-1] for t in temp]
    if 'hmd_separator' in platforms:
        platforms.remove('hdm_separator')
    total_platforms.append(platforms)


# Create final output by looping over lists and put in a dictionary.
output = []
for info in zip(titles, prices, tags, total_platforms):
    resp = {
        'title':     info[0],
        'price':     info[1],
        'tags':      info[2],
        'platforms': info[3],
    }
    output.append(resp)

# Save as a .json file.
with open('scarped_steam_games.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)
