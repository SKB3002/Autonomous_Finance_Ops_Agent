import matplotlib.pyplot as plt
import uuid


def generate_chart(data: dict, chart_type: str, title: str):
    chart_id = str(uuid.uuid4())
    file_path = f"charts/{chart_id}.png"

    keys = list(data.keys())
    values = list(data.values())

    plt.figure()
    if chart_type == "bar":
        plt.bar(keys, values)
    elif chart_type == "line":
        plt.plot(keys, values)
    else:
        raise ValueError("Unsupported chart type")

    plt.title(title)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

    return file_path

