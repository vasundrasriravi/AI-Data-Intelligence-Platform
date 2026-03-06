from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors

def generate_pdf_report(filepath, explanations, dataset_type, models, metrics):

    doc = SimpleDocTemplate(filepath)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("<b>AI Data Intelligence Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Dataset Type
    if dataset_type:
        elements.append(Paragraph(f"<b>Dataset Type:</b> {dataset_type}", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    # Recommended Models
    if models:
        elements.append(Paragraph("<b>Recommended Models:</b>", styles["Heading2"]))
        model_list = [ListItem(Paragraph(m, styles["Normal"])) for m in models]
        elements.append(ListFlowable(model_list, bulletType="bullet"))
        elements.append(Spacer(1, 0.2 * inch))

    # Recommended Metrics
    if metrics:
        elements.append(Paragraph("<b>Recommended Evaluation Metrics:</b>", styles["Heading2"]))
        metric_list = [ListItem(Paragraph(m, styles["Normal"])) for m in metrics]
        elements.append(ListFlowable(metric_list, bulletType="bullet"))
        elements.append(Spacer(1, 0.2 * inch))

    # Cleaning Explanation
    if explanations:
        elements.append(Paragraph("<b>Cleaning Insights:</b>", styles["Heading2"]))
        explanation_list = [ListItem(Paragraph(e, styles["Normal"])) for e in explanations]
        elements.append(ListFlowable(explanation_list, bulletType="bullet"))

    doc.build(elements)