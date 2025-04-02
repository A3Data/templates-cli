{ pkgs, lib, inputs }:
args:
let
  finalArgs = args // {
    projectName = args.projectName or "Demo da daily de titulo pro README";
    description = args.description or "Esse é um projeto demo da daily de titulo pro README e outros patches";
    version = args.version or "1.0";
    options = args.options or {
      deleteBase24 = false;
    };
  };
  inherit (finalArgs) projectName description version options;
in
pkgs.stdenv.mkDerivation {
  pname = projectName;
  version = "1.0";
  src = pkgs.fetchFromGitHub {
    owner = "A3Data";
    repo = "buora-oficial";
    rev = "main";
    sha256 = "sha256-WtroUX4eILFD+2Y5XKF/sNcQQ1KrLrIyLjm5cr6EOEU=";
  };
  patches =
    [    ];

  # postPatch = ''
  #   substituteInPlace README.md --replace-fail \
  #     "# Documentação CICD" \
  #     "# ${projectName}"
  # '';

  phases = [
    "unpackPhase"
    "patchPhase"
    "installPhase"
  ];

  installPhase = ''
    mkdir -p $out
    cp -r . $out/
  '';
}
