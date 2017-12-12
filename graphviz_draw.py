# Copyright 2017 ETH Zurich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Stdlib
from define import(
    JOINING_ASES
)
from graphviz import Graph

from lib import find_AS_in_list

def draw_topology(topo):
    """
    Draws the topology
    :param topo:
    :return: dot graph object
    """
    dot = Graph(name='topology', filename='topology.gv')
    # add nodes to the graph
    for node in topo:
        node_name = node.get_name()
        dot.node(node_name, node_name, _attributes={'shape': 'box'})
    current = ["1-1"]
    drawn = []

    next_neighbors, drawn = draw_edges_from_current(current, drawn, dot)

    while len(drawn) < JOINING_ASES:
        next_neighbors, drawn = draw_edges_from_current(next_neighbors, drawn, dot)

    return topo

def draw_edges_from_current(current, drawn, graph):
    next_neighbors = []
    # draw edges from
    for cur in current:
        drawn.append(cur)
        ISD, AS = string_to_int(nb)
        nb_entry = find_AS_in_list(ISD, AS)
        for nb in cur.neighbors:
            if nb not in drawn:
                ISD, AS = string_to_int(nb)
                nb_entry = find_AS_in_list(ISD, AS)
                graph.edge(cur.get_name(), nb.get_name())
                if nb not in next_neighbors:
                    if nb not in current:
                        next_neighbors.append(nb)
    return next_neighbors, drawn

def string_to_int(IA):
    list = IA.split("-")
    return int(list[0]), int(list[1])
