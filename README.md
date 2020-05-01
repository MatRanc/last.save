# last.save
Save lastfm data to a spreadsheet! The non-webapp version of last.charts.

**USAGE:**  
1. Create a file called `secret_key.py` and put this code in it   ```lastfm_apikey = "[YOUR_KEY]"```, replacing [YOUR_KEY] with your last.fm api key.  
2. Edit this line `load_top_artists("username", 20, "6month")` (ctrl+f to find it) with the following options  
  
`load_top_artists(lastfm_username, artist_limit, time_period)`  
  artist load limit = 1-1000  
  time period = overall, 7day, 1month, 3month, 6month, 12month  
  
 3. run `python main.py`
 4. ???
 5. Profit!
