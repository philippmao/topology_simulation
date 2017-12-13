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
import random

from define import(
    JOINING_ASES,
    OPEN_PORTS,
    CHOSEN_NEIGHBORS,
    MAX_TOTAL,
    USE_PF
)




class ASInformation(object):
    """
    Class to represent all information of an AS
    """
    def __init__(self, ISD, AS):
        random.seed()
        self.AS = AS
        self.ISD = ISD
        self.neighbors = []
        self.PF = 5
        if OPEN_PORTS:
            self.max_neighbors = random.randint(1,JOINING_ASES)
            if MAX_TOTAL < self.max_neighbors:
                self.max_neighbors = MAX_TOTAL
        else:
            self.max_neighbors = MAX_TOTAL
        if AS == 1 and ISD == 1:
            self.max_neighbors = MAX_TOTAL

    def getdict(self):
        dict = {}
        dict['ia'] = "%s-%s" % (self.AS, self.ISD)
        dict['neighbors'] = self.neighbors
        dict['max_neighbors'] = self.max_neighbors
        return dict

    def getdegree(self):
        print(len(self.neighbors), self.ISD, self.AS)
        return len(self.neighbors)

    def get_name(self):
        return "%s-%s" % (self.ISD, self.AS)

def choose_neighbors(topo):
    """
    from a list of potential neighbors choose the
    :param topo:
    :return: list of chosen neighbors
    """
    chosen_neighbors = []
    # add performance score to each potential neighbors
    for pot_neighbor in topo:
        if USE_PF:
            random.seed()
            pot_neighbor.PF = random.randint(1,4)
    i = 0
    pot_list = []
    for nb in topo:
        pot_list.append(nb.get_name())
    while i < CHOSEN_NEIGHBORS:
        if not pot_list:
            return chosen_neighbors
        best_neighbor = choose_best_neighbors(topo, pot_list)
        pot_list = remove_neighbor(pot_list, best_neighbor)
        chosen_neighbors.append(best_neighbor)
        i += 1
    print("chosen neighbors:", chosen_neighbors)
    return chosen_neighbors


def choose_best_neighbors(topo, pot_list):
    """
    chooses the best neighbor from a list of potential neigbhors
    :param topo:
    :return:
    """
    print("choosing neighbors from list:", pot_list)
    pot_topo = []
    for ia in pot_list:
        ISD, AS = string_to_int(ia)
        node = find_AS_in_list(ISD, AS, topo)
        pot_topo.append(node)
    best_neighbor = pot_topo[0]
    for pot_neighbor in pot_topo:
        if best_neighbor.getdegree() >= best_neighbor.max_neighbors:
            best_neighbor = pot_neighbor
        if pot_neighbor.getdegree() >= best_neighbor.max_neighbors:
            continue
        if best_neighbor.PF > pot_neighbor.PF:
            free_ports = pot_neighbor.max_neighbors - pot_neighbor.getdegree()
            if free_ports > 0:
                best_neighbor = pot_neighbor
        if best_neighbor.PF == pot_neighbor.PF:
            if best_neighbor.getdegree() > pot_neighbor.getdegree():
                free_ports = pot_neighbor.max_neighbors - pot_neighbor.getdegree()
                if free_ports > 0:
                    best_neighbor = pot_neighbor
    print("neighbor chosen: ", best_neighbor)
    return best_neighbor


def remove_neighbor(pot_list, neighbor):
    """
    removes a neighbor from a list of neighbors
    :param topo: list
    :param neighbor: neighbor to remove
    :return: updated list
    """
    i = 0
    for nb in pot_list:
        if nb == neighbor.get_name():
            pot_list.pop(i)
        i += 1
    return pot_list


def update_topo(topo, join_as, neighbors):
    """
    Updates the topology with the new as
    :param topo: topology list
    :param join_as: joining box
    :param neighbors: chosen neighbors for the box
    :return:
    """
    for nb in neighbors:
        # update join_as neighbors
        join_as.neighbors.append(nb.get_name())
        for entry in topo:
            if entry.ISD == nb.ISD:
                if entry.AS == nb.AS:
                    nb.neighbors.append(join_as.get_name())
    topo.append(join_as)
    print("updated topology:", topo)
    return topo


def find_AS_in_list(ISD, AS, topo):
    for entry in topo:
        if entry.ISD == ISD:
            if entry.AS == AS:
                return entry
    return {}

def string_to_int(IA):
    list = IA.split("-")
    return int(list[0]), int(list[1])
