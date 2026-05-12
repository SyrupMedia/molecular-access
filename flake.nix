{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
  };

  outputs = {nixpkgs, ...}:
  let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
    molaccessPkg = pkgs.callPackage ./molaccess.nix { };
  in {
    # allows building with `nix build`
    packages.x86_64-linux.default = molaccessPkg;

    devShells.x86_64-linux = {
      # dev env, default for `nix develop`
      default = pkgs.mkShell {
        inputsFrom = [ molaccessPkg ];
      };
      # autoformat task (`nix develop .#format`)
      format = pkgs.mkShellNoCC {
        packages = [
          pkgs.black
          pkgs.uncrustify
        ];
        # TODO: look in to whether this is the 'correct'/idiomatic way to do this kind of thing with nix
        shellHook = ''exec ./misc/integration/tasks/format.sh'';
      };
      # lint task (`nix develop .#lint`)
      lint = pkgs.mkShell {
        inputsFrom = [ molaccessPkg ];
        packages = [
          pkgs.clang-tools
          (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
            pylint
          ]))
        ];
        shellHook = ''exec ./misc/integration/tasks/lint.sh'';
      };
      # clang-tidy autofix task (`nix develop .#lintfix`)
      lintfix = pkgs.mkShell {
        # TODO: figure out if theres a way to exclude python
        inputsFrom = [ molaccessPkg ];
        packages = [
          pkgs.clang-tools
        ];
        shellHook = ''exec ./misc/integration/tasks/lintfix.sh'';
      };
      # tests task (`nix develop .#tests`)
      tests = pkgs.mkShell {
        inputsFrom = [ molaccessPkg ];
        shellHook = ''exec ./misc/integration/tasks/tests.sh'';
      };
    };
  };
}
