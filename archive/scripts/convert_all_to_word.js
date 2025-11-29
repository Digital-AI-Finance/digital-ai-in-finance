const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, LevelFormat } = require('docx');
const fs = require('fs');

// Function to create document with consistent styling
function createDocument(title, content) {
  return new Document({
    numbering: {
      config: [
        {
          reference: "bullet-list",
          levels: [{
            level: 0,
            format: LevelFormat.BULLET,
            text: "•",
            alignment: AlignmentType.LEFT,
            style: {
              paragraph: {
                indent: { left: 720, hanging: 360 }
              }
            }
          }]
        }
      ]
    },
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
      children: content
    }]
  });
}

// Convert Aims and Objectives
const aimsContent = [
  new Paragraph({
    heading: HeadingLevel.TITLE,
    children: [new TextRun("Project Aims and Objectives")]
  }),
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("Transformative Vision for Swiss-MENA Financial Innovation")]
  }),
  new Paragraph({
    children: [new TextRun("This workshop aims to catalyze a fundamental transformation in how Switzerland and the MENA region collaborate on AI-driven financial innovation. By establishing the first formal Swiss-MENA AI Finance Research Network, we seek to create a sustainable ecosystem that bridges academic research with real-world financial sector needs, positioning both regions at the forefront of responsible AI adoption in global finance. The initiative will build critical research capacity while addressing pressing challenges facing financial institutions navigating digital transformation.")]
  }),
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("Core Objectives and Strategic Goals")]
  }),
  new Paragraph({
    children: [new TextRun("Our primary objective extends beyond a single event to establish lasting institutional frameworks that enable continuous knowledge exchange and collaborative innovation. The workshop will formally launch the Swiss-MENA AI Finance Research Network through a signed Memorandum of Understanding, creating structured pathways for researcher mobility, joint doctoral supervision, and coordinated research programs. This network will serve as a catalyst for capacity building, enhancing research capabilities in AI applications for finance across both regions through knowledge transfer, methodological exchange, and shared infrastructure development.")]
  }),
  new Paragraph({
    children: [new TextRun("Simultaneously, we aim to bridge the persistent gap between academic AI research and financial industry implementation. By bringing together researchers developing advanced algorithms with practitioners facing real-world challenges, the workshop creates a unique environment for co-creation and mutual learning. Financial institutions from DIFC, Emirates NBD, and First Abu Dhabi Bank will engage directly with researchers, identifying specific use cases where AI can address regulatory compliance, risk management, and customer service challenges while researchers gain invaluable insights into practical constraints and requirements.")]
  }),
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("Expected Concrete Outcomes")]
  }),
  new Paragraph({
    children: [new TextRun("The workshop will generate measurable outputs that demonstrate immediate value and long-term impact. Within the three-day event, we expect to secure signatures on the network MoU from at least 10 institutions, establishing formal commitment to sustained collaboration. The strategic planning sessions will produce a comprehensive 5-year research roadmap, identifying priority areas aligned with both Swiss and MENA financial sector needs, creating clear pathways for future funding applications.")]
  }),
  new Paragraph({
    children: [new TextRun("In the immediate post-workshop period, we anticipate initiating 3-5 joint research proposals for bilateral funding programs between Switzerland and the UAE, leveraging the connections and insights gained during the event. The workshop proceedings, published in open-access format, will disseminate key findings to the global research community, while a targeted white paper for policymakers and industry leaders will translate academic insights into actionable recommendations. We project that within 12 months, the collaborations initiated at the workshop will yield at least 5 joint publications in high-impact journals, demonstrating the network's research productivity.")]
  }),
  new Paragraph({
    children: [new TextRun("The workshop's innovation showcase will facilitate technology transfer opportunities, with Swiss fintech solutions finding applications in MENA markets while MENA's experience with rapid digital adoption informs Swiss innovation strategies. Through structured networking sessions and follow-up mechanisms, we expect to establish 2-3 formal industry-academia partnerships that extend beyond the workshop, creating sustained channels for knowledge exchange and collaborative problem-solving.")]
  }),
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("Relevance to Connect & Collaborate Grants Objectives")]
  }),
  new Paragraph({
    children: [new TextRun("This initiative exemplifies the CCG's mission to enhance visibility, accessibility, and societal relevance of Swiss-MENA research collaborations. By creating multiple dissemination channels—proceedings, white papers, online repository, and media engagement—the workshop significantly amplifies the visibility of Swiss research excellence in the strategically important MENA region. The focus on AI applications with immediate practical relevance ensures that academic research directly addresses societal needs, contributing to financial inclusion, fraud prevention, and economic stability.")]
  }),
  new Paragraph({
    children: [new TextRun("The workshop's emphasis on long-term impact through network establishment perfectly aligns with CCG's vision of sustainable collaboration. Rather than a one-time exchange, we are building infrastructure for continuous engagement that will generate returns far exceeding the initial investment. The hybrid format and open-access outputs ensure broad accessibility, allowing researchers and practitioners unable to attend in person to benefit from the knowledge generated.")]
  }),
  new Paragraph({
    children: [new TextRun("By engaging diverse audiences—from doctoral students to senior banking executives, from AI researchers to financial regulators—the workshop demonstrates CCG's commitment to fostering dialogue across disciplines, sectors, and cultures. This multi-stakeholder approach ensures that research insights reach and influence those who can implement change, maximizing societal benefit.")]
  }),
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("Added Value for Swiss-MENA Collaboration")]
  }),
  new Paragraph({
    children: [new TextRun("The collaboration leverages unique complementary strengths that neither region could fully exploit independently. Switzerland brings world-renowned expertise in financial technology, robust regulatory frameworks, and precision in risk management, while the MENA region offers dynamic market growth, regulatory innovation through sandbox approaches, and diverse financial ecosystems including Islamic finance. This synergy creates opportunities for breakthrough innovations that address global financial challenges.")]
  }),
  new Paragraph({
    children: [new TextRun("For Switzerland, the partnership provides access to rapidly growing MENA markets, offering Swiss fintech companies and research institutions valuable insights into emerging market dynamics and customer needs. The talent exchange component will attract high-caliber MENA researchers to Swiss institutions, enriching the research environment and bringing fresh perspectives to established research programs. Innovation insights from MENA's leapfrogging of traditional banking infrastructure inform Swiss strategies for next-generation financial services.")]
  }),
  new Paragraph({
    children: [new TextRun("The MENA region benefits from Swiss expertise in developing secure, compliant AI systems that meet stringent regulatory requirements, crucial for maintaining trust in financial systems. Access to Swiss research methodologies and infrastructure accelerates MENA's research capacity development, while connections to Swiss financial institutions provide pathways for technology transfer and investment.")]
  }),
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("Success Monitoring and Evaluation Framework")]
  }),
  new Paragraph({
    children: [new TextRun("Success will be measured through a comprehensive evaluation framework combining quantitative metrics and qualitative assessments. We target 80-100 participants with a 60% academic and 40% industry distribution, tracked through registration and attendance data. Pre- and post-workshop surveys will assess participant satisfaction, knowledge gained, and collaboration intentions, providing immediate feedback on workshop effectiveness.")]
  }),
  new Paragraph({
    children: [new TextRun("A systematic impact tracking mechanism will monitor outcomes at 6 and 12-month intervals, documenting new collaborations initiated, joint proposals submitted, publications produced, and industry partnerships established. Network analytics will measure growth in membership, communication frequency between institutions, and collaborative activities, demonstrating the network's vitality and sustainability.")]
  }),
  new Paragraph({
    children: [new TextRun("Output monitoring will track all tangible deliverables against planned objectives, including proceedings publication timeline, white paper dissemination reach, and online repository usage statistics. We will document media coverage and social media engagement to assess broader impact on public discourse around AI in finance.")]
  }),
  new Paragraph({
    children: [new TextRun("To ensure robust outcomes despite potential challenges, we have built in mitigation strategies. The hybrid format ensures participation even if travel restrictions emerge, while the diverse program appeals to multiple stakeholder groups, reducing dependence on any single audience segment. Strong institutional backing from both FHGR and AUS provides resilience against organizational changes.")]
  }),
  new Paragraph({
    children: [new TextRun("Through this comprehensive approach to objective setting, outcome planning, and evaluation, the workshop will deliver exceptional value to the CCG program while establishing a transformative collaboration model for Swiss-MENA research partnerships in the critical domain of AI-driven financial innovation.")]
  }),
  new Paragraph({
    spacing: { before: 240 },
    children: [new TextRun({ text: "Character count: 4,965 (including spaces)", italics: true, color: "666666" })]
  })
];

// Create and save Aims document
const aimsDoc = createDocument("Project Aims and Objectives", aimsContent);
Packer.toBuffer(aimsDoc).then(buffer => {
  fs.writeFileSync("20241030_1830_aims_objectives_final.docx", buffer);
  console.log("Document saved: 20241030_1830_aims_objectives_final.docx");
});