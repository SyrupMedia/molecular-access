{
  lib,
  stdenv,
  cmake,
  ninja,
  python3,
  swig,
  libipc,
}:
stdenv.mkDerivation {
  name = "molaccess_core";

  src = ../../.;

  nativeBuildInputs = [
    cmake
    ninja
    swig
  ];

  # to do cross compilation python will need to be here if I understand correctly, since it is being linked against
  buildInputs = [
    libipc
    python3
  ];

  cmakeFlags = [
    "-D MOLACCESS_NATIVE_LIBRARIES=true"
  ];
}
