#ifndef __GRAPH_H__
#define __GRAPH_H__

#include <map>
#include <cstddef>
// #include <string>
#include <fstream>
#include "Vertex.h"


/*
 *  the OG graph class
 */
class Graph
{
    private:

    protected:
    public:
        std::map<long, Vertex> vertices;

    public:

        Graph();
        ~Graph();

        void load_txt(char* path);

        long size();

        void add_vertex(long name);

        Vertex& get_vertex(long name);

        std::map<long, Vertex>::iterator get_vertices();

};


class BaseGraph : Graph
{
    private:

    protected:

    public:
};


class ColoringGraph
{
    private:
        Graph* base;

    protected:

    public:
};


#endif
