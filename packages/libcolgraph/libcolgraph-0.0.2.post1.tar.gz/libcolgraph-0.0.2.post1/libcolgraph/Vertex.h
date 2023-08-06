#ifndef __VERTEX_H__
#define __VERTEX_H__

#include <unordered_set>
#include <list>
#include <cstddef>
#include <stdexcept>
#include <math.h>
#include <limits.h>

#include "Graph.h"
#include "GraphTemplates.h"

// forward declarations
class Vertex;
class BaseVertex;
class ColoringVertex;
class MetaVertex;
template <typename V> class Graph;
class BaseGraph;
class ColoringGraph;
class MetaGraph;


class BaseVertexNeighborIterator : public VertexNeighborIterator<BaseVertex>
{
    public:
        std::unordered_set<long>::iterator it;
        long len;

        BaseVertexNeighborIterator() {};
        BaseVertexNeighborIterator(std::unordered_set<long>::iterator it_, long len_);

        long next() override;

        bool hasnext() override;
};


class ColoringVertexNeighborIterator : public VertexNeighborIterator<ColoringVertex>
{
    public:
        long name;
        int colors;
        ColoringGraph* graph;

        // long remaining;
        int outerpos;
        int positionctr;
        int colorctr;

        ColoringVertexNeighborIterator() {};
        ColoringVertexNeighborIterator(long name_, int colors_, ColoringGraph* graph_);

        // ~ColoringVertexNeighborIterator() {};

        long next() override;

        bool hasnext() override;

};


class MetaVertexNeighborIterator : public VertexNeighborIterator<MetaVertex>
{
    public:
        std::unordered_set<long>::iterator it;
        long len;

        MetaVertexNeighborIterator() {};
        MetaVertexNeighborIterator(std::unordered_set<long>::iterator it_, long len_);

        long next() override;

        bool hasnext() override;
};


class Vertex
{
    public:
        // the name of this vertex. must ve unique within its Graph instance
        long name;

        // depth and lowpoint variables, specific to Tarjans
        int depth;
        int lowpoint;
        // stores a list iterator object pointing to a position in some list
        // where the vertex's parent lies. useful in Tarjans
        std::list<long>::iterator parent;

        Vertex() {};
        // constructor to initialize it with a name
        Vertex(long name_);

        // default deconstructor
        virtual ~Vertex();

        // override the equality operator. equality is
        // determined by matching names
        bool operator==(const Vertex& other);

        // helper methods to support state-preserving iteration
        virtual long get_next_neighbor() = 0;
        virtual void reset_neighbor_track() = 0;

        virtual long get_name() const;

        // virtual VertexNeighborIterator<Vertex>* __iter__() = 0;
        // virtual VertexNeighborIterator<Vertex>* get_neighbors() = 0;
};


class BaseVertex : public Vertex
{
    public:
        // BaseVertex stores its neighbors as a set
        std::unordered_set<long> neighbors;
        // state preserving iterator object to support iteration over its
        // neighbors
        BaseVertexNeighborIterator* nt;

        // default constructor
        BaseVertex() {};
        // preferred constructor with its name
        BaseVertex(long name_);

        // add a neighbor `other` to its vertex list
        void add_neighbor(Vertex& other);

        // helper methods to support state-preserving iteration
        long get_next_neighbor() override;
        void reset_neighbor_track() override;

        // returns a pointer to a BaseVertexNeighborIterator object to
        // support iteration over its neighbors
        BaseVertexNeighborIterator* __iter__();
        BaseVertexNeighborIterator* get_neighbors();
};


class ColoringVertex : public Vertex
{
    public:
        // variable colors, indicating how many colors this scheme of colorings
        // has
        const int colors;
        // pointer to the ColoringGraph that this vertex belongs to
        ColoringGraph* graph;
        // state preserving iterator object to support iteration over its
        // neighbors. has specially implemented methods to get neighbors of a
        // coloring vertex based on computation, rather than by storing a list,
        // because coloring graphs can be huge.
        ColoringVertexNeighborIterator* nt;

        // preferred constructor
        ColoringVertex(long name_, int k, ColoringGraph* graph_);

        // helper methods to support state-preserving iteration
        long get_next_neighbor() override;
        void reset_neighbor_track() override;

        // returns a pointer to a ColoringVertexNeighborIterator object to
        // support iteration over its neighbors
        ColoringVertexNeighborIterator* __iter__();
        ColoringVertexNeighborIterator* get_neighbors();
};



class MetaVertex : public Vertex
{
    public:
        // an unordered_set to store its neighbors
        std::unordered_set<long> neighbors;
        // an unordered_set to store the names of vertices in this MetaVertex
        // taken from the underlying Graph that Tarjans was run on
        typename std::unordered_set<long> vertices;
        // an instance of a neighbor iterator
        MetaVertexNeighborIterator* nt;
        // stores an `identity` name, that is associated with the name of some
        // vertex of the graph Tarjans was run on. useful to compare cut meta
        // vertices with actual cut vertex objects
        long identity;

        // preferred constructor. name should be unique among all MetaVertex
        // objects of its MetaGraph
        MetaVertex(long name_);

        // deconstructor
        ~MetaVertex() {};

        // adds a neighbor `other` to this MetaVertex
        void add_neighbor(MetaVertex& other);

        // add to each other's neighbor list
        void connect(MetaVertex* v);
        // remove from each other's neighbor list
        void disconnect(MetaVertex* v);

        // helper methods to support state-preserving iteration
        long get_next_neighbor() override;
        void reset_neighbor_track() override {};

        // returns a pointer to a MetaVertexNeighborIterator object to support
        // iteration over its neighbors
        MetaVertexNeighborIterator* __iter__();
        MetaVertexNeighborIterator* get_neighbors();


};



#endif
