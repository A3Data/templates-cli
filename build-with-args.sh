nix-build --expr '
  with import <nixpkgs> {};
  let
    template = import ./templates/color-schemes/default.nix { inherit pkgs lib; };
    args = {
      projectName = "demo-da-daily2";
      version = "1.0";
      includeModules = {
        deleteBase24 = false;
      };
    };
  in
  template args
'