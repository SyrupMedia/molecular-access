{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      packages = forAllSystems (
        system:
        let
          pkgs = (import nixpkgs { inherit system; });
          libipc = pkgs.callPackage ./misc/nix/dependencies/libipc.nix { };
          molaccess_core = pkgs.callPackage ./misc/nix/molaccess_core.nix { inherit libipc; };
          molaccess_python = pkgs.callPackage ./misc/nix/molaccess_python.nix { inherit molaccess_core; };
          molaccess = pkgs.callPackage ./misc/nix/molaccess.nix {
            inherit molaccess_python;
            inherit molaccess_core;
          };
        in
        {
          inherit molaccess_core;
          inherit molaccess_python;
          default = molaccess;
          devShell = pkgs.mkShell {
            inputsFrom = [
              molaccess_core
              molaccess_python
            ];
          };
          # Used inside of container images
          container = pkgs.mkShell {
            inputsFrom = [
              molaccess_core
              molaccess_python
            ];
            packages = [
              molaccess_core
              molaccess_python
            ];
            shellHook = "exec ./misc/integration/tasks/nix_container.sh";
          };
          # autoformat task (`nix develop .#format`)
          format = pkgs.mkShellNoCC {
            packages = [
              pkgs.black
              pkgs.uncrustify
            ];
            # TODO: look in to whether this is the 'correct'/idiomatic way to do this kind of thing with nix
            shellHook = "exec ./misc/integration/tasks/format.sh";
          };
          # lint task (`nix develop .#lint`)
          lint = pkgs.mkShell {
            inputsFrom = [
              molaccess_core
              molaccess_python
            ];
            packages = [
              pkgs.clang-tools
              (pkgs.python3.withPackages (
                python-pkgs: with python-pkgs; [
                  pylint
                ]
              ))
            ];
            shellHook = "exec ./misc/integration/tasks/lint.sh";
          };
          # clang-tidy autofix task (`nix develop .#lintfix`)
          lintfix = pkgs.mkShell {
            # TODO: figure out if theres a way to exclude python
            inputsFrom = [
              molaccess_core
              molaccess_python
            ];
            packages = [
              pkgs.clang-tools
            ];
            shellHook = "exec ./misc/integration/tasks/lintfix.sh";
          };
          # tests task (`nix develop .#tests`)
          tests = pkgs.mkShell {
            inputsFrom = [
              molaccess_core
              molaccess_python
            ];
            shellHook = "exec ./misc/integration/tasks/tests.sh";
          };
        }
      );
    };
}
