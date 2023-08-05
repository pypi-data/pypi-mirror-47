# Datalog (py)

An implementation of Datalog in Python (eventually other languages too).

Features an interactive `datalog` interpreter.

## Usage

`pip install --user arrdem.datalog`

## Status

This is a complete to my knowledge implementation of a traditional datalog.

Support is included for binary `=` as builtin relation, and for negated terms in
rules (prefixed with `~`)

Rules, and the recursive evaluation of rules is supported with some guards to
prevent infinite recursion.

The interactive interpreter supports definitions (terms ending in `.`),
retractions (terms ending in `!`) and queries (terms ending in `?`), see the
interpreter's `help` response for more details.

### Limitations

Recursion may have some completeness bugs. I have not yet encountered any, but I
also don't have a strong proof of correctness for the recursive evaluation of
rules yet.

The current implementation of negated clauses CANNOT propagate positive
information. This means that negated clauses can only be used in conjunction
with positive clauses. It's not clear if this is an essential limitation.

There is as of yet no query planner - not even segmenting rules and tuples by
relation to restrict evaluation. This means that the complexity of a query is
`O(dataset * term count)`, which is clearly less than ideal.

## License

Mirrored from https://git.arrdem.com/arrdem/datalog-py

Published under the MIT license. See [LICENSE.md](LICENSE.md)
