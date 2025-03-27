import { $ } from "bun";
import type { Template } from "./types";


const batch: Template = {
    name: "batch",
    description: "Batch template",
    version: "1.0",
    nixName: "andre-brandao/demo/a3",
    questions: [{
        type: "string",
        question: "Qual o nome do projeto?",
        option: "projectName",
        answer: "Demo da daily de titulo pro README"
    },
    {
        type: "string",
        question: "Qual a descrição do projeto?",
        option: "description",
        answer: "Esse é um projeto demo da daily de titulo pro README e outros patches"
    },
    {
        type: "string",
        question: "Qual a versão do projeto?",
        option: "version",
        answer: "1.0"
    }
    ]
} as const

const poc: Template = {
    name: 'poc',
    description: "Proof of concept",
    version: "1.0",
    nixName: "andre-brandao/demo/a3",
    questions: [
        {
            type: "string",
            question: "Qual o nome do projeto?",
            option: "projectName",
            answer: "Demo da daily de titulo pro README"
        },
        {
            type: "string",
            question: "Qual a descrição do projeto?",
            option: "description",
            answer: "Esse é um projeto demo da daily de titulo pro README e outros patches"
        },
        {
            type: "string",
            question: "Qual a versão do projeto?",
            option: "version",
            answer: "1.0"
        },
        {
            type: "bool",
            question: "Você deseja incluir as cores base24",
            option: "deleteBase24",
            answer: true
        }
    ]
} as const

const templates: Template[] = [
    batch,
    poc
]

const batchToNix = (options: {
    projectName: string;
    description: string;
    version: string;
}) => `with import <nixpkgs> {};
let
  template = builtins.getFlake "github:andre-brandao/demo/a3";
    args = {
        projectName = "${options.projectName}";
        description = "${options.description}";
        version = "${options.version}";
        };
    in
    template.packages.x86_64-linux.batch args
`

const pocToNix = (options: {
    projectName: string;
    description: string;
    version: string;
    deleteBase24: boolean;
}) => `with import <nixpkgs> {};
let
    template = builtins.getFlake "github:andre-brandao/demo/a3";
    args = {
        projectName = "${options.projectName}";
        description = "${options.description}";
        version = "${options.version}";
        options = {
            deleteBase24 = ${options.deleteBase24 ? "true" : "false"};
        };
    };
    in
    template.packages.x86_64-linux.poc args
`




const repo = {
    handleCreate: async function (req: Request): Promise<Response> {
        try {
            // Run nix build
            await $`nix-build --expr '
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
            '`.quiet();

            // Zip the result directory
            await $`zip -r result.zip result`.quiet();

            // Return the zip file
            return new Response(Bun.file("result.zip"));
        } catch (err) {
            //   console.log(`Failed with code ${err.exitCode}`);
            //   console.log(err.stdout.toString());
            //   console.log(err.stderr.toString());
            return new Response("Build failed", { status: 500 });
        }
    }
}




const server = Bun.serve({
    routes: {
        "/": () => new Response("Hello World!"),
        "/api/repo": {
            POST: repo.handleCreate
        },
    },
    fetch(req) {
        return new Response("Not Found", { status: 404 });
    },

});

console.log(`Listening on ${server.url}`);