#ifndef __VERTEX_CPP__
#define __VERTEX_CPP__

#include <string>
#include <sstream>
#include "Vertex.h"


/*******************************************************************************
***************************** VERTEX *******************************************
*******************************************************************************/


Vertex::
Vertex(long name_)
    : name(name_) //, nt(new VertexNeighborIterator<Vertex>())
{}

Vertex::
~Vertex()
{}


bool
Vertex::
operator==(const Vertex& other)
{
    return name == other.get_name();
}


long
Vertex::
get_name() const
{
    return name;
}


/*******************************************************************************
****************************** BASEVERTEX **************************************
*******************************************************************************/

BaseVertex::
BaseVertex(long name_)
    : Vertex(name_), nt(new BaseVertexNeighborIterator())
{}


void
BaseVertex::
add_neighbor(Vertex& other)
{
    neighbors.insert(other.get_name());
    delete nt;
    nt = new BaseVertexNeighborIterator(neighbors.begin(),
                                        (long)neighbors.size());
}

long
BaseVertex::
get_next_neighbor()
{
    return nt->next();
}

void
BaseVertex::
reset_neighbor_track()
{
    delete nt;
    nt = new BaseVertexNeighborIterator(neighbors.begin(),
                                        (long)neighbors.size());
}


BaseVertexNeighborIterator*
BaseVertex::
get_neighbors()
{
    return this->__iter__();
}


BaseVertexNeighborIterator*
BaseVertex::
__iter__()
{
    return new BaseVertexNeighborIterator(neighbors.begin(),
                                          (long)neighbors.size());
}


/*******************************************************************************
***************************** ColoringVertex ***********************************
*******************************************************************************/


ColoringVertex::
ColoringVertex(long name_, int k, ColoringGraph* graph_)
    : Vertex(name_), colors(k), graph(graph_)
{
    nt = new ColoringVertexNeighborIterator(name_, k, graph_);
}


long
ColoringVertex::
get_next_neighbor()
{
    return nt->next();
}


void
ColoringVertex::
reset_neighbor_track()
{
    delete nt;
    nt = new ColoringVertexNeighborIterator(name, colors, graph);
}


ColoringVertexNeighborIterator*
ColoringVertex::
get_neighbors()
{
    return __iter__();
}


ColoringVertexNeighborIterator*
ColoringVertex::
__iter__()
{
    return new ColoringVertexNeighborIterator(name, colors, graph);
}


/*******************************************************************************
***************************** VertexNeighborIterator ***************************
*******************************************************************************/

template <typename V>
long
VertexNeighborIterator<V>::
__next__()
{
    return next();
}


template <typename V>
VertexNeighborIterator<V>*
VertexNeighborIterator<V>::
__iter__()
{
    return this;
}


/*******************************************************************************
*************************** BaseVertexNeighborIterator *************************
*******************************************************************************/


BaseVertexNeighborIterator::
BaseVertexNeighborIterator(std::unordered_set<long>::iterator it_, long len_)
    : it(it_), len(len_)
{}


long
BaseVertexNeighborIterator::
next()
{
    if (this->len--)
        return *this->it++;

    throw std::out_of_range("");
}


bool
BaseVertexNeighborIterator::
hasnext()
{
    return (this->len > 0);
}


/*******************************************************************************
********************** ColoringVertexNeighborIterator **************************
*******************************************************************************/


ColoringVertexNeighborIterator::
ColoringVertexNeighborIterator(long name_, int k, ColoringGraph* graph_)
    : name(name_), colors(k), graph(graph_)
{
    positionctr = 0;
    colorctr = 0;
    // remaining = graph->base->size() * colors;
}


long
ColoringVertexNeighborIterator::
next()
{
    for (; positionctr < graph->base->size(); positionctr++)
    {
        long newcoloring;
        int curcol;
        std::unordered_map<long, ColoringVertex*>::iterator it;
        long divisor = graph->precompexp[positionctr][1];

        // std::cerr << "name: " << name
        //           << " divisor: " << divisor
        //           << std:: endl;

        for (; colorctr < colors; colorctr++)
        {
            curcol = (name / divisor) % colors;
            if (curcol == colorctr)
                continue;

            newcoloring = name;
            // std::cerr << std::endl << "start newcoloring with name " << newcoloring
            //           << std::endl;
            newcoloring -= graph->precompexp[positionctr][curcol];
            // std::cerr << "remove current color " << newcoloring
            //           << std::endl;
            newcoloring += graph->precompexp[positionctr][colorctr];
            // std::cerr << "add colorctr color to it " << newcoloring
            //           << std::endl;

            // std::cerr << "Potential neighbor of " << name
            //           << ": " << newcoloring << " when posn=" << positionctr
            //           << " and colctr=" << colorctr << std::endl;

            it = graph->vertices.find(newcoloring); // valid coloring?

            // std::cerr << "trying to see if iterator found anything" << std::endl;
            if (it == graph->vertices.end())
                continue;

            // std::cerr << "Confirmed neighbor of " << name << ": "
            //           << newcoloring << std::endl;

            colorctr++;
            return newcoloring;
        }

        colorctr = 0;
    }

    positionctr = 0;
    colorctr = 0;
    throw std::out_of_range("");
}


bool
ColoringVertexNeighborIterator::
hasnext()
{
    int p = positionctr, c = colorctr;
    // long rem = remaining;

    try
    {
        next();
        positionctr = p;
        colorctr = c;
        // remaining = rem;
        return true;// and remaining;
    }
    catch (std::out_of_range& e)
    {
        return false;
    }
}



#endif
