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

      testing = "batch";
    in
    {
      packages.${system} = {
        default = (f testing) (import ./templates/${testing}/variables.nix);
        batch = f "batch";
        poc = f "proof-of-concept";
      };
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          (writeShellScriptBin "build-batch" ''
            nix build .\#packages.x86_64-linux.default
          '')
            (writeShellScriptBin "cli" ''
# Check if an argument was provided
if [ $# -lt 1 ]; then
  echo "Usage: $0 'json_args'"
  echo "Example: $0 '{\"projectName\":\"My Project\",\"description\":\"Project description\",\"version\":\"1.0\"}'"
  exit 1
fi

# Use the first argument as the args
nix-build --expr "
  with import <nixpkgs> {};
  let
    template = builtins.getFlake \"github:andre-brandao/demo/a3\";
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
          echo "DevShell ready. Run 'build-batch' to build the repository."
        '';
      };
    };
}
