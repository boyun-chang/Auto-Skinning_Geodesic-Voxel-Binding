#pragma once
#include "GridMesh.h"
#include "Edge.h"
#include "Path.h"
#include <queue>
#include <limits>
#include <iostream>

using namespace std;

class Grid;
class Edge;
class Path;
class Graph
{
public:
	//vector<Grid*> _grids;
	vector<Grid> _grids;
	vector<GridDevice> _gridDevices;
	GridDevice* d_grids = nullptr;
	//vector<Edge*> _edges;
	int _res;
public:
	Graph(void) {}
	/*
	Graph(vector<Grid*> grids, vector<Edge*> edges, int res)
	{
		_grids = grids;
		//_edges = edges;
		_res = res;
	}*/
	Graph(vector<Grid*> grids, int res)
	{
		for (auto g : grids)
		{
			_grids.push_back(*g);
		}

		_res = res;

		int count = 0;
		GridDevice gridDevice;
		for (auto g : _grids)
		{
			g.toDevice(gridDevice);
			_gridDevices.push_back(gridDevice);
			count++;
		}
	}
	~Graph(void);
public:
	Grid* GetGrid(int index);
	Path* Find(int source);
	Path* Find(Grid* grid);
	vector<Path*> Permutation(void);
public:
	void copyToDeivice(void);
};

