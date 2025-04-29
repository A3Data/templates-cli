{
  description = "Flake for building the color-schemes repository with selected modules";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    batch = {
      url = "github:A3DAndre/templates";
      flake = false;
    };

    buora = {
      url = "git+ssh://git@github.com/A3Data/buora-oficial.git?ref=main";
      flake = false;
    };

    buora_infra = {
      url = "git+ssh://git@github.com/A3Data/buora_infra.git?ref=refact/clear-buora-lambda";
      flake = false;
    };

  };

  outputs =
    { self, nixpkgs, ... }@inputs:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      lib = pkgs.lib;
      f = name: import ./templates/${name}/default.nix { inherit pkgs lib inputs; };
      v = name: import ./templates/${name}/variables.nix;
    in
    {
      packages.${system} = {
        default = (f "buora") (v "buora");
        batch = f "batch";
        poc = f "poc";
        buora = f "buora";
        tBuora = (import ./templates/buora/default.nix { inherit pkgs lib inputs; }) (v "buora");

        web = import ./uiv2 { inherit pkgs; };

      };
      devShells.${system}.default =
        let
          templateRepo = "github:andre-brandao/demo/a3";
        in
        # templateRepo = "path:${self}";
        pkgs.mkShell {
          buildInputs =
            with pkgs;
            let
              makePython3JobScriptWithPythonPackages =
                name: packagesSelectionFun: text:
                let
                  shellEscape =
                    (import <nixpkgs/nixos/modules/system/boot/systemd-lib.nix> (
                      with pkgs; { inherit config pkgs lib; }
                    )).shellEscape;
                  mkScriptName = s: (builtins.replaceStrings [ "\\" ] [ "-" ] (shellEscape s));
                  x = pkgs.writeTextFile {
                    name = "unit-script.py";
                    executable = true;
                    destination = "/bin/${mkScriptName name}";
                    text = "#!/usr/bin/env python3\n${text}";
                  };
                  deriv = pkgs.stdenv.mkDerivation {
                    name = mkScriptName name;
                    buildInputs = [
                      (pkgs.python36.withPackages (pythonPackages: packagesSelectionFun pythonPackages))
                    ];
                    unpackPhase = "true";
                    installPhase = ''
                      mkdir -p $out/bin
                      cp ${x}/bin/${mkScriptName name} $out/bin/${mkScriptName name}
                    '';
                  };
                in
                "${deriv}/bin/${mkScriptName name}";
            in
            [
              gum
              (python3.withPackages (python-pkgs: [
                python-pkgs.pandas
                python-pkgs.requests
                python-pkgs.pyaml
              ]))
              (writeShellScriptBin "feml2" ''
                # Check if an argument was provided
                if [ $# -lt 1 ]; then
                  echo "Usage: a3-t <template-name> '<nix-args>'"
                  echo "Example: a3-t batch '{\"projectName\":\"My Project\";\"description\":\"Project description\";\"version\":\"1.0\";}'"
                  exit 1
                fi

                # Use the first argument as the selected function, second as args
                nix-build --expr "
                  with import <nixpkgs> {};
                  let
                    template = builtins.getFlake \"${templateRepo}\";
                    args = $2;
                  in
                  template.packages.x86_64-linux.$1 args
                " --extra-experimental-features flakes --extra-experimental-features nix-command

                # Check if the build was successful
                if [ -e result ]; then
                  # Copy the content of result to the current directory
                  mkdir -p $1
                  cp -r result/* ./$1

                  # Delete the result symlink
                  rm result

                  echo "Build successful. Files copied to current directory."
                else
                  echo "Build failed."
                  exit 1
                fi
              '')

            ];
          shellHook = ''
            echo "DevShell ready. Run 'feml' to build the repository."
          '';
        };
    };
}
