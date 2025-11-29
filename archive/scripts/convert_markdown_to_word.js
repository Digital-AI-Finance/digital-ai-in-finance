const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require('docx');
const fs = require('fs');

function convertMarkdownToWord(inputFile, outputFile) {
  const mdContent = fs.readFileSync(inputFile, 'utf8');
  const lines = mdContent.split('\n');

  const children = [];

  lines.forEach(line => {
    // Skip character count and separator lines
    if (line.includes('Character count:') || line === '---') return;

    // Handle title (# )
    if (line.startsWith('# ')) {
      children.push(new Paragraph({
        heading: HeadingLevel.TITLE,
        children: [new TextRun(line.substring(2))]
      }));
      return;
    }

    // Handle empty lines
    if (line.trim() === '') {
      children.push(new Paragraph({ children: [new TextRun('')] }));
      return;
    }

    // Handle lines with bold formatting (**text**)
    const textRuns = [];
    let remainingText = line;
    let isBold = false;

    while (remainingText.length > 0) {
      const boldIndex = remainingText.indexOf('**');

      if (boldIndex === -1) {
        // No more bold markers, add remaining text
        if (remainingText) {
          textRuns.push(new TextRun({ text: remainingText, bold: isBold }));
        }
        break;
      } else if (boldIndex === 0) {
        // Bold marker at the start
        isBold = !isBold;
        remainingText = remainingText.substring(2);
      } else {
        // Text before bold marker
        textRuns.push(new TextRun({ text: remainingText.substring(0, boldIndex), bold: isBold }));
        remainingText = remainingText.substring(boldIndex);
      }
    }

    children.push(new Paragraph({ children: textRuns.length > 0 ? textRuns : [new TextRun(line)] }));
  });

  const doc = new Document({
    sections: [{
      properties: {
        page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
      },
      children: children
    }]
  });

  Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(outputFile, buffer);
    console.log(`Document saved: ${outputFile}`);
  });
}

// Convert all 5 documents
const files = [
  ['01_project_overview_reduced.md', '01_project_overview_reduced.docx'],
  ['02_aims_objectives_reduced.md', '02_aims_objectives_reduced.docx'],
  ['03_format_organization_reduced.md', '03_format_organization_reduced.docx'],
  ['04_partnership_roles_reduced.md', '04_partnership_roles_reduced.docx'],
  ['05_timeline_feasibility_reduced.md', '05_timeline_feasibility_reduced.docx']
];

files.forEach(([input, output]) => {
  convertMarkdownToWord(input, output);
});

console.log('\nAll 5 documents converted to Word format with bold formatting preserved!');