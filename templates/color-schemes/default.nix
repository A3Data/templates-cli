{ pkgs, lib }:
config:
let
  # let
  #   defaultValues = {
  #     projectName = "color-schemes";
  #     version = "1.0";
  #     includeModules = {
  #       deleteBase24 = true;
  #     };
  #   };

  # in

in
pkgs.stdenv.mkDerivation {
  pname = config.projectName;
  version = config.version or "1.0";
  src = pkgs.fetchFromGitHub {
    owner = "andre-brandao";
    repo = "color-schemes";
    rev = "hyprshell";
    sha256 = "sha256-WtroUX4eILFD+2Y5XKF/sNcQQ1KrLrIyLjm5cr6EOEU=";
  };
  patches = [
    (pkgs.writeText "readme-project-name.patch" ''
      From d161e7932c7a2aa44f099ba05498e2cd7ca550b5 Mon Sep 17 00:00:00 2001
      From: andre-brandao <82166576+andre-brandao@users.noreply.github.com>
      Date: Wed, 26 Mar 2025 00:10:12 -0300
      Subject: [PATCH] Update project name in README

      ---
       README.md | 2 +-
       1 file changed, 1 insertion(+), 1 deletion(-)

      diff --git a/README.md b/README.md
      index 818a9e9..a13fc24 100644
      --- a/README.md
      +++ b/README.md
      @@ -1,4 +1,4 @@
      -# tinted-schemes
      +# ${config.projectName}

       Scheme families:
    '')

  ] ++ (if config.includeModules.deleteBase24 then [ ./deleteBase24.patch ] else [ ]);

  installPhase = ''
    mkdir -p $out
    cp -r . $out/
  '';
}
