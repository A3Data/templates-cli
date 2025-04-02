# docker.nix
{ pkgs ? import <nixpkgs> {} }:

let
  bunApp = pkgs.stdenv.mkDerivation {
    name = "bun-template-project";
    version = "1.0.0";
    

    src = ./.;
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
  
  copyToRoot = dockerEnv;
  
  config = {
    Cmd = [ "${bunApp}/bin/run-app" ];
    WorkingDir = "${bunApp}/app";
    ExposedPorts = {
      "3000/tcp" = {};
    };
    Volumes = {
      "/nix/store" = {};
      "/nix/var" = {};
    };
  };
}