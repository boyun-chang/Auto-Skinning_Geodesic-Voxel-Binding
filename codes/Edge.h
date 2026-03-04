#pragma once

#include "GridMesh.h"

class Grid;
class Edge
{
public:
	Grid *_from;
	Grid *_to;
	double _weight;
public:
	Edge(void) {}
	Edge(Grid *g0, Grid *g1, double weight = 1.0f)
	{
		_from = g0;
		_to = g1;
		_weight = weight;
	}
	~Edge(void) {}
public:
	Grid* Neighbor(Grid *grid);
	bool Has(Grid *grid);
};

