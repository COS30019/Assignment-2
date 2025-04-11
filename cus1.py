def dls (node,goal,edges,path,explored,limit,count):
    if node in goal:
        return node, count, path
    
    if limit <=0:
        return None, count,[]
    
    explored.add(node)

    for (_from, _to), _ in sorted(edges.items()):
        if _from == node and _to not in explored:
            new_path = path+[_to]
            goal_found, created, found_path= dls(_to, goal, edges, new_path,explored, limit -1, count +1)
            if goal_found:
                return goal_found, created, found_path
    
    explored.remove(node)
    return None,count,[]

def cus1(nodes, edges,orgin, destination):
    limit=5 #can limit the node lvl as u nned
    explored=set()
    return dls(orgin,set(destination), edges, [orgin], explored, limit, 1)
