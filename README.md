# Twitter Image Scraping Script

This script allows you to scrape images from your favorite tweets on Twitter and save them to a SQLite database file.  
It will only scrape tweets that were posted after the last scraping date you specified in the configuration file, so you don't have to worry about scraping the same tweets multiple times. Optionally, you can also download the images to your computer.  
See the [Configuration](#configuration) section for more information. It uses the [Tweepy](https://www.tweepy.org/) library to access the Twitter API.

## Installation

1. Clone this repository: `git clone https://github.com/weazzylee/tw-image-scrapper.git`
2. Move into the project directory: `cd tw-image-scrapper`
3. Install the dependencies: `pip install -r requirements.txt`
4. Fill in the `config.ini` file with your Twitter API credentials and file paths. See the [Configuration](#configuration) section for more information.
5. Run the script: `python run.py`

## Configuration

You need to fill in the `config.ini` file before running the script. Here is an example configuration file:

```ini
[Twitter API]
consumer_key = YOUR_CONSUMER_KEY
consumer_secret = YOUR_CONSUMER_SECRET
access_token = YOUR_ACCESS_TOKEN
access_token_secret = YOUR_ACCESS_TOKEN_SECRET

[File Paths]
database_file = /path/to/database.db

[Options]
save_images = True

[Scraping]
last_scraping_date = 2023-05-28 12:00:00
```

Replace `YOUR_CONSUMER_KEY`, `YOUR_CONSUMER_SECRET`, `YOUR_ACCESS_TOKEN`, and `YOUR_ACCESS_TOKEN_SECRET` with your own Twitter API credentials. Also, specify the correct path to the SQLite database file.  
`last_scraping_date` is the date and time of the last scraping. The script will only scrape tweets that were posted after this date.  
If you want to scrape all tweets, set this value to `1970-01-01 00:00:00`. The date and time must be in the format `YYYY-MM-DD HH:MM:SS`.

## Database

The script uses a SQLite database to store information about the images. The database file is specified in the `[File Paths]` section of the configuration file. By default, if the database file doesn't exist, it will be created automatically when the script is executed.

## Images
`save_images` is a boolean value that indicates whether the images should be downloaded to your computer or not. If you set it to `False`, the images will only be saved to the database.  
If `save_images` is set to `True`, the images will be saved in the `images` directory. The directory will be created automatically if it doesn't exist.

## License

This project is licensed under the [MIT License](LICENSE).
