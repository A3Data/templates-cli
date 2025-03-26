{
  description = "Flake for building the color-schemes repository with selected modules";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      lib = pkgs.lib;

      batch = import ./templates/batch/default.nix { inherit pkgs lib; };

    in
    {
      packages.${system} = {
        default = batch (import ./variables.nix);
        batch = batch;
      };
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          (writeShellScriptBin "build-batch" ''
            nix build .\#packages.x86_64-linux.default
          '')

        ];
        shellHook = ''
          echo "DevShell ready. Run 'build-batch' to build the repository."
        '';
      };
    };
}
