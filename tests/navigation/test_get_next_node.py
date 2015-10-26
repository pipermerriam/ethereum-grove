import pytest


tree_nodes = (
    ('a', 18),
    ('b', 0),
    ('c', 7),
    ('d', 11),
    ('e', 16),
    ('f', 3),
    ('g', 16),
    ('h', 17),
    ('i', 17),
    ('j', 18),
    ('k', 12),
    ('l', 3),
    ('m', 4),
    ('n', 6),
    ('o', 11),
    ('p', 5),
    ('q', 12),
    ('r', 1),
    ('s', 1),
    ('t', 16),
    ('u', 14),
    ('v', 3),
    ('w', 7),
    ('x', 13),
    ('y', 6),
    ('z', 17),
)

@pytest.fixture(scope="module")
def big_tree(deployed_contracts):
    grove = deployed_contracts.Grove

    for _id, value in tree_nodes:
        grove.insert('test', _id, value)
    return grove


@pytest.mark.parametrize(
    '_id,next_id',
    (
        ('b', 'r'),
        ('r', 's'),
        ('s', 'f'),
        ('f', 'l'),
        ('l', 'v'),
        ('v', 'm'),
        ('m', 'p'),
        ('p', 'n'),
        ('n', 'y'),
        ('y', 'c'),
        ('c', 'w'),
        ('w', 'd'),
        ('d', 'o'),
        ('o', 'k'),
        ('k', 'q'),
        ('q', 'x'),
        ('x', 'u'),
        ('u', 'e'),
        ('e', 'g'),
        ('g', 't'),
        ('t', 'h'),
        ('h', 'i'),
        ('i', 'z'),
        ('z', 'a'),
        ('a', 'j'),
        ('j', None),
    )
)
def test_getting_next_node(deploy_coinbase, big_tree, _id, next_id):
    def get_val(node_id):
        if node_id is None:
            return None
        return big_tree.getNodeValue(node_id)

    index_id = big_tree.computeIndexId(deploy_coinbase, "test")

    node_id = big_tree.computeNodeId(index_id, _id)
    actual_next_id = big_tree.getNextNode(node_id)
    assert actual_next_id == next_id


@pytest.mark.parametrize(
    '_id,previous_id',
    (
        ('b', None),
        ('r', 'b'),
        ('s', 'r'),
        ('f', 's'),
        ('l', 'f'),
        ('v', 'l'),
        ('m', 'v'),
        ('p', 'm'),
        ('n', 'p'),
        ('y', 'n'),
        ('c', 'y'),
        ('w', 'c'),
        ('d', 'w'),
        ('o', 'd'),
        ('k', 'o'),
        ('q', 'k'),
        ('x', 'q'),
        ('u', 'x'),
        ('e', 'u'),
        ('g', 'e'),
        ('t', 'g'),
        ('h', 't'),
        ('i', 'h'),
        ('z', 'i'),
        ('a', 'z'),
        ('j', 'a'),
    )
)
def test_getting_previous_node(deploy_coinbase, big_tree, _id, previous_id):
    def get_val(node_id):
        if node_id is None:
            return None
        return big_tree.getNodeValue(node_id)

    index_id = big_tree.computeIndexId(deploy_coinbase, "test")

    node_id = big_tree.computeNodeId(index_id, _id)
    actual_previous_id = big_tree.getPreviousNode(node_id)
    assert actual_previous_id == previous_id
