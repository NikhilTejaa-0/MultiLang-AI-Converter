from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter

def generate_report(
    converted_results,
    logs,
    output_path="conversion_report.pdf"
):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "MultiLang AI Conversion Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1, 20)
    )

    # RESULTS

    for result in converted_results:

        heading = Paragraph(
            f"<b>File:</b> {result['input_name']}",
            styles["Heading2"]
        )

        elements.append(heading)

        elements.append(
            Spacer(1, 10)
        )

        explanation = Paragraph(
            result["explanation"],
            styles["BodyText"]
        )

        elements.append(explanation)

        elements.append(
            Spacer(1, 20)
        )

    # LOGS

    log_heading = Paragraph(
        "Conversion Logs",
        styles["Heading2"]
    )

    elements.append(log_heading)

    elements.append(
        Spacer(1, 10)
    )

    for log in logs:

        log_para = Paragraph(
            log,
            styles["BodyText"]
        )

        elements.append(log_para)

    doc.build(elements)

    return output_path