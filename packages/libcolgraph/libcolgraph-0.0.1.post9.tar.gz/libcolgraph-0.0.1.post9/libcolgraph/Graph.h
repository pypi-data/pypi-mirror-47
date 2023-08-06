#ifndef __GRAPH_H__
#define __GRAPH_H__

#include <unordered_map>
#include <cstddef>
#include <stdexcept>
#include <iostream>
#include <fstream>
#include <vector>
#include "GraphTemplates.h"
#include "Vertex.h"


class Vertex;
class BaseVertex;
class ColoringVertex;
template <typename V> class Graph;
class BaseGraph;
class ColoringGraph;



class BaseGraphVertexIterator : public GraphVertexIterator<BaseVertex>
{
    public:
        BaseGraphVertexIterator() {};
        BaseGraphVertexIterator(typename std::unordered_map<long, BaseVertex*>::iterator it_, long len_)
            : GraphVertexIterator<BaseVertex>(it_, len_) {};

        // BaseGraphVertexIterator* __iter__();
};


class ColoringGraphVertexIterator : public GraphVertexIterator<ColoringVertex>
{
    public:
        ColoringGraphVertexIterator() {};
        ColoringGraphVertexIterator(typename std::unordered_map<long, ColoringVertex*>::iterator it_, long len_)
            : GraphVertexIterator<ColoringVertex>(it_, len_) {};

        // ColoringGraphVertexIterator* __iter__();
};


// template <typename V = Vertex>
class BaseGraph : public Graph<BaseVertex>
{
    public:
        BaseGraph();

        void load_txt(char* path);

        void add_vertex(long name) override;
        void make_edge(long a, long b);

        bool is_valid_coloring(long coloring, int k);

        int get_vertex_color(long coloring, long name, int k);

        ColoringGraph* build_coloring_graph(int k);

        const BaseGraphVertexIterator* __iter__() override;
        const BaseGraphVertexIterator* get_vertices() override;
};


// template <typename V = ColoringVertex>
class ColoringGraph : public Graph<ColoringVertex>
{
    public:
        int colors;
        BaseGraph* base;
        // precompexp[p][c] --> c * (COLORS ** p)
        std::vector<std::vector<long> > precompexp;

        ColoringGraph(int k, BaseGraph* bg);

        void add_vertex(long name) override;

        // ColoringVertex& get_vertex(long name);
        // ColoringVertex& get_some_vertex();

        const ColoringGraphVertexIterator* __iter__() override;
        const ColoringGraphVertexIterator* get_vertices() override;

};


#endif
