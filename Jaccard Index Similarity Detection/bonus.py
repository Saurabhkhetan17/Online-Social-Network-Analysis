import copy
import math
import networkx as nx
import urllib.request


def jaccard_wt(graph, node):

    nbr_a = set(graph.neighbors(node))
    a = graph.degree(nbr_a)
    tup_score = []
    deg_a = 0

    for i in a:
        deg_a += a[i]

    for nod in graph.nodes():
        if nod not in nbr_a and nod != node:

            nbr_b = set(graph.neighbors(nod))
            b = graph.degree(nbr_b)
            deg_b = 0

            for n in b:
                deg_b += b[n]

            den = (1/deg_a) + (1/deg_b)
            common = nbr_a & nbr_b
            comm_deg = graph.degree(common)


            for n in comm_deg:
                comm_deg[n] = 1/comm_deg[n]
            num = sum(comm_deg.values())
            jaccard_score = num / den
            tup_score.append(((node,nod), jaccard_score))

    return tup_score

pass
