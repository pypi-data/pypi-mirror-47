
#include <iostream>
#include <cstdlib>
#include "Graph.h"

using namespace std;

int main(int argc, char *argv[])
{
    cout << "before init!" << endl;

    char* testpath = "../test/input/g1.in";

    BaseGraph bg;

    cout << "loading graph from " << testpath << endl;
    bg.load_txt(testpath);

    cout << "graph size: " << bg.size() << endl;

    cout << "building coloring. k=? " << endl;
    int k;
    cin >> k;

    ColoringGraph* cg = bg.build_coloring_graph(k);

    cout << "coloring graph size: " << cg->size() << endl;

    cout << "reached EOF tester" << endl;

    return 0;
}
