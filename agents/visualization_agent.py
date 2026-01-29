from tools.chart_tools import generate_chart
from agents.audit_agent import log_event


def create_visualization(run_id: str, data: dict, chart_type: str, title: str):
    """
    Generates charts from structured data.
    """
    chart_path = generate_chart(
        data=data,
        chart_type=chart_type,
        title=title
    )

    log_event(
        run_id,
        "visualization_agent",
        "chart_generated",
        {
            "chart_type": chart_type,
            "title": title
        },
        {
            "chart_path": chart_path
        }
    )

    return chart_path

