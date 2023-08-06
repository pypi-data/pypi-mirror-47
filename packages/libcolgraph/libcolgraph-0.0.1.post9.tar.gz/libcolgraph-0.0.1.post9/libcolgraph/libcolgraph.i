/* example.i */
%module libcolgraph

%include "exception.i"

%{
    #include <Python.h>
    #include <assert.h>
    #include "GraphTemplates.h"
    #include "Graph.h"
    #include <iostream>
    #include "Vertex.h"
    #include <stdexcept>
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
    %}
};

%include "GraphTemplates.h"

%template(GBVIt) GraphVertexIterator<BaseVertex>;
%template(GCVIt) GraphVertexIterator<ColoringVertex>;
%template(BVNIt) VertexNeighborIterator<BaseVertex>;
%template(CVNIt) VertexNeighborIterator<ColoringVertex>;
%template(BGraph) Graph<BaseVertex>;
%template(CGraph) Graph<ColoringVertex>;

/* %include "GraphTemplates.h" */
%include "Graph.h"
%include "Vertex.h"
