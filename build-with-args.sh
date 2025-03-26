nix-build --expr '
  with import <nixpkgs> {};
  let
    template = import ./templates/batch/default.nix { inherit pkgs lib; };
    args = {
      projectName = "Demo da daily de titulo pro README";
      description = "Esse é um projeto demo da daily de titulo pro README e outros patches";
      version = "1.0";
    };
  in
  template args
'