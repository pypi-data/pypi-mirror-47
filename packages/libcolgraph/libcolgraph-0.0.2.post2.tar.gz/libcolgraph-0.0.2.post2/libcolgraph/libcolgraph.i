/* example.i */
%module libcolgraph

%include "exception.i"

%{
    #include <Python.h>
    #include <assert.h>
    #include <stdexcept>
    #include <iostream>

    #include "GraphTemplates.h"
    #include "Graph.h"
    #include "Vertex.h"
%}


%exception GraphVertexIterator::__next__
{
    try
    {
        $action
    }
    catch(std::out_of_range& e)
    {
        PyErr_SetString(PyExc_StopIteration, "end of iterator reached");
        SWIG_fail;
    }
}
%exception VertexNeighborIterator::__next__
{
    try
    {
        $action
    }
    catch(std::out_of_range& e)
    {
        PyErr_SetString(PyExc_StopIteration, "end of iterator reached");
        SWIG_fail;
    }
}
%exception Vertex::get_next_neighbor
{
    try
    {
        $action
    }
    catch(std::out_of_range& e)
    {
        PyErr_SetString(PyExc_StopIteration, "end of iterator reached");
        SWIG_fail;
    }
}
%exception Graph::get_vertex
{
    try
    {
        $action
    }
    catch(std::out_of_range& e)
    {
        PyErr_SetString(PyExc_KeyError, "queried key not found in lookup");
        SWIG_fail;
    }
}
%exception BaseGraph::load_txt
{
    try
    {
        $action
    }
    catch(std::runtime_error& e)
    {
        PyErr_SetString(PyExc_FileNotFoundError, "unable to load from txt");
        SWIG_fail;
    }
}

%extend Vertex {
    %pythoncode %{
        def __str__(self):
            '''
            '''
            return '<Vertex [{}] of {} >'.format(self.get_name(), type(self))

        def __repr__(self):
            return self.__str__()
    %}
};
%extend Graph {
    %pythoncode %{
        def __str__(self):
            '''
            '''
            return '<Graph (size={}) of {} >'.format(len(self), type(self))

        def __repr__(self):
            return self.__str__()

        def __len__(self):
            '''
            proxy method that just calls this->size()
            '''
            return self.size()
    %}
};

%import "GraphTemplates.h"

%template(GBVIt) GraphVertexIterator<BaseVertex>;
%template(GCVIt) GraphVertexIterator<ColoringVertex>;
%template(GMVIt) GraphVertexIterator<MetaVertex>;
%template(BVNIt) VertexNeighborIterator<BaseVertex>;
%template(CVNIt) VertexNeighborIterator<ColoringVertex>;
%template(MVNIt) VertexNeighborIterator<MetaVertex>;
%template(BGraph) Graph<BaseVertex>;
%template(CGraph) Graph<ColoringVertex>;
%template(MGraph) Graph<MetaVertex>;

%include "GraphTemplates.h"
%include "Graph.h"
%include "Vertex.h"
