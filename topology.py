import argparse
from graphviz import Graph
from graphviz import Source

from lib import(
    ASInformation,
    choose_neighbors,
    update_topo
)

from graphviz_draw import draw_topology

from define import(
    JOINING_ASES
)

def simulate_topology():
    """
    Simulate the topology algorithm
    :return: topo of simulated topology
    """
    topo = []
    core_as = ASInformation(1, 1)
    topo.append(core_as)
    for i in range(2,JOINING_ASES+2):
        join_as = ASInformation(1,i)
        # choose set of neighbors for new AS
        neighbors = choose_neighbors(topo)
        # update topology list with new neighbors
        topo = update_topo(topo, join_as, neighbors)
    return topo




def main():
    """
    Draws the topology of an example topology run
    """
    topo = simulate_topology()
    dot = draw_topology(topo)
    s = Source(dot, filename=dot.filename, format="pdf")
    s.render(directory="output.gv")

if __name__ == '__main__':
    main()
