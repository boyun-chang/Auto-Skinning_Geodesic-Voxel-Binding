#pragma once
#include "GridMesh.h"
#include "Edge.h"
#include "Graph.h"

class Grid;
class Graph;
class Path
{
public:
	static const int SOURCE = -1;
	vector<int> _indices;
	int _source;
public:
	Path(void) {}
	Path(vector<Grid*> grids, int source, int res);
	~Path(void) {}
public:
	int Prev(int index);
	bool Traverse(int destination, vector<int>& indices);
	bool Traverse(Graph* graph, int destination, vector<Grid*>& grids);
};

