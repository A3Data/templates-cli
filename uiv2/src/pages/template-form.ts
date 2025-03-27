import type { Template } from "../types";
import renderHtml from "./render";

export function renderTemplateForm(template: Template): string {
    let formFields = '';
    
    template.questions.forEach(question => {
        if (question.type === "string") {
            formFields += `
            <div class="form-group">
                <label for="${question.option}">${question.question}</label>
                <input type="text" id="${question.option}" name="${question.option}" value="${question.answer}" required>
            </div>
            `;
        } else if (question.type === "bool") {
            formFields += `
            <div class="form-group">
                <label>
                    <input type="checkbox" id="${question.option}" name="${question.option}" ${question.answer ? 'checked' : ''}>
                    ${question.question}
                </label>
            </div>
            `;
        }
    });
    
    return renderHtml(`${template.name} Template`, `
        <a href="/" class="back-link">← Back to templates</a>
        <h1>${template.name} Template</h1>
        <p>${template.description}</p>
        
        <form id="templateForm">
            <input type="hidden" name="templateName" value="${template.name}">
            ${formFields}
            <button type="submit" class="button">Generate Project</button>
        </form>
        
        <script>
            document.getElementById('templateForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                const templateName = formData.get('templateName');
                
                // Convert form data to JSON
                const jsonData = {};
                formData.forEach((value, key) => {
                    if (key === 'templateName') return;
                    
                    // Handle checkboxes properly
                    if (document.getElementById(key)?.type === 'checkbox') {
                        jsonData[key] = document.getElementById(key).checked;
                    } else {
                        jsonData[key] = value;
                    }
                });
                
                try {
                    const response = await fetch('/api/repo', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            templateName,
                            options: jsonData
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Failed to generate project');
                    }
                    
                    // Create a blob from the response
                    const blob = await response.blob();
                    
                    // Create a download link and trigger it
                    const downloadUrl = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = downloadUrl;
                    a.download = \`\${templateName}-project.zip\`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    
                    alert('Project generated successfully!');
                } catch (error) {
                    console.error('Error:', error);
                    alert('Failed to generate project. Please try again.');
                }
            });
        </script>
    `);
}