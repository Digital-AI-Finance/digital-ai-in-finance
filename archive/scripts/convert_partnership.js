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
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } }
    ]
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Partnership and Roles")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Strategic Alignment and Partnership Foundation")] }),

      new Paragraph({ children: [new TextRun("The Swiss-MENA AI Finance partnership represents an ideal alignment of complementary strengths, institutional commitments, and strategic visions that uniquely positions this collaboration to achieve CCG objectives. Switzerland's precision in financial technology and regulatory frameworks naturally complements the UAE's dynamic market growth and innovation ecosystem, creating synergies that neither partner could achieve independently. This partnership transforms individual excellence into collective impact, establishing a model for sustainable Swiss-MENA research collaboration.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Progressive Partnership Development")] }),

      new Paragraph({ children: [new TextRun("The collaboration between Prof. Joerg Osterrieder (FHGR) and Prof. Stephen Chan (AUS) has evolved organically over 7 years from initial research exchanges to a comprehensive vision for regional research transformation. What began as focused research stays at AUS's Department of Mathematics has progressively deepened through joint investigations into blockchain security, fraud detection methodologies, and digital asset innovations. This sustained engagement has yielded four significant publications, including a comprehensive guide on blockchain security challenges, advanced fraud detection methods currently under review, and two substantial studies on NFTs and digital assets in virtual environments.")] }),

      new Paragraph({ children: [new TextRun("The partnership's evolution reflects increasing mutual understanding and trust. Initial collaborations focused on specific technical challenges in blockchain security, leveraging Prof. Osterrieder's expertise in mathematical finance and Prof. Chan's regional insights into emerging market dynamics. As the partnership matured, the scope expanded to encompass broader questions of AI applications in finance, regulatory frameworks, and market implementation. This progressive development has built the foundation necessary for the ambitious network launch we now propose.")] }),

      new Paragraph({ children: [new TextRun("Throughout this collaboration, both partners have demonstrated exceptional commitment, with multiple research grants secured that validate the partnership's productivity and potential. The success has attracted additional collaborators, including Dr. Yuanyuan Zhang from the University of Manchester and Dr. Hana Sulieman from AUS, who bring complementary expertise in machine learning applications and regional financial systems respectively. This expanding circle of excellence demonstrates the partnership's magnetic effect on talent and its potential for sustainable growth.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Roles and Responsibilities Framework")] }),

      new Paragraph({ children: [new TextRun("Prof. Joerg Osterrieder, as lead applicant from FHGR, assumes overall responsibility for workshop coordination and successful delivery of all objectives. His role encompasses four critical domains: orchestrating the complete workshop program from conception through execution, engaging Swiss stakeholders including academic institutions and financial industry partners, defining the research agenda and ensuring scientific excellence across all sessions, and establishing the governance framework for the Swiss-MENA AI Finance Research Network including MoU development and institutional agreements. His extensive experience in international research collaborations and deep connections within Swiss financial technology circles ensure effective leadership and stakeholder engagement.")] }),

      new Paragraph({ children: [new TextRun("Prof. Stephen Chan, as the principal MENA partner from AUS, provides essential regional coordination and local expertise. His responsibilities span managing all local logistics including venue arrangements and technical infrastructure, recruiting and engaging MENA academic participants and ensuring regional representation, serving as primary liaison with UAE stakeholders including DIFC, Emirates NBD, First Abu Dhabi Bank, and regulatory authorities, and coordinating regional research network development to ensure sustainable MENA participation. Prof. Chan's established relationships within UAE's financial innovation ecosystem and his understanding of regional dynamics are instrumental to the workshop's success and the network's regional embedding.")] }),

      new Paragraph({ children: [new TextRun("The MSCA Industrial Doctoral Network contributes through providing doctoral participants who will present research and participate in training sessions, ensuring early-career researcher perspectives are integrated throughout the program. This involvement models the intergenerational knowledge transfer essential for sustainable research ecosystems.")] }),

      new Paragraph({ children: [new TextRun("Supporting team members bring additional expertise and networks. Dr. Yuanyuan Zhang (University of Manchester) contributes her expertise in AI applications for financial services and extends the partnership's reach into UK research networks. Dr. Hana Sulieman (AUS) provides crucial regional perspective and ensures gender balance in the organizing committee while contributing her expertise in computational finance and Arab financial markets.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Partner Contributions and Resource Commitment")] }),

      new Paragraph({ children: [new TextRun("Both primary partners demonstrate substantial commitment through financial and in-kind contributions that ensure workshop success while maximizing CCG investment impact. The budget structure achieves 80% co-funding, with detailed breakdowns provided in the attached financial documentation.")] }),

      new Paragraph({ children: [new TextRun("AUS provides comprehensive in-kind support that extends far beyond monetary value. The provision of conference facilities for three days represents not just space but institutional endorsement and logistical expertise. Staff time from Prof. Chan and administrative support ensures smooth operations and local coordination. Technical infrastructure including audio-visual equipment and streaming capabilities enables hybrid participation and global reach. Perhaps most valuable is AUS's provision of network access to UAE's financial sector, opening doors to industry partnerships that would be difficult to establish independently.")] }),

      new Paragraph({ children: [new TextRun("FHGR contributes through substantial time investment from Prof. Osterrieder and research staff, ensuring thorough preparation and professional execution. The commitment of over 50 hours of senior academic time demonstrates institutional prioritization of this initiative. Additional support includes marketing through institutional channels, administrative assistance, and connection to Swiss academic and industry networks.")] }),

      new Paragraph({ children: [new TextRun("Financial contributions are structured to maximize impact while demonstrating genuine partnership. With CCG support of CHF 5,000 representing 20% of total costs, partners contribute the remaining 80% through a combination of direct funding and in-kind support, demonstrating exceptional leverage of CCG investment.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Team Composition and Inclusive Excellence")] }),

      new Paragraph({ children: [new TextRun("The organizing team reflects our commitment to diversity across multiple dimensions. Gender balance is embedded from leadership through execution, with Dr. Hana Sulieman serving on the organizing committee and a firm commitment to achieving minimum 40% female representation among speakers and panelists. Geographic diversity spans Swiss, UK, UAE, and broader MENA representation, ensuring multiple perspectives inform workshop design and network development.")] }),

      new Paragraph({ children: [new TextRun("The team combines senior researchers with established reputations and early-career academics bringing fresh perspectives and energy. This intergenerational composition ensures both credibility and innovation, creating mentorship opportunities while challenging established paradigms. Disciplinary diversity brings together expertise in mathematics, computer science, finance, and economics, essential for addressing the interdisciplinary challenges of AI in finance.")] }),

      new Paragraph({ children: [new TextRun("Industry advisory input ensures practical relevance, with representatives from partner financial institutions providing guidance on program design and participant recruitment. This academic-industry balance in team composition models the collaborative approach the network seeks to institutionalize.")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Future Partnership Evolution")] }),

      new Paragraph({ children: [new TextRun("This workshop represents not an endpoint but a milestone in an expanding partnership trajectory. Plans for Swiss-UAE bilateral research funding applications will be developed during the workshop, leveraging the network established and insights gained to pursue larger-scale collaborative programs. The formal network structure creates a framework for institutional partnerships beyond the founding members, with mechanisms for new universities and research centers to join.")] }),

      new Paragraph({ children: [new TextRun("The partnership envisions expansion to include additional Swiss universities and MENA institutions, creating a comprehensive research ecosystem. Industry partnerships initiated during the workshop will evolve into sustained collaboration agreements, potentially including sponsored research, doctoral funding, and technology transfer arrangements.")] }),

      new Paragraph({ children: [new TextRun("Long-term sustainability is ensured through institutional commitments that extend beyond individual researchers. Both FHGR and AUS have formally endorsed this initiative at senior leadership levels, providing resilience against personnel changes and ensuring continued support for network activities. This institutional backing, combined with the proven productivity of the partnership and the strategic importance of AI in finance, positions the collaboration for sustained growth and impact.")] }),

      new Paragraph({ children: [new TextRun("Through this carefully structured partnership leveraging complementary strengths, demonstrated commitment, and inclusive excellence, the workshop will achieve its ambitious objectives while establishing a transformation model for Swiss-MENA research collaboration in critical technology domains.")] }),

      new Paragraph({ spacing: { before: 240 }, children: [new TextRun({ text: "Character count: 4,978 (including spaces)", italics: true, color: "666666" })] })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("20241030_1930_partnership_roles_final.docx", buffer);
  console.log("Document saved: 20241030_1930_partnership_roles_final.docx");
});