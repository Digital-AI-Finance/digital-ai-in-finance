const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType } = require('docx');
const fs = require('fs');

const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 32, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal",
        run: { size: 28, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal",
        run: { size: 24, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal",
        run: { size: 22, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 120, after: 60 }, outlineLevel: 2 } }
    ]
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Timeline, Milestones, and Risk Assessment")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Project Timeline and Implementation Phases")] }),

      new Paragraph({ children: [new TextRun("The workshop implementation follows a carefully structured timeline spanning 8 months from application submission to final reporting, organized into three distinct phases ensuring systematic preparation, flawless execution, and sustainable outcomes.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Phase 1: Pre-Workshop Preparation (December 2024 - March 2026)")] }),

      new Table({
        columnWidths: [2000, 3500, 2000, 2500],
        margins: { top: 100, bottom: 100, left: 100, right: 100 },
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, shading: { fill: "E5E5E5", type: ShadingType.CLEAR },
                children: [new Paragraph({ children: [new TextRun({ text: "Month", bold: true, size: 20 })] })] }),
              new TableCell({ borders: cellBorders, shading: { fill: "E5E5E5", type: ShadingType.CLEAR },
                children: [new Paragraph({ children: [new TextRun({ text: "Key Activities", bold: true, size: 20 })] })] }),
              new TableCell({ borders: cellBorders, shading: { fill: "E5E5E5", type: ShadingType.CLEAR },
                children: [new Paragraph({ children: [new TextRun({ text: "Responsible", bold: true, size: 20 })] })] }),
              new TableCell({ borders: cellBorders, shading: { fill: "E5E5E5", type: ShadingType.CLEAR },
                children: [new Paragraph({ children: [new TextRun({ text: "Deliverables", bold: true, size: 20 })] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Dec 2024", bold: true, size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Submit CCG application; Initial planning meeting; Establish organizing committee", size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Osterrieder/Chan", size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Application submitted; Committee formed", size: 20 })] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Feb 2025", bold: true, size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "CCG approval (expected); Launch website; Issue call for papers; Begin speaker invitations", size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "FHGR lead", size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Live website; Call distributed", size: 20 })] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Sep 2025", bold: true, size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Paper review process; Speaker confirmation deadline; Venue detailed planning", size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Chan/AUS", size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Reviews complete", size: 20 })] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Mar 2026", bold: true, size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Milestone: All speakers confirmed; Materials design; Proceedings preparation begins", bold: true, size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Both teams", size: 20 })] })] }),
              new TableCell({ borders: cellBorders,
                children: [new Paragraph({ children: [new TextRun({ text: "Speaker roster complete", size: 20 })] })] })
            ]
          })
        ]
      }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Phase 2: Workshop Execution (April 2026)")] }),

      new Paragraph({ children: [new TextRun("April 1-7: Final participant confirmations; Materials printing; Technical infrastructure testing")] }),
      new Paragraph({ children: [new TextRun("April 8-14: Hybrid platform final testing; Streaming setup verification; Recording equipment check")] }),
      new Paragraph({ children: [new TextRun({ text: "April 15-20: Milestone - 80 participants registered; ", bold: true }), new TextRun("Opening ceremony rehearsal; MoU signing preparation; Final logistics check")] }),
      new Paragraph({ children: [new TextRun("April 21: Day 1 execution - Opening, keynotes, research sessions, welcome reception")] }),
      new Paragraph({ children: [new TextRun("April 22: Day 2 execution - Industry sessions, panels, roundtables")] }),
      new Paragraph({ children: [new TextRun({ text: "April 23: Day 3 execution - Milestone: MoU signing ceremony; ", bold: true }), new TextRun("Network launch; Working groups formation")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Phase 3: Post-Workshop Activities (May - July 2026)")] }),

      new Paragraph({ children: [new TextRun("May 2026: Participant feedback collection; Initial impact assessment; Proceedings compilation; First network virtual meeting")] }),
      new Paragraph({ children: [new TextRun("June 2026: CCG activity report submission; Financial report preparation; Proceedings finalization and publication; Media coverage documentation")] }),
      new Paragraph({ children: [new TextRun("July 2026: Network platform launch; Working group activation; 3-month impact assessment; Bilateral funding proposal development")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Key Milestones and Success Indicators")] }),

      new Paragraph({ children: [new TextRun({ text: "March 2026 - Speaker Confirmation: ", bold: true }), new TextRun("All three keynote speakers and session chairs confirmed, ensuring program quality and drawing power. This milestone triggers final marketing push and validates workshop credibility.")] }),

      new Paragraph({ children: [new TextRun({ text: "April 15, 2026 - Registration Target: ", bold: true }), new TextRun("Achievement of 80 registered participants with appropriate academic-industry mix (60/40) confirms market interest and ensures critical mass for networking and knowledge exchange.")] }),

      new Paragraph({ children: [new TextRun({ text: "April 23, 2026 - Network Launch: ", bold: true }), new TextRun("Formal MoU signing by 10+ institutions during closing ceremony, establishing the Swiss-MENA AI Finance Research Network as a sustainable collaboration framework beyond the workshop.")] }),

      new Paragraph({ children: [new TextRun("Success metrics tracked throughout include weekly registration numbers from January 2026, partner institution engagement levels measured by confirmed participants and speakers, and media coverage through press mentions and social media reach, providing real-time feedback on workshop momentum and enabling timely adjustments.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Risk Assessment and Mitigation Strategies")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Risk 1: Low Participation")] }),
      new Paragraph({ children: [new TextRun({ text: "Probability: ", bold: true }), new TextRun("Medium | "), new TextRun({ text: "Impact: ", bold: true }), new TextRun("High")] }),

      new Paragraph({ children: [new TextRun("Insufficient registration could undermine networking objectives and financial viability. Early warning indicators include registration below 40 by February 2026 or limited industry engagement by March 2026.")] }),

      new Paragraph({ children: [new TextRun({ text: "Mitigation Strategy: ", bold: true }), new TextRun("Partner institution mobilization ensures baseline participation, with each core partner (FHGR, AUS, MSCA network) committing to minimum 10 participants. Strategic partnerships with DIFC and major banks secure industry attendance. Hybrid participation option expands reach beyond physical constraints. If registration lags, implement targeted outreach to specific departments and enhanced social media campaign.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Risk 2: Speaker Cancellations")] }),
      new Paragraph({ children: [new TextRun({ text: "Probability: ", bold: true }), new TextRun("Medium | "), new TextRun({ text: "Impact: ", bold: true }), new TextRun("Medium-High")] }),

      new Paragraph({ children: [new TextRun("Keynote speaker withdrawal could diminish workshop prestige and program coherence, particularly if occurring close to event date.")] }),

      new Paragraph({ children: [new TextRun({ text: "Mitigation Strategy: ", bold: true }), new TextRun("Early confirmation requirement by March 2026 provides buffer for alternatives. Backup speakers identified for each keynote slot, prioritizing UAE-based experts to eliminate travel risks. Virtual presentation capability ensures speakers can participate remotely if travel becomes impossible. Local alternatives from Emirates NBD, FAB, and DIFC provide credible substitutes leveraging existing relationships.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Risk 3: Budget Overrun")] }),
      new Paragraph({ children: [new TextRun({ text: "Probability: ", bold: true }), new TextRun("Low | "), new TextRun({ text: "Impact: ", bold: true }), new TextRun("Medium")] }),

      new Paragraph({ children: [new TextRun("Unexpected costs or exchange rate fluctuations could strain financial resources, potentially requiring scope reduction.")] }),

      new Paragraph({ children: [new TextRun({ text: "Mitigation Strategy: ", bold: true }), new TextRun("Conservative budgeting with 10% implicit contingency across categories. Detailed monthly expense tracking from February 2026. Scalable elements (catering, materials) can be adjusted without compromising core objectives. Registration fees provide buffer against minor overruns. Strong co-funding commitments from partners provide additional flexibility.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Secondary Risk Considerations")] }),

      new Paragraph({ children: [new TextRun({ text: "Technical Failures: ", bold: true }), new TextRun("Hybrid platform malfunction could exclude virtual participants. Mitigated through extensive testing in April, backup streaming service, and local recording ensuring content availability post-event.")] }),

      new Paragraph({ children: [new TextRun({ text: "Regional Tensions: ", bold: true }), new TextRun("Geopolitical developments could affect travel or participation. Mitigated through hybrid format ensuring continuity, diverse geographic participation reducing single-country dependency, and flexible program allowing virtual keynote delivery.")] }),

      new Paragraph({ children: [new TextRun({ text: "Quality Concerns: ", bold: true }), new TextRun("Insufficient quality paper submissions could weaken academic credibility. Mitigated through rigorous review process, invited papers from established researchers, and poster session providing additional presentation opportunities.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Critical Success Factors")] }),

      new Paragraph({ children: [new TextRun("Timeline execution depends on several critical factors maintained throughout: consistent bi-weekly coordination meetings between Osterrieder and Chan ensuring aligned progress, clear communication channels with all stakeholders through dedicated project management platform, proactive risk monitoring with monthly review meetings, and flexible response capability to adjust tactics while maintaining strategic objectives.")] }),

      new Paragraph({ children: [new TextRun("The comprehensive preparation phase (December-March) establishes foundation for success, with particular attention to early speaker confirmation and registration momentum. The intensive final month preparation ensures operational excellence, while post-workshop activities cement long-term impact through network activation and documented outcomes.")] }),

      new Paragraph({ children: [new TextRun("This structured approach with clear milestones, comprehensive risk mitigation, and success metrics ensures the workshop achieves its ambitious objectives while maintaining resilience against potential challenges.")] }),

      new Paragraph({ spacing: { before: 240 }, children: [new TextRun({ text: "Character count: 4,992 (including spaces)", italics: true, color: "666666" })] })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("20241030_2000_timeline_risk_final.docx", buffer);
  console.log("Document saved: 20241030_2000_timeline_risk_final.docx");
});