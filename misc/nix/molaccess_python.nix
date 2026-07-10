{
  lib,
  python314Packages,
  callPackage,
  molaccess_core,
}:
let
  import_patch = ''
  sys.path.append(
      '"${molaccess_core}/lib"'
  )

  import molaccesspy
  '';
in
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

  postPatch = ''
      substituteInPlace apps/molmessg/cli.py \
          --replace "import molaccesspy" "${import_patch}"
      substituteInPlace apps/molaccessd/cli.py \
          --replace "import molaccesspy" "${import_patch}"
  '';
}
