// HTML rendering helpers
export default function renderHtml(title: string, content: string): string {
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <title>${title}</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #333;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }
            .template-list {
                list-style: none;
                padding: 0;
            }
            .template-item {
                background-color: #f9f9f9;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .template-item h2 {
                margin-top: 0;
            }
            .template-item p {
                margin-bottom: 10px;
            }
            .button {
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                text-decoration: none;
                border-radius: 4px;
                border: none;
                cursor: pointer;
            }
            .button:hover {
                background-color: #45a049;
            }
            form {
                background-color: #f9f9f9;
                border-radius: 5px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            input[type="text"], textarea {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            input[type="checkbox"] {
                margin-right: 8px;
            }
            .back-link {
                display: inline-block;
                margin-bottom: 20px;
                text-decoration: none;
                color: #666;
            }
            .back-link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        ${content}
    </body>
    </html>
    `;
}