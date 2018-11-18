# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:33:11 2018

@author: doshi
"""
import json
import sys
import re

id_tweet_dict = {}

#Fetching data from 
with open('Tweets.json', 'r') as fh:
    for line in fh:
        tweet = json.loads(line)
        id_tweet_dict[tweet['id']] = re.sub('(\\n)',' ',re.sub('(http.*)*(\.\.\.)*','',tweet['text']))         #tweet['text']
        
seed_list = []

#Reading Seeding file line by line and seprate from commas and store in list

with open('InitialSeeds.txt','r') as sf:
    for line in sf:
        seed_list.append(line.split(',')[0])

def jaccard_distance(x,y):
    
    x = x.split(" ")
    y = y.split(" ")
    x_U_y = len(set(x).union(set(y)))
    x_I_y = len(set(x).intersection(set(y)))    
    d = 1 - (x_I_y/x_U_y)
    return d

def calculate_SSE(cluster):
    SSE = 0
    for id,tweets in cluster.items():
        for tweet in tweets:
            SSE_dist = jaccard_distance(id_tweet_dict[int(id)],id_tweet_dict[tweet])
#            print("SSE_dist:"+str(SSE_dist))
#            print()
            SSE = SSE + SSE_dist * SSE_dist 
    return SSE

def k_means(k, seed_list, id_tweet_dict, output):
    
    if k > len(seed_list):
        print("Number of clusters ", k ," is more than Numbers of Seeds",len(seed_list))
        return
    elif k < len(seed_list):
        print("Truncating seed list as k is less than number of seeds")
        seed_list = seed_list[0:k]
        

    cluster = {}
    
    for seed in seed_list:
        cluster[seed] = []
    
#Creating Cluster by measuring each tweet with each seed and adding it in respective cluster
    for id,tweet in id_tweet_dict.items():
        min_dist = sys.maxsize
        min_seed = ''
        for seed in seed_list:
            dist = jaccard_distance(id_tweet_dict[int(seed)],tweet)
            if(dist < min_dist):
                min_dist = dist
                
                min_seed = seed
        cluster[min_seed].append(id)
        
    seed_list = []

#Make new seed list from new clusters by taking mean
    for id,tweets in cluster.items():
        best_centroid_dist = 255
        best_centroid = ''
        for tweet in tweets:
            distance = 0
            for each_tweet in tweets:
                distance = distance + jaccard_distance(id_tweet_dict[int(tweet)],id_tweet_dict[int(each_tweet)])

            mean = distance/len(tweets)
            
            if(mean < best_centroid_dist):
                best_centroid_dist = distance
                best_centroid = tweet
        seed_list.append(best_centroid)    


    if output == str(cluster):
        count = 1
        file = open('tweets-k-means-output.txt.','w')
        i=1
        for key,value in cluster.items():
            file.write(str(i) + '     ' )
            for x in value:
                count += 1
                file.write(str(x) +', ')
            file.write('\n')
            i+=1
#        print(count)
        file.write("SSE:" + str(calculate_SSE(cluster)))
        file.close()
        return    
        
    output = str(cluster)
    k_means(k, seed_list,id_tweet_dict, output)
    
k_means(25, seed_list, id_tweet_dict, output='')