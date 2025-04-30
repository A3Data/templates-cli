{ pkgs ? import <nixpkgs> {} }:

let

name = "cli3";

python = pkgs.python3.withPackages (pypkgs: [
    pypkgs.pandas
    pypkgs.requests
    pypkgs.pyaml
  ]);
  cliPkgs = [
    pkgs.gum
    pkgs.bat
    python
    # pkgs.nix
  ];
in
pkgs.stdenv.mkDerivation {
  name = name;
  src = ./.; # Assuming script is in same directory

  buildInputs = cliPkgs;
  nativeBuildInputs = [ pkgs.makeWrapper ];

  installPhase = ''
      mkdir -p $out/bin
      mkdir -p $out/lib/${name}

      # Copy the Python script and make it executable
      cp cli.py $out/lib/${name}/cli.py
      chmod +x $out/lib/${name}/cli.py

      # Copy the utils directory with Python modules
      cp -r utils $out/lib/${name}/

      # Create launcher script with proper Python path
      makeWrapper $out/lib/${name}/cli.py $out/bin/${name} \
        --prefix PYTHONPATH : $out/lib \
        --set PATH ${pkgs.lib.makeBinPath cliPkgs}
  '';
}
