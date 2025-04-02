{ pkgs, lib, inputs }:
args:
let
  finalArgs = args // {
    projectName = args.projectName or "Buora";
    description = args.description or "afd";
    version = args.version or "1.0";
    options = args.options or {
      include = {
        functions = [ "agent1" "fn_authorizeers" "fn_conversation_db" ];
        frontend = true;
      };
    };
  };
  inherit (finalArgs) projectName description version options;

  buora = inputs.buora;
  buora_infra = inputs.buora_infra;
in pkgs.stdenv.mkDerivation {
  pname = projectName;
  version = "1.0";
  # src = inputs.buora;
  patches = [ ];

  phases = [
    # "unpackPhase" 
    "patchPhase"
    "installPhase"
  ];

  # installPhase = ''
  #   mkdir -p $out
  #   cp -r . $out/
  # '';
  installPhase = ''
    mkdir -p $out

    # Copy buora files
    cp -r ${buora}/* $out/

    # Copy buora_infra files to a subdirectory
    mkdir -p $out/infra
    cp -r ${buora_infra}/* $out/infra/

    # Optional: Apply the README substitution that was in your commented code
    substituteInPlace $out/README.md --replace-fail \
      "# Documentação CICD" \
      "# ${projectName}"
  '';
}
