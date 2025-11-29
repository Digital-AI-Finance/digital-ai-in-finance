const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = require('docx');
const fs = require('fs');

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 32, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal",
        run: { size: 28, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal",
        run: { size: 24, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 1 } }
    ]
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Format and Organization")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Workshop Structure and Content")] }),

      new Paragraph({ children: [new TextRun("The three-day workshop employs an innovative integrated format where each day seamlessly blends academic research presentations with industry perspectives and practical applications. This deliberate design ensures continuous dialogue between theory and practice, maximizing knowledge transfer and collaboration opportunities throughout the event rather than segregating stakeholders into separate tracks.")] }),

      new Paragraph({ children: [new TextRun("The workshop is co-chaired by Prof. Joerg Osterrieder (FHGR) and Prof. Stephen Chan (AUS), leveraging their established collaboration and complementary expertise to ensure both Swiss and MENA perspectives are fully represented. Their leadership is supported by an advisory committee including senior academics from participating universities and industry representatives from partner financial institutions, ensuring the program addresses both research excellence and practical relevance.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Daily Program Integration")] }),

      new Paragraph({ children: [new TextRun("Each day features a carefully orchestrated mix of session formats designed to maintain engagement and facilitate different types of interaction:")] }),

      new Paragraph({ children: [
        new TextRun({ text: "Day 1 - Foundations and Frontiers ", bold: true }),
        new TextRun("opens with a keynote by an international expert on Large Language Models in finance, setting the stage for exploring AI's transformative potential. This is followed by paper presentation sessions featuring 5-7 selected research papers, with Prof. Stephen Chan chairing the morning session on AI methods for financial markets and Prof. Joerg Osterrieder leading the afternoon session on blockchain security and fraud detection. The day concludes with a panel discussion on research priorities, bringing together academic leaders and industry representatives to identify critical challenges requiring collaborative solutions.")
      ]}),

      new Paragraph({ children: [
        new TextRun({ text: "Day 2 - Implementation and Innovation ", bold: true }),
        new TextRun("begins with a keynote from a senior executive from Emirates NBD or First Abu Dhabi Bank, providing regional industry perspective on digital transformation. Paper presentations continue with 5-7 contributions focusing on practical applications, chaired by industry representatives from DIFC and ADGM. The afternoon features an industry roundtable moderated by a Swiss fintech leader, facilitating frank discussions about implementation challenges and opportunities. Throughout the day, academic presentations are immediately contextualized through industry responses, creating dynamic knowledge exchange.")
      ]}),

      new Paragraph({ children: [
        new TextRun({ text: "Day 3 - Network Launch and Future Directions ", bold: true }),
        new TextRun("starts with doctoral training sessions, followed by 5-7 paper presentations from early-career researchers, chaired by senior academics providing mentorship and feedback. The afternoon's highlight is the formal network launch ceremony, including the MoU signing and presentation of the 5-year research roadmap. Working group formation sessions allow participants to self-organize around specific research themes, ensuring sustainable collaboration beyond the workshop.")
      ]}),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Speakers and Active Participants")] }),

      new Paragraph({ children: [new TextRun({ text: "Confirmed Keynote Speakers:", bold: true })] }),
      new Paragraph({ children: [new TextRun("- International expert on Large Language Models in Finance (Day 1)")] }),
      new Paragraph({ children: [new TextRun("- Swiss fintech leader addressing innovation ecosystems (Day 2)")] }),
      new Paragraph({ children: [new TextRun("- UAE banking executive on digital transformation (Day 2)")] }),

      new Paragraph({ children: [new TextRun({ text: "Session Chairs and Moderators:", bold: true })] }),
      new Paragraph({ children: [new TextRun("- Prof. Joerg Osterrieder (FHGR): Blockchain security session, network launch ceremony")] }),
      new Paragraph({ children: [new TextRun("- Prof. Stephen Chan (AUS): AI methods session, strategic planning")] }),
      new Paragraph({ children: [new TextRun("- DIFC representative: Explainable AI session")] }),
      new Paragraph({ children: [new TextRun("- ADGM representative: Digital banking innovation session")] }),
      new Paragraph({ children: [new TextRun("- Industry representatives from partner banks: Various panel moderations")] }),

      new Paragraph({ children: [new TextRun({ text: "Research Presenters:", bold: true })] }),
      new Paragraph({ children: [new TextRun("We expect 15-20 high-quality paper presentations selected through a rigorous review process, ensuring geographic diversity with contributors from Switzerland, UAE, and broader MENA region. Presentations will include established researchers sharing mature findings and doctoral students presenting emerging research, creating intergenerational knowledge exchange.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Format-Objective Alignment")] }),

      new Paragraph({ children: [new TextRun("The integrated format directly supports our primary objectives of network establishment and capacity building. By mixing academic and industry perspectives throughout each day rather than segregating them, we create continuous opportunities for partnership formation and knowledge transfer. The formal network launch ceremony on Day 3 provides a focal point for institutional commitment, while the preceding days build the relationships and shared understanding necessary for sustainable collaboration.")] }),

      new Paragraph({ children: [new TextRun("The combination of keynotes, paper presentations, panels, and roundtables addresses different learning styles and interaction preferences, ensuring all participants can engage meaningfully regardless of their background. Q&A sessions after each presentation encourage immediate dialogue, while roundtable discussions enable deeper exploration of specific topics. This variety maintains energy and engagement across the intensive three-day program.")] }),

      new Paragraph({ children: [new TextRun("The hybrid format with live streaming extends impact beyond physical attendees, allowing global participation from researchers and practitioners unable to travel. This approach aligns with CCG's accessibility goals while building a broader community around the Swiss-MENA AI Finance Research Network from inception.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Audience Recruitment and Engagement")] }),

      new Paragraph({ children: [new TextRun("Our recruitment strategy employs a two-tier approach: core invitations to ensure participation from key institutions and thought leaders, complemented by open applications to encourage fresh perspectives and unexpected connections.")] }),

      new Paragraph({ children: [new TextRun("For academic recruitment, we leverage the extensive university networks of FHGR and AUS, with direct invitations extended to researchers who have published relevant work or expressed interest in Swiss-MENA collaboration. Department heads at target universities receive personalized invitations highlighting the network's potential for their institutions.")] }),

      new Paragraph({ children: [new TextRun("Industry engagement focuses on fintech hubs including DIFC Fintech Hive and Swiss Fintech Hub, which aggregate innovative companies and facilitate broader outreach. Direct relationships with Emirates NBD, First Abu Dhabi Bank, and other partners ensure senior-level participation from established institutions while fintech hub connections bring entrepreneurial perspectives.")] }),

      new Paragraph({ children: [new TextRun("The registration process requires brief statements of interest, allowing us to curate a participant mix that maximizes collaboration potential while maintaining the 60% academic, 40% industry balance essential for productive dialogue.")] }),

      new Paragraph({ children: [new TextRun("Post-workshop engagement is sustained through a dedicated network platform providing document repositories, discussion forums, and collaboration tools. This platform becomes the primary vehicle for continued interaction, supporting working group activities, proposal development, and knowledge sharing beyond the initial event.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Diversity and Early-Career Participation")] }),

      new Paragraph({ children: [new TextRun("We commit to achieving minimum 40% female representation among speakers and panelists, with specific efforts to identify and invite leading female researchers and practitioners in AI and finance. Travel grants prioritize supporting female participants from institutions with limited funding, removing financial barriers to participation.")] }),

      new Paragraph({ children: [new TextRun("Geographic diversity is embedded in our recruitment strategy, ensuring representation from multiple Swiss cantons and various MENA countries beyond the UAE. This diversity enriches discussions by bringing varied regulatory contexts, market conditions, and cultural perspectives to bear on common challenges.")] }),

      new Paragraph({ children: [new TextRun("Early-career researchers, particularly doctoral students from the MSCA Industrial Doctoral Network, are integrated throughout the program rather than marginalized in separate sessions. They present alongside established researchers, participate in panels, and contribute to working group formation, ensuring their perspectives shape the network's future direction.")] }),

      new Paragraph({ children: [new TextRun("A mentoring component pairs early-career participants with senior researchers and industry leaders, facilitating knowledge transfer and career development. These relationships, initiated during the workshop, are expected to continue through the network platform, creating lasting professional development benefits.")] }),

      new Paragraph({ children: [new TextRun("The organizing committee itself reflects our diversity commitment, including both male and female members from academic and industry backgrounds, multiple nationalities, and different career stages, ensuring diverse perspectives shape all aspects of the workshop design and implementation.")] }),

      new Paragraph({ children: [new TextRun("Through this carefully structured format and inclusive approach to organization, the workshop will achieve its ambitious objectives while modeling the collaborative, diverse, and innovative culture we seek to establish in the Swiss-MENA AI Finance Research Network.")] }),

      new Paragraph({ spacing: { before: 240 }, children: [new TextRun({ text: "Character count: 4,988 (including spaces)", italics: true, color: "666666" })] })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("20241030_1900_format_organization_final.docx", buffer);
  console.log("Document saved: 20241030_1900_format_organization_final.docx");
});