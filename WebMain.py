from NetworkConnectivity import NetworkGraph
import networkx as nx
import bottle

graph = NetworkGraph()
down_buf = {}


def tojson(graph):
    nodes = []
    edges = []
    g = nx.Graph()
    g.add_nodes_from(graph.nodes)
    g.add_edges_from(graph.edges)
    pos = nx.spring_layout(g, scale=500.0)

    for node in graph.nodes:
        nodes.append({'id': node,
                      'label': str(node),
                      'x': int(pos[node][0]),
                      'y': int(pos[node][1]),
                      'size': 3,
                      'color': '#B30000'})
    for i, val in enumerate(graph.edges):
        edges.append({'id': i,
                      'source': val[0],
                      'target': val[1],
                      'color': '#B30000'})
    return {'nodes': nodes, 'edges': edges}


@bottle.route('/')
def index():
    return bottle.static_file('index.html', root='./assets/')


@bottle.route('/assets/:path#.+#')
def assets(path):
    return bottle.static_file(path, root='./assets/')


@bottle.route('/generate')
def generate():
    try:
        node_num = int(bottle.request.params.get("node_num", None))
        edge_num = int(bottle.request.params.get("edge_num", None))
    except:
        return {'result': False}
    graph.random_generator(node_num, edge_num)
    while not graph.connective():
        graph.random_generator(node_num, edge_num)
    return {'result': True}


@bottle.route('/redundancy')
def redundancy():
    global down_buf
    result = []
    g, edges = graph.check_redundancy()
    for e in edges:
        result.append(graph.edges.index(e))
    down_buf = tojson(g)
    return {'result': result}


@bottle.route('/reliability')
def reliability():
    global down_buf
    result = []
    _, edges = graph.check_reliability()
    for e in edges:
        result.append(graph.edges.index(e))
    down_buf = {'reliability_edge': edges}
    return {'result': result}


@bottle.route('/key_node')
def key_node():
    global down_buf
    nodes = graph.key_node()
    down_buf = {'key_node': nodes}
    return {'result': nodes}


@bottle.route('/json')
def json():
    global down_buf
    down_buf = tojson(graph)
    return down_buf


@bottle.route('/download')
def download():
    return down_buf


bottle.run(host='localhost', port=8080)
