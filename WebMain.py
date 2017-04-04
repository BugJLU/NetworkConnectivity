from NetworkConnectivity import NetworkGraph
import networkx as nx
import bottle

graph = NetworkGraph()
last_graph = None
layout = {}


def do_layout(scale=500.0):
    global graph, layout
    g = nx.Graph()
    g.add_nodes_from(graph.nodes)
    g.add_edges_from(graph.edges)
    layout = nx.spring_layout(g, scale=scale)


def to_json(network_graph):
    nodes = []
    edges = []
    for node in network_graph.nodes:
        nodes.append({
            'id': node,
            'label': str(node),
            'x': int(layout[node][0]),
            'y': int(layout[node][1]),
            'size': 3
        })
    for i, val in enumerate(network_graph.edges):
        edges.append({
            'id': i,
            'source': val[0],
            'target': val[1]
        })
    return {'nodes': nodes, 'edges': edges}


@bottle.route('/')
def index():
    return bottle.static_file('index.html', root='./assets/')


@bottle.route('/assets/:path#.+#')
def assets(path):
    return bottle.static_file(path, root='./assets/')


@bottle.route('/generate')
def generate():
    global graph, last_graph
    try:
        node_num = int(bottle.request.params.get("node_num", None))
        edge_num = int(bottle.request.params.get("edge_num", None))
    except:
        return {'result': False, 'error': 'Parameter error.'}
    try_times = 0
    while True:
        graph.random_generator(node_num, edge_num)
        try_times += 1
        if graph.connective():
            break
        if try_times >= 5:
            return {'result': False, 'error': 'Unconnective.'}
    do_layout()
    last_graph = graph
    return {'result': True}


@bottle.route('/raw_graph')
def raw_graph():
    global graph, last_graph
    last_graph = graph
    return {'graph': to_json(graph)}


@bottle.route('/redundancy')
def redundancy():
    global graph, last_graph
    result = []
    g, edges = graph.check_redundancy()
    for e in edges:
        result.append(graph.edges.index(e))
    last_graph = g
    return {'graph': to_json(g)}


@bottle.route('/reliability')
def reliability():
    global last_graph
    result, edges = last_graph.check_reliability()
    json = {'result': result, 'graph': to_json(last_graph), 'edges': []}
    for e in edges:
        json['edges'].append(last_graph.edges.index(e))
    return json


@bottle.route('/key_node')
def key_node():
    global last_graph
    nodes = last_graph.key_node()
    return {'result': nodes}


bottle.run(host='localhost', port=8080)
