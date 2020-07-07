import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')

links = soup.select('.storylink')
subtext = soup.select('.subtext')

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for index, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace('points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)

sorted_stories = create_custom_hn(links, subtext)

#create html file to display results in
head = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><link rel="stylesheet" href="styles.css"></head><body><h1>Top Hacker News</h1>'
closingTags = '</body></html>'
with open("index.html", mode='w') as htmlFile:
    text = head
    for i, story in enumerate(sorted_stories):
        heading = '<h2>' + story['title'] + '</h2>'
        link = '<a href="' + story['link'] + ' " target="_blank">View</a>'
        votes = '<p> votes:' + str(story['votes']) + '</p>'
        text = text + '<div class="card">'+ heading + link+ votes +'</div>'
    text = text + closingTags
    htmlFile.write(text)
   
