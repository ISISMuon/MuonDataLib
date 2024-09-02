#include "_utils.h"
#include <iostream>
/*
 * This is a simple method for removing an element from a vector in cython.
 * It is needed as the erase method in cython can only accept iterators.
 *
*/
std::vector<double> remove_from_vector(std::vector <double> vec, int index){
	vec.erase(vec.begin() + index);
	return vec;

}

_MinFilter::_MinFilter() {
}

_MinFilter::_MinFilter(vector<double> input_data){
	data = input_data;
	active = false;
	_min = 0.0;
}

_MinFilter::~_MinFilter() {}

bool _MinFilter::IsActive(){
	return active;
}
void _MinFilter::SetValue(double value){
	_min = value;
	active = true;
}

void _MinFilter::Remove(){
	active = false;
}

bool _MinFilter::Filter(int k){
	//cout<<data[k][0]<<endl;
	double val = data[k];
	if(val >= _min){
		return true;}
	return false;
}

std::vector<double> _MinFilter::GetData(){
	vector<double> a;
	return a;//data;
}

_FilterManager::_FilterManager() {
}

_FilterManager::_FilterManager(vector<double> input_data){
	times = input_data;
	active2 = false;
	_min2 = 0.0;
}

_FilterManager::~_FilterManager() {}

bool _FilterManager::IsActive(){
	return min_filter.IsActive();
}
void _FilterManager::SetMinFilter(vector<double> input_data, double value){
	min_filter = _MinFilter(input_data);
	min_filter.SetValue(value);
}

void _FilterManager::Remove(){
	min_filter.Remove();
}

vector<double> _FilterManager::Filter(){
 	vector<double> result;
	for(auto k=0; k < times.size(); k++){
		if (min_filter.Filter(k)){
			result.push_back(times[k]);
		}
	}
	return result;
}


std::vector<double> _FilterManager::GetData(){
	return times;
}



//_FilterManager::
