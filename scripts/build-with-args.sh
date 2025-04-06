 nix-build --expr '
  with import <nixpkgs> {};
  let
    template = builtins.getFlake "/home/andre/dev/demo";
    args = {
    projectName = "teste";
  description =
    "Demo do template do buora para criar um projeto com a estrutura de pastas e arquivos padrão.";
  version = "1.0";
  options = {
      includeDocs = true;
      includeFrontend = false;
      includeTerraform = false;
      
      includeAgent1 = true;
      includeFnAuthorizers = true;
      includeFnConversationDb = true;
    };
    };
  in
  template.packages.x86_64-linux.buora args
'