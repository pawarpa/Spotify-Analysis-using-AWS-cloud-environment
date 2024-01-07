#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Extracting data from Spotify and creating structured data - Albums, Artist, Songs


# In[2]:


get_ipython().system('pip install spotipy')


# In[3]:


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# In[4]:


# provide client_id and client_secret - Authentication 
client_credentials_manager = SpotifyClientCredentials(client_id='', client_secret='')


# In[5]:


#Create spotify object to use & extract data from Spotify - Authorization 
sp = spotipy.Spotify(client_credentials_manager= client_credentials_manager)


# In[6]:


# Assign URL of Top Songs - Global playlist to a variable 
playlist_link = 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF'


# In[7]:


# Extracting playlist ID using split
playlist_ID= playlist_link.split('/')[-1]


# In[8]:


data = sp.playlist_tracks(playlist_ID)


# In[9]:


data #json data - information about artist, album, songs


# In[10]:


len(data['items'])
#total number of songs


# In[11]:


data['items'][0]['track']['album']['name']
#Top song


# In[12]:


data['items'][0]['track']['album']['release_date']


# In[13]:


data['items'][0]['track']['album']['total_tracks']


# In[14]:


data['items'][0]['track']['album']['external_urls']['spotify']


# In[15]:


for row in data['items']:
    album_id = row['track']['album']['id']
    album_name = row['track']['album']['name']
    album_release_date = row['track']['album']['release_date']
    album_total_tracks = row['track']['album']['total_tracks']
    album_url = row['track']['album']['external_urls']['spotify']
    print(album_name)


# In[16]:


album_list = []
for row in data['items']:
    album_id = row['track']['album']['id']
    album_name = row['track']['album']['name']
    album_release_date = row['track']['album']['release_date']
    album_total_tracks = row['track']['album']['total_tracks']
    album_url = row['track']['album']['external_urls']['spotify']
    album_element = {'album_id':album_id,'name':album_name,'release_date':album_release_date,
                        'total_tracks':album_total_tracks,'url':album_url}
    album_list.append(album_element)


# In[17]:


album_list #creating more stuctured data for albums


# In[18]:


artist_list = []
for row in data['items']:
    for key, value in row.items():
        if key == "track":
            for artist in value['artists']:
                artist_dict = {'artist_id':artist['id'], 'artist_name':artist['name'], 'external_url': artist['href']}
                artist_list.append(artist_dict)


# In[19]:


artist_list


# In[20]:


song_list = []
for row in data['items']:
    song_id = row['track']['id']
    song_name = row['track']['name']
    song_duration = row['track']['duration_ms']
    song_url = row['track']['external_urls']['spotify']
    song_popularity = row['track']['popularity']
    song_added = row['added_at']
    album_id = row['track']['album']['id']
    artist_id = row['track']['album']['artists'][0]['id']
    song_element = {'song_id':song_id,'song_name':song_name,'duration_ms':song_duration,'url':song_url,
                    'popularity':song_popularity,'song_added':song_added,'album_id':album_id,
                    'artist_id':artist_id
                   }
    song_list.append(song_element)


# In[21]:


song_list


# In[22]:


#Converting ino dataframes
import pandas as pd
album_df = pd.DataFrame.from_dict(album_list)


# In[23]:


album_df.head()


# In[24]:


album_df.info()


# In[25]:


album_df = album_df.drop_duplicates(subset=['album_id']) #drop duplicates


# In[26]:


album_df.info()


# In[27]:


#Artist Dataframe
artist_df = pd.DataFrame.from_dict(artist_list)


# In[28]:


artist_df.head()


# In[29]:


artist_df = artist_df.drop_duplicates(subset=['artist_id'])


# In[30]:


#Song Dataframe
song_df = pd.DataFrame.from_dict(song_list)


# In[31]:


song_df.head()


# In[32]:


album_df['release_date'] = pd.to_datetime(album_df['release_date']) #changed datatype of release date to datetime


# In[33]:


album_df.info()


# In[34]:


song_df['song_added'] =  pd.to_datetime(song_df['song_added'])


# In[35]:


song_df.info()


# In[36]:


song_df.head()


# In[37]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[38]:


# Set the style for seaborn
sns.set(style="whitegrid")


# In[39]:


# Visualization: Album Release Distribution
plt.figure(figsize=(12, 6))
sns.lineplot(x='release_date', y='total_tracks', data=album_df, label='Number of Tracks')
plt.title('Album Release Distribution')
plt.xlabel('Release Date')
plt.ylabel('Number of Tracks')
plt.show()


# In[40]:


# Visualization: Top 10 Albums by Popularity
top_n = 10
top_albums = album_df.nlargest(top_n, 'total_tracks')

plt.figure(figsize=(12, 6))
sns.barplot(x='total_tracks', y='name', data=top_albums, palette='viridis')
plt.title(f'Top {top_n} Albums by Total Tracks')
plt.xlabel('Total Tracks')
plt.ylabel('Album Name')
plt.show()

