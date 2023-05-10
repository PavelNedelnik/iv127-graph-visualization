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
        } | params
    }

def graph_as_elements(G, pos=None, scale_x=1, scale_y=1):
    elements = [{
            'data': {
                'id': garph_index_to_elements(idx),
            } | params, 
            'position': {'x': int(pos[idx][0] * scale_x), 'y': int(pos[idx][1] * scale_y)} if pos is not None else {'x': 0, 'y': 0}
        } for idx, params in G.nodes(data=True) ]
    elements += [graph_edge_as_elements(s, t, params) for s, t, params in G.edges(data=True)]
    return elements

def graph_from_elements(elements, size):
    G = nx.DiGraph(size=size)
    G.add_nodes_from([(graph_index_from_elements(elem), elem['data'])
                      for elem in elements if not is_element_edge(elem)])
    for elem in elements:
        if is_element_edge(elem):
            G.add_edge(*edge_pair_from_elements(elem), updated=elem['data']['updated'], type=elem['data']['type'])
    return G


def modify_by_id(elements, id, key, value):
    elems = [elem for elem in elements if elem['data']['id'] == id]
    if len(elems) != 1:
        raise RuntimeError(f'Detected {len(elems)} elements for {id=}. Expected 1.')
    elem = elems[0]
    elem['data'][key] = value
    return [elem for elem in elements if elem['data']['id'] != id] + [elem]