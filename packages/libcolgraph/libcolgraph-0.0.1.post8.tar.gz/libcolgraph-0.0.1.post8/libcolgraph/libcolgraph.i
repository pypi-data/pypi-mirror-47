/* example.i */
%module libcolgraph

%include "exception.i"

%{
    #include <assert.h>
    #include "Graph.h"
    #include "Vertex.h"
    static int myErr = 0;
%}

%exception Graph::next {
  assert(!myErr);
  $action
  if (myErr) {
    myErr = 0; // clear flag for next time
    PyErr_SetString(PyExc_StopIteration, "End of iterator");
    return NULL;
  }
}

%inline %{
  struct GraphVertexIterator {
    std::map<long, Vertex>::iterator it;
    long len;
  };
%}

%include "Graph.h"
%include "Vertex.h"

%extend GraphVertexIterator {
  struct GraphVertexIterator* __iter__() {
    return $self;
  }

  Vertex __next__() {
    if ($self->len--) {
      return (*$self->it++).second;
    }
    myErr = 1;
    return 0;
  }
}

%extend Graph {
  struct GraphVertexIterator __iter__() {
    struct GraphVertexIterator ret = { $self->vertices.begin(), $self->size() };
    return ret;
  }

}
