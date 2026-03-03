%module molaccesspy

%include <std_shared_ptr.i>


%{
/* Includes the header in the wrapper code */

#include "../../include/molaccess.hpp"
#include "./molaccess_python.hpp"
%}

/* Parse the header file to generate wrappers */
%include "../../include/molaccess.hpp"
%include "./molaccess_python.hpp"