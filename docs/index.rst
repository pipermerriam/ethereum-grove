.. Grove documentation master file, created by
   sphinx-quickstart on Wed Sep 30 12:46:03 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Grove's documentation!
=================================

Grove is an ethereum contract that provides an API for storing and retrieving
ordered data in a fast manner.

The current implementation uses an AVL tree for storage which has on average
``O(log n)`` time complexity for inserts and lookups.

The Grove contract can be accessed at
``0x6b07cb54be50bc040cca0360ec792d7b5609f4db``.  If you would like to verify
the source, it was compiled using version ``0.1.3-1736fe80`` of the ``solc``
compiler with the ``--optimize`` flag turned on.


Indexes
-------

In grove, an index represents one set of ordered data, such as the ages of a
set of people.

Indexes are namespaced by ethereum address, meaning that any write operations
to an index by different addresses will write to different indexes.  Each index
has an id which can be computed as ``sha3(ownerAddress, indexName)``.

You can also use the ``getIndexId(address ownerAddress, bytes32 indexName)``
function to compute this for you.

Nodes
-----

Within each index, there is a binary tree that stores the data.  The tree is
comprised of nodes which have the following attributes.

* **indexId (bytes32):** the index this node belongs to.
* **id (bytes32):** A unique identifier for the data element that this node
  represents.  Within an index, there is a 1:1 relationship between id and a
  node in the index.
* **nodeId (bytes32):** a unique identifier for the node, computed as ``sha3(indexId, id)``
* **value (int):** an integer that can be used to compare this node with other
  nodes to determine ordering.
* **parent (bytes32):** the nodeId of this node's parent (0x0 if no parent).
* **left (bytes32):** the nodeId of this node's left child (0x0 if no left
  child).
* **right (bytes32):** the nodeId of this node's right child (0x0 if no right
  child).
* **height (bytes32):** the longest path from this node to a child leaf node.

For a given piece of data that you wish to track and query the ordering using
Grove, you must be able to provide a unique identifier for that data element,
as well as an integer value that can be used to order the data element with
respect to the other elements.

Node API
^^^^^^^^

* **function getIndexName(bytes32 indexId) constant returns (bytes32)**

  Returns the name for the given index id.

* **function getIndexRoot(bytes32 indexId) constant returns (bytes32)**

  Returns the root node for a given index.

* **function getNodeId(bytes32 nodeId) constant returns (bytes32)**

  Returns the id of the node.

* **function getNodeIndexId(bytes32 nodeId) constant returns (bytes32)**

  Returns the indexId of the node.

* **function getNodeValue(bytes32 nodeId) constant returns (int)**

  Returns the value for the node.

* **function getNodeHeight(bytes32 nodeId) constant returns (uint)**

  Returns the height for the node.

* **function getNodeParent(bytes32 nodeId) constant returns (bytes32)**

  Returns the parent of the node.

* **function getNodeLeftChild(bytes32 nodeId) constant returns (bytes32)**

  Returns the left child of the node.

* **function getNodeRightChild(bytes32 nodeId) constant returns (bytes32)**

  Returns the right child of the node.

Insertion
^^^^^^^^^

**function insert(bytes32 indexName, bytes32 id, int value) public**

You can use the ``insert`` function insert a new piece of data into the index.

* **indexName:** The name of this index.  The index id is automatically
  computed based on ``msg.sender``.
* **id:** The unique identifier for this data.
* **value (int):** The value that can be used to order this node with respect
  to the other nodes.

Querying
^^^^^^^^

**function query(bytes32 indexId, bytes2 operator, int value) public returns (bytes32)**

Each index can be queried using the ``query`` function.

* **indexId:** The id of the index that should be queried.  Note that this is
  **not** the name of the index.
* **operator:** The comparison operator that should be used.  Supported
  operators are ``<``, ``<=``, ``>``, ``>=``, ``==``.
* **value:** The value that each node in the index should be compared againt.

For ``>``, ``>=`` and ``==`` the left-most node that satisfies the comparison
is returned.

For ``<`` and ``<=`` the right-most node that satisfies the comparison is
returned.

If no nodes satisfy the comparison, then 0x0 is returned.


Abstract Solidity Contract
--------------------------

This abstract contract can be used to let your contracts access the Grove API
natively.

.. code-block:: solidity

    contract GroveAPI {
        /*
         *  Shortcuts
         */
        function getIndexId(address ownerAddress, bytes32 indexName) constant returns (bytes32);
        function getNodeId(bytes32 indexId, bytes32 id) constant returns (bytes32);

        /*
         *  Node and Index API
         */
        function getIndexName(bytes32 indexId) constant returns (bytes32);
        function getIndexRoot(bytes32 indexId) constant returns (bytes32);
        function getNodeId(bytes32 nodeId) constant returns (bytes32);
        function getNodeIndexId(bytes32 nodeId) constant returns (bytes32);
        function getNodeValue(bytes32 nodeId) constant returns (int);
        function getNodeHeight(bytes32 nodeId) constant returns (uint);
        function getNodeParent(bytes32 nodeId) constant returns (bytes32);
        function getNodeLeftChild(bytes32 nodeId) constant returns (bytes32);
        function getNodeRightChild(bytes32 nodeId) constant returns (bytes32);

        /*
         *  Insert and Query API
         */
        function insert(bytes32 indexName, bytes32 id, int value) public;
        function query(bytes32 indexId, bytes2 operator, int value) public returns (bytes32);
    }

Contract ABI
------------

The contract can be accessed via web3.js with

.. code-block:: javascript

    var Gove = web3.eth.contract([{"constant":true,"inputs":[{"name":"nodeId","type":"bytes32"}],"name":"getNodeLeftChild","outputs":[{"name":"","type":"bytes32"}],"type":"function"},{"constant":true,"inputs":[{"name":"indexId","type":"bytes32"},{"name":"id","type":"bytes32"}],"name":"getNodeId","outputs":[{"name":"","type":"bytes32"}],"type":"function"},{"constant":true,"inputs":[{"name":"nodeId","type":"bytes32"}],"name":"getNodeValue","outputs":[{"name":"","type":"int256"}],"type":"function"},{"constant":true,"inputs":[{"name":"nodeId","type":"bytes32"}],"name":"getNodeRightChild","outputs":[{"name":"","type":"bytes32"}],"type":"function"},{"constant":false,"inputs":[{"name":"indexName","type":"bytes32"},{"name":"id","type":"bytes32"},{"name":"value","type":"int256"}],"name":"insert","outputs":[],"type":"function"},{"constant":true,"inputs":[{"name":"nodeId","type":"bytes32"}],"name":"getNodeParent","outputs":[{"name":"","type":"bytes32"}],"type":"function"},{"constant":true,"inputs":[{"name":"indexId","type":"bytes32"}],"name":"getIndexName","outputs":[{"name":"","type":"bytes32"}],"type":"function"},{"constant":true,"inputs":[{"name":"nodeId","type":"bytes32"}],"name":"getNodeIndexId","outputs":[{"name":"","type":"bytes32"}],"type":"function"},{"constant":true,"inputs":[{"name":"nodeId","type":"bytes32"}],"name":"getNodeHeight","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[{"name":"nodeId","type":"bytes32"}],"name":"getNodeId","outputs":[{"name":"","type":"bytes32"}],"type":"function"},{"constant":true,"inputs":[{"name":"indexId","type":"bytes32"}],"name":"getIndexRoot","outputs":[{"name":"","type":"bytes32"}],"type":"function"},{"constant":true,"inputs":[{"name":"owner","type":"address"},{"name":"indexName","type":"bytes32"}],"name":"getIndexId","outputs":[{"name":"","type":"bytes32"}],"type":"function"},{"constant":false,"inputs":[{"name":"indexId","type":"bytes32"},{"name":"operator","type":"bytes2"},{"name":"value","type":"int256"}],"name":"query","outputs":[{"name":"","type":"bytes32"}],"type":"function"}]).at(0x6b07cb54be50bc040cca0360ec792d7b5609f4db);

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
