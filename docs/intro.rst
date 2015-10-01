Introduction to Grove
=====================

To understand how Grove can be used, we need a situation where we care about
the ordering of our data.  Lets explore this in the context of a name
registrar.  Suppose we have a contract which holds some set of key/value
mappings.

.. code-block:: solidity

    contract namereg {
        struct Record {
            address owner;
            bytes32 key;
            bytes32 value;
            uint expires;
        }
        ...
    }

One question that someone might want to ask this data is *"Which record will
expire next"*.  To enable this, the namereg contract would need to feed
registrations into and index in grove.

.. code-block:: javascript

    contract namereg {
        // Here, Grove might be an abstract solidity contract that allows our 
        // namereg contract to interact with it's public API.
        Grove grove = Grove('0x6b07cb54be50bc040cca0360ec792d7b5609f4db');

        struct Record {
            address owner;
            bytes32 key;
            bytes32 value;
            uint expires;
        }
        function register(bytes32 key, bytes32 value) {
            ... // Do the actual registration

            grove.insert("recordExpiration", key, record.expires);
        }
    }

So, each time someone registers a key, it tells grove about the record, using
the ``key`` as the ``id``, and the expiration time of the record as the
``value`` that grove will use for ordering.  Grove will store these records in
the index ``recordExpiration``.

Someone who wished to query for the next record to expire would do something
like the following.  We'll assume that we've loaded the Grove ABI into a
contract object in web3.

.. code-block:: javascript

    // Compute the ID for the index we want to query
    > index_id = Grove.getIndexId(namereg.address, "recordExpiration")
    // Query grove for the first record that is greater than 'now'.
    > node_id = Grove.query(index_id, ">", now_timestamp)
    > record_id = Grove.getNodeId(node_id)


In this example, ``node_id`` would either be ``0x0`` if there is no record
who's expiration is greater than the ``now_timestamp`` value, or the
``bytes32`` of the first node in the index that is greater than
``now_timestamp``.

Assuming that ``node_id`` is not ``0x0``, we can then fetch the ``key`` for the
record using the ``grove.getNodeId`` function.
