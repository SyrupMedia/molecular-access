%module molaccess

%include <std_shared_ptr.i>


%{
/* Includes the header in the wrapper code */

#include "../../include/molaccess.hpp"
%}

/* Parse the header file to generate wrappers */
%include "../../include/molaccess.hpp"