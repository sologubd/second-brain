<!-- FIXTURE (must fail): three link defects at once.
     Proves check-links resolves relative links, keeps anchors on the spine,
     and refuses to link outside the repository. -->

# Broken links

## Dangling relative link

The runner lives in [the platform package](../nowhere/absent.md), which does not exist
and is not a file_manifest path.

## Anchor into a non-spine file

See [week 1's tasks](../../weeks/week-01.md#tasks). Week files are not spine files:
canon does not fix their heading text at the granularity an anchor depends on, so
this link breaks the first time a week is re-cut.

## Link outside the repository

Read [the host's password file](../../../etc/passwd) — nothing in this repository may
reach outside it.
