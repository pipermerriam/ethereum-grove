values_a = (
    ('a', 1),
    ('b', 2),
    ('c', 3),
)

# value, parent, left, right, height
tree_a = {
    ('a', 1, 'b', None, None, 1),
    ('b', 2, None, 'a', 'b', 2),
    ('c', 3, 'b', None, None, 1),
}


def test_tree_autobalancing(deployed_contracts):
    grove = deployed_contracts.Grove

    def get_id(node_id):
        if node_id is None:
            return None
        return grove.getNodeId.call(node_id)

    for id, node_value in values_a:
        grove.insert('test', id, node_value)

    actual = set()

    for id, _ in values_a:
        node_id = grove.getNodeId.call('test', id)
        value = grove.getNodeValue.call(node_id)
        _parent = grove.getNodeParent.call(node_id)
        parent = get_id(_parent)
        _left = grove.getNodeLeftChild.call(node_id)
        left = get_id(_left)
        _right = grove.getNodeRightChild.call(node_id)
        right = get_id(_right)
        height = grove.getNodeHeight.call(node_id)

        actual.add((id, value, parent, left, right, height))

    from pprint import pprint

    assert actual == tree_a
