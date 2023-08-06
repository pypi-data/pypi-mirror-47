#ifndef __GRAPH_TEMPLATES_H__
#define __GRAPH_TEMPLATES_H__

#include <unordered_map>
#include <set>
#include <fstream>


// forward declarations
class Vertex;
class BaseVertex;
class ColoringVertex;
template <typename V> class Graph;
class BaseGraph;
class ColoringGraph;
// template <typename V> struct GraphVertexIterator;


template <typename V>
class VertexNeighborIterator
{
    public:
        VertexNeighborIterator() {};
        virtual ~VertexNeighborIterator() {};

        virtual long next() = 0;
        virtual long __next__();

        virtual bool hasnext() = 0;

        virtual VertexNeighborIterator<V>* __iter__();
};


template <typename V>
class GraphVertexIterator
{
    public:
        typename std::unordered_map<long, V*>::iterator it;
        long len;

        GraphVertexIterator<V>() {};
        GraphVertexIterator<V>(typename std::unordered_map<long, V*>::iterator it_,
                               long len_)
            : it(it_), len(len_) {};
        virtual ~GraphVertexIterator() {};

        virtual V next();
        virtual V __next__();

        virtual bool hasnext();

        virtual GraphVertexIterator<V>* __iter__();
};


template <typename V>
class Graph
{
    public:
        std::unordered_map<long, V*> vertices;

        Graph();
        virtual ~Graph();

        virtual void load_txt(char* path) {};

        virtual long size();
        virtual long __len__() { return size(); };

        // virtual char* __repr__() {};

        virtual void add_vertex(long name) = 0;

        virtual V& get_vertex(long name);
        virtual V& get_some_vertex();

        virtual const GraphVertexIterator<V>* __iter__() = 0;
        virtual const GraphVertexIterator<V>* get_vertices() = 0;


};

#endif
