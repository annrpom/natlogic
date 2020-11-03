# Natural Logic
## Larry Moss


Hello, this README is basically useless for now since this repo is private, but I might use this to jot down ramblings of a documentation before I try to start making everything look pretty with Jupyter.


Plan:
- [ ] Functional Code
- [ ] Rough Documentation
- [ ] Refactored Code
- [ ] Full Documentation (Jupyter)
- [ ] Overview


Some weird SageMath stuff and the equivalent in Python:
- var() aka Symbolic Variables, they are strings of characters that you can define as a symbol. 

> In that case we want to try and minimise dependencies.
> Anything using Sage that could instead use the Python
> standard library should do so. For things not available in
> the Python standard library, we could check what other
> packages provide the functionality that are smaller than
> Sage to install. For example, SymPy might have most of
> the required functionality. And maybe we need networkx
> or igraph for some of the graph things. 








### What the code does:
Beginning code using `symbols()` initializes variables as symbolic variables.

`ran()` creates a list of n elements, with items 0 to n-1.

`cmp_to_key`

`isOdd` determines if n is odd

`maxx` returns max of an iterable, if iterable is empty then returns 0-a safe `max()`

`ssup` adds 1 to every element in the given list and takes the max of it

`last` returns the last element in a list


