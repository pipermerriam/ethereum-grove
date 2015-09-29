### MVP

Grove provides data structures for managing ordered data.

- Keeps an index for each field for which ordering should be tracked.
- Each index is represented as a tree structure, where the nodes have a left
  and righ child.  The left child is always *before* the node, and the right
  child is always *after* the node.
- Each index implements a self-balancing tree to store its data
    - Maybe 2-3 Tree (https://en.wikipedia.org/wiki/2-3_tree)
        - Algorithm seems easier but the data structure seems more compler.
    - Maybe AA_tre (https://en.wikipedia.org/wiki/AA_tree)
        - Algorithm seems slightly harder, but data structure seems simpler.
- Each record has an identifier
- Each identifier has a value used for ordering.  This relationship is 1:1.
  The value `0` is reserved to represent `nil`.
- Supported Operations.
    - Insertion: places the identifier in the tree.
    - Querying: finds first identifier who's value matches the query.
        - Lookup: return the record for the identifier (internal)
        - Existence: first identifier that equals.
        - `> , >= , < , <=`: first identifier that satisfies the comparison to
          a provided value.
- Possible Extra Operations.
    - Iteration: implemented as a cursor that tracks position and direction and
      advances through the structure one element at a time. (would require
      transactional interactions)
    - Removal: removes the identifier from the tree.
