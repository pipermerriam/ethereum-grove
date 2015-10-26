import pytest

import random


tree_nodes = (
    ('a', 8),
    ('b', 6),
    ('c', 7),
    ('d', 10),
    ('e', 2),
    ('f', 12),
    ('g', 3),
    ('h', 15),
    ('i', 13),
    ('j', 5),
    ('k', 19),
    ('l', 11),
    ('m', 17),
    ('n', 0),
    ('o', 4),
    ('p', 14),
    ('q', 18),
    ('r', 9),
    ('s', 16),
    ('t', 1),
)


@pytest.mark.parametrize(
    'ids_to_remove,expected_states',
    (
        # id, value, parent, left, right, height
        # Leaf Nodes
        (
            ['n'], {
                ('t', 1, 'g', None, 'e', 2),
            }
        ),
        (
            ['l'], {
                ('f', 12, 'd', None, None, 1),
            }
        ),
        (
            ['q'], {
                ('k', 19, 'm', None, None, 1),
            }
        ),
        (
            ['b'], {
                ('j', 5, 'g', 'o', None, 2),
            }
        ),
        # One from bottom.
        (
            ['t'], {
                ('n', 0, 'g', None, 'e', 2),
                ('e', 2, 'n', None, None, 1),
                ('g', 3, 'c', 'n', 'j', 3),
            }
        ),
        (
            ['a'], {
                ('r', 9, 'd', None, None, 1),
                ('d', 10, 'i', 'r', 'f', 3),
            }
        ),
        (
            ['a', 'r'], {
                ('l', 11, 'i', 'd', 'f', 2),
                ('d', 10, 'l', None, None, 1),
                ('f', 12, 'l', None, None, 1),
                ('i', 13, 'c', 'l', 'm', 4),
            }
        ),
        (
            ['f'], {
                ('l', 11, 'd', None, None, 1),
                ('d', 10, 'i', 'a', 'l', 3),
            }
        ),
        (
            ['f', 'l'], {
                ('r', 9, 'i', 'a', 'd', 2),
                ('a', 8, 'r', None, None, 1),
                ('d', 10, 'r', None, None, 1),
                ('i', 13, 'c', 'r', 'm', 4),
            }
        ),
        # Mid tree
        (
            ['g'], {
                ('e', 2, 'c', 't', 'j', 3),
                ('t', 1, 'e', 'n', None, 2),
                ('j', 5, 'e', 'o', 'b', 2),
                ('c', 7, None, 'e', 'i', 5),
            }
        ),
        (
            ['i'], {
                ('f', 12, 'c', 'd', 'm', 4),
                ('d', 10, 'f', 'a', 'l', 3),
                ('l', 11, 'd', None, None, 1),
                ('m', 17, 'f', 'h', 'k', 3),
                ('c', 7, None, 'g', 'f', 5),
            }
        ),
        # Root
        (
            ['c'], {
                ('b', 6, None, 'g', 'i', 5),
                ('j', 5, 'g', 'o', None, 2),
                ('g', 3, 'b', 't', 'j', 3),
                ('i', 13, 'b', 'd', 'm', 4),
            }
        ),
    )
#tree_nodes = (
#    ('a', 8),
#    ('b', 6),
#    ('c', 7),
#    ('d', 10),
#    ('e', 2),
#    ('f', 12),
#    ('g', 3),
#    ('h', 15),
#    ('i', 13),
#    ('j', 5),
#    ('k', 19),
#    ('l', 11),
#    ('m', 17),
#    ('n', 0),
#    ('o', 4),
#    ('p', 14),
#    ('q', 18),
#    ('r', 9),
#    ('s', 16),
#    ('t', 1),
#)
)
def test_removing_nodes(deploy_coinbase, deployed_contracts, ids_to_remove, expected_states):
    index_name = "test-{0}".format(''.join(ids_to_remove))

    grove = deployed_contracts.Grove

    for _id, value in tree_nodes:
        grove.insert(index_name, _id, value)

    index_id = grove.computeIndexId(deploy_coinbase, index_name)

    for _id in ids_to_remove:
        node_id = grove.computeNodeId(index_id, _id)
        assert grove.exists(index_id, _id) is True
        grove.remove(index_name, _id)
        assert grove.exists(index_id, _id) is False

    actual_states = set()

    for _id, _, _, _, _, _ in expected_states:
        node_id = grove.computeNodeId(index_id, _id)
        value = grove.getNodeValue(node_id)
        parent = grove.getNodeParent(node_id)
        left = grove.getNodeLeftChild(node_id)
        right = grove.getNodeRightChild(node_id)
        height = grove.getNodeHeight(node_id)

        actual_states.add((_id, value, parent, left, right, height))

    assert expected_states == actual_states


def test_deleting_sets_new_root(deploy_coinbase, deployed_contracts):
    grove = deployed_contracts.Grove

    index_name = "test-root_deletion"
    index_id = grove.computeIndexId(deploy_coinbase, index_name)

    grove.insert(index_name, 'a', 2)
    grove.insert(index_name, 'b', 1)
    grove.insert(index_name, 'c', 3)

    node_a_id = grove.computeNodeId(index_id, 'a')
    node_b_id = grove.computeNodeId(index_id, 'b')

    assert grove.getIndexRoot(index_id) == 'a'

    grove.remove(index_name, 'a')

    assert grove.getIndexRoot(index_id) == 'b'
