import requests
import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# api_key is stored in config.py
import config
import networkx as nx

import collections



#Function to flatten dictionary nesting of channel resp for dataframe format
#Returns a list of dictionaries where each key in the dictionary maps to a column of interest.
#As input takes a list of dictionaries where each dictionary is a specific 'item' from the original json.


### Pulling channel details by channel origin
def extract_channel_details(channels_details_items_list):
    '''Function to flatten dictionary nesting of channel resp for dataframe format.
    Returns a list of dictionaries where each key in the dictionary maps to a column of interest.
    As input takes a list of dictionaries where each dictionary is a specific 'item' from the original json.'''
    # Instantite empty channels details list for new dictionary format
    if channels_details_items_list is None:
        return None
    channels_details_list = list()
    
    # Loop over each channel's json dictionary in details_list
    for channel in channels_details_items_list:
        # Instantiate new details dictionary; in series update the dictionary to include relevant details
        channel_details_dict = {}
        channel_details_dict.update(dict(id=channel['id']))
        channel_details_dict.update(channel['snippet'])
        channel_details_dict.update(channel['contentDetails'])
        #channel_details_dict.update(channel['topicDetails'])
        channel_details_dict.update(channel['status'])
        channel_details_dict.update(channel['statistics'])
        channel_details_dict.update(channel['brandingSettings']['channel'])
        channel_details_dict.update(dict(distance=channel['distance']))
        #print(channel.keys())
        
        
        # Append the added channel's new dictionary format to channel details list
        channels_details_list.append(channel_details_dict)
    return channels_details_list


def create_df_from_details_list(channel_details_list):
    if channel_details_list is None:
        return None
    df = pd.DataFrame(channel_details_list)
    df['videos'] = df['videoCount'].map(lambda x: int(x))
    df['commentCount'] = df['commentCount'].map(lambda x: int(x))
    df['views'] = df['viewCount'].map(lambda x: int(x))
    df['subscribers'] = df['subscriberCount'].map(lambda x: int(x))
    df['distance'] = df['distance'].map(lambda x: int(x))
    df['outDegree'] = df['featuredChannelsUrls'].apply(lambda x: 0 if type(x) == float else len(x))
    return df

features = ['id','title','description','customUrl','publishedAt','country','isLinked', 'views', 'commentCount', 'subscribers', 'hiddenSubscriberCount','keywords','showRelatedChannels','featuredChannelsUrls', 'outDegree']
