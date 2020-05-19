from secret_key import *

import pandas as pd
import requests as rq
import json

def load_top_artists(lastfm_username, artist_limit, time_period): #artist load limit = 1-1000   ///   time period = overall, 7day, 1month, 3month, 6month, 12month

    #declares array
    global top_artists_rawarray
    global top_artists_playcount_rawarray
    top_artists_rawarray = []
    top_artists_playcount_rawarray = []

    #loads from api and formats
    top_artists_requests_json = json.loads(rq.get("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+lastfm_username+"&api_key="+lastfm_apikey+"&format=json&limit="+str(artist_limit)+"&period="+time_period).text)
    top_artists_total = int(top_artists_requests_json["topartists"]["@attr"]["total"])
    top_artists_perpage = int(top_artists_requests_json["topartists"]["@attr"]["perPage"])

    #if user input for artist range is bigger than whats availible, to avoid error it will display the max availible number of artists
    if top_artists_perpage < top_artists_total:
        top_artists_acceptablerange = top_artists_perpage
    else: top_artists_acceptablerange = top_artists_total

    print("Loaded data for "+lastfm_username+"'s top "+str(top_artists_acceptablerange)+" artists for a time period of "+time_period+"\n")

    for x in range(top_artists_acceptablerange):
        #adds artist name to array
        artist_name = top_artists_requests_json["topartists"]["artist"][x]["name"]
        top_artists_rawarray.append(artist_name)

        #adds artist playcount to arrays
        artist_playcount = top_artists_requests_json["topartists"]["artist"][x]["playcount"]
        top_artists_playcount_rawarray.append(artist_playcount)

def load_top_artist_pandadb():
    global artists_dataframe
    #sets panda series
    top_artists = pd.Series(top_artists_rawarray)
    top_artists_playcount = pd.Series(top_artists_playcount_rawarray)
    #combines into single dataframe
    artists_dataframe = pd.DataFrame({"Artists":top_artists,"Playcount":top_artists_playcount})

def load_top_albums(lastfm_username, album_limit, time_period): #artist load limit = 1-1000   ///   time period = overall, 7day, 1month, 3month, 6month, 12month

    #declares array
    global top_albums_rawarray
    global top_albums_playcount_rawarray
    global top_albums_acceptablerange
    
    top_albums_rawarray = []
    top_albums_playcount_rawarray = []
    top_albums_acceptablerange = 0

    #loads from api and formats
    lastfm_apiurl_albums = "http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user="+lastfm_username+"&api_key="+lastfm_apikey+"&format=json&limit="+str(album_limit)+"&period="+time_period
    top_albums_requests_json = json.loads(rq.get(lastfm_apiurl_albums).text)
    top_albums_total = int(top_albums_requests_json["topalbums"]["@attr"]["total"])
    top_albums_perpage = int(top_albums_requests_json["topalbums"]["@attr"]["perPage"])

    #if user input for artist range is bigger than whats availible, to avoid error it will display the max availible number of artists
    if top_albums_perpage <= top_albums_total:
        top_albums_acceptablerange = top_albums_perpage
    else: top_albums_acceptablerange = top_albums_total

    print("Loaded data for "+lastfm_username+"'s top "+str(top_albums_acceptablerange)+" artists for a time period of "+time_period+"\n")
    for x in range(top_albums_acceptablerange):
        #only adds artist to array if their playcount is greater than __
        #make this a clickable option
        if int(top_albums_requests_json["topalbums"]["album"][x]["playcount"]) >= 2:
            #adds artist name to array
            album_name = (top_albums_requests_json["topalbums"]["album"][x]["name"]).replace("'", " ").replace("\\", " ").replace(","," ").replace("/", " ") #whats with artists putting \ and ' in there name???
            top_albums_rawarray.append(album_name)

            #adds artist playcount to arrays
            album_playcount = top_albums_requests_json["topalbums"]["album"][x]["playcount"]
            top_albums_playcount_rawarray.append(album_playcount)
        else: pass

def load_top_albums_pandadb():
    global albums_dataframe
    #sets panda series
    top_albums = pd.Series(top_albums_rawarray)
    top_albums_playcount = pd.Series(top_albums_playcount_rawarray)
    #combines into single dataframe
    albums_dataframe = pd.DataFrame({"Albums":top_albums,"Playcount":top_albums_playcount})

print("Requesting data from last.fm...")
load_top_artists("MatRanc", 20, "6month")
load_top_artist_pandadb()
load_top_albums("MatRanc", 20, "overall")
load_top_albums_pandadb()

print(artists_dataframe)
print(albums_dataframe)

print("\nExporting spreadsheet...")
#EDIT THE PATH TO WHERE YOU WANT THE SPREADSHEET EXPORTED
artists_dataframe.to_excel(r"D:\Development\last.charts\output\useroutput.xlsx")
print("Export complete.")

"""
pip install:
flask
requests
pandas
openpyxl
"""
