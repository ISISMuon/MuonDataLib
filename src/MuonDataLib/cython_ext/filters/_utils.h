
#ifndef _UTILS_H
#define _UTILS_H

#include <vector>
#include <map>
#include <string>

using namespace std;

std::vector<double> remove_from_vector(std::vector <double> vec, int index);

class _MinFilter{
	private:
		vector<double> data;
		double _min;
		bool active;
	public:
		_MinFilter();
		_MinFilter(vector<double> input_data);
		~ _MinFilter();
		bool IsActive();
		void SetValue(double value);
		void Remove();
		vector<double> GetData();
		bool Filter(int k);
};


class _FilterManager{
	private:
		vector<double> times;
		double _min2;
		bool active2;
		_MinFilter min_filter;
	public:
		_FilterManager();
		_FilterManager(vector<double> input_data);
		~ _FilterManager();
		bool IsActive();
		void SetMinFilter(vector<double> input_data, double value);
		void Remove();
		vector<double> GetData();
		vector<double> Filter();
};




#endif
