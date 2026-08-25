<!-- FIXTURE (must fail, with dupe-a.md): see dupe-a.md. -->

# Retrieval index rebuild — operator note B

The retrieval index rebuild procedure runs nightly and writes a manifest of every
document it touched during the pass, so a partial rebuild can be replayed from the
last complete manifest rather than started again from an empty index.

This file is otherwise entirely its own.
