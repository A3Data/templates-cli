{
  pkgs,
  lib,
  inputs,
}:
args:
let
  finalArgs = (import ./variables.nix) // args;
  inherit (finalArgs)
    projectName
    description
    version
    options
    ;
in
pkgs.stdenv.mkDerivation {
  pname = projectName;
  version = "1.0";
  src = pkgs.fetchFromGitHub {
    owner = "andre-brandao";
    repo = "color-schemes";
    rev = "hyprshell";
    sha256 = "sha256-WtroUX4eILFD+2Y5XKF/sNcQQ1KrLrIyLjm5cr6EOEU=";
  };
  patches =
    [ ]
    ++ (
      if options.deleteBase24 then
        [
          (pkgs.fetchpatch {
            url = "https://patch-diff.githubusercontent.com/raw/andre-brandao/color-schemes/pull/1.patch";
            sha256 = "sha256-FcS10WAy6aUGk5mnfFGaGY5KLWjN7ZDLKrCHYtJlaG4=";
          })
        ]
      else
        [ ]
    );

  postPatch = ''
    substituteInPlace README.md --replace-fail \
      "tinted-schemes" \
      "${projectName}"
  '';
  installPhase = ''
    mkdir -p $out
    cp -r . $out/
  '';
}
