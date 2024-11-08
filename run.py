import requests, pprint, re
from bs4 import BeautifulSoup


KEYWORDS = [
    'train',
    'lionel'
]

KEYWORD_REGEX = re.compile(r'(' + '|'.join(map(re.escape, KEYWORDS)) + ')')

base_url = 'https://slocalestateauctions.com'
response = requests.get(base_url)


notable = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    autions = soup.find_all(class_='auction-groups')

    for auction in autions[:1]:
        auction_card = auction.find(class_='card-body')
        auction_header = auction_card.find('h4', class_='AuctionGroupsLink')

        auction_description = auction_header.find('span')
        auction_link = auction_header.find('a')
        auction_description_text = auction_description.get_text()

        auction_title_keyword_match = KEYWORD_REGEX.search(auction_description_text)
        
        if auction_title_keyword_match:
            notable.append({
                    'type': 'auction',
                    'keyword': auction_title_keyword_match.group(),
                    'link': f"{base_url}{auction_link.get('href')}"
                })
            

        auction_response = requests.get(f"{base_url}{auction_link.get('href')}")
        auction_soup = BeautifulSoup(auction_response.text, 'html.parser')


        auction_main = auction_soup.find(class_='main-container')
        figures = auction_main.find_all('figure')

        for figure in figures:
            item_link = figure.find_next('a')
            item_image = item_link.find('img')
            item_description = item_image.get('alt')
            item_description_match = KEYWORD_REGEX.search(item_description)     
            
            if item_description_match:
                notable.append({
                    'type': 'item',
                    'keyword': item_description_match.group(),
                    'link': f"{base_url}{item_link.get('href')}",
                    'image': item_image.get('src')
                })


pprint.pprint(notable)
