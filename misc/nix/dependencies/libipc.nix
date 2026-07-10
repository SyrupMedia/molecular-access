{
  lib,
  stdenv,
  fetchFromGitHub,
  cmake,
  ninja,
}:
stdenv.mkDerivation {
  name = "cpp-ipc";
  src = fetchFromGitHub {
    owner = "mutouyun";
    repo = "cpp-ipc";
    rev = "a0c7725a1441d18bc768d748a93e512a0fa7ab52";
    sha256 = "sha256-W8tWjc1YRUteYlLKpsl8XUjRCuMKsz9VBiVcexQj9BY=";
  };

  nativeBuildInputs = [
    cmake
    ninja
  ];
}
