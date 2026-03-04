#ifndef __MESH_H__
#define __MESH_H__

#pragma once
#include "Face.h"
#include "GridMesh.h"
#include "Skeleton.h"
#include <algorithm>

using namespace std;

class Mesh
{
public:
	vector<Face*>	_faces;
	vector<Vertex*>	_vertices;
	GridMesh		*_gridMesh;
	Skeleton		*_skeleton;
	double			_boundDistance;
	const char		*_hierarchyFile, *_transformFile, *_outputCsvFile;
	int				_res;
public:
	Mesh();
	Mesh(int res, const char *objFile, const char *hierarchyFile, const char *transformFile, const char *outputCsvFile)
	{
		_res = res;
		_hierarchyFile = hierarchyFile;
		_transformFile = transformFile;
		_outputCsvFile = outputCsvFile;
		loadObj(objFile);
		//clampWeight();
	}
	~Mesh();
public:
	Vec3<float>	SCALAR_TO_COLOR(float scalar);
	//void	clampWeight(void);
public:
	void	loadObj(const char *file);
	void	buildList(void);
	void	computeNormal(void);
	void	moveToCenter(Vec3<double> minBound, Vec3<double> maxBound, double scale);
public:
	void	drawVoxel(void);
	void	drawPoint(void);
	void	drawSkeleton(void);
	void	drawSurface(bool smoothing = false);
	void	drawWeight(void);
};

#endif