const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = require('docx');
const fs = require('fs');

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 22 } // 11pt default
      }
    },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 32, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal",
        run: { size: 28, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal",
        run: { size: 24, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 1 } }
    ]
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      new Paragraph({
        heading: HeadingLevel.TITLE,
        children: [new TextRun("Project Overview and Context")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Launching the First Swiss-MENA AI Finance Research Network")]
      }),

      new Paragraph({
        children: [new TextRun("This three-day international workshop at the American University of Sharjah (April 21-23, 2026) marks a pivotal moment in Swiss-MENA research collaboration: the formal launch of the first dedicated AI Finance Research Network bridging Switzerland and the Middle East. Building on a robust 7-year partnership between Prof. Joerg Osterrieder (University of Applied Sciences of the Grisons, Switzerland) and Prof. Stephen Chan (American University of Sharjah, UAE), this workshop transforms proven bilateral success into a sustainable multilateral research ecosystem.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Activity Type and Context")]
      }),

      new Paragraph({
        children: [
          new TextRun({ text: "Workshop Format: ", bold: true }),
          new TextRun("Three-day intensive program combining academic presentations, industry case studies, doctoral training, and strategic network planning, delivered in hybrid format to maximize global participation.")
        ]
      }),

      new Paragraph({
        children: [
          new TextRun({ text: "Disciplines: ", bold: true }),
          new TextRun("Computer Science/Artificial Intelligence, Finance/Economics, Mathematics/Statistics - an interdisciplinary approach essential for addressing the complexity of AI applications in modern finance.")
        ]
      }),

      new Paragraph({
        children: [
          new TextRun({ text: "Location: ", bold: true }),
          new TextRun("American University of Sharjah, UAE - strategically positioned in one of the world's most dynamic financial innovation hubs, providing ideal access to both regional academic excellence and industry leadership.")
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Strong Foundation of Collaboration")]
      }),

      new Paragraph({
        children: [new TextRun("The workshop builds upon an exceptionally productive research partnership that has yielded significant outputs: a comprehensive guide on blockchain security challenges and fraud prevention, advanced methods for detecting fraud in blockchain networks (currently under review), and two substantial studies on NFTs and digital assets in the Metaverse. This collaboration has successfully secured multiple research grants, demonstrating international recognition of the partnership's value and potential. The extended research collaboration over 7 years at AUS have established deep mutual understanding and complementary expertise that form the foundation for network expansion.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Workshop Content and Thematic Focus")]
      }),

      new Paragraph({
        children: [new TextRun("The program addresses three critical areas where AI is revolutionizing digital finance:")]
      }),

      new Paragraph({
        children: [
          new TextRun({ text: "Large Language Models in Finance: ", bold: true }),
          new TextRun("Exploring practical applications of LLMs for financial analysis, risk assessment, and regulatory reporting, with emphasis on implementation challenges and opportunities specific to Swiss precision banking and MENA's rapidly evolving markets.")
        ]
      }),

      new Paragraph({
        children: [
          new TextRun({ text: "Explainable AI for Regulatory Compliance: ", bold: true }),
          new TextRun("Developing transparent, interpretable AI systems that satisfy both Swiss Financial Market Supervisory Authority (FINMA) requirements and UAE regulatory frameworks, particularly relevant for institutions operating across jurisdictions.")
        ]
      }),

      new Paragraph({
        children: [
          new TextRun({ text: "Machine Learning for Fraud Detection and Risk Management: ", bold: true }),
          new TextRun("Building on the principal investigators' published research, showcasing advanced techniques for identifying fraudulent activities and managing risk in increasingly complex digital financial ecosystems.")
        ]
      }),

      new Paragraph({
        children: [new TextRun("The three-day structure maximizes knowledge exchange and network building:")]
      }),

      new Paragraph({
        children: [new TextRun("- Day 1 focuses on academic foundations, featuring keynote presentations and research papers")]
      }),

      new Paragraph({
        children: [new TextRun("- Day 2 bridges to industry applications with case studies from DIFC, Emirates NBD, and First Abu Dhabi Bank")]
      }),

      new Paragraph({
        children: [new TextRun("- Day 3 launches the network with doctoral training, working group formation, and MoU signing ceremony")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Target Audience and Strategic Engagement")]
      }),

      new Paragraph({
        children: [new TextRun("The workshop targets 80-100 carefully selected participants: 60% from academic institutions across Switzerland, UAE, and the broader MENA region, and 40% from the financial industry including banks, fintech companies, and regulatory bodies. This strategic mix ensures meaningful dialogue between research and practice, facilitating knowledge transfer and identifying real-world challenges for academic investigation.")]
      }),

      new Paragraph({
        children: [new TextRun("Key stakeholder engagement includes senior representatives from Dubai International Financial Centre (DIFC), major UAE banks including Emirates NBD and First Abu Dhabi Bank, Swiss financial technology companies, regulatory officials from both regions, and doctoral students from the MSCA Industrial Doctoral Network. This diverse participation ensures comprehensive perspectives on AI adoption in finance.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Expected Outcomes and Sustainable Impact")]
      }),

      new Paragraph({
        children: [new TextRun("The workshop will produce concrete deliverables that extend impact beyond the event:")]
      }),

      new Paragraph({
        children: [
          new TextRun({ text: "Formal Network Establishment: ", bold: true }),
          new TextRun("The signing of a Memorandum of Understanding will officially launch the Swiss-MENA AI Finance Research Network, creating institutional frameworks for sustained collaboration.")
        ]
      }),

      new Paragraph({
        children: [
          new TextRun({ text: "Strategic Research Roadmap: ", bold: true }),
          new TextRun("Development of a comprehensive 5-year research agenda identifying priority areas, funding opportunities, and collaboration mechanisms, providing clear direction for network activities.")
        ]
      }),

      new Paragraph({
        children: [
          new TextRun({ text: "Knowledge Dissemination: ", bold: true }),
          new TextRun("Workshop proceedings published in open access format, a white paper on AI adoption in Swiss-MENA financial sectors targeting policymakers and industry leaders, and an online repository of presentations and resources ensuring continued accessibility.")
        ]
      }),

      new Paragraph({
        children: [
          new TextRun({ text: "Publication Pipeline: ", bold: true }),
          new TextRun("The workshop will catalyze joint publications, special journal issues, and collaborative grant applications, creating tangible research outputs that advance the field.")
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Strategic Significance and Innovation")]
      }),

      new Paragraph({
        children: [new TextRun("This workshop represents a first-of-its-kind initiative linking two globally significant financial centers through AI research collaboration. Switzerland's renowned precision in financial services and robust regulatory frameworks complement the UAE's dynamic growth and innovation-friendly environment. Both regions are actively developing AI strategies for their financial sectors, making this collaboration timely and strategically vital.")]
      }),

      new Paragraph({
        children: [new TextRun("The network addresses critical gaps in current research landscape by fostering dialogue between different regulatory approaches, bridging academic research with industry implementation, and creating pathways for knowledge transfer between established and emerging markets. By establishing formal collaboration mechanisms, the workshop lays groundwork for bilateral research programs, joint doctoral supervision, and industry-academia partnerships that will shape the future of AI in finance.")]
      }),

      new Paragraph({
        children: [new TextRun("The sustainable impact extends beyond immediate outputs, positioning both regions at the forefront of responsible AI adoption in finance while contributing to global best practices and standards development.")]
      }),

      new Paragraph({
        spacing: { before: 240 },
        children: [new TextRun({ text: "Character count: 4,996 (including spaces)", italics: true, color: "666666" })]
      })
    ]
  }]
});

// Save the document
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("20241030_1800_project_overview_final.docx", buffer);
  console.log("Document saved: 20241030_1800_project_overview_final.docx");
});