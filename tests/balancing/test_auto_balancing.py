def test_single_node_tree(deploy_coinbase, deployed_contracts):
    grove = deployed_contracts.Grove

    index_id = grove.computeIndexId(deploy_coinbase, "test-a")

    grove.insert('test-a', 'a', 20)
    node_id = grove.computeNodeId(index_id, 'a')

    assert grove.getNodeParent(node_id) is None
    assert grove.getNodeLeftChild(node_id) is None
    assert grove.getNodeRightChild(node_id) is None
    assert grove.getNodeHeight(node_id) == 1
    assert grove.getNodeValue(node_id) == 20


def test_two_node_tree(deploy_coinbase, deployed_contracts):
    grove = deployed_contracts.Grove

    index_id = grove.computeIndexId(deploy_coinbase, "test-b")

    grove.insert('test-b', 'a', 20)
    node_a_id = grove.computeNodeId(index_id, 'a')

    grove.insert('test-b', 'b', 25)
    node_b_id = grove.computeNodeId(index_id, 'b')

    root = grove.getIndexRoot.call(index_id)
    assert root == 'a'

    assert grove.getNodeParent(node_a_id) is None
    assert grove.getNodeLeftChild(node_a_id) is None
    assert grove.getNodeRightChild(node_a_id) == 'b'
    assert grove.getNodeHeight(node_a_id) == 2
    assert grove.getNodeValue(node_a_id) == 20

    assert grove.getNodeParent(node_b_id) == 'a'
    assert grove.getNodeLeftChild(node_b_id) is None
    assert grove.getNodeRightChild(node_b_id) is None
    assert grove.getNodeHeight(node_b_id) == 1
    assert grove.getNodeValue(node_b_id) == 25


values_a = (
    ('a', 1),
    ('b', 2),
    ('c', 3),
)

# value, parent, left, right, height
tree_a = {
    ('a', 1, 'b', None, None, 1),
    ('b', 2, None, 'a', 'c', 2),
    ('c', 3, 'b', None, None, 1),
}


def test_right_heavy_three_node_tree(deploy_coinbase, deployed_contracts):
    grove = deployed_contracts.Grove

    for id, node_value in values_a:
        grove.insert('test-c', id, node_value)

    index_id = grove.computeIndexId(deploy_coinbase, "test-c")

    root = grove.getIndexRoot.call(index_id)
    assert root == 'b'

    actual = set()

    for id, _ in values_a:
        node_id = grove.computeNodeId.call(index_id, id)
        value = grove.getNodeValue.call(node_id)
        parent = grove.getNodeParent.call(node_id)
        left = grove.getNodeLeftChild.call(node_id)
        right = grove.getNodeRightChild.call(node_id)
        height = grove.getNodeHeight.call(node_id)

        actual.add((id, value, parent, left, right, height))

    assert actual == tree_a


values_b = (
    ('a', 3),
    ('b', 2),
    ('c', 1),
)

# value, parent, left, right, height
tree_b = {
    ('a', 3, 'b', None, None, 1),
    ('b', 2, None, 'c', 'a', 2),
    ('c', 1, 'b', None, None, 1),
}


def test_left_heavy_three_node_tree(deploy_coinbase, deployed_contracts):
    grove = deployed_contracts.Grove

    for id, node_value in values_b:
        grove.insert('test-d', id, node_value)

    index_id = grove.computeIndexId(deploy_coinbase, "test-d")

    root = grove.getIndexRoot.call(index_id)
    assert root == 'b'

    actual = set()

    for id, _ in values_b:
        node_id = grove.computeNodeId.call(index_id, id)
        value = grove.getNodeValue.call(node_id)
        parent = grove.getNodeParent.call(node_id)
        left = grove.getNodeLeftChild.call(node_id)
        right = grove.getNodeRightChild.call(node_id)
        height = grove.getNodeHeight.call(node_id)

        actual.add((id, value, parent, left, right, height))

    from pprint import pprint

    assert actual == tree_b


values_c = (
    ('a', 25),
    ('b', 30),
    ('c', 35),
    ('d', 33),
    ('e', 40),
    ('f', 38),
)

# value, parent, left, right, height
tree_c = {
    ('a', 25, 'b', None, None, 1),
    ('b', 30, 'c', 'a', 'd', 2),
    ('c', 35, None, 'b', 'e', 3),
    ('d', 33, 'b', None, None, 1),
    ('e', 40, 'c', 'f', None, 2),
    ('f', 38, 'e', None, None, 1),
}


def test_right_heavy_six_node_tree(deploy_coinbase, deployed_contracts):
    grove = deployed_contracts.Grove

    for id, node_value in values_c:
        grove.insert('test-e', id, node_value)

    index_id = grove.computeIndexId(deploy_coinbase, "test-e")

    root = grove.getIndexRoot.call(index_id)
    assert root == 'c'

    actual = set()

    for id, _ in values_c:
        node_id = grove.computeNodeId.call(index_id, id)
        value = grove.getNodeValue.call(node_id)
        parent = grove.getNodeParent.call(node_id)
        left = grove.getNodeLeftChild.call(node_id)
        right = grove.getNodeRightChild.call(node_id)
        height = grove.getNodeHeight.call(node_id)

        actual.add((id, value, parent, left, right, height))

    from pprint import pprint

    assert actual == tree_c
