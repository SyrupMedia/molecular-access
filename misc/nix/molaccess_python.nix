{
  lib,
  python314Packages,
  callPackage,
  molaccess_core,
}:
with python314Packages;
buildPythonApplication {
  pname = "molaccess-python";
  version = "0.1.0";

  propagatedBuildInputs = [
    tinydb
    molaccess_core
  ];

  pyproject = true;
  build-system = [ setuptools ];

  src = ../../.;
}
