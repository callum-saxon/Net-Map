import requests
from bs4 import BeautifulSoup
import networkx as nx
from pyvis.network import Network

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links

def create_network_map(start_urls, depth=2):
    G = nx.Graph()

    for start_url in start_urls:
        queue = [(start_url, 0)]

        while queue:
            current_url, current_depth = queue.pop(0)

            if current_depth <= depth:
                links = get_links(current_url)

                for link in links:
                    G.add_edge(current_url, link)
                    if link not in G.nodes:
                        queue.append((link, current_depth + 1))

    return G

def visualize_network_pyvis(G):
    net = Network(height="750px", width="100%", notebook=True)
    net.from_nx(G)
    net.show("network_visualization.html")

start_urls = ['https://www.youtube.com/',]
depth = 2
graph = create_network_map(start_urls, depth)
visualize_network_pyvis(graph)
