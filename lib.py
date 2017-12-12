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
    MAX_NEIGHBORS,
    CHOSEN_NEIGHBORS,
    MAX_TOTAL,
    USE_PF
)


random.seed()


class ASInformation(object):
    """
    Class to represent all information of an AS
    """
    def __init__(self, ISD, AS):
        self.AS = AS
        self.ISD = ISD
        self.neighbors = []
        self.PF = 5
        if MAX_NEIGHBORS:
            self.max_neighbors = random.randint(1,JOINING_ASES)
        else:
            self.max_neighbors = JOINING_ASES

    def getdict(self):
        dict = {}
        dict['ia'] = "%s-%s" % (self.AS, self.ISD)
        dict['neighbors'] = self.neighbors
        dict['max_neighbors'] = self.max_neighbors
        return dict

    def getdegree(self):
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
            pot_neighbor.PF = random.randint(1,4)

    i = 0
    while i < CHOSEN_NEIGHBORS:
        if not topo:
            return chosen_neighbors
        best_neighbor = choose_best_neighbors(topo)
        topo = remove_neighbor(topo, best_neighbor)
        chosen_neighbors.append(best_neighbor)
        i += 1
    print("chosen neighbors:", chosen_neighbors)
    return chosen_neighbors


def choose_best_neighbors(topo):
    """
    chooses the best neighbor from a list of potential neigbhors
    :param topo:
    :return:
    """
    print("choosing neighbors from list:", topo)
    best_neighbor = topo[0]
    for pot_neighbor in topo:
        if best_neighbor.PF > pot_neighbor.PF:
            free_ports = pot_neighbor.max_neighbors - pot_neighbor.getdegree()
            if free_ports > 0:
                if MAX_NEIGHBORS:
                    if pot_neighbor.getdegree() <= MAX_TOTAL:
                        best_neighbor = pot_neighbor
        if best_neighbor.PF == pot_neighbor.PF:
            if best_neighbor.getdegree() > pot_neighbor.getdegree():
                free_ports = pot_neighbor.max_neighbors - pot_neighbor.getdegree()
                if free_ports > 0:
                    if MAX_NEIGHBORS:
                        if pot_neighbor.getdegree() <= MAX_TOTAL:
                            best_neighbor = pot_neighbor
    print("neighbor chosen: ", best_neighbor)
    return best_neighbor


def remove_neighbor(topo, neighbor):
    """
    removes a neighbor from a list of neighbors
    :param topo: list
    :param neighbor: neighbor to remove
    :return: updated list
    """
    i = 0
    for nb in topo:
        if nb.ISD == neighbor.ISD:
            if nb.AS == neighbor.AS:
                topo.pop(i)
        i += 1
    return topo


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
        join_as.neighbors.append("%s-%s" % (nb.ISD, nb.AS))
        for entry in topo:
            if entry.ISD == nb.ISD:
                if entry.AS == nb.AS:
                    nb.neighbors.append("%s-%s" % (join_as.ISD, join_as.AS))
    print("updated topology:", topo)
    return topo


def find_AS_in_list(ISD, AS, topo):
    for entry in topo:
        if entry.ISD == ISD:
            if entry.AS == AS:
                return entry
    return {}
