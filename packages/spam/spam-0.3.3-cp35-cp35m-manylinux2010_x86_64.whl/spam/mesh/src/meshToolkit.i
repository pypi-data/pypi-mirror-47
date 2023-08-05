/* File: meshToolkit.i */

%module meshToolkit

%{
    #define SWIG_FILE_WITH_INIT
    #include "meshToolkit.hpp"
    #include "connectivityMatrix.hpp"
%}


%include "numpy.i"
%include "std_string.i"
%include "std_vector.i"

%template(VectorDouble)         std::vector<double>;
%template(VectorVectorDouble)   std::vector<std::vector<double> >;
%template(VectorString)         std::vector<std::string>;
%template(VectorUnsigned)       std::vector<unsigned int>;

%init %{
    import_array();
%}


%apply (int DIM1, int DIM2,           float* IN_ARRAY2        ) { ( int numTetrahedrals_numVertices,       int numTetrahedrals_three,            float* numTetrahedrals_vertices         ) };
%apply (int DIM1,                     float* IN_ARRAY1        ) { ( int numTetrahedrals_numWeights,                                              float* numTetrahedrals_weights          ) };

%apply (int DIM1, int DIM2,           float* IN_ARRAY2        ) { ( int connectivityMatrix_numVertices,    int connectivityMatrix_three,         float* connectivityMatrix_vertices      ) };
%apply (int DIM1,                     float* IN_ARRAY1        ) { ( int connectivityMatrix_numWeights,                                           float* connectivityMatrix_weights       ) };
%apply (int DIM1, int DIM2,    unsigned int* INPLACE_ARRAY2   ) { ( int connectivityMatrix_numTet,         int connectivityMatrix_four,  unsigned int * connectivityMatrix_connectivity  ) };

%include "meshToolkit.hpp"
%include "connectivityMatrix.hpp"
