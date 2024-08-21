#include "_utils.h"

/*
 * This is a simple method for removing an element from a vector in cython.
 * It is needed as the erase method in cython can only accept iterators.
 *
*/
std::vector<double> remove_from_vector(std::vector <double> vec, int index){
	vec.erase(vec.begin() + index);
	return vec;

}
