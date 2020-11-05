import pandas as pd
from pybliometrics.scopus import ScopusSearch, AbstractRetrieval, AuthorRetrieval, ContentAffiliationRetrieval
import networkx as nx

nodes=pd.DataFrame()
edges=[]
gen={}

Acquisti = "10.1257/jel.54.2.442"  
ab = AbstractRetrieval(Acquisti, view="FULL")


nodes=pd.DataFrame()
nodes = nodes.append({"id":"", "title": ab.title, "sourcetitle": ab.sourcetitle_abbreviation, "publicationyear": ab.coverDate[0:4], "eid": ab.eid, "gen": '0' }, ignore_index=True)
ref_df = pd.DataFrame(ab.references)
ref_df["eid"] = '2-s2.0-' + ref_df['id']
ref_df['gen'] = '-1'

ref_df2 = pd.concat([ref_df['eid'], ref_df['id'], ref_df['publicationyear'], ref_df['sourcetitle'], ref_df['title'], ref_df['gen']], axis=1, keys=['eid', 'id', 'publicationyear', 'sourcetitle', 'title', 'gen'], sort=True)
#ref_df2 = ref_df2.drop(18)
nodes = nodes.append(ref_df2, ignore_index = True, sort=True)
print("\n\n===========================step 1============================\n\n")
for row in ref_df2.itertuples():
    edges.append((row.eid, ab.eid))

len(nodes)

s = ScopusSearch(ab.eid) 
for x in s.results:
    if(x.eid not in list(nodes['eid'])):
        print(x.title)
        nodes = nodes.append({"id":"", "title": x.title, "sourcetitle": "", "publicationyear": x.coverDate[0:4], "eid": x.eid, "gen": '1' }, ignore_index=True)
    edges.append((ab.eid, x.eid))

print(len(nodes))

print("\n\n===========================step 2============================\n\n")

for y in ab.references:
    try:
        refs = AbstractRetrieval(y.id, view="FULL")
        if(refs.references != None):
            ref_df = pd.DataFrame(refs.references)
            ref_df["eid"] = '2-s2.0-' + ref_df['id']
            ref_df['gen'] = '-2'
            ref_df2 = pd.concat([ref_df['eid'], ref_df['id'], ref_df['publicationyear'], ref_df['sourcetitle'], ref_df['title'], ref_df['gen']], axis=1, keys=['eid', 'id', 'publicationyear', 'sourcetitle', 'title', 'gen'])
            
            for row in ref_df2.itertuples():
                if(row.id == '0000131597'):
                    print("here")
                edges.append((row.eid, '2-s2.0-' + y.id))
                if(row.id == '0000131597'):
                    print((row.eid, '2-s2.0-' + y.id))
                    print("now here")
                if(row.eid not in list(nodes['eid'])):
                    
                    nodes = nodes.append({"id":row.id, "title": row.title, "sourcetitle": row.sourcetitle, "publicationyear": row.publicationyear, "eid": row.eid, "gen": '-2' }, ignore_index=True)
                    print(row.title)
 
    except Exception as e:
        print("error ========= ")
        print(e)
        pass
           
len(nodes)

print("\n\n===========================step 3============================\n\n")
for x in s.results:
    s = AbstractRetrieval(x.eid, view="FULL")
    if(s.references != None):
        ref_df = pd.DataFrame(s.references)
        ref_df['eid'] = '2-s2.0-'+ ref_df['id']
        ref_df['gen'] = '9'
        ref_df2 = pd.concat([ref_df['eid'], ref_df['id'], ref_df['publicationyear'], ref_df['sourcetitle'], ref_df['title'], ref_df['gen']], axis=1, keys=['eid', 'id', 'publicationyear', 'sourcetitle', 'title', 'gen'])
        
        for row in ref_df2.itertuples():
            if(row.eid not in list(nodes['eid'])):
                print(row.title)
                nodes = nodes.append({"id": row.id, "title": row.title, "sourcetitle": row.sourcetitle, "publicationyear": row.publicationyear, "eid": row.eid, "gen": row.gen }, ignore_index=True)
            edges.append((row.eid, x.eid))
    
print(len(nodes))


import time
import random
print("\n\n===========================step 4============================\n\n")
then = time.time()
for y in ab.references:
    try:

        search = ScopusSearch(y.id, verbose=True)
        for x in search.results:
            edges.append(('2-s2.0-' + y.id, x.eid))
            if(x.eid not in list(nodes['eid'])):
                print(x.title)
                nodes = nodes.append({"id":"", "title": x.title, "sourcetitle": "", "publicationyear": x.coverDate[0:4], "eid": x.eid, "gen": "9"}, ignore_index = True)
    except Exception as e:
        print("error ========= ")
        print(e)
        pass
now = time.time()
print("It took: ", now-then, " seconds")


print("\n\n===========================step 5============================\n\n")
s = ScopusSearch(ab.eid) 
        
for x in s.results:
    s = ScopusSearch(x.eid, verbose = True)
    if (s.results != None):
        for z in s.results:
            edges.append((x.eid, z.eid))
            if(z.eid not in list(nodes['eid'])):
                nodes = nodes.append({"id":"", "title": z.title, "sourcetitle": "", "publicationyear": z.coverDate[0:4], "eid": z.eid, "gen": "2"}, ignore_index = True)
                print(z.title)
len(nodes)



import matplotlib.pyplot as plt # Version 3.0.3
import numpy as np
print("\n\n===========================step 6============================\n\n")
node_names = nodes['eid']   
gen = nodes.set_index('eid')['gen'].to_dict()

G = nx.DiGraph()
G.add_nodes_from(node_names)
G.add_edges_from(edges)
nx.set_node_attributes(G, gen, "gen")

print(node_names)

all_indegree = nx.in_degree_centrality(G)
all_closeness = nx.closeness_centrality(G)
all_katz = nx.katz_centrality(G)
all_eigens = nx.eigenvector_centrality(G, max_iter=2000)
all_pagerank = nx.pagerank(G)

selected_nodes = [n for n,v in G.nodes(data=True) if v['gen'] == '0' or v['gen'] == '-1' or v['gen'] == '-2']  

indegree = {key:value for key,value in all_indegree.items() if key in selected_nodes}
closeness = {key:value for key,value in all_closeness.items() if key in selected_nodes}
katz = {key:value for key,value in all_katz.items() if key in selected_nodes}
eigens = {key:value for key,value in all_eigens.items() if key in selected_nodes}
pagerank = {key:value for key,value in all_pagerank.items() if key in selected_nodes}

gen1 = [n for n,v in G.nodes(data=True) if v['gen'] == '-1']  
gen1_indegree = {key:value for key,value in all_indegree.items() if key in gen1}
gen1_closeness = {key:value for key,value in all_closeness.items() if key in gen1}
gen1_katz = {key:value for key,value in all_katz.items() if key in gen1}
gen1_eigens = {key:value for key,value in all_eigens.items() if key in gen1}
gen1_pagerank = {key:value for key,value in all_pagerank.items() if key in gen1}

print("Paper 0")
print("Indegree: ", indegree[ab.eid])
print("Closeness: ", closeness[ab.eid])
print("Katz: ", katz[ab.eid])
print("Eigenvector centrality: ", eigens[ab.eid])
print("PageRank: ", pagerank[ab.eid])
