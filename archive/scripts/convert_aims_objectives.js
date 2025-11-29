const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require('docx');
const fs = require('fs');

// Read the markdown file
const mdContent = fs.readFileSync('02_aims_objectives_reduced.md', 'utf8');
const lines = mdContent.split('\n');

const children = [];
let inList = false;

lines.forEach(line => {
  // Skip character count line
  if (line.includes('Character count:')) return;
  if (line === '---') return;

  if (line.startsWith('# ')) {
    children.push(new Paragraph({
      heading: HeadingLevel.TITLE,
      children: [new TextRun(line.substring(2))]
    }));
  } else if (line.startsWith('## ')) {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_1,
      children: [new TextRun(line.substring(3))]
    }));
  } else if (line.startsWith('### ')) {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_2,
      children: [new TextRun(line.substring(4))]
    }));
  } else if (line.includes('**') && line.includes(':')) {
    // Handle bold text
    const parts = line.split('**');
    const textRuns = [];
    parts.forEach((part, index) => {
      if (index % 2 === 1) {
        textRuns.push(new TextRun({ text: part, bold: true }));
      } else if (part) {
        textRuns.push(new TextRun(part));
      }
    });
    children.push(new Paragraph({ children: textRuns }));
  } else if (line.trim() !== '') {
    children.push(new Paragraph({ children: [new TextRun(line)] }));
  } else {
    children.push(new Paragraph({ children: [new TextRun('')] }));
  }
});

const doc = new Document({
  sections: [{
    properties: {},
    children: children
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('02_aims_objectives_reduced.docx', buffer);
  console.log('Document 2 (Aims & Objectives) saved: 02_aims_objectives_reduced.docx');
});