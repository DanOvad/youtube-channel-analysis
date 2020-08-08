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






def extract_channel_details(channel_resp):
    # Instantite empty channels details list for new dictionary format
    channel_details_list = list()
    
    # Loop over each channel's json dictionary in details_list
    for channel in channel_resp:
        # Instantiate new details dictionary; in series update the dictionary to include relevant details
        channel_details_dict = {}
        channel_details_dict.update(dict(id=channel['id']))
        channel_details_dict.update(channel['snippet'])
        channel_details_dict.update(channel['contentDetails'])
        #channel_details_dict.update(channel['topicDetails'])
        channel_details_dict.update(channel['status'])
        channel_details_dict.update(channel['statistics'])
        channel_details_dict.update(channel['brandingSettings']['channel'])
        
        # Append the added channel's new dictionary format to channel details list
        channel_details_list.append(channel_details_dict)
    return channel_details_list

#CHANNEL_DETAILS_LIST = extract_channel_details(CHANNEL_RESP)

# Insert list of dictionaries into pandas dataframe
#df = pd.DataFrame(CHANNEL_DETAILS_LIST)



def create_dataframe(channel_details_list):
    df = pd.DataFrame(channel_details_list)
    df['videoCount'] = df['videoCount'].map(lambda x: int(x))
    df['commentCount'] = df['commentCount'].map(lambda x: int(x))
    df['viewCount'] = df['viewCount'].map(lambda x: int(x))
    df['subscriberCount'] = df['subscriberCount'].map(lambda x: int(x))
    df['featuredChannelsCount'] = df['featuredChannelsUrls'].apply(lambda x: 0 if type(x) == float else len(x))
    return df

features = ['id','title','description','customUrl','publishedAt','country','isLinked', 'viewCount', 'commentCount', 'subscriberCount',
           'hiddenSubscriberCount','keywords','showRelatedChannels','featuredChannelsUrls', 'featuredChannelsCount']

#DF = create_dataframe(CHANNEL_DETAILS_LIST)
#DF.shape


def extract_featured_channels(channel_response):
    ''' Function to extract a set of featured channelIds from a list of channelIds'''
    
    featured_channels_list = list()
    channels_wo_features_count = 0
    for channel in channel_response:

        if 'featuredChannelsUrls' in channel['brandingSettings']['channel']:
            featured_channels_list.extend(channel['brandingSettings']['channel']['featuredChannelsUrls'])
        else:
            channels_wo_features_count +=1
    print(f'{channels_wo_features_count} out of {len(channel_response)} channels do not feature channels')
    return set(featured_channels_list)