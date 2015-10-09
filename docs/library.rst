Library Usage
=============

Grove can be used as a `solidity library <https://github.com/ethereum/wiki/wiki/Solidity-Tutorial#libraries>`_, allowing use of all of Groves functionality using your own contracts storage.

The primary Grove contract itself is actually just a wrapper around the
deployed library contract.


Example
-------

In this example, we will use a fictional contract ``Members`` which tracks
information about some set of members for an organization.


.. code-block:: solidity

    library GroveAPI {
        struct Index {
                bytes32 id;
                bytes32 name;
                bytes32 root;
                mapping (bytes32 => Node) nodes;
        }

        struct Node {
                bytes32 nodeId;
                bytes32 indexId;
                bytes32 id;
                int value;
                bytes32 parent;
                bytes32 left;
                bytes32 right;
                uint height;
        }

        function insert(Index storage index, bytes32 id, int value) public;
        function query(Index storage index, bytes2 operator, int value) public returns (bytes32);
    }

    contract Members {
        Grove.Index ageIndex;
            
        function addMember(bytes32 name, uint age) {
            ... // Do whatever needs to be done to add the member.

            // Update the ageIndex with this new member's age.
            Grove.insert(ageIndex, name, age);
        }

        function isAnyoneThisOld(uint age) constant returns (bool) {
            return Grove.query("==", age) != 0x0;
        }
    }


The ``Members`` contract above interfaces with the Grove library in two places.

First, within the ``addMember`` function, everytime a member is added to the
organization, their age is tracked in the ``ageIndex``.

Second, the ``isAnyoneThisOld`` allows checking whether any member is a
specific age.
