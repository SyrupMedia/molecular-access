{ stdenv, fetchgit, cmake, ninja, python3, swig }:
stdenv.mkDerivation {
  name = "molaccess";

  src = ./.;

  nativeBuildInputs = [ cmake ninja swig ];

  # to do cross compilation python will need to be here if I understand correctly, since it is being linked against
  buildInputs = [ python3 ];
}
