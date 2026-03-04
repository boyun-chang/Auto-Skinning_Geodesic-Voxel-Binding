#include <cuda_runtime.h>
#include <cuda.h>
#include "Graph.h"

Graph::~Graph()
{
	if (d_grids) cudaFree(d_grids);
}
/*
Grid* Graph::GetGrid(int index)
{
	return _grids[index];
}

__global__ void computeDistance(GridDevice* gridDevices, int N, int* d_sources)
{
	int srcId = d_sources[blockIdx.x];
	int tid = threadIdx.x;

	if (srcId < N)
	{
		for (int i = 0; i < N; i++)
		{
			auto grid = gridDevices[i]; 
			if (grid._type == GridType::INTERIOR_NODE || grid._type == GridType::BOUNDARAY_NODE)
			{
				grid._distance = (i != srcId) ? numeric_limits<double>::infinity() : 0.0f;
				grid._prev = nullptr;
			}
		}
	}
}

void Graph::copyToDeivice()
{
	cudaMalloc(&d_grids, _gridDevices.size() * sizeof(GridDevice));
	cudaMemcpy(d_grids, _gridDevices.data(), _gridDevices.size() * sizeof(GridDevice), cudaMemcpyHostToDevice);
}

Path* Graph::Find(int source)
{
	copyToDeivice();
}*/
/*
Path* Graph::Find(int source)
{
	priority_queue<pair<double, Grid*>> queue;

	for (int i = 0; i < _grids.size(); i++)
	{
		auto grid = _grids[i];
		if (grid->_type == GridType::INTERIOR_NODE || grid->_type == GridType::BOUNDARAY_NODE)
		{
			grid->_distance = (i != source) ? numeric_limits<double>::infinity() : 0.0f;
			grid->_prev = nullptr;
			queue.push({ grid->_distance, grid });
		}
	}
	
	while (!queue.empty())
	{
		auto pair = queue.top();
		queue.pop();

		Grid *u = pair.second;

		for (auto edge : u->_edges)
		{
			Grid *v = edge->Neighbor(u);
			float alt = u->_distance + edge->_weight;
			if (alt < v->_distance)
			{
				v->_distance = alt;
				v->_prev = u;
				queue.push({ v->_distance, v });
			}
		}
	}

	return new Path(_grids, source, _res);
}*/

Path* Graph::Find(Grid *grid)
{
	auto index = grid->_i * _res * _res + grid->_j * _res + grid->_k;
	return Find(index);
}

vector<Path*> Graph::Permutation(void)
{
	vector<Path*> routes;
	for (int i = 0; i < _grids.size(); i++)
	{
		routes.push_back(Find(i));
	}
	return routes;
}