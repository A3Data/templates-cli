nix-build --expr '
  with import <nixpkgs> {};
  let
    template = builtins.getFlake "github:andre-brandao/demo";
    args = {
      projectName = "demo-da-daily2";
      version = "1.0";
      includeModules = {
        deleteBase24 = false;
      };
    };
  in
  template.packages.x86_64-linux.template1 args
'