#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd


# In[2]:


def scrape_page(url):
    scraper = cloudscraper.create_scraper()
    scrapedPage = scraper.get(url).text
    soup = BeautifulSoup(scrapedPage, 'html.parser')
    return soup


# In[3]:


soup = scrape_page('https://spotifycharts.com/regional/pl/daily/latest')
chart_track = soup.find_all("td", class_="chart-table-track")
streams = soup.find_all("td", class_="chart-table-streams")


# In[4]:


def save_data(csvName):
    file=open(csvName,"w",encoding = 'utf-8')
    file.write('Title;Artist;Streams\n')
    for (track,streamsCount) in zip(chart_track,streams):
        song_title=track.find("strong").get_text()
        song_artist=track.find("span").get_text()[3:]
        stream_count=streamsCount.get_text()
        file.write(song_title+';'+song_artist+';'+stream_count+'\n')
    file.close()


# In[5]:


save_data('TopSpotifyPolandLatest.csv')


# In[6]:


csvPoland = pd.read_csv('TopSpotifyPolandLatest.csv', encoding = 'utf-8', header=0, delimiter=';')


# In[7]:


print("Top 10 Spotify Songs in Poland Today")
csvPoland.head(10)


# In[8]:


soup = scrape_page('https://spotifycharts.com/regional/global/daily/latest')
chart_track = soup.find_all("td", class_="chart-table-track")
streams = soup.find_all("td", class_="chart-table-streams")
save_data('TopSpotifyGlobalLatest.csv')


# In[9]:


csvGlobal = pd.read_csv('TopSpotifyGlobalLatest.csv', encoding = 'utf-8', header=0, delimiter=';')


# In[10]:


print("Top 10 Spotify Songs Global Today")
csvGlobal.head(10)


# In[11]:


soup = scrape_page('https://spotifycharts.com/regional/pl/daily/latest')
chart_track_Poland = soup.find_all("td", class_="chart-table-track")
song_artists_Poland = []
song_titles_Poland = []
for track in chart_track_Poland:
    song_artists_Poland.append(track.find("span").get_text()[3:])
    song_titles_Poland.append(track.find("strong").get_text())


# In[12]:


soup = scrape_page('https://spotifycharts.com/regional/global/daily/latest')
chart_track_Global = soup.find_all("td", class_="chart-table-track")
song_artists_Global = []
song_titles_Global = []
for track in chart_track_Global:
    song_artists_Global.append(track.find("span").get_text()[3:])
    song_titles_Global.append(track.find("strong").get_text())


# In[13]:


common_artists = []
for artist in song_artists_Poland:
    if(artist in song_artists_Global and artist not in common_artists):
        common_artists.append(artist)


# In[14]:


common_titles = []
for title in song_titles_Poland:
    if(title in song_titles_Global and title not in common_titles):
        common_titles.append(title)


# In[15]:


print("Artists that made it to the top both in Poland and globally: ")
for artist in common_artists:
    print(artist)


# In[16]:


print("Songs that made it to the top both in Poland and globally: ")
for song in common_titles:
    print(song)


# In[17]:


col_list = ["Streams"]
df = pd.read_csv("TopSpotifyGlobalLatest.csv", usecols=col_list, sep=';')
print("Most streams globally: " + df["Streams"][0])


# In[18]:


df = pd.read_csv("TopSpotifyPolandLatest.csv", usecols=col_list, sep=';')
print("Most streams in Poland: " + df["Streams"][0])


# In[ ]:




