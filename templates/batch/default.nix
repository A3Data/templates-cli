{
  pkgs,
  lib,
  inputs,
}:
args:
let
  finalArgs = (import ./variables.nix) // args; # get default parameters and override with args
  inherit (finalArgs)
    name
    description
    version
    options
    ; # extract parameters
  inherit (inputs) batch; # extract inputs
in
pkgs.stdenv.mkDerivation {
  pname = name;
  version = version;
  src = batch;
  patches = [ ];
  postPatch = ''
    substituteInPlace README.md --replace-fail \
      "Template Deploy Batch" \
      "${name}"

    substituteInPlace README.md --replace-fail \
      "Este repositório apresenta um pipeline de Machine Learning completo utilizando o dataset Iris. Ele cobre as etapas de download de dados, pré-processamento, treinamento de modelos e predição. Nesse repositório também estão implementadas as melhores práticas e diversas outras features." \
      "${description}"
  '';
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
