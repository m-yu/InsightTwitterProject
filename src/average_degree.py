#!/usr/bin/env python

import sys
import json
from datetime import datetime

class Graph():
    def __init__(self):
        self.vertList = {}

    def addVertex(self,vertex):
        if vertex not in self.vertList:
           self.vertList[vertex] = []

    def addEdge(self,edgef,edget):
        if edgef in self.vertList:
           if edget not in self.vertList[edgef]:
              self.vertList[edgef].append(edget)
        else:
           self.vertList[edgef] = [edget]

    def vertex_degree(self,vertex):
        return len(self.vertList[vertex])
        
if  __name__ == "__main__":

    with open(sys.argv[1],'r') as json_file:
        #construct a list of tuple to store [(time:[hashtags])]
        tweetList = []
        ave_degree = 0.00

        f = open(sys.argv[2],'w')
        for line in json_file:
           json_data = json.loads(unicode(line))
           if "created_at" not in json_data:
              continue
           ttweet = datetime.strptime(json_data["created_at"], '%a %b %d %H:%M:%S +0000 %Y')

           hashtags = []
           for tag in json_data["entities"]["hashtags"]:
             hashtags.append(tag['text'])
           hashtags = list(set(hashtags))

           """ whether the new tweet arrives out of order in time? 
            deltaT = time of new tweet - the maximum timestamp
            deltaT > 0 in order
            deltaT > -60 and deltaT < 0 out of order but within 60 sec frame
            deltaT < -60 should be ignrored
           """
           if tweetList:
             deltaT = (ttweet - tweetList[-1][0]).total_seconds()
           else:
             deltaT = 10.0
             
           # tweet with zero or one hashtags would be ignored
           if len(hashtags) <= 1 or deltaT < -60.0:
              f.write('%.2f\n'%(int(ave_degree*100.0/100.0)))

           else:
             tweetList.append((ttweet,hashtags))
             if deltaT < 0:
               tweetList.sort(key= lambda tup: tup[0])
             # remove an old tweet that is more than 60 seconds old
             stop = False
             while not stop :
                  age = (tweetList[-1][0]-tweetList[0][0]).total_seconds()
                  if age >= 60:
                     tweetList.pop(0)
                  else:
                    stop = True
             #create a graph
             graph = Graph()
             for itweet in range(len(tweetList)):
               for vertexi in tweetList[itweet][1]:
                 graph.addVertex(vertexi)
               for i in range(len(tweetList[itweet][1])-1):
                 for j in range(i+1,len(tweetList[itweet][1])):
                   graph.addEdge(tweetList[itweet][1][i],tweetList[itweet][1][j])
                   graph.addEdge(tweetList[itweet][1][j],tweetList[itweet][1][i])
             #calculate the average degree of vertex
             sum_degree = 0
             for i in graph.vertList:
                 sum_degree += graph.vertex_degree(i)
             ave_degree = sum_degree / float(len(graph.vertList))
             f.write("%.2f\n"%(int(ave_degree*100.0)/100.0))
        f.close()

