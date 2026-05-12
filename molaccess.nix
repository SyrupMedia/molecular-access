{ lib, stdenv, fetchgit, fetchFromGitHub, cmake, ninja, python3, swig }:
stdenv.mkDerivation {
  name = "molaccess";

  src = ./.;

  nativeBuildInputs = [ cmake ninja swig ];

  # to do cross compilation python will need to be here if I understand correctly, since it is being linked against
  buildInputs = [ 
    (
      # Build libipc
      stdenv.mkDerivation {
        name = "cpp-ipc";
        src = fetchFromGitHub {
          owner = "mutouyun";
          repo = "cpp-ipc";
          rev = "a0c7725a1441d18bc768d748a93e512a0fa7ab52";
          sha256 = "sha256-W8tWjc1YRUteYlLKpsl8XUjRCuMKsz9VBiVcexQj9BY=";
        };

        nativeBuildInputs = [ cmake ninja ];
      }
    )

    python3   
  ];

  cmakeFlags =  [
    "-D MOLACCESS_NATIVE_LIBRARIES=true"
  ];
}
