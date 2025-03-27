import type { Template } from "../types";
import renderHtml from "./render";
export function renderHomepage(templates:Template[]): string {
    let templatesHtml = '';
    
    templates.forEach(template => {
        templatesHtml += `
        <li class="template-item">
            <h2>${template.name}</h2>
            <p><strong>Description:</strong> ${template.description}</p>
            <p><strong>Version:</strong> ${template.version}</p>
            <a href="/template/${template.name}" class="button">Use Template</a>
        </li>
        `;
    });
    
    return renderHtml("Template Selection", `
        <h1>Available Templates</h1>
        <ul class="template-list">
            ${templatesHtml}
        </ul>
    `);
}
