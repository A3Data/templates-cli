{ pkgs, lib, inputs }:
args:
let
  finalArgs = args // {
    projectName = args.projectName or "Buora";
    description = args.description or "afd";
    version = args.version or "1.0";
    options = args.options or {
      includeDocs = false;
      includeFrontend = false;
      includeTerraform = false;
      
      includeAgent1 = true;
      includeFnAuthorizers = false;
      includeFnConversationDb = true;
    };
  };
  inherit (finalArgs) projectName description version options;
  buora = inputs.buora;
  buora_infra = inputs.buora_infra;
in pkgs.stdenv.mkDerivation {
  pname = projectName;
  version = version;
  
  # Skip unpacking since we're not using any source
  dontUnpack = true;
  
  buildPhase = ''
    mkdir -p build

    cp -r --no-preserve=mode ${buora}/* build/

    mkdir -p build/infra
    
    cp -r --no-preserve=mode ${buora_infra}/* build/infra/
  
    ${lib.optionalString (!options.includeDocs) "rm -rf build/infra/docs"}
    ${lib.optionalString (!options.includeFrontend) "rm -rf build/infra/frontend"}
    ${lib.optionalString (!options.includeTerraform) "rm -rf build/infra/terraform"}
    
    ${lib.optionalString (!options.includeAgent1) "rm -rf build/infra/functions/agent1"}
    ${lib.optionalString (!options.includeFnAuthorizers) "rm -rf build/infra/functions/fn_authorizers"}
    ${lib.optionalString (!options.includeFnConversationDb) "rm -rf build/infra/functions/fn_conversation_db"}
  '';
  
  installPhase = ''
    # Copy the filtered build directory to output
    mkdir -p $out
    cp -r build/* $out/
    
    substituteInPlace $out/README.md --replace \
      "# Documentação CICD" \
      "# ${projectName}" || true

  '';
}