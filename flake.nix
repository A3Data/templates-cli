{
  description = "Flake for building the color-schemes repository with selected modules";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      lib = pkgs.lib;

      template1 = import ./templates/color-schemes/default.nix { inherit pkgs lib; };

    in
    {
      packages.${system} = {
        default = template1 (import ./variables.nix);
        template1 = template1;
      };
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          (pkgs.writeShellScriptBin "build-template1" ''
            nix build .\#packages.x86_64-linux.default
          '')
        ];
        shellHook = ''
          echo "DevShell ready. Run 'build-template1' to build the repository."
        '';
      };
    };
}
