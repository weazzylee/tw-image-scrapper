import tweepy
import sqlite3
import configparser
import datetime
import os
import requests

config = configparser.ConfigParser()
config.read('config.ini')

consumer_key = config.get('Twitter API', 'consumer_key')
consumer_secret = config.get('Twitter API', 'consumer_secret')
access_token = config.get('Twitter API', 'access_token')
access_token_secret = config.get('Twitter API', 'access_token_secret')
database_file = config.get('File Paths', 'database_file')
save_images = config.getboolean('Options', 'save_images')

conn = sqlite3.connect(database_file)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS images (id TEXT PRIMARY KEY, url TEXT, author TEXT)''')

last_scraping_date = config.get('Scraping', 'last_scraping_date', fallback='')

if last_scraping_date:
    last_scraping_date = datetime.datetime.strptime(last_scraping_date, '%Y-%m-%d %H:%M:%S')
else:
    last_scraping_date = datetime.datetime.min

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

favorite_tweets = tweepy.Cursor(api.favorites, tweet_mode='extended').items()

for tweet in favorite_tweets:
    if tweet.created_at > last_scraping_date:
        for media in tweet.entities.get("media", []):
            if media["type"] == "photo":
                image_id = media["id_str"]
                image_url = media["media_url"]
                author = tweet.user.screen_name

                c.execute('''SELECT id FROM images WHERE id=?''', (image_id,))
                if not c.fetchone():
                    c.execute('''INSERT INTO images (id, url, author) VALUES (?, ?, ?)''', (image_id, image_url, author))
                    
                    if save_images:
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            image_data = response.content
                            image_filename = f"{image_id}.jpg"
                            image_path = os.path.join("images", image_filename)
                            os.makedirs("images", exist_ok=True)
                            with open(image_path, 'wb') as image_file:
                                image_file.write(image_data)

current_date = datetime.datetime.now()
current_date_str = current_date.strftime('%Y-%m-%d %H:%M:%S')
config.set('Scraping', 'last_scraping_date', current_date_str)
with open('config.ini', 'w') as config_file:
    config.write(config_file)

conn.commit()
conn.close()
