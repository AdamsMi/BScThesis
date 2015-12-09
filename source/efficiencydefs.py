import networkx as nx

def globalefficiency(G):
    nodes = G.nodes()   # get nodes
    N = len(nodes)      # count nodes
    ssl = 0            # sum of inverse of the shortest path lengths

    # nicked from nx.single_source_shortest_path_length to sum shortest lengths
    for node in nodes:
        seen={}                  # level (number of hops) when seen in BFS
        level=0                  # the current level
        nextlevel={node:1}  # dict of nodes to check at next level
        while nextlevel:
            thislevel=nextlevel  # advance to next level
            nextlevel={}         # and start a new list (fringe)
            for v in thislevel:
                if v not in seen: 
                    seen[v]=level # set the level of vertex v
                    nextlevel.update(G[v]) # add neighbors of v
            level=level+1
        if sum(seen.values())>0:
            invpl = 1/(float(sum(seen.values())))
            ssl = ssl+invpl         # sum shortest path lengths
    
    if N>1:
        Geff = (1/(float(N)*(float(N-1))))*float(ssl)
        return Geff
    else:
        return 'NA'
    

def nodalefficiency(G,i):
    nodes = G.nodes()   # get nodes
    if i in nodes:
        nodes.remove(i)
        N = len(nodes)      # count nodes
    
        # nicked from nx.single_source_shortest_path_length to sum shortest lengths
        seen={}                  # level (number of hops) when seen in BFS
        level=0                  # the current level
        nextlevel={i:1}  # dict of nodes to check at next level
        while nextlevel:
            thislevel=nextlevel  # advance to next level
            nextlevel={}         # and start a new list (fringe)
            for v in thislevel:
                if v not in seen: 
                    seen[v]=level # set the level of vertex v
                    nextlevel.update(G[v]) # add neighbors of v
            level=level+1
                
        invpl = 1/(float(sum(seen.values())))      # inverse of shortest path length
        
        Neff = float(N-1)*float(invpl)
        
        print 'Nodal efficiency = '+str(Neff)
        return Neff
       
    else:
        return 'NA'

def localefficiency(G,nodelist):      # nodelist are the nodes of subgraph within graph G
    edges = G.edges()
    sgedges = []       #create list of subgraph edges
    for edge in edges:
        if (edge[0] in nodelist and edge[1] in nodelist):
            sgedges.append(edge)
    sg = nx.Graph()             # create subgraph
    sg.add_nodes_from(nodelist)                 #populate subgraph with nodes
    sg.add_edges_from(sgedges)                # populate subgraph with edges
    
    N = len(nodelist)      # count nodes
    ssl = 0            # sum of inverse of the shortest path lengths

    # nicked from nx.single_source_shortest_path_length to sum shortest lengths
    for node in nodelist:
        nodelist.remove(node)
        seen={}                  # level (number of hops) when seen in BFS
        level=0                  # the current level
        nextlevel={node:1}  # dict of nodes to check at next level
        while nextlevel:
            thislevel=nextlevel  # advance to next level
            nextlevel={}         # and start a new list (fringe)
            for v in thislevel:
                if v not in seen:
                    seen[v]=level # set the level of vertex v
                    nextlevel.update(sg[v]) # add neighbors of v
            level=level+1
        
        if sum(seen.values()) >0:         
            invpl = 1/(float(sum(seen.values())))      # inverse of shortest path length
            ssl = ssl+invpl         # sum shortest path lengths
        nodelist.append(node)
    
    if N>1:
        Leff = (1/(float(N)*(float(N-1))))*float(ssl)
        return Leff
    else:
        return 'Na'
        
        