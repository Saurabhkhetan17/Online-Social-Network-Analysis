import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI
import pickle


def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    consumer_key = 'aSDmzRI0ajSveMxy5NQXaVRNo'
    access_token = '2998615999-KlweTZygNtdbSSzi0pIVc9b7vRlMx333ANCK8nS'
    consumer_secret = 'waNH54S3XUdgJQwHUivr4yUqc9tdc6ToJHVY4tZZKManNkceRg'
    access_token_secret = 'QShQOJ7rXlEdp0RCpn2vdlxKu4tLG2fXJLPcJ9y71G3o6'

    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def read_screen_names(filename):

    screen_names=open(filename,'r')
    ss = [s.strip() for s in screen_names.readlines()]
    return (ss)


def robust_request(twitter, resource, params, max_tries=5):

    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)

def get_users(twitter, screen_names):

    resource='users/lookup'
    params={'screen_name':screen_names}
    request = robust_request(twitter, resource, params)
    users= [i for i in request]
    return users

def get_friends(twitter, screen_name):

    resource = 'followers/ids'
    params={'screen_name':screen_name,'count':500}
    request= robust_request(twitter, resource ,params)
    friends= [i for i in request]
    return sorted(friends)

def add_all_friends(twitter, users):

    for i in range(len(users)):
        users[i]['friends'] = get_friends(twitter, users[i]['screen_name'])

def create_graph(users):

    graph=nx.Graph()
    for i in range(len(users)):
        user=users[i]['screen_name']
        graph.add_node(user)
        frnd = users[i]['friends']
        for f in frnd:
            graph.add_edge(user,str(f))
    return graph

def draw_network(graph, users, filename):

    candidates=set(u['screen_name'] for u in users)
    labels={}
    for n in graph.nodes():
        if n in candidates:
            labels[n] = n
        else:
            labels[n] = ''
    plt.figure(figsize=(12,12))
    nx.draw_networkx(graph,alpha=.5, labels=labels, width=.1, node_size=100)
    plt.axis("off")
    plt.savefig(filename)

def get_tweets(twitter, screen_name):

    tweets = []
    resource = 'search/tweets'
    for s in screen_name:
        request=robust_request(twitter,resource, {'q': s, 'lang':'en', 'count': 100})
        for t in request:
            tweets.append(t)
    return tweets

def main():

    twitter = get_twitter()
    screen_names = read_screen_names('candidates.txt')
    print(screen_names)
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    print('Found %d users with screen_names %s' %
          (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    graph = create_graph(users)
    draw_network(graph, users, 'network.png')
    pickle.dump(graph, open('graph.pickle', 'wb'), pickle.HIGHEST_PROTOCOL)
    tweets = get_tweets(twitter,screen_names)
    pickle.dump(tweets, open('tweets.pickle', 'wb'), pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    main()
