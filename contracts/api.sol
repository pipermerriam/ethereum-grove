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
         *  Traversal
         */
        function getNextNode(bytes32 nodeId) constant returns (bytes32);
        function getPreviousNode(bytes32 nodeId) constant returns (bytes32);

        /*
         *  Insert and Query API
         */
        function insert(bytes32 indexName, bytes32 id, int value) public;
        function query(bytes32 indexId, bytes2 operator, int value) public returns (bytes32);
        function exists(bytes32 indexId, bytes32 id) constant returns (bool);
        function remove(bytes32 indexName, bytes32 id) public;
}
