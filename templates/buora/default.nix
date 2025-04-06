{ pkgs, lib, inputs }:
args:
let
  finalArgs = (import ./variables.nix) // args; # get default parameters and override with args
  inherit (finalArgs) projectName description version options; # extract parameters
  inherit (inputs) buora buora_infra; # extract inputs
in pkgs.stdenv.mkDerivation {
  pname = projectName;
  version = version;
  
  dontUnpack = true;
  
  buildPhase = ''
    # mkdir -p build

    # cp -r --no-preserve=mode ${buora}/* build/

    mkdir -p build
    
    cp -r --no-preserve=mode ${buora_infra}/* build/
  
    ${lib.optionalString (!options.includeDocs) "rm -rf build/docs"}
    ${lib.optionalString (!options.includeFrontend) "rm -rf build/frontend"}
    ${lib.optionalString (!options.includeTerraform) "rm -rf build/terraform"}
    ${lib.optionalString (!options.includeAgent1) "rm -rf build/functions/agent1"}
    ${lib.optionalString (!options.includeFnAuthorizers) "rm -rf build/functions/fn_authorizers"}
    ${lib.optionalString (!options.includeFnConversationDb) "rm -rf build/functions/fn_conversation_db"}
  '';
  
  installPhase = ''
    # Copy the filtered build directory to output
    mkdir -p $out
    cp -r build/* $out/
    
    substituteInPlace $out/README.md --replace \
      "buora_infra" \
      "${projectName}" || true

  '';
}