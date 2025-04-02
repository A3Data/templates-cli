import { $ } from "bun";

import type { Template , Question, QuestionBool, QuestionString} from "./types.d.ts";

import * as pages from './pages'

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
} as const;

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
} as const;

const templates: Template[] = [
    batch,
    poc
];

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
`;

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
`;




const repo = {
    handleCreate: async function (req: Request): Promise<Response> {
        try {
            const data = await req.json();
            const { templateName, options } = data;
            
            let nixExpression = '';
            
            // Determine which template to use
            if (templateName === 'batch') {
                nixExpression = batchToNix({
                    projectName: options.projectName || "Default Project",
                    description: options.description || "Default Description",
                    version: options.version || "1.0",
                });
            } else if (templateName === 'poc') {
                nixExpression = pocToNix({
                    projectName: options.projectName || "Default Project",
                    description: options.description || "Default Description",
                    version: options.version || "1.0",
                    deleteBase24: options.deleteBase24 || false,
                });
            } else {
                return new Response("Invalid template name", { status: 400 });
            }
            
            // Write the nix expression to a temporary file
            await Bun.write('temp.nix', nixExpression);
            
            // Run nix build with the generated expression
            await $`nix-build temp.nix`.quiet();
            
            // Zip the result directory
            await $`zip -r result.zip result`.quiet();
            
            // Clean up temporary files
            await $`rm temp.nix`.quiet();
            
            // Return the zip file
            return new Response(Bun.file("result.zip"), {
                headers: {
                    "Content-Type": "application/zip",
                    "Content-Disposition": `attachment; filename="${templateName}-project.zip"`
                }
            });
        } catch (err) {
            console.error("Build failed:", err);
            return new Response("Build failed", { status: 500 });
        }
    }
};

const server = Bun.serve({
    port: 3000,
    hostname: "127.0.0.1",
    fetch(req) {
        const url = new URL(req.url);
        const path = url.pathname;
        
        // Route handling
        if (path === "/") {
            return new Response(pages.renderHomepage(templates), {
                headers: { "Content-Type": "text/html" }
            });
        }
        
        // Handle template page
        if (path.startsWith("/template/")) {
            const templateName = path.split("/").pop();
            const template = templates.find(t => t.name === templateName);
            
            if (!template) {
                return new Response("Template not found", { status: 404 });
            }
            
            return new Response(pages.renderTemplateForm(template), {
                headers: { "Content-Type": "text/html" }
            });
        }
        
        // Handle API routes
        if (path === "/api/repo" && req.method === "POST") {
            return repo.handleCreate(req);
        }
        
        return new Response("Not Found", { status: 404 });
    },
});

console.log(`Server running at ${server.url}`);

// const server = Bun.serve({
//     port: 3000,
//     routes: {
//         "/api/repo": {
//             POST: repo.handleCreate
//         },
//         "/template/:name": (req) => {
//             const name = req.params.name
//             const template = templates.find(t => t.name === name);
//             if (!template) {
//                 return new Response("Template not found", { status: 404 });
//             }
//             return new Response(pages.renderTemplateForm(template), {
//                 headers: { "Content-Type": "text/html" }
//             });
//         }
//     },
//     fetch(req) {
//         console.log(req.url);



//         return new Response(pages.renderHomepage(templates), {
//             headers: { "Content-Type": "text/html" }
//         })
//     },
//     error(error) {
//         return new Response(`<pre>${error}\n${error.stack}</pre>`, {
//             headers: {
//                 "Content-Type": "text/html",
//             },
//         });
//     }
// });