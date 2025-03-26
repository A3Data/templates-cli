nix-build --expr '
  with import <nixpkgs> {};
  let
    template = builtins.getFlake "github:andre-brandao/demo/a3";
    args = {
      projectName = "Demo da daily de titulo pro README";
      description = "Esse é um projeto demo da daily de titulo pro README e outros patches";
      version = "1.0";
    };
  in
  template.packages.x86_64-linux.batch args
'