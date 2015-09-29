contract Grove {
        /*
         *  Call tracking API
         */
        struct Node {
                bytes32 nodeId;
                bytes32 indexId;
                bytes32 id;
                uint value;
                bytes32 parent;
                bytes32 left;
                bytes32 right;
                uint height;
        }

        bytes32 public rootNodeID;

        // Maps an index id to the id of it's root node.
        mapping (bytes32 => bytes32) index_to_root;

        // Maps node_id to Node
        mapping (bytes32 => Node) node_lookup;

        function getNodeId(bytes32 indexId, bytes32 id) public returns (bytes32) {
                return sha3(indexId, id);
        }

        function max(uint a, uint b) internal returns (uint) {
            if (a >= b) {
                return a;
            }
            return b;
        }

        /*
         *  Node getters
         */
        function getNodeId(bytes32 nodeId) public returns (bytes32) {
            return node_lookup[nodeId].id;
        }

        function getNodeIndexId(bytes32 nodeId) public returns (bytes32) {
            return node_lookup[nodeId].indexId;
        }

        function getNodeValue(bytes32 nodeId) public returns (uint) {
            return node_lookup[nodeId].value;
        }

        function getNodeHeight(bytes32 nodeId) public returns (uint) {
            return node_lookup[nodeId].height;
        }

        function getNodeParent(bytes32 nodeId) public returns (bytes32) {
            return node_lookup[nodeId].parent;
        }

        function getNodeLeftChild(bytes32 nodeId) public returns (bytes32) {
            return node_lookup[nodeId].left;
        }

        function getNodeRightChild(bytes32 nodeId) public returns (bytes32) {
            return node_lookup[nodeId].right;
        }

        function insert(bytes32 indexId, bytes32 id, uint value) public {
                int balanceFactor;
                uint leftHeight;
                uint rightHeight;

                bytes32 previousNodeId = 0x0;
                bytes32 nodeId = getNodeId(indexId, id);
                var currentNode = node_lookup[index_to_root[indexId]];

                // Do insertion
                while (true) {
                    if (currentNode.indexId == 0x0) {
                        // This is a new unpopulated node.
                        currentNode.nodeId = nodeId;
                        currentNode.parent = previousNodeId;
                        currentNode.indexId = indexId;
                        currentNode.id = id;
                        currentNode.value = value;
                        break;
                    }

                    // Set the previous node id.
                    previousNodeId = currentNode.nodeId;

                    // The new node belongs in the right subtree
                    if (value >= currentNode.value) {
                        if (currentNode.right == 0x0) {
                            currentNode.right = nodeId;
                        }
                        currentNode = node_lookup[currentNode.right];
                        continue;
                    }

                    // The new node belongs in the left subtree.
                    if (currentNode.left == 0x0) {
                        currentNode.left = nodeId;
                    }
                    currentNode = node_lookup[currentNode.left];
                }

                // Trace back up rebalancing.
                while (true) {
                    balanceFactor = _getBalanceFactor(currentNode.nodeId);

                    if (balanceFactor == 2) {
                        // Right rotation (tree is heavy on the left)
                        if (_getBalanceFactor(currentNode.left) == -1) {
                            // The subtree is leaning right so it need to be
                            // rotated left before the current node is rotated
                            // right.
                            _rotateLeft(currentNode.left);
                        }
                        _rotateRight(currentNode.nodeId);
                    }

                    if (balanceFactor == -2) {
                        // Left rotation (tree is heavy on the right)
                        if (_getBalanceFactor(currentNode.right) == 1) {
                            // The subtree is leaning left so it need to be
                            // rotated right before the current node is rotated
                            // left.
                            _rotateRight(currentNode.right);
                        }
                        _rotateLeft(currentNode.nodeId);
                    }

                    if ((-1 <= balanceFactor) && (balanceFactor <= 1)) {
                        _updateNodeHeight(currentNode.nodeId);
                    }

                    if (currentNode.parent == 0x0) {
                        // Reached the root so break.
                        break;
                    }

                    currentNode = node_lookup[currentNode.parent];
                }
        }

        function _getBalanceFactor(bytes32 nodeId) internal returns (int) {
                var node = node_lookup[nodeId];

                return int(node_lookup[node.left].height) - int(node_lookup[node.right].height);
        }

        function _updateNodeHeight(bytes32 nodeId) internal {
                var node = node_lookup[nodeId];

                node.height = max(node_lookup[node.left].height, node_lookup[node.right].height) + 1;
        }

        function _rotateLeft(bytes32 nodeId) internal {
            var node = node_lookup[nodeId];

            if (node.right == 0x0) {
                // Cannot rotate left if there is no right node to rotate into
                // place.
                __throw();
            }

            // The right child is the new root, so it gets the original
            // `node.parent` as it's parent.
            var rightChild = node_lookup[node.right];
            rightChild.parent = node.parent;

            if (node.parent != 0x0) {
                // If there is a parent node, it needs to now point downward at
                // the rightChild which is rotating into the place where `node` was.
                var parent = node_lookup[node.parent];

                // figure out if we're a left or right child and have the
                // parent point to the new node.
                if (parent.left == node.nodeId) {
                    parent.left = rightChild.nodeId;
                }
                if (parent.right == node.nodeId) {
                    parent.right = rightChild.nodeId;
                }
            }


            if (rightChild.left != 0) {
                // If the right child had a left child, that moves to the
                // location that the right child used to be on the original
                // node.
                var leftChild = node_lookup[rightChild.left];
                node.right = rightChild.left;
                leftChild.parent = node.nodeId;
                _updateNodeHeight(leftChild.nodeId);
            }

            // Update the rightChild's left node to point at the original node.
            node.parent = rightChild.nodeId;
            rightChild.left = node.nodeId;

            // TODO: are both of these updates necessary?
            _updateNodeHeight(node.nodeId);
            _updateNodeHeight(rightChild.nodeId);
        }

        function _rotateRight(bytes32 nodeId) internal {
            var node = node_lookup[nodeId];

            if (node.left == 0x0) {
                // Cannot rotate right if there is no left node to rotate into
                // place.
                __throw();
            }

            // The left child is taking the place of node, so we update it's
            // parent to be the original parent of the node.
            var leftChild = node_lookup[node.left];
            leftChild.parent = node.parent;

            if (node.parent != 0x0) {
                // If the node has a parent, update the correct child to point
                // at the leftChild now.
                var parent = node_lookup[node.parent];

                if (parent.left == node.nodeId) {
                    parent.left = leftChild.nodeId;
                }
                if (parent.right == node.nodeId) {
                    parent.right = leftChild.nodeId;
                }
            }

            if (leftChild.right != 0x0) {
                var rightChild = node_lookup[leftChild.right];
                node.left = leftChild.right;
                rightChild.parent = node.nodeId;
                _updateNodeHeight(rightChild.nodeId);
            }

            node.parent = leftChild.nodeId;
            leftChild.right = node.nodeId;

            // TODO: are both of these updates necessary?
            _updateNodeHeight(node.nodeId);
            _updateNodeHeight(leftChild.nodeId);
        }

        function __throw() {
            int[] x;
            x[1];
        }
}
