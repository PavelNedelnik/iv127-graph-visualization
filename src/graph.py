import networkx as nx

def is_element_edge(element):
    return 'source' in element['data']

def graph_index_from_elements(element):
    if 'data' in element:
        return int(element['data']['id'][1:])
    return int(element['id'][1:])

def edge_pair_from_elements(element):
    return int(element['data']['source'][1:]), int(element['data']['target'][1:])

def garph_index_to_elements(idx, edge=False):
    return f'e{idx}' if edge else f'n{idx}'


def graph_edge_as_elements(source, target, params):
    return {
        'data': {
            'source': garph_index_to_elements(source),
            'target': garph_index_to_elements(target),
            'color': params['color']
        }
    }

def graph_as_elements(G, pos):
    elements = [{
            'data': {
                'id': garph_index_to_elements(idx),
                'label':params['label'],
                'color': params['color']
            } | params, 
            'position': {'x': pos[idx][0], 'y': pos[idx][1]}
        } for idx, params in G.nodes(data=True) ]
    elements += [graph_edge_as_elements(s, t, params) for s, t, params in G.edges(data=True)]
    return elements

def graph_from_elements(elements, size):
    G = nx.DiGraph(size=size)
    G.add_nodes_from([(graph_index_from_elements(elem), elem['data'])
                      for elem in elements if 'source' not in elem['data']])
    G.add_edges_from([edge_pair_from_elements(elem) for elem in elements if 'source' in elem['data'] and elem['data']['color'] == 'black'], color='black')
    G.add_edges_from([edge_pair_from_elements(elem) for elem in elements if 'source' in elem['data'] and elem['data']['color'] == 'silver'], color='silver')
    return G