# docker.nix
{ pkgs ? import <nixpkgs> {} }:

let
  # Create a package for the Bun application
  bunApp = pkgs.stdenv.mkDerivation {
    name = "bun-template-project";
    version = "1.0.0";
    
    # Make sure to replace this with your actual source directory
    src = ./.;
    
    # We need Bun for building and running the app
    buildInputs = [
      pkgs.bun
      pkgs.zip
      pkgs.bash
    ];
    
    # Installation phase
    installPhase = ''
      mkdir -p $out/app
      cp -r $src/* $out/app/
      mkdir -p $out/bin
      
      cat > $out/bin/run-app <<EOF
      #!/bin/sh
      cd $out/app && exec ${pkgs.bun}/bin/bun run ./src/server.ts
      EOF
      
      chmod +x $out/bin/run-app
    '';
  };
  
  # Create a single environment with all required packages
  dockerEnv = pkgs.buildEnv {
    name = "docker-env";
    paths = [
      pkgs.bun
      pkgs.coreutils
      pkgs.bash
      pkgs.zip
      pkgs.nix
      bunApp
    ];
  };

in
pkgs.dockerTools.buildImage {
  name = "bun-template-app";
  tag = "latest";
  
  # Use copyToRoot instead of contents (which is deprecated)
  copyToRoot = dockerEnv;
  
  # Configure working directory and exposed port
  config = {
    Cmd = [ "${bunApp}/bin/run-app" ];
    WorkingDir = "${bunApp}/app";
    ExposedPorts = {
      "3000/tcp" = {};
    };
  };
}