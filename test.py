import networkx as nx
import plotly.graph_objects as go

# Example graph data: nodes are courses, edges are prerequisites relationships
graph_data = {
    "ENGN 0040": ["ENGN 0041", "ENGN 0042"],
    "CSCI 0150": ["CSCI 0160"],
    "MATH 0200": ["CSCI 0150", "ENGN 0040"]
}

# Create a directed graph
G = nx.DiGraph()
for course, postreqs in graph_data.items():
    for postreq in postreqs:
        G.add_edge(course, postreq)

# 3D layout
pos = nx.spring_layout(G, dim=3)  # Generate positions in 3D space

# Extract node positions
node_x, node_y, node_z = [], [], []
for node in G.nodes():
    x, y, z = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_z.append(z)

# Extract edge start and end points
edge_x, edge_y, edge_z = [], [], []
for edge in G.edges():
    x0, y0, z0 = pos[edge[0]]
    x1, y1, z1 = pos[edge[1]]
    edge_x += [x0, x1, None]  # None separates each edge visually
    edge_y += [y0, y1, None]
    edge_z += [z0, z1, None]

# Create edge trace
edge_trace = go.Scatter3d(
    x=edge_x, y=edge_y, z=edge_z,
    mode='lines',
    line=dict(width=1, color='blue'),
    hoverinfo='none'
)

# Create node trace
node_trace = go.Scatter3d(
    x=node_x, y=node_y, z=node_z,
    mode='markers+text',
    marker=dict(size=8, color='red', opacity=0.8),
    text=list(G.nodes()),
    textposition='top center',
    hoverinfo='text'
)

# Combine edge and node traces
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title="3D Interactive Course Prerequisite Visualization",
                    scene=dict(
                        xaxis=dict(showbackground=True),
                        yaxis=dict(showbackground=True),
                        zaxis=dict(showbackground=True),
                    ),
                    margin=dict(l=0, r=0, b=0, t=40)
                ))

fig.show()
