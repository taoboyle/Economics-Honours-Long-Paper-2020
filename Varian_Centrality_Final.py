# Run in terminal first?
# pip install pybliometrics

import pandas as pd
from pybliometrics.scopus import ScopusSearch, AbstractRetrieval, AuthorRetrieval, ContentAffiliationRetrieval, CitationOverview
import networkx as nx
import sys
 
import json

nodes=pd.DataFrame()
edges=[]
gen={}
outp=[]


# Papers 
# identiified using the DOI

Varian = "10.1007/b104899_7" 
ab = AbstractRetrieval(Varian, view="FULL")


# Paper 1

nodes=pd.DataFrame()
nodes = nodes.append({"id":"", "title": ab.title, "sourcetitle": ab.sourcetitle_abbreviation, "publicationyear": ab.coverDate[0:4], "eid": ab.eid, "gen": '0' }, ignore_index=True)

print("started running")

# First Generation of citations

s = ScopusSearch(ab.eid)
# print(list(nodes['eid']))
print(ab.eid)
# eid = 2-s2.0-78650750690


print("made it here 2")


generations = open("generations.csv", "w")
for x in s.results:
    if(x.eid not in list(nodes['eid'])):
        # print(x.title)
        nodes = nodes.append({"id":"", "title": x.title, "sourcetitle": "", "publicationyear": x.coverDate[0:4], "eid": x.eid, "gen": '1' }, ignore_index=True)
        outp.append({"id":"", "title": x.title})
    edges.append((ab.eid, x.eid))
    print("\n"+ab.eid+"           "+x.eid)
    generations.write(ab.eid+","+x.eid+"\n")


# print(len(nodes))

# f = open("file.json", "w")
# f.write(json.dumps(outp))
# f.close()

# Second Generation of citations

s = ScopusSearch(ab.eid) 
        
print("================================== second generation ========================\n\n\n\n")

for x in s.results:
    s = ScopusSearch(x.eid, verbose = True)
    if (s.results != None):
        for z in s.results:
            # print(ab.eid+"           "+x.eid)
            # edges.append((ab.eid, x.eid))
            if(z.eid not in list(nodes['eid'])):
                print(x.eid+"           "+z.eid)
                generations.write(x.eid+","+z.eid+"\n")
                
                nodes = nodes.append({"id":"", "title": z.title, "sourcetitle": "", "publicationyear": z.coverDate[0:4], "eid": z.eid, "gen": "2"}, ignore_index = True)
generations.close()
          
print(len(nodes))

print("================================== measures of centrality ========================\n\n\n\n")

import matplotlib.pyplot as plt # Version 3.0.3
import numpy as np

node_names = nodes['eid']   
gen = nodes.set_index('eid')['gen'].to_dict()

G = nx.DiGraph()
G.add_nodes_from(node_names)
G.add_edges_from(edges)
nx.set_node_attributes(G, gen, "gen")
selected_nodes = [n for n,v in G.nodes(data=True) if v['gen'] == '0' or v['gen'] == '1' or v['gen'] == '0'] 


all_indegree = nx.in_degree_centrality(G)
all_katz = nx.katz_centrality(G)
all_eigens = nx.eigenvector_centrality_numpy(G)
all_pagerank = nx.pagerank(G)
all_closeness = nx.closeness_centrality(G)

print("all_indegree")
# print(all_indegree)

katz = {key:value for key,value in all_katz.items() if key in selected_nodes}
indegree = {key:value for key,value in all_indegree.items() if key in selected_nodes}
eigens = {key:value for key,value in all_eigens.items() if key in selected_nodes}
pagerank = {key:value for key,value in all_pagerank.items() if key in selected_nodes}
closeness = {key:value for key,value in all_closeness.items() if key in selected_nodes}

print("indegree")
# print(indegree)


gen1 = [n for n,v in G.nodes(data=True) if v['gen'] == '1']  
gen1_katz = {key:value for key,value in all_katz.items() if key in gen1}
gen1_indegree = {key:value for key,value in all_indegree.items() if key in gen1}
gen1_eigens = {key:value for key,value in all_eigens.items() if key in gen1}
gen1_pagerank = {key:value for key,value in all_pagerank.items() if key in gen1}
gen1_closeness = {key:value for key,value in all_closeness.items() if key in gen1}

print("Indegree")
# print(gen1_indegree)

print("trying to find "+ab.eid)

print(indegree)

print("Paper 0")
print("PageRank: ", pagerank[ab.eid])
print("Indegree: ", indegree[ab.eid])
print("Katz: ", katz[ab.eid])
print("Eigenvector: ", eigens[ab.eid])
print("Closeness: ", closeness[ab.eid])

# new_df = pd.DataFrame()
# for i in gen1:
#     new_df=new_df.append({"eid": i,
#                           "original.katz": gen1_katz[i],
#                           "discounted.katz": gen1_katz[i]*0.98**(2019-nodes[nodes['eid'] == i]['publicationyear'].astype(float)).values[0],
#                           "original.indegree": gen1_indegree[i],
#                           "discounted.indegree": gen1_indegree[i]*0.98**(2019-nodes[nodes['eid'] == i]['publicationyear'].astype(float)).values[0],
#                          "original.eigens": gen1_eigens[i],
#                          "discounted.eigens": gen1_eigens[i]*0.98**(2019-nodes[nodes['eid'] == i]['publicationyear'].astype(float)).values[0],
#                          "original.closeness": gen1_closeness[i],
#                          "discounted.closeness": gen1_closeness[i]*0.98**(2019-nodes[nodes['eid'] == i]['publicationyear'].astype(float)).values[0],
#                          "original.pagerank": gen1_pagerank[i],
#                          "discounted.pagerank": gen1_pagerank[i]*0.98**(2019-nodes[nodes['eid'] == i]['publicationyear'].astype(float)).values[0]}, ignore_index=True)
# #     new_df=new_df.append({"eid": i,"discounted": gen1_eigens[i]}, ignore_index=True)
# new_df.sort_values("discounted.pagerank", ascending=False)


# #new_df.to_excel("Example1.xlsx")

# print("PageRank: ", pagerank[ab.eid])
# print("Indegree: ", indegree[ab.eid])
# print("Katz: ", katz[ab.eid])
# print("Eigenvector: ", eigens[ab.eid])
# print("Closeness: ", closeness[ab.eid])








