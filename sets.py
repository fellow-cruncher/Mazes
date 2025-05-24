import itertools

values = list(range(0, 101, 10))
triples = itertools.product(values, repeat=3)
pairs = itertools.product(values, repeat=2)

# Implementacje - Ja vs. GitHub
#SETS = [[x,x,x,y,y,y] for x,y in pairs]

# Metody - AStar vs. DFS vs. Dijkstra
#SETS = [[x,y,z,x,y,z] for x,y,z in triples]

SETS = [[i for _ in range(6)] for i in range(100,-1,-2)]