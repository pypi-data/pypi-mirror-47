## coloring-graphs
[![pipeline status](https://aalok-sathe.gitlab.io/coloring-graphs/build.svg?v=584755128329022273)](https://gitlab.com/aalok-sathe/coloring-graphs/)

a coloring graphs library written in C++ for speedy computation and wrapped in
Python for ease of development and extension!

### what
this library provides support to construct graphs and their coloring graphs.
a coloring graph is a metagraph representing all the valid colorings of a graph.
each vertex of a coloring graph represents a coloring of the base graph.

in this project, we represent a coloring as an integer, which, when converted to
base k (for a k-coloring), represents the vertex-wise colors [0,k).

the library is under development being written using Python and C/C++.
for documentation, feel free to take a look inside `libcolgraph/` and read the docstrings.
for examples, see the files in `test/`.
for questions, reach out.

### how
1. installation:

    - manual installation

        refer to [detailed install instructions](INSTALL.md)
        
    
    - [pypi](https://pypi.org/project/libcolgraph/) 

        ```bash
        python3 -m pip install libcolgraph [--user]
        ```

        things to note:
        - currently a binary wheel is available only for [`manylinux`](https://www.python.org/dev/peps/pep-0513/)
          distributions e.g. centOS, Debian family, RedHat family, etc.
        - if your distribution is not `manylinux`-supported, then pip
          will need to compile locally using `swig` and `setuptools`.
          in that case, make sure you have `setuptools` and
          [swig](http://www.swig.org/download.html) installed, as they
          will be needed for compilation.
        - in the future we will release wheels for MacOS as well. these
          might not be as frequently maintained, however, so your best
          bet would be to compile locally using `swig`.


2. quickstart:

    - usage:

    ```python
    import libcolgraph
    g = libcolgraph.Graph()
    g.load_txt('./test/input/g1.in')
    
    g.add_vertex(314)
    
    print(g.size())
    ```

    - run a test suite!
    `make test`

    - try the sandbox file (`test/sandbox.py`) to see how plotting works (currently pure python-only)
        - `python3 test/sandbox.py 3`
        - `python3 test/sandbox.py 3 test/input/g1.in`


### contribute

see [contributing guide](CONTRIBUTING.md)

### help

full documentation coming soon


### who

Coloring Graphs lab, University of Richmond. Multiple contributors.
















