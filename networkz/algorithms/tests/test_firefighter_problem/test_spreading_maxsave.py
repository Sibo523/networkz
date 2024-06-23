"""

The Paper - 
Approximability of the Firefighter Problem Computing Cuts over Time

Paper Link -
https://www.math.uwaterloo.ca/~cswamy/papers/firefighter-journ.pdf

Authors - 
Elliot Anshelevich
Deeparnab Chakrabarty
Ameya Hate 
Chaitanya Swamy

Developers - 
Yuval Bubnovsky
Almog David
Shaked Levi

"""

import pytest
import networkx as nx
import json
import random

from networkz.algorithms.approximation.firefighter_problem.Firefighter_Problem import spreading_maxsave
from networkz.algorithms.approximation.firefighter_problem.Utils import parse_json_to_networkx, calculate_gamma, calculate_epsilon, find_best_direct_vaccination

with open("networkz/algorithms/tests/test_firefighter_problem/graphs.json", "r") as file:
        json_data = json.load(file)
graphs = parse_json_to_networkx(json_data)

@pytest.mark.parametrize("graph_key, budget, source, targets", [
    ("RegularGraph_Graph-1", 1, -2, [1, 2, 3, 4, 5, 6]),
    ("RegularGraph_Graph-4", 1, 8, [1, 2, 4, 6, 7]),
    ("RegularGraph_Graph-6", 1, 10, [0, 2, 3, 5, 6, 7, 8, 9]),
    ("RegularGraph_Graph-8", 1, 17, [1, 7, 12, 14, 8, 3, 11, 2]),
    ("RegularGraph_Graph-3", 1, 6, [1, 3, 5]),
])
def test_source_not_in_graph(graph_key, budget, source, targets):
    with pytest.raises(ValueError):
        spreading_maxsave(graphs[graph_key], budget, source, targets)

@pytest.mark.parametrize("graph_key, budget, source, targets", [
    ("RegularGraph_Graph-2", 1, 0, [1, 2, 3, 9, 5, 16]),
    ("RegularGraph_Graph-3", 1, 4, [1, 2, 3, 6, 7]),
    ("RegularGraph_Graph-6", 1, 3, [0, 2, 5, 6, 7, 8, 10]),
    ("RegularGraph_Graph-8", 1, 11, [1, 3, 12, 19, 8, 10, 4, 2]),
    ("RegularGraph_Graph-7", 1, 2, [1, 3, -1, 5]),
])
def test_target_not_in_graph(graph_key, budget, source, targets):
    with pytest.raises(ValueError):
        spreading_maxsave(graphs[graph_key], budget, source, targets)

@pytest.mark.parametrize("graph_key, budget, source, targets", [
    ("RegularGraph_Graph-1", 1, 0, [1, 2, 3, 0, 4, 5, 6]),
    ("RegularGraph_Graph-3", 1, 1, [5, 1, 4]),
    ("RegularGraph_Graph-4", 1, 4, [1, 2, 3, 4, 5, 6, 7]),
    ("RegularGraph_Graph-6", 1, 0, [0, 3, 5, 6, 7, 8, 9]),
    ("RegularGraph_Graph-8", 1, 0, [13, 10, 8, 6, 5, 4, 3, 0, 1, 2]),
])
def test_source_is_target(graph_key, budget, source, targets):
    with pytest.raises(ValueError):
        spreading_maxsave(graphs[graph_key], budget, source, targets)

@pytest.mark.parametrize("graph_key, source, targets, expected_gamma, expected_direct_vaccination", [
    ("Dirlay_Graph-5", 0, [1, 2, 3, 4, 5 ,6 ,7 ,8], {
        1: [(2, 1), (4, 1), (1, 1), (1, 2)],
        2: [(2, 1)],
        3: [(2, 1), (5, 1), (3, 1), (3, 2)],
        4: [(4, 1)],
        5: [(5, 1)],
        6: [(4, 1), (5, 1), (6, 1), (6, 2)],
        7: [(5, 1), (6, 1), (7, 1), (7, 2)],
        8: [(4, 1), (5, 1), (6, 1), (6, 2), (7, 1), (7, 2), (8, 1), (8, 2), (8, 3)],
    }, {
        (1, 1): [1],
        (1, 2): [1],
        (2, 1): [1, 2, 3],
        (3, 1): [3],
        (3, 2): [3],
        (4, 1): [1, 4, 6, 8],
        (5, 1): [3, 5, 6, 7, 8],
        (6, 1): [6, 7, 8],
        (6, 2): [6, 8],
        (7, 1): [7, 8],
        (7, 2): [7, 8],
        (8, 1): [8],
        (8, 2): [8],
        (8, 3): [8]
    }),
    ("RegularGraph_Graph-1", 0, [1, 3, 4, 5], {
        1: [(1, 1)],
        2: [(2, 1)],
        3: [(1, 1), (2, 1), (3, 1), (3, 2)],
        4: [(1, 1), (4, 1), (4, 2)],
        5: [(1, 1), (2, 1), (3, 1), (3, 2), (5, 1), (5, 2), (5, 3)],
        6: [(2, 1), (6, 1), (6, 2)],
    }, {
        (1, 1): [1, 3, 4, 5],
        (2, 1): [3, 5],
        (3, 1): [3, 5],
        (3, 2): [3, 5],
        (4, 1): [4],
        (4, 2): [4],
        (5, 1): [5],
        (5, 2): [5],
        (5, 3): [5],
        (6, 1): [],
        (6, 2): [],
    })
])
def test_calculate_gamma(graph_key, source, targets, expected_gamma, expected_direct_vaccination):
    print(calculate_gamma(graphs[graph_key], source, targets))
    calculated_gamma, calculated_direct_vaccination = calculate_gamma(graphs[graph_key], source, targets)
    
    for key in expected_gamma:
        assert key in calculated_gamma, f"Expected key {key} to be in {calculated_gamma}"
    assert calculated_direct_vaccination == expected_direct_vaccination

@pytest.mark.parametrize("direct_vaccinations, expected_epsilon", [
    ({
        (1, 1): [1, 3, 4, 5],
        (2, 1): [2, 3, 5, 6],
        (3, 1): [3, 5],
        (3, 2): [3, 5],
        (4, 1): [4],
        (4, 2): [4],
        (5, 1): [5],
        (5, 2): [5],
        (5, 3): [5],
        (6, 1): [6],
        (6, 2): [6],
    }, [
        [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],
        [(3, 2), (4, 2), (5, 2), (6, 2)],
        [(5, 3)]
    ]),
    ({
        (1, 1): [1],
        (1, 2): [1],
        (2, 1): [1, 2, 3],
        (3, 1): [3],
        (3, 2): [3],
        (4, 1): [1, 4, 6, 8],
        (5, 1): [3, 5, 6, 7, 8],
        (6, 1): [4, 6, 8],
        (6, 2): [6, 8],
        (7, 1): [7, 8],
        (7, 2): [7, 8],
        (8, 1): [8],
        (8, 2): [8],
        (8, 3): [8],
    }, [
        [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1)],
        [(1, 2), (3, 2), (6, 2), (7, 2), (8, 2)],
        [(8, 3)]
    ]),
])
def test_calculate_epsilon(direct_vaccinations, expected_epsilon):
    calculated_epsilon = calculate_epsilon(direct_vaccinations)
    
    assert calculated_epsilon == expected_epsilon

@pytest.mark.parametrize("graph_key, direct_vaccinations, current_epsilon, targets, expected_best_direct_vaccination", [
    ("RegularGraph_Graph-1",
     {
     (1, 1): [1, 2, 3, 4, 5, 7],
        (2, 1): [2, 3, 4, 7],
        (2, 2): [2, 3, 7],
        (3, 1): [3, 4, 7],
        (3, 2): [3, 4, 7],
        (3, 3): [3, 7],
        (4, 1): [4, 7],
        (4, 2): [4, 7],
        (4, 3): [4, 7],
        (5, 1): [2, 3, 4, 5, 7],
        (5, 2): [3, 4, 5, 7],
        (6, 1): [3, 4, 5, 6, 7],
    }, 
    [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],
    [1, 3, 4, 5, 6], 
    (1, 1)),
    ("Dirlay_Graph-5", 
     {
        (1, 1): [1],
        (1, 2): [1],
        (2, 1): [1, 2, 3],
        (3, 1): [3],
        (3, 2): [3],
        (4, 1): [1, 4, 6, 8],
        (5, 1): [3, 5, 6, 7, 8],
        (6, 1): [4, 6, 8],
        (6, 2): [6, 8],
        (7, 1): [7, 8],
        (7, 2): [7, 8],
        (8, 1): [8],
        (8, 2): [8],
        (8, 3): [8],
    }, 
    [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1)],
    [1, 2, 3, 4, 5, 6, 7, 8],
    (5, 1))
])
  
def test_find_best_direct_vaccination(graph_key, direct_vaccinations, current_epsilon, targets, expected_best_direct_vaccination):
    calculated_best_direct_vaccination = find_best_direct_vaccination(graphs[graph_key],direct_vaccinations,current_epsilon,targets)[0]
    
    assert calculated_best_direct_vaccination == expected_best_direct_vaccination

@pytest.mark.parametrize("graph_key, budget, source, targets, expected_length", [
    ("RegularGraph_Graph-1", 1, 0, [1, 2, 3, 4, 5, 6], 2),
    ("Dirlay_Graph-5", 2, 0, [1, 2, 3, 4, 5, 6, 7, 8], 3),
])
def test_strategy_length(graph_key, budget, source, targets, expected_length):
    graph = graphs[graph_key]
    calculated_strategy = spreading_maxsave(graph, budget, source, targets)[0]
    
    assert len(calculated_strategy) == expected_length


@pytest.mark.parametrize("graph_key, budget, source, targets, expected_strategy", [
    ("RegularGraph_Graph-1", 1, 0, [1, 2, 3, 4, 5, 6], [(1, 1), (6, 2)]),
    ("Dirlay_Graph-5", 2, 0, [1, 2, 3, 4, 5, 6, 7, 8], [(5, 1), (2, 1), (8, 2)]),
])
def test_save_all_vertices(graph_key, budget, source, targets, expected_strategy):
    graph = graphs[graph_key]
    calculated_strategy = spreading_maxsave(graph, budget, source, targets)[0]
    
    assert calculated_strategy == expected_strategy

@pytest.mark.parametrize("graph_key, budget, source, targets, expected_strategy", [
    ("RegularGraph_Graph-6", 2, 1, [3, 9, 0, 5, 6], [(2, 1), (0, 1)]),
    ("RegularGraph_Graph-4", 1, 0, [2, 6, 4], [(1, 1), (3, 2)]),
])
def test_save_subgroup_vertices(graph_key, budget, source, targets, expected_strategy):
    graph = graphs[graph_key]
    calculated_strategy = spreading_maxsave(graph, budget, source, targets)[0]
    
    assert calculated_strategy == expected_strategy

@pytest.mark.parametrize("graph_key, budget, source, targets, expected_nodes_saved_list", [
    ("RegularGraph_Graph-1", 1, 0, [1, 2, 3, 4, 5, 6], {1, 3, 4, 5, 6}),
    ("Dirlay_Graph-5", 2, 0, [1, 2, 3, 4, 5, 6, 7, 8], {1, 2, 3, 5, 6, 7, 8}),
])
def test_save_all_vertices_nodes_list(graph_key, budget, source, targets, expected_nodes_saved_list):
    graph = graphs[graph_key]
    calculated_nodes_saved_list = spreading_maxsave(graph, budget, source, targets)[1]
    print(calculated_nodes_saved_list)
    
    assert calculated_nodes_saved_list == expected_nodes_saved_list

@pytest.mark.parametrize("graph_key, budget, source, targets, expected_nodes_saved_list", [
    ("RegularGraph_Graph-6", 2, 1, [3, 9, 0, 5, 6], {0, 3, 5, 6, 9}),
    ("RegularGraph_Graph-4", 1, 0, [2, 6, 4], {2, 4}),
])
def test_save_subgroup_vertices_nodes_list(graph_key, budget, source, targets, expected_nodes_saved_list):
    graph = graphs[graph_key]
    calculated_nodes_saved_list = spreading_maxsave(graph, budget, source, targets)[1]
    
    assert calculated_nodes_saved_list == expected_nodes_saved_list

def test_random_graph():
    for i in range(10):
        num_nodes = random.randint(2,100)
        nodes = list(range(num_nodes+1))
        num_edges = 1000
        save_amount = random.randint(1,num_nodes)
        targets = []
        G = nx.DiGraph()
        
        G.add_nodes_from(nodes, status="target")
        for _ in range(num_edges):
            source = random.randint(0, num_nodes - 1)
            target = random.randint(0, num_nodes - 1)
            if source != target:  # Ensure no self-loops
                G.add_edge(source, target)
        for node in range(save_amount):
            probability = random.random()
            if probability < 0.75 and node!=0:
                targets.append(node)
        
        ans = spreading_maxsave(G,1,0,targets)[0]
        print(len(ans))
        print(len(G.nodes))
       
        assert len(ans) <= len(G.nodes)
    
    print("All tests have passed!")