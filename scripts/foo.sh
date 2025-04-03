nix build --impure --print-out-paths --expr '
  with import <nixpkgs> {};
  let
    template = builtins.getFlake "github:A3DAndre/demo/a3";
      # template = import ./templates/poc/default.nix { inherit pkgs lib; };
    args = {
        projectName = "Rogerio";
        description =
            "Esse é um projeto demo da daily de titulo pro README e outros patches";
        version = "1.0";
        options = {
            includeDocs = true;
            includeFrontend = true;
            includeTerraform = true;

            includeAgent1 = true;
            includeFnAuthorizers = true;
            includeFnConversationDb = true;
            };
        };

  in
  template.packages.x86_64-linux.buora args
'