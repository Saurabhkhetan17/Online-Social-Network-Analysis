# -*- coding: utf-8 -*-
import pickle

def read_data():

    file = open("summary.txt", "w",encoding="utf8",newline='')
    graph = pickle.load(open('graph.pickle', 'rb'))
    print('\ntotal users in network: %d' % len(graph.nodes()))
    file.write('\ntotal users in network: %d' % len(graph.nodes()))
    tweets = pickle.load(open('tweets.pickle', 'rb'))
    print('\ntotal tweets: %d' % len(tweets))
    file.write('\ntotal tweets: %d' % len(tweets))
    clusters = pickle.load(open('clusters.pickle', 'rb'))
    print('\ntotal communities: %d' %(len(clusters)))
    file.write('\ntotal communities: %d' %(len(clusters)))
    num_users=0
    for i in range(len(clusters)):
        num_users += (clusters[i].order())
    print('\nusers per community: %f' %(num_users/(len(clusters))))
    file.write('\nusers per community: %f' %(num_users/(len(clusters))))
    (positives,negatives,combine) = pickle.load(open('classify.pickle', 'rb'))
    print('\ntotal positive, negative and combine tokens: %d positive instances , %d negative instances and %d combine instances'
    %(len(positives), len(negatives), len(combine)))
    file.write('\ntotal positive, negative and combine tokens: %d positive instances , %d negative instances and %d combine instances'
    %(len(positives), len(negatives), len(combine)))
    print('\n')
    file.write('\nexample of pos, neg, combine tokens: ')
    for tweet, pos, neg in sorted(positives, key=lambda x: x[1], reverse=False):
        positive = (pos,neg,tweet)
    print(positive[2])
    print("************")

    for tweet, pos, neg in sorted(negatives, key=lambda x: x[2], reverse=False):
        negative = (neg,pos,tweet)
    print(negatives[2])
    for tweet, pos, neg in sorted(combine, key=lambda x: x[2], reverse=True):
        combined = (pos,neg,tweet)

    print('positive:')
    print(positive)
    file.write('\npositive:')
    file.write(positive[2])
    print('negative:\n')
    print(negative)
    file.write('\nnegative:')
    file.write(negative[2])
    print('combined:')
    print(combined)
    file.write('\ncombined:')
    file.write(combined[2])
    file.close

def main():
    read_data()

if __name__ == '__main__':
    main()
