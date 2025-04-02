{ pkgs, lib, inputs }:
config:
pkgs.stdenv.mkDerivation {
  pname = config.projectName;
  version = config.version or "1.0";
  # src = pkgs.fetchFromGitHub {
  #   owner = "A3DAndre";
  #   repo = "templates";
  #   rev = "main";
  #   sha256 = "sha256-QIA0p7KshOO+cHrQzXyZY+1M33D6XRDkP7NCKp5PY4M=";
  # };
  src = inputs.batch;
  patches = [ ];
  postPatch = ''
    substituteInPlace README.md --replace-fail \
      "Template Deploy Batch" \
      "${config.projectName}"

    substituteInPlace README.md --replace-fail \
      "Este repositório apresenta um pipeline de Machine Learning completo utilizando o dataset Iris. Ele cobre as etapas de download de dados, pré-processamento, treinamento de modelos e predição. Nesse repositório também estão implementadas as melhores práticas e diversas outras features." \
      "${config.description}"
  '';
  phases = [ "unpackPhase" "patchPhase" "installPhase" ];

  installPhase = ''
    mkdir -p $out
    cp -r . $out/
  '';
}
