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
        buildInputs = with pkgs;[
          (writeShellScriptBin "build-template1" ''
            nix build .\#packages.x86_64-linux.default
          '')

          (writers.writePython3Bin "pyFib"
            {
              flakeIgnore = [ "E265" "E225" ];
            } /*python */ ''
def fib(n):
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b


print(list(fib(10)))
          '')
          (writers.writePython3Bin /*python */ "pyTest"
            {
              libraries = [ pkgs.python3Packages.pyyaml ];
              flakeIgnore = [ "E265" "E225" ];
            } ''
            import yaml

            y = yaml.load("""
              - test: success
            """)
            print(y[0]['test'])
          '')

        ];
        shellHook = ''
          echo "DevShell ready. Run 'build-template1' to build the repository."
        '';
      };
    };
}
