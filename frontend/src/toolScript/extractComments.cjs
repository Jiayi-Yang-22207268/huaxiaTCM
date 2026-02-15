const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun } = require("docx");

// Only process the src folder
const targetDir = path.resolve(__dirname, "../../src");
const outputPath = path.resolve(__dirname, "output.docx");

// Recursively get all .js files under src
function getAllJSFiles(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach((file) => {
        const fullPath = path.resolve(dir, file);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            results = results.concat(getAllJSFiles(fullPath));
        } else if (file.endsWith(".js")) {
            results.push(fullPath);
        }
    });
    return results;
}

// Extract all /** */ or /* */ block comments
function extractAllBlockComments(content) {
    const blockComments = content.match(/\/\*\*?[\s\S]*?\*\//g) || [];
    return blockComments;
}

function main() {
    const files = getAllJSFiles(targetDir);
    const paragraphs = [];
    files.forEach((filePath) => {
        const content = fs.readFileSync(filePath, "utf8");
        const comments = extractAllBlockComments(content);

        comments.forEach((comment) => {
            // File path (relative to src/)
            const relativePath = path.relative(targetDir, filePath);
            paragraphs.push(new Paragraph({
                children: [new TextRun({
                    text: `File: src/${relativePath}`,
                    bold: true,
                    color: "444444",
                })],
                spacing: { after: 200 },
            }));

            // Comment content
            paragraphs.push(new Paragraph({
                children: [new TextRun(comment)],
                spacing: { after: 400 },
            }));
        });
    });

    if (paragraphs.length === 0) {
        console.log("❗ 未找到任何注释。");
        return;
    }

    const doc = new Document({
        creator: "Comment Extractor",
        title: "JS 文件注释导出",
        description: "从 src 目录下提取的注释文档",
        sections: [{ children: paragraphs }],
    });

    Packer.toBuffer(doc).then((buffer) => {
        fs.writeFileSync(outputPath, buffer);
        console.log(`✅ 注释已成功导出到：${outputPath}`);
    });
}

main();
