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
        grove.insert('test-querying', _id, value)
    return grove


@pytest.mark.parametrize(
    'operator,value,expected',
    (
        # parent, left, right, height
        ("==", 7, (7, None, 4, 16, 6)),
        ("==", 6, (6, 4, 5, 6, 2)),
        ("==", 11, (11, 11, 7, None, 2)),
        ("==", 17, (17, 16, 16, 18, 4)),
        ("==", 15, None),
        ("==", 2, None),
        ("==", 8, None),
        # LT
        ("<", 4, (3, 3, None, None, 1)),
        ("<", 5, (4, 7, 3, 6, 4)),
        ("<", 8, (7, 11, None, None, 1)),
        ("<", 14, (13, 14, None, None, 1)),
        ("<", 16, (14, 12, 13, None, 2)),
        ("<", 17, (16, 16, None, None, 1)),
        ("<", 18, (17, 17, None, None, 1)),
        ("<", -1, None),
        ("<", 0, None),
        # GT
        (">", 6, (7, None, 4, 16, 6)),
        (">", 3, (4, 7, 3, 6, 4)),
        (">", 16, (17, 16, 16, 18, 4)),
        (">", 18, None),
        (">", 19, None),
        # LTE
        ("<=", 4, (4, 7, 3, 6, 4)),
        ("<=", 5, (5, 6, None, None, 1)),
        ("<=", 8, (7, 11, None, None, 1)),
        ("<=", 7, (7, 11, None, None, 1)),
        ("<=", 6, (6, 6, None, None, 1)),
        ("<=", 16, (16, 16, None, None, 1)),
        ("<=", 15, (14, 12, 13, None, 2)),
        ("<=", 0, (0, 1, None, None, 1)),
        ("<=", 18, (18, 18, None, None, 1)),
        ("<=", 19, (18, 18, None, None, 1)),
        ("<=", -1, None),
        # GTE
        (">=", 0, (0, 1, None, None, 1)),
        (">=", 3, (3, 4, 1, 3, 3)),
        (">=", 13, (13, 14, None, None, 1)),
        (">=", 14, (14, 12, 13, None, 2)),
        (">=", 15, (16, 7, 11, 17, 5)),
        (">=", 17, (17, 16, 16, 18, 4)),
        (">=", 18, (18, 17, 17, 18, 3)),
        (">=", 19, None),
    )
)
def test_tree_querying(deploy_coinbase, big_tree, operator, value, expected):
    index_id = big_tree.computeIndexId(deploy_coinbase, "test-querying")

    def get_val(node_id):
        if node_id is None:
            return None
        return big_tree.getNodeValue(big_tree.computeNodeId(index_id, node_id))

    _id = big_tree.query(index_id, operator, value)

    if _id is None:
        assert expected is None
    else:
        node_id = big_tree.computeNodeId(index_id, _id)

        val = big_tree.getNodeValue(node_id)
        parent = get_val(big_tree.getNodeParent(node_id))
        left = get_val(big_tree.getNodeLeftChild(node_id))
        right = get_val(big_tree.getNodeRightChild(node_id))
        height = big_tree.getNodeHeight(node_id)

        actual = (val, parent, left, right, height)
        assert actual == expected
