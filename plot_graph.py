# References
# https://stackoverflow.com/questions/28910766/python-networkx-set-node-color-automatically-based-on-number-of-attribute-opt
# https://stackoverflow.com/questions/46784028/edge-length-in-networkx

import re
import matplotlib.patches as mpatches
import json
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns


def clean(name):

    name = name.strip().upper()
    name = name.replace("\n", " ").replace('"', "'")
    name = re.sub("\s+", " ", name)

    return name


def get_nodes_edges_cmap(data):

    all_nodes = set()
    all_edges = set()
    
    REGISTERED_AGENT = "Registered Agent"
    OWNER = "Owner Name"
    COMMERCIAL_REGISTERED_AGENT = 'Commercial Registered Agent'

    colorId_to_Entity = {
        0: "Registered Agent",
        1: "Owner",
        2: "Commercial Registered Agent",
        3: "Business"
    }
    
    for id, info in data.items(): 

        ra_agent = owner = comm_reg_agent = None

        business_name = clean(info["TITLE"])

        if REGISTERED_AGENT in info:
            ra_agent = clean(info[REGISTERED_AGENT])
        
        if OWNER in info:
            owner = clean(info[OWNER])

        if COMMERCIAL_REGISTERED_AGENT in info:
            comm_reg_agent = clean(info[COMMERCIAL_REGISTERED_AGENT])


        all_nodes.add((business_name, 3))

        for cmap_id, entity in enumerate([ra_agent, owner, comm_reg_agent]):

            if entity:

                all_nodes.add((entity, cmap_id))
                all_edges.add(((entity, cmap_id), (business_name, 3)))
    

    return all_nodes, all_edges, colorId_to_Entity


def draw_graph(G, colorId_to_Entity):

    color_palette = sns.color_palette("tab10")
    colors = [color_palette[node[1]] for node in list(G.nodes())]


    plt.figure(figsize=(15, 15))
    pos = nx.spring_layout(G)
    legend = [mpatches.Patch(color=color_palette[i], label=colorId_to_Entity[i]) for i in range(4)]

    nx.draw_networkx(G, pos=pos, node_size=30, node_color=colors, with_labels=False)
    plt.legend(handles=legend, loc='upper right')
    plt.title("Businesses starting with letter 'X' and are Active")
    plt.savefig("businesses_graph.png", bbox_inches='tight')


def plot_businesses():

    with open("businesses_data.json", "r") as srcf:
        data = json.load(srcf)

    nodes, edges, colorId_to_Entity = get_nodes_edges_cmap(data)
    
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges, weight=0.8)

    draw_graph(G, colorId_to_Entity)



if __name__ == '__main__':

    with open("businesses_data.json", "r") as srcf:
        data = json.load(srcf)

    nodes, edges, colorId_to_Entity = get_nodes_edges_cmap(data)
    
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges, weight=0.8)

    draw_graph(G, colorId_to_Entity)