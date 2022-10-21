import subprocess
import random

NODES = 20
X = float('inf')
graph = []
for i in range(NODES):
    graph.append([X] * NODES)

# Generate a random graph
for i in range(NODES):
    for j in range(NODES):
        if random.random() < 0.1:
            graph[i][j] = random.randint(1, 50)

# Copy the graph
init_graph = [row[:] for row in graph]

# Render the graph as DOT and save an image
dot = 'digraph G {'
for i in range(NODES):
    for j in range(NODES):
        if init_graph[i][j] != X:
            dot += '%d -> %d [label=%d];' % (i, j, init_graph[i][j])
dot += '}'
with open('graph.dot', 'w') as f:
    f.write(dot)
subprocess.call(['circo', '-Tpng', 'graph.dot', '-o', 'graph-init.png'])

# Run the algorithm
for k in range(NODES):  # For every intermediate node
    for i in range(NODES):
        for j in range(NODES):
            # For every path that doesn't go through the intermediate node
            if k != i and k != j:
                # If it is shorter to go through the intermediate node,
                if graph[i][j] > graph[i][k] + graph[k][j]:
                    # update the path to go through the intermediate node
                    graph[i][j] = graph[i][k] + graph[k][j]
                    
# Render the graph as DOT and save an image
dot = 'digraph G {'
for i in range(NODES):
    for j in range(NODES):
        if graph[i][j] != X:
            dot += '%d -> %d [label=%d];' % (i, j, graph[i][j])
dot += '}'
with open('graph.dot', 'w') as f:
    f.write(dot)
subprocess.call(['circo', '-Tpng', 'graph.dot', '-o', 'graph-final.png'])

template = open('report_template.tex')
template = template.read()
for row in template.splitlines():
    if '<<sourcecode>>' in row:
        print(open('simple.py').read())
    elif '<<matrix-init>>' in row:
        print(r'\begin{array}{' + ''.join(['c'] * NODES) + '}')
        for i in range(NODES):
            print(' & '.join(
                [f"{x}" if x != X else r'\infty' for x in init_graph[i]]
            ) + r' \\ ')
        print(r'\end{array}')
    elif '<<matrix-result>>' in row:
        print(r'\begin{array}{' + ''.join(['c'] * NODES) + '}')
        for i in range(NODES):
            print(' & '.join(
                [f"{x}" if x != X else r'\infty' for x in graph[i]]
            ) + r' \\')
        print(r'\end{array}')
    else:
        print(row.strip())
