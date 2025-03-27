{
  description = "Flake for building the color-schemes repository with selected modules";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    batch = {
      url = "github:A3DAndre/templates";
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
        default = (f "poc") ({ });
        batch = f "batch";
        poc = f "poc";

      };
      devShells.${system}.default =
        let
          # templateRepo = "github:andre-brandao/demo/a3";
          templateRepo = "path:${self}";
        in
        pkgs.mkShell {
          buildInputs = with pkgs; [
            (writeShellScriptBin "a3-t" ''
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
              "

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
