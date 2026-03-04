#include "Edge.h"

Grid* Edge::Neighbor(Grid *grid)
{
	if (_from == grid) return _to;
	return _from;
}
bool Edge::Has(Grid* grid)
{
	return (_from == grid) || (_to == grid);
}