<!-- FIXTURE (must fail, with dupe-b.md): the paragraph below is repeated
     verbatim in dupe-b.md and matches no canon exemption.
     Proves check-dupes detects a 12-gram shingled span across two files. -->

# Retrieval index rebuild — operator note A

The retrieval index rebuild procedure runs nightly and writes a manifest of every
document it touched during the pass, so a partial rebuild can be replayed from the
last complete manifest rather than started again from an empty index.

Everything else in this file is unique to it.
