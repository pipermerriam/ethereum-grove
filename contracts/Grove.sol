// Grove v0.3
import "libraries/GroveLib.sol";


/// @title Grove - queryable indexes for ordered data.
/// @author Piper Merriam <pipermerriam@gmail.com>
contract Grove {
        /*
         *  Indexes for ordered data
         *
         *  Address: 0x8017f24a47c889b1ee80501ff84beb3c017edf0b
         */
        // Map index_id to index
        mapping (bytes32 => GroveLib.Index) index_lookup;

        // Map node_id to index_id.
        mapping (bytes32 => bytes32) node_to_index;
        mapping (bytes32 => bytes32) node_id_lookup;

        /// @notice Computes the id for a Grove index which is sha3(owner, indexName)
        /// @param owner The address of the index owner.
        /// @param indexName The name of the index.
        function computeIndexId(address owner, bytes32 indexName) constant returns (bytes32) {
                return sha3(owner, indexName);
        }

        /// @notice Computes the id for a node in a given Grove index which is sha3(indexId, id)
        /// @param indexId The id for the index the node belongs to.
        /// @param id The unique identifier for the data this node represents.
        function computeNodeId(bytes32 indexId, bytes32 id) constant returns (bytes32) {
                return sha3(indexId, id);
        }

        /*
         *  Node getters
         */
        /// @notice Retrieves the id of the root node for this index.
        /// @param indexId The id of the index.
        function getIndexRoot(bytes32 indexId) constant returns (bytes32) {
            return index_lookup[indexId].root;
        }

        /// @dev Retrieve the index id for the node.
        /// @param nodeId The id for the node
        function getNodeIndexId(bytes32 nodeId) constant returns (bytes32) {
            return node_to_index[nodeId];
        }

        /// @dev Retrieve the value of the node.
        /// @param nodeId The id for the node
        function getNodeValue(bytes32 nodeId) constant returns (int) {
            return GroveLib.getNodeValue(index_lookup[node_to_index[nodeId]], node_id_lookup[nodeId]);
        }

        /// @dev Retrieve the height of the node.
        /// @param nodeId The id for the node
        function getNodeHeight(bytes32 nodeId) constant returns (uint) {
            return GroveLib.getNodeHeight(index_lookup[node_to_index[nodeId]], node_id_lookup[nodeId]);
        }

        /// @dev Retrieve the parent id of the node.
        /// @param nodeId The id for the node
        function getNodeParent(bytes32 nodeId) constant returns (bytes32) {
            return GroveLib.getNodeParent(index_lookup[node_to_index[nodeId]], node_id_lookup[nodeId]);
        }

        /// @dev Retrieve the left child id of the node.
        /// @param nodeId The id for the node
        function getNodeLeftChild(bytes32 nodeId) constant returns (bytes32) {
            return GroveLib.getNodeLeftChild(index_lookup[node_to_index[nodeId]], node_id_lookup[nodeId]);
        }

        /// @dev Retrieve the right child id of the node.
        /// @param nodeId The id for the node
        function getNodeRightChild(bytes32 nodeId) constant returns (bytes32) {
            return GroveLib.getNodeRightChild(index_lookup[node_to_index[nodeId]], node_id_lookup[nodeId]);
        }

        /** @dev Retrieve the id of the node that comes immediately before this
         *  one.  Returns 0x0 if there is no previous node.
         */
        /// @param nodeId The id for the node
        function getPreviousNode(bytes32 nodeId) constant returns (bytes32) {
            return GroveLib.getPreviousNode(index_lookup[node_to_index[nodeId]], node_id_lookup[nodeId]);
        }

        /** @dev Retrieve the id of the node that comes immediately after this
         *  one.  Returns 0x0 if there is no previous node.
         */
        /// @param nodeId The id for the node
        function getNextNode(bytes32 nodeId) constant returns (bytes32) {
            return GroveLib.getNextNode(index_lookup[node_to_index[nodeId]], node_id_lookup[nodeId]);
        }

        /** @dev Update or Insert a data element represented by the unique
         *  identifier `id` into the index.
         */
        /// @param indexName The human readable name for the index that the node should be upserted into.
        /// @param id The unique identifier that the index node represents.
        /// @param value The number which represents this data elements total ordering.
        function insert(bytes32 indexName, bytes32 id, int value) public {
                bytes32 indexId = computeIndexId(msg.sender, indexName);
                GroveLib.Index storage index = index_lookup[indexId];

                bytes32 nodeId = computeNodeId(indexId, id);
                // Store the mapping from nodeId to the indexId
                node_to_index[nodeId] = indexId;
                node_id_lookup[nodeId] = id;

                GroveLib.insert(index, id, value);
        }

        /// @dev Query whether a node exists within the specified index for the unique identifier.
        /// @param indexId The id for the index.
        /// @param id The unique identifier of the data element.
        function exists(bytes32 indexId, bytes32 id) constant returns (bool) {
            return GroveLib.exists(index_lookup[indexId], id);
        }

        /// @dev Remove the index node for the given unique identifier.
        /// @param indexName The name of the index.
        /// @param id The unique identifier of the data element.
        function remove(bytes32 indexName, bytes32 id) public {
            GroveLib.remove(index_lookup[computeIndexId(msg.sender, indexName)], id);
        }

        /** @dev Query the index for the edge-most node that satisfies the
         * given query.  For >, >=, and ==, this will be the left-most node
         * that satisfies the comparison.  For < and <= this will be the
         * right-most node that satisfies the comparison.
         */
        /// @param indexId The id of the index that should be queried
        /** @param operator One of '>', '>=', '<', '<=', '==' to specify what
         *  type of comparison operator should be used.
         */
        function query(bytes32 indexId, bytes2 operator, int value) constant returns (bytes32) {
                return GroveLib.query(index_lookup[indexId], operator, value);
        }
}
