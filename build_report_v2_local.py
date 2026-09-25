from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas as canvas_mod

# ---------------------------------------------------------------
# Page furniture: footer with page numbers + running title
# ---------------------------------------------------------------
class NumberedCanvas(canvas_mod.Canvas):
    def __init__(self, *args, **kwargs):
        canvas_mod.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            canvas_mod.Canvas.showPage(self)
        canvas_mod.Canvas.save(self)

    def draw_footer(self, page_count):
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(0.85*inch, 0.55*inch,
                         "Unsupervised vs. Supervised Detection in CW-TF-QKD")
        self.drawRightString(7.65*inch, 0.55*inch,
                              f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#999999"))
        self.setLineWidth(0.5)
        self.line(0.85*inch, 0.72*inch, 7.65*inch, 0.72*inch)


# ---------------------------------------------------------------
# Styles
# ---------------------------------------------------------------
styles = getSampleStyleSheet()

NAVY = colors.HexColor("#1a1a2e")
SLATE = colors.HexColor("#22223b")
GREY = colors.HexColor("#555555")
LIGHT = colors.HexColor("#f2f2f7")
ACCENT = colors.HexColor("#3a5a9b")

styles.add(ParagraphStyle(name="ReportTitle", fontName="Helvetica-Bold", fontSize=17,
    leading=21, alignment=TA_CENTER, spaceAfter=6, textColor=NAVY))
styles.add(ParagraphStyle(name="Authors", fontName="Helvetica", fontSize=10.5,
    leading=14, alignment=TA_CENTER, spaceAfter=2, textColor=colors.HexColor("#333333")))
styles.add(ParagraphStyle(name="AbstractHead", fontName="Helvetica-Bold", fontSize=10.5,
    leading=13, alignment=TA_LEFT, spaceBefore=14, spaceAfter=4))
styles.add(ParagraphStyle(name="AbstractBody", fontName="Helvetica", fontSize=9.6,
    leading=13.2, alignment=TA_JUSTIFY, leftIndent=18, rightIndent=18))
styles.add(ParagraphStyle(name="Keywords", fontName="Helvetica-Oblique", fontSize=9.4,
    leading=12.5, alignment=TA_LEFT, leftIndent=18, rightIndent=18, spaceBefore=8))
styles.add(ParagraphStyle(name="TOCEntry", fontName="Helvetica", fontSize=10,
    leading=16, alignment=TA_LEFT, leftIndent=6))
styles.add(ParagraphStyle(name="TOCEntrySub", fontName="Helvetica", fontSize=9.3,
    leading=14.5, alignment=TA_LEFT, leftIndent=22, textColor=GREY))
styles.add(ParagraphStyle(name="H1", fontName="Helvetica-Bold", fontSize=13, leading=16,
    spaceBefore=18, spaceAfter=8, textColor=NAVY))
styles.add(ParagraphStyle(name="H2", fontName="Helvetica-Bold", fontSize=11, leading=14,
    spaceBefore=12, spaceAfter=6, textColor=SLATE))
styles.add(ParagraphStyle(name="H3", fontName="Helvetica-BoldOblique", fontSize=9.8, leading=13,
    spaceBefore=8, spaceAfter=4, textColor=SLATE))
styles.add(ParagraphStyle(name="Body", fontName="Helvetica", fontSize=10, leading=14.6,
    alignment=TA_JUSTIFY, spaceAfter=7))
styles.add(ParagraphStyle(name="CustomBullet", fontName="Helvetica", fontSize=9.7, leading=13.6,
    alignment=TA_JUSTIFY, spaceAfter=4, leftIndent=4))
styles.add(ParagraphStyle(name="Caption", fontName="Helvetica-Oblique", fontSize=8.8,
    leading=11.5, alignment=TA_LEFT, spaceBefore=4, spaceAfter=14, textColor=colors.HexColor("#444444")))
styles.add(ParagraphStyle(name="Eq", fontName="Helvetica-Oblique", fontSize=10, leading=15,
    alignment=TA_CENTER, spaceBefore=4, spaceAfter=10))
styles.add(ParagraphStyle(name="RefEntry", fontName="Helvetica", fontSize=9.2, leading=13,
    leftIndent=14, firstLineIndent=-14, spaceAfter=5, alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name="BoxHead", fontName="Helvetica-Bold", fontSize=10, leading=13,
    textColor=colors.white))
styles.add(ParagraphStyle(name="BoxBody", fontName="Helvetica", fontSize=9.4, leading=13.2,
    alignment=TA_JUSTIFY, textColor=colors.HexColor("#1a1a2e")))
styles.add(ParagraphStyle(name="BoxBullet", fontName="Helvetica", fontSize=9.2, leading=12.8,
    alignment=TA_LEFT, textColor=colors.HexColor("#1a1a2e")))


def bullets(items, style="CustomBullet", bullet_char="\u2022"):
    return ListFlowable(
        [ListItem(Paragraph(t, styles[style]), leftIndent=12, spaceAfter=3) for t in items],
        bulletType="bullet", start=bullet_char, bulletFontSize=8.5,
        bulletColor=ACCENT, leftIndent=14
    )


def key_box(title, items, fill=NAVY):
    header = Table([[Paragraph(title, styles["BoxHead"])]], colWidths=[6.6*inch])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), fill),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
    ]))
    body_flow = bullets(items, style="BoxBullet")
    body = Table([[body_flow]], colWidths=[6.6*inch])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#cccccc")),
    ]))
    return [header, body, Spacer(1, 12)]


story = []

# ---------------------------------------------------------------
# Title block
# ---------------------------------------------------------------
story.append(Spacer(1, 4))
story.append(Paragraph(
    "A Comparative Study of Unsupervised Clustering and Supervised "
    "Classification for Physical-Layer Attack Detection in "
    "Continuous-Wave Twin-Field QKD Systems", styles["ReportTitle"]))
story.append(Paragraph("Technical Report", styles["Authors"]))
story.append(Paragraph("Simulation Study &mdash; Lang&ndash;Kobayashi Feature Space", styles["Authors"]))
story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#999999")))

story.append(Paragraph("Abstract", styles["AbstractHead"]))
story.append(Paragraph(
    "Twin-field quantum key distribution (TF-QKD) extends the achievable range of "
    "quantum-secured communication by interfering weak coherent pulses at a central "
    "untrusted relay, but continuous-wave (CW) implementations expose a physical "
    "side channel absent from idealized, discrete-variable treatments. This report "
    "evaluates two machine-learning strategies for recognizing attack fingerprints "
    "from physically derived features: unsupervised geometric clustering (Gaussian "
    "Mixture Models, K-Means) and supervised discriminative classification "
    "(XGBoost, SVM). Using a simulated CW-TF-QKD dataset with Nominal, "
    "Frequency-Injection-Modulation (FIM), and TWIRL attack classes generated from "
    "the Lang&ndash;Kobayashi laser rate equations, we find a sharp performance "
    "gap&mdash;approximately 36.7% unsupervised proxy accuracy versus 88.2% "
    "supervised accuracy&mdash;and trace it to the non-convex overlap of classes in "
    "the phase-decoherence&ndash;sideband-power feature plane. We conclude with the "
    "complementary role of one-class detectors such as Deep SVDD for identifying "
    "attacks unseen during training.", styles["AbstractBody"]))
story.append(Paragraph(
    "<b>Keywords:</b> twin-field QKD, continuous-wave side channel, Gaussian mixture "
    "models, K-means, XGBoost, support vector machines, Deep SVDD, anomaly detection, "
    "Lang&ndash;Kobayashi equations.", styles["Keywords"]))
story.append(Spacer(1, 4))
story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#999999")))

# ---------------------------------------------------------------
# Table of contents
# ---------------------------------------------------------------
story.append(Spacer(1, 10))
story.append(Paragraph("Contents", styles["H1"]))
toc = [
    ("1.  Introduction", "3"),
    ("2.  Background", "3"),
    ("     2.1  Physical Features and the Attack Model", "3"),
    ("     2.2  Unsupervised Clustering", "4"),
    ("     2.3  Supervised Classification", "4"),
    ("3.  Methodology", "5"),
    ("     3.1  Dataset Construction", "5"),
    ("     3.2  Model Configuration", "5"),
    ("4.  Results", "5"),
    ("     4.1  Structural Comparison", "5"),
    ("     4.2  Empirical Performance", "6"),
    ("5.  Discussion", "6"),
    ("     5.1  Why Unsupervised Clustering Fails Here", "6"),
    ("     5.2  Why Supervised Classification Succeeds Here", "7"),
    ("     5.3  Implications for Zero-Day Detection", "7"),
    ("6.  Conclusion and Recommendations", "8"),
    ("     References", "8"),
]
toc_rows = []
for label, pg in toc:
    st = "TOCEntrySub" if label.startswith("     ") else "TOCEntry"
    toc_rows.append([Paragraph(label.strip(), styles[st]), Paragraph(pg, styles[st])])
toc_table = Table(toc_rows, colWidths=[5.6*inch, 0.6*inch])
toc_table.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("ALIGN", (1,0), (1,-1), "RIGHT"),
    ("TOPPADDING", (0,0), (-1,-1), 1),
    ("BOTTOMPADDING", (0,0), (-1,-1), 1),
]))
story.append(toc_table)
story.append(PageBreak())

# ---------------------------------------------------------------
# 1. Introduction
# ---------------------------------------------------------------
story.append(Paragraph("1. Introduction", styles["H1"]))
story.append(Paragraph(
    "Twin-field quantum key distribution (TF-QKD) was introduced to overcome the "
    "fundamental rate&ndash;distance limit that constrains point-to-point QKD "
    "links. In its continuous-wave (CW) realization, security depends not only on "
    "the discrete statistics of detected clicks but also on the physical stability "
    "of the transmitting lasers, whose phase and intensity are actively locked "
    "across the link. This dependence opens an attack surface outside conventional "
    "discrete-variable security proofs: an adversary who couples energy into the "
    "laser cavity, or manipulates the phase-locking servo, may bias interference "
    "outcomes at the relay while the reported QBER stays within tolerance.", styles["Body"]))
story.append(Paragraph(
    "Detecting this class of attack is a physical-layer anomaly detection problem. "
    "Two machine-learning paradigms are available, each with a different "
    "operational promise:", styles["Body"]))
story.append(bullets([
    "<b>Unsupervised clustering</b> &mdash; partitions feature vectors by geometric "
    "or probabilistic similarity with no access to ground-truth attack labels; "
    "attractive because it needs no labeled attack data and can, in principle, "
    "flag never-before-seen behavior.",
    "<b>Supervised classification</b> &mdash; trains on a labeled corpus of "
    "Nominal and attack traces to learn an explicit decision boundary; attractive "
    "because it can exploit fine-grained, non-convex structure that purely "
    "geometric methods cannot represent.",
]))
story.append(Paragraph(
    "This report evaluates both paradigms on a simulated CW-TF-QKD dataset with "
    "Nominal, FIM, and TWIRL classes, quantifies the resulting performance gap, "
    "explains its geometric origin, and outlines when each approach&mdash;and "
    "their combination&mdash;is appropriate for an operational detection pipeline.", styles["Body"]))

# ---------------------------------------------------------------
# 2. Background
# ---------------------------------------------------------------
story.append(Paragraph("2. Background", styles["H1"]))

story.append(Paragraph("2.1 Physical Features and the Attack Model", styles["H2"]))
story.append(Paragraph(
    "Features are derived from the Lang&ndash;Kobayashi (LK) delay-differential "
    "equations, which model the coupled evolution of a laser's electric field "
    "amplitude, phase, and carrier density under external optical feedback or "
    "injection. Two derived quantities dominate class separability:", styles["Body"]))
story.append(bullets([
    "<b>Phase decoherence (&Delta;&phi;)</b> &mdash; cycle-to-cycle drift of the "
    "transmitted phase relative to the locked reference; sensitive to "
    "perturbations of the phase-locking loop.",
    "<b>Spectral sideband power (P<sub>sb</sub>)</b> &mdash; energy leaking into "
    "frequency components adjacent to the carrier as a result of injection or "
    "modulation attacks.",
]))
story.append(Paragraph(
    "Nominal operation shows small, approximately stationary fluctuations in both "
    "quantities. The FIM attack raises P<sub>sb</sub> while initially leaving "
    "&Delta;&phi; largely unaffected; the TWIRL attack perturbs the phase "
    "trajectory directly, growing in &Delta;&phi; before becoming spectrally "
    "visible. Because both attacks are designed to be stealthy, their early-stage "
    "signatures sit deliberately close to the Nominal distribution &mdash; making "
    "this a meaningful stress test rather than a trivially separable problem.", styles["Body"]))

story.append(Paragraph("2.2 Unsupervised Clustering", styles["H2"]))
story.append(Paragraph(
    "K-Means partitions n feature vectors into k clusters by minimizing the "
    "within-cluster sum of squared distances to each centroid &mu;<sub>j</sub>:", styles["Body"]))
story.append(Paragraph(
    "J = &sum;<sub>j=1</sub><super>k</super> &sum;<sub>x&isin;C<sub>j</sub></sub> "
    "&#8214;x &minus; &mu;<sub>j</sub>&#8214;<super>2</super>", styles["Eq"]))
story.append(Paragraph(
    "This objective implicitly assumes each cluster occupies a roughly convex, "
    "isotropic region. The Gaussian Mixture Model (GMM) relaxes isotropy by "
    "modeling the data as a weighted sum of k multivariate Gaussians, fit via "
    "expectation&ndash;maximization to maximize:", styles["Body"]))
story.append(Paragraph(
    "log L = &sum;<sub>i=1</sub><super>n</super> log "
    "&sum;<sub>j=1</sub><super>k</super> &pi;<sub>j</sub> "
    "N(x<sub>i</sub> | &mu;<sub>j</sub>, &Sigma;<sub>j</sub>)", styles["Eq"]))
story.append(Paragraph(
    "Even with full covariance matrices, a GMM component describes only a single "
    "elliptical density &mdash; it cannot represent a boundary that curves back on "
    "itself or depends on a conjunction of thresholds across features. Because "
    "discovered clusters carry no labels by construction, cluster identities are "
    "matched to ground truth after the fact (e.g. by majority vote), which is why "
    "the resulting figure is described as a <i>proxy accuracy</i> rather than a "
    "classification accuracy.", styles["Body"]))

story.append(Paragraph("2.3 Supervised Classification", styles["H2"]))
story.append(Paragraph(
    "XGBoost is an ensemble of gradient-boosted decision trees. Each tree splits "
    "the feature space along axis-aligned thresholds (x<sub>j</sub> &le; t), and "
    "successive trees fit the residual gradient of a regularized loss, so the "
    "ensemble approximates an irregular decision boundary as a union of "
    "rectangular regions. Support vector machines instead seek a maximum-margin "
    "hyperplane, optionally in a kernel-induced space that makes the effective "
    "boundary non-linear in the original coordinates. Both require labeled "
    "training data, but in exchange can carve decision regions that follow the "
    "true, possibly non-convex, shape of the class-conditional distributions.", styles["Body"]))

story.append(PageBreak())

# ---------------------------------------------------------------
# 3. Methodology
# ---------------------------------------------------------------
story.append(Paragraph("3. Methodology", styles["H1"]))
story.append(Paragraph("3.1 Dataset Construction", styles["H2"]))
story.append(Paragraph(
    "Time series for laser field amplitude, phase, and carrier density were "
    "generated by numerically integrating the Lang&ndash;Kobayashi equations "
    "under three regimes:", styles["Body"]))
story.append(bullets([
    "<b>Nominal</b> &mdash; no external perturbation beyond the model's intrinsic noise terms.",
    "<b>FIM</b> &mdash; periodic modulation of the injection current.",
    "<b>TWIRL</b> &mdash; direct perturbation of the phase trajectory.",
]))
story.append(Paragraph(
    "From each simulated trace, summary features including &Delta;&phi; and "
    "P<sub>sb</sub> were extracted over sliding windows, producing a labeled "
    "feature table with one row per window and one column per derived physical "
    "quantity.", styles["Body"]))

story.append(Paragraph("3.2 Model Configuration", styles["H2"]))
story.append(bullets([
    "<b>Unsupervised branch:</b> K-Means and a full-covariance GMM, each fit with "
    "the number of components fixed to the number of true classes (k = 3); "
    "clusters mapped to labels by majority assignment before scoring.",
    "<b>Supervised branch:</b> XGBoost and an RBF-kernel SVM, trained on a "
    "held-out split and evaluated on a disjoint test split, using the same "
    "feature columns as the unsupervised models.",
]))
story.append(Paragraph(
    "Using identical features across both branches ensures that any performance "
    "difference is attributable to the modeling paradigm rather than to a "
    "difference in the information available to each approach.", styles["Body"]))

# ---------------------------------------------------------------
# 4. Results
# ---------------------------------------------------------------
story.append(Paragraph("4. Results", styles["H1"]))
story.append(Paragraph("4.1 Structural Comparison of the Two Paradigms", styles["H2"]))
story.append(Paragraph(
    "Table 1 summarizes the structural differences between the two approaches, "
    "independent of their measured performance on this dataset.", styles["Body"]))

table1_data = [
    ["Feature", "Unsupervised Clustering\n(GMM / K-Means)", "Supervised Classification\n(XGBoost / SVM)"],
    ["Objective",
     "Group data into k clusters by geometric distance or density, with no prior knowledge of class identity.",
     "Learn decision boundaries that explicitly separate known, labeled classes."],
    ["Labels required?",
     "No. Patterns are discovered blind to the true attack type.",
     "Yes. Requires a labeled training set of Nominal, FIM, and TWIRL data."],
    ["Zero-day detection",
     "Can naturally group unseen anomalies into outlier clusters, provided they are geometrically distant from normal data.",
     "Fails on unseen attack types unless paired with a dedicated anomaly detector (e.g. Deep SVDD)."],
    ["Best-suited data geometry",
     "Performs well when classes form distinct, isolated \u201cblobs\u201d in feature space.",
     "Performs well even under significant class overlap, provided there exist informative orthogonal splits or non-linear boundaries."],
]
tbl1 = Table(table1_data, colWidths=[1.15*inch, 2.75*inch, 2.75*inch])
tbl1.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8.3),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("ALIGN", (0,0), (-1,0), "CENTER"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#bbbbbb")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
]))
story.append(tbl1)
story.append(Paragraph(
    "Table 1. Structural comparison of unsupervised clustering and supervised "
    "classification as applied to physical-layer attack detection in CW-TF-QKD.",
    styles["Caption"]))

story.append(Paragraph("4.2 Empirical Performance on the CW-TF-QKD Dataset", styles["H2"]))
story.append(Paragraph(
    "Applied to the same feature set, the two paradigms diverge sharply. The "
    "unsupervised proxy accuracy, obtained by matching GMM clusters to "
    "ground-truth labels post hoc, reaches only ~36.68% &mdash; close to the "
    "accuracy expected from an uninformed three-way partition. The supervised "
    "XGBoost classifier reaches ~88.22%, more than double. Table 2 summarizes "
    "this gap.", styles["Body"]))

table2_data = [
    ["Method", "Paradigm", "Reported Accuracy"],
    ["Gaussian Mixture Model (GMM)", "Unsupervised (proxy)", "~36.68%"],
    ["XGBoost", "Supervised", "~88.22%"],
]
tbl2 = Table(table2_data, colWidths=[2.6*inch, 2.1*inch, 1.9*inch])
tbl2.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ALIGN", (2,0), (2,-1), "CENTER"),
    ("ALIGN", (0,0), (-1,0), "CENTER"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#bbbbbb")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
]))
story.append(tbl2)
story.append(Paragraph(
    "Table 2. Measured performance of the representative unsupervised and "
    "supervised models on the CW-TF-QKD Nominal / FIM / TWIRL classification task.",
    styles["Caption"]))

story.extend(key_box("Key Result", [
    "Supervised classification (XGBoost) outperforms unsupervised clustering "
    "(GMM) by more than a factor of two on this dataset (~88% vs. ~37%).",
    "The gap is geometric, not incidental: it stems from non-convex class "
    "overlap in the &Delta;&phi;&ndash;P<sub>sb</sub> feature plane, which "
    "defeats distance- and density-based clustering but is tractable for "
    "axis-aligned tree splits.",
]))

story.append(PageBreak())

# ---------------------------------------------------------------
# 5. Discussion
# ---------------------------------------------------------------
story.append(Paragraph("5. Discussion", styles["H1"]))

story.append(Paragraph("5.1 Why Unsupervised Clustering Fails on This Dataset", styles["H2"]))
story.append(Paragraph(
    "The root cause is geometric rather than algorithmic: both K-Means and GMM "
    "describe each class as a single convex region &mdash; a sphere for K-Means, "
    "an ellipse for a Gaussian component. In the &Delta;&phi;&ndash;P<sub>sb</sub> "
    "plane, however:", styles["Body"]))
story.append(bullets([
    "The Nominal state and the early stages of the FIM and TWIRL attacks bleed "
    "into one another continuously rather than forming separated blobs.",
    "The region occupied by each attack class is itself non-convex, curving "
    "around the Nominal region as the attack progresses from stealthy onset to "
    "detectable magnitude.",
    "A density-based mixture model has no mechanism to draw a curved or "
    "conjunctive boundary, so it resolves the ambiguity by collapsing the three "
    "classes into one broad, continuous high-density region.",
]))
story.append(Paragraph(
    "This is precisely why the resulting proxy accuracy sits so close to chance "
    "level for a three-way partition.", styles["Body"]))

story.append(Paragraph("5.2 Why Supervised Classification Succeeds on This Dataset", styles["H2"]))
story.append(Paragraph(
    "XGBoost's ensemble of shallow, axis-aligned decision trees is not "
    "constrained to convex or elliptical regions:", styles["Body"]))
story.append(bullets([
    "Each split tests a single feature against a threshold, and successive "
    "trees combine many such splits.",
    "The ensemble can approximate a conjunctive rule such as \u201cif "
    "P<sub>sb</sub> exceeds X and &Delta;&phi; is below Y, classify as "
    "TWIRL\u201d &mdash; exactly the rule shape needed to carve overlapping, "
    "curved class boundaries.",
    "Because this rule set is learned directly from labeled examples rather "
    "than inferred from unlabeled density alone, the model exploits subtle, "
    "class-specific structure invisible to a geometry-only objective.",
]))

story.append(Paragraph("5.3 Implications for Zero-Day Attack Detection", styles["H2"]))
story.append(Paragraph(
    "The performance gap above is not a blanket endorsement of supervised "
    "methods for every stage of a detection pipeline. Supervised classifiers "
    "cannot recognize an attack category absent from their training labels; "
    "presented with a genuinely novel perturbation, XGBoost or an SVM will "
    "confidently assign it to whichever known class it most resembles, rather "
    "than flagging it as anomalous. This is where one-class methods retain a "
    "distinct advantage.", styles["Body"]))
story.append(Paragraph(
    "A one-class detector such as Deep Support Vector Data Description (Deep "
    "SVDD) trains exclusively on Nominal data, learning a neural-network mapping "
    "that pulls Nominal samples toward a single center c in a learned feature "
    "space, minimizing:", styles["Body"]))
story.append(Paragraph(
    "min<sub>&theta;</sub> (1/n) &sum;<sub>i=1</sub><super>n</super> "
    "&#8214;&phi;(x<sub>i</sub>; &theta;) &minus; c&#8214;<super>2</super> "
    "+ &lambda;&#8214;&theta;&#8214;<super>2</super>", styles["Eq"]))
story.append(Paragraph(
    "Any operating point falling outside the resulting learned boundary &mdash; "
    "FIM, TWIRL, or a never-before-seen attack &mdash; is flagged as anomalous "
    "without requiring a label for it, making Deep SVDD the more appropriate "
    "tool for zero-day detection, complementing rather than replacing the "
    "supervised classifier used for known attack types.", styles["Body"]))

# ---------------------------------------------------------------
# 6. Conclusion
# ---------------------------------------------------------------
story.append(Paragraph("6. Conclusion and Recommendations", styles["H1"]))
story.append(Paragraph(
    "On the CW-TF-QKD dataset examined here, supervised classification "
    "substantially outperforms unsupervised clustering for distinguishing known "
    "attack types from Nominal operation (~88.22% with XGBoost vs. ~36.68% proxy "
    "accuracy with GMM). The gap traces to non-convex overlap of the Nominal, "
    "FIM, and TWIRL classes &mdash; a geometry that favors the conjunctive, "
    "axis-aligned rules learnable by a supervised tree ensemble over the convex "
    "or elliptical regions assumed by distance- and density-based clustering.", styles["Body"]))

story.extend(key_box("Recommendations", [
    "<b>Use supervised classification (e.g. XGBoost)</b> for day-to-day "
    "discrimination between Nominal operation and previously characterized "
    "attacks such as FIM and TWIRL, wherever labeled data is available.",
    "<b>Pair it with a one-class boundary detector (e.g. Deep SVDD)</b>, "
    "trained solely on Nominal data, so that genuinely novel perturbations of "
    "the laser dynamics are surfaced as anomalies rather than silently "
    "misclassified.",
    "<b>Treat the two paradigms as complementary layers</b> of a "
    "defense-in-depth detection architecture, not as competing solutions to "
    "the same problem.",
], fill=ACCENT))

story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#999999")))
story.append(Paragraph("References", styles["H2"]))
refs = [
    "Gisin, N., Ribordy, G., Tittel, W., &amp; Zbinden, H. Quantum cryptography. "
    "<i>Reviews of Modern Physics</i>.",
    "Lucamarini, M., Yuan, Z. L., Dynes, J. F., &amp; Shields, A. J. Overcoming the "
    "rate&ndash;distance limit of quantum key distribution without quantum repeaters. "
    "<i>Nature</i>.",
    "Lang, R., &amp; Kobayashi, K. External optical feedback effects on "
    "semiconductor injection laser properties. <i>IEEE Journal of Quantum "
    "Electronics</i>.",
    "Reynolds, D. A. Gaussian mixture models. In <i>Encyclopedia of Biometrics</i>.",
    "Chen, T., &amp; Guestrin, C. XGBoost: A scalable tree boosting system. "
    "<i>Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge "
    "Discovery and Data Mining</i>.",
    "Ruff, L., Vandermeulen, R., Goernitz, N., et al. Deep one-class "
    "classification. <i>Proceedings of the 35th International Conference on "
    "Machine Learning</i>.",
]
for i, r in enumerate(refs, 1):
    story.append(Paragraph(f"[{i}] {r}", styles["RefEntry"]))

# ---------------------------------------------------------------
# Build
# ---------------------------------------------------------------
doc = SimpleDocTemplate(
    "Unsupervised_vs_Supervised_CW_TFQKD_Report.pdf",
    pagesize=letter,
    leftMargin=0.85*inch, rightMargin=0.85*inch,
    topMargin=0.85*inch, bottomMargin=0.9*inch,
    title="Unsupervised vs. Supervised Detection in CW-TF-QKD",
    author="Technical Report"
)
doc.build(story, canvasmaker=NumberedCanvas)
print("done")
