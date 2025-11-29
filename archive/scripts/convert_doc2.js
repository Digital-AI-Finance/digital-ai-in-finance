const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, LevelFormat } = require('docx');
const fs = require('fs');

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullet-list",
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: "•",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
      }]
    }]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 120, after: 120 }, alignment: AlignmentType.CENTER } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal",
        run: { size: 24, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 120, after: 60 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal",
        run: { size: 22, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 60, after: 60 }, outlineLevel: 1 } }
    ]
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Project Aims and Objectives")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Primary Aim")] }),
      new Paragraph({ children: [new TextRun("Establish the Swiss-MENA AI Finance Research Network through a three-day workshop that disseminates research findings, facilitates knowledge exchange, and creates sustainable collaboration frameworks between Switzerland and MENA region stakeholders in artificial intelligence applications for digital finance.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Core Objectives")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("1. Launch Formal Research Network")] }),
      new Paragraph({ children: [new TextRun({ text: "Objective: ", bold: true }), new TextRun("Establish the Swiss-MENA AI Finance Research Network through institutional MoU signing")] }),
      new Paragraph({ children: [new TextRun({ text: "Outputs:", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Signed Memorandum of Understanding from 10+ institutions")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Governance framework and operational structure")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("5-year strategic research roadmap")] }),
      new Paragraph({ children: [new TextRun({ text: "Impact: ", bold: true }), new TextRun("Creates sustainable infrastructure for continuous collaboration beyond single events, enabling researcher mobility, joint supervision, and coordinated funding applications.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2. Disseminate Research and Best Practices")] }),
      new Paragraph({ children: [new TextRun({ text: "Objective: ", bold: true }), new TextRun("Communicate latest AI finance research to 80-100 participants from academia and industry")] }),
      new Paragraph({ children: [new TextRun({ text: "Outputs:", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("15-20 paper presentations across three thematic days")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Workshop proceedings in open-access format")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Online repository of all presentations and resources")] }),
      new Paragraph({ children: [new TextRun({ text: "Impact: ", bold: true }), new TextRun("Advances field knowledge by sharing Swiss precision banking expertise and MENA innovation insights, reaching global audience through hybrid format and open publication.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3. Bridge Academia-Industry Gap")] }),
      new Paragraph({ children: [new TextRun({ text: "Objective: ", bold: true }), new TextRun("Facilitate dialogue between researchers and financial practitioners on AI implementation")] }),
      new Paragraph({ children: [new TextRun({ text: "Outputs:", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Industry case studies from DIFC, Emirates NBD, First Abu Dhabi Bank")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Roundtable discussions on practical challenges")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("White paper with actionable recommendations for industry and regulators")] }),
      new Paragraph({ children: [new TextRun({ text: "Impact: ", bold: true }), new TextRun("Ensures academic research addresses real-world financial sector needs while practitioners gain evidence-based insights for AI adoption strategies.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("4. Build Research Capacity")] }),
      new Paragraph({ children: [new TextRun({ text: "Objective: ", bold: true }), new TextRun("Enhance AI finance research capabilities through training and mentorship")] }),
      new Paragraph({ children: [new TextRun({ text: "Outputs:", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Doctoral training workshop for 20+ early-career researchers")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Mentorship pairings between senior and junior participants")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Best practice guidelines for AI research methodologies")] }),
      new Paragraph({ children: [new TextRun({ text: "Impact: ", bold: true }), new TextRun("Develops next-generation researchers equipped with skills and networks for international collaboration, strengthening research ecosystems in both regions.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("5. Catalyze Future Collaborations")] }),
      new Paragraph({ children: [new TextRun({ text: "Objective: ", bold: true }), new TextRun("Generate concrete partnership opportunities and funding proposals")] }),
      new Paragraph({ children: [new TextRun({ text: "Outputs:", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Formation of 4 thematic working groups")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("3-5 joint research proposals for bilateral funding")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Industry-academia partnership agreements")] }),
      new Paragraph({ children: [new TextRun({ text: "Impact: ", bold: true }), new TextRun("Transforms workshop connections into funded research projects, ensuring long-term return on CCG investment through sustained collaborative activities.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Communication and Dissemination Strategy")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Target Audiences and Tailored Approaches")] }),
      new Paragraph({ children: [new TextRun({ text: "Academic Researchers (60% of participants):", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Peer-reviewed paper presentations")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Methodological workshops")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Proceedings publication")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Research collaboration opportunities")] }),

      new Paragraph({ children: [new TextRun({ text: "Financial Industry Practitioners (40% of participants):", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Executive keynotes on digital transformation")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Implementation case studies")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Practical roundtables")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Networking with research partners")] }),

      new Paragraph({ children: [new TextRun({ text: "Policy Makers and Regulators:", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("White paper on regulatory frameworks")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Panel discussions on AI governance")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Evidence-based policy recommendations")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Direct engagement with FINMA and UAE authorities")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Dissemination Channels")] }),
      new Paragraph({ children: [new TextRun({ text: "Immediate (During Workshop): ", bold: true }), new TextRun("Live presentations to 80-100 on-site participants, hybrid streaming to global audience, real-time social media engagement, press releases to financial media")] }),
      new Paragraph({ children: [new TextRun({ text: "Short-term (1-3 months post): ", bold: true }), new TextRun("Open-access proceedings publication, white paper distribution to stakeholders, workshop report to CCG and partners, follow-up webinars for virtual participants")] }),
      new Paragraph({ children: [new TextRun({ text: "Long-term (3-12 months): ", bold: true }), new TextRun("Journal special issues from workshop papers, policy briefs for government stakeholders, industry implementation reports, network platform for continuous knowledge sharing")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Alignment with CCG Objectives")] }),
      new Paragraph({ children: [new TextRun("This initiative directly addresses CCG's mission to enhance visibility, accessibility, and societal relevance of Swiss-MENA research:")] }),
      new Paragraph({ children: [new TextRun({ text: "Visibility: ", bold: true }), new TextRun("Multiple dissemination channels amplify Swiss research excellence in strategically important MENA markets, positioning Switzerland as partner of choice for AI finance innovation.")] }),
      new Paragraph({ children: [new TextRun({ text: "Accessibility: ", bold: true }), new TextRun("Hybrid format, open publications, and online repository ensure broad access regardless of geographic or financial constraints, democratizing knowledge sharing.")] }),
      new Paragraph({ children: [new TextRun({ text: "Societal Relevance: ", bold: true }), new TextRun("Focus on practical AI applications addresses pressing challenges in financial inclusion, fraud prevention, and regulatory compliance, contributing to economic stability and consumer protection.")] }),
      new Paragraph({ children: [new TextRun({ text: "Sustainability: ", bold: true }), new TextRun("Network establishment creates lasting infrastructure for collaboration, multiplying CCG's investment impact through continuous activities rather than one-time exchange.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Success Metrics")] }),
      new Paragraph({ children: [new TextRun({ text: "Quantitative Indicators:", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("80-100 workshop participants (60% academic, 40% industry)")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("10+ institutions signing network MoU")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("15-20 papers presented and published")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("4 working groups established")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("3-5 funding proposals submitted within 12 months")] }),

      new Paragraph({ children: [new TextRun({ text: "Qualitative Indicators:", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Participant satisfaction (>80% rating excellent/good)")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("New collaborations initiated (tracked via follow-up survey)")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Media coverage and stakeholder engagement")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Policy influence through white paper citations")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Network activity levels post-workshop")] }),

      new Paragraph({ children: [new TextRun("The exceptional 80% co-funding rate (CHF 20,000 from partners vs CHF 5,000 CCG request) demonstrates strong stakeholder commitment to achieving these objectives.")] })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("02_aims_objectives_reduced.docx", buffer);
  console.log("Document 2 saved: 02_aims_objectives_reduced.docx");
});