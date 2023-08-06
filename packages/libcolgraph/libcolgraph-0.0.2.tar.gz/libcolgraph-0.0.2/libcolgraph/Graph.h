#ifndef __GRAPH_H__
#define __GRAPH_H__

#include <unordered_map>
#include <cstddef>
#include <stdexcept>
#include <iostream>
#include <fstream>
#include <vector>
#include <list>
#include <stack>
#include "GraphTemplates.h"
#include "Vertex.h"


// forward declarations
class Vertex;
class BaseVertex;
class ColoringVertex;
class MetaVertex;
template <typename V> class Graph;
class BaseGraph;
class ColoringGraph;
class MetaGraph;


// an iterator class subclassed from GraphVertexIterator to specifically
// support iteration over a BaseGraph's Vertices, i.e., BaseVertex objects
class BaseGraphVertexIterator : public GraphVertexIterator<BaseVertex>
{
    public:
        BaseGraphVertexIterator() {};
        // constructor that takes in an iterator over vertex map
        BaseGraphVertexIterator(typename std::unordered_map<long, BaseVertex*>::iterator it_, long len_)
            : GraphVertexIterator<BaseVertex>(it_, len_) {};
};


// an iterator class subclassed from GraphVertexIterator to specifically
// support iteration over a ColoringGraph's Vertices, i.e., ColoringVertex
class ColoringGraphVertexIterator : public GraphVertexIterator<ColoringVertex>
{
    public:
        ColoringGraphVertexIterator() {};
        // constructor that takes in an iterator over vertex map
        ColoringGraphVertexIterator(typename std::unordered_map<long, ColoringVertex*>::iterator it_, long len_)
            : GraphVertexIterator<ColoringVertex>(it_, len_) {};

};


// an iterator class subclassed from GraphVertexIterator to specifically
// support iteration over a MetaGraph's Vertices, i.e., MetaVertex
class MetaGraphVertexIterator : public GraphVertexIterator<MetaVertex>
{
    public:
        MetaGraphVertexIterator() {};
        MetaGraphVertexIterator(typename std::unordered_map<long, MetaVertex*>::iterator it_, long len_)
            : GraphVertexIterator<MetaVertex>(it_, len_) {};

        // MetaGraphVertexIterator* __iter__();
};


// class BaseGraph subclassed from a particular template instance of Graph,
// that for BaseVertex objects
class BaseGraph : public Graph<BaseVertex>
{
    public:
        // default constructor
        BaseGraph();

        // method that takes a path to a file containing an adjacency matrix
        // description of a graph
        void load_txt(char* path);

        // adds a vertex of supplied name to the vertex list
        void add_vertex(long name) override;
        // adds an edge between two vertices with supplied names
        void make_edge(long a, long b);

        // given a coloring encoding in base 10 and parameter k for how many
        // colors, tries to assign coloring to vertices and determines if
        // it is a valid coloring
        bool is_valid_coloring(long coloring, int k);

        // given a coloring encoding, the name of a vertex, and param k,
        // determines the color of the vertex with supplied name in this
        // encoding
        int get_vertex_color(long coloring, long name, int k);

        // builds a coloring graph with k colors for this graph
        ColoringGraph* build_coloring_graph(int k);

        // returns an iterator object pointer over this graph's vertices
        const BaseGraphVertexIterator* __iter__() override;
        const BaseGraphVertexIterator* get_vertices() override;
};


class ColoringGraph : public Graph<ColoringVertex>
{
    public:
        // private constant, the number of colors this coloring graph has
        const int colors;
        // stores a pointer to the graph that this graph was constructed from
        BaseGraph* base;
        // precompexp[p][c] --> c * (COLORS ** p)
        std::vector<std::vector<long> > precompexp;

        // preferred constructor
        ColoringGraph(int k, BaseGraph* bg);

        // adds a vertex with given name to this graph
        void add_vertex(long name) override;

        // returns an iterator object pointer over this graph's vertices
        const ColoringGraphVertexIterator* __iter__() override;
        const ColoringGraphVertexIterator* get_vertices() override;

};


class MetaGraph : public Graph<MetaVertex>
{
    public:
        // default constructor
        MetaGraph();

        void add_vertex(long name) override;
        MetaVertex* add_vertex();

        // removes vertex with
        void remove_vertex(MetaVertex* m);

        // returns an iterator object pointer over this graph's vertices
        const MetaGraphVertexIterator* __iter__() override;
        const MetaGraphVertexIterator* get_vertices() override;

};




#endif
