#ifndef __VERTEX_H__
#define __VERTEX_H__

#include <unordered_set>
#include <cstddef>
#include <stdexcept>
#include <math.h>

#include "Graph.h"
#include "GraphTemplates.h"

class Vertex;
class BaseVertex;
class ColoringVertex;
template <typename V> class Graph;
class BaseGraph;
class ColoringGraph;


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
        int positionctr;
        int colorctr;

        ColoringVertexNeighborIterator() {};
        ColoringVertexNeighborIterator(long name_, int colors_, ColoringGraph* graph_);

        // ~ColoringVertexNeighborIterator() {};

        long next() override;

        bool hasnext() override;

};


class Vertex
{
    public:
        long name;

        Vertex() {};
        Vertex(long name_);

        virtual ~Vertex();

        // virtual const char* __repr__();
        // virtual const char* __str__();

        bool operator==(const Vertex& other);

        virtual long get_next_neighbor() = 0;
        virtual void reset_neighbor_track() = 0;

        virtual long get_name() const;

        // virtual VertexNeighborIterator<Vertex>* __iter__() = 0;
        // virtual VertexNeighborIterator<Vertex>* get_neighbors() = 0;
};


class BaseVertex : public Vertex
{
    public:
        std::unordered_set<long> neighbors;
        BaseVertexNeighborIterator* nt;

        BaseVertex() {};
        BaseVertex(long name_);

        void add_neighbor(Vertex& other);

        long get_next_neighbor() override;
        void reset_neighbor_track() override;

        BaseVertexNeighborIterator* __iter__();
        BaseVertexNeighborIterator* get_neighbors();
};


class ColoringVertex : public Vertex
{
    public:
        int colors;
        ColoringGraph* graph;
        ColoringVertexNeighborIterator* nt;

        ColoringVertex(long name_, int k, ColoringGraph* graph_);

        long get_next_neighbor() override;
        void reset_neighbor_track() override;

        ColoringVertexNeighborIterator* __iter__();
        ColoringVertexNeighborIterator* get_neighbors();
};

#endif
