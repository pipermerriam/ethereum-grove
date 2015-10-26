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


def test_exists_query(deploy_coinbase, deployed_contracts):
    grove = deployed_contracts.Grove
    index_id = grove.computeIndexId(deploy_coinbase, "test-a")

    for _id, value in tree_nodes:
        assert grove.exists(index_id, _id) is False

        grove.insert('test-a', _id, value)

        assert grove.exists(index_id, _id) is True

    # Make sure it still registers as having all of the nodes.
    for _id, _ in tree_nodes:
        assert grove.exists(index_id, _id) is True

    # Sanity check
    for _id in ('aa', 'tsra', 'arst', 'bb', 'cc'):
        assert grove.exists(index_id, _id) is False


def test_exists_query_special_case(deploy_coinbase, deployed_contracts):
    grove = deployed_contracts.Grove
    index_id = grove.computeIndexId(deploy_coinbase, "test-b")

    grove.insert('test-b', 'key', 1234)

    assert grove.exists(index_id, '') is False
