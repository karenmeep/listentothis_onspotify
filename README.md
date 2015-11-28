# listentothis_onspotify
Turns [listentothis](https://www.reddit.com/r/listentothis/) subreddit's top from month to a Spotify playlist

## Quick start

1. Create an application at https://developer.spotify.com 
1. Get your client id and client secret key, setup a dummy redirect url (eg. 'http://localhost')
1. Setup your environment:
  ```
  export SPOTIPY_CLIENT_ID='your_client_id'
  export SPOTIPY_CLIENT_SECRET='your_client_secret'
  export SPOTIPY_REDIRECT_URI='your_redirect_url'
  ```
  
1. Install script dependencies 

  `pip install -r requirements.txt`

1. Run the script using your Spotify username

  `$ python main.py --username your_username`
  
