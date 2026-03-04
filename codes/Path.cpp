#include "Path.h"

Path::Path(vector<Grid*> grids, int source, int res)
{
	this->_source = source;
	for (int i = 0; i < grids.size(); i++)
	{
		if (i == source)
		{
			_indices.push_back(SOURCE);
		}
		else
		{
			if (grids[i]->_prev != nullptr)
			{
				auto grid = grids[i]->_prev;
				int id = grid->_i * res * res + grid->_j * res + grid->_k;
				_indices.push_back(id);
			}
			else
			{
				_indices.push_back(-1);
			}
		}
	}
}

int Path::Prev(int index)
{
	return _indices[index];
}

bool Path::Traverse(int destination, vector<int>& indices)
{
	while (destination != _source)
	{
		indices.push_back(destination);
		destination = Prev(destination);
		if (destination < 0)
		{
			return false;
		}
	}
	return true;
}

bool Path::Traverse(Graph* graph, int destination, vector<Grid*>& grids)
{
	vector<int> indices;
	bool result = Traverse(destination, indices);
	if (!result)
	{
		return false;
	}
	for (auto index : indices)
	{
		grids.push_back(graph->GetGrid(index));
	}
	grids.push_back(graph->GetGrid(_source));
	return true;
}