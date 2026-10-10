import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
METRICS = json.loads((ROOT / "metrics.json").read_text(encoding="utf-8"))
CHARTS = ROOT / "charts"
CHARTS.mkdir(exist_ok=True)


def bar_chart(filename, title, subtitle, items, value_key, color="#235347", suffix="%"):
    width, height = 1100, 620
    left, right, top, bottom = 270, 70, 130, 80
    plot_width = width - left - right
    row_height = (height - top - bottom) / len(items)
    max_value = max(value for _, value, _ in items) * 1.15
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="#fffaf1"/>',
             f'<text x="55" y="58" font-family="Arial" font-size="30" font-weight="700" fill="#251914">{title}</text>',
             f'<text x="55" y="92" font-family="Arial" font-size="17" fill="#755f55">{subtitle}</text>']
    for index, (label, value, sample) in enumerate(items):
        y = top + index * row_height
        bar_width = plot_width * value / max_value if max_value else 0
        lines += [f'<text x="{left-20}" y="{y+30}" text-anchor="end" font-family="Arial" font-size="18" fill="#35241d">{label}</text>',
                  f'<rect x="{left}" y="{y+8}" width="{bar_width:.1f}" height="32" rx="7" fill="{color}"/>',
                  f'<text x="{left+bar_width+12:.1f}" y="{y+31}" font-family="Arial" font-size="17" font-weight="700" fill="#35241d">{value:.1f}{suffix}</text>',
                  f'<text x="{left}" y="{y+61}" font-family="Arial" font-size="13" fill="#8c7469">n={sample:,}</text>']
    lines += [f'<text x="55" y="{height-28}" font-family="Arial" font-size="13" fill="#8c7469">Source: Hotel Booking Demand dataset. Scope: Resort Hotel only.</text>', '</svg>']
    (CHARTS / filename).write_text("\n".join(lines), encoding="utf-8")


def rate_items(group):
    return [(key, value["cancellation_rate"] * 100, value["bookings"]) for key, value in group.items()]


bar_chart("cancellation_by_year.svg", "Cancellation rate increased in 2017", "Annual Resort Hotel cancellation rate", rate_items(METRICS["by_year"]), "cancellation_rate", "#cc6b3d")
lead_order = ["0-7", "8-30", "31-90", "91-180", "181-365", ">365"]
bar_chart("cancellation_by_lead_time.svg", "Longer lead time is associated with more cancellations", "Business-relevant ranges; sample size shown for every group", [(key, METRICS["by_lead_time"][key]["cancellation_rate"] * 100, METRICS["by_lead_time"][key]["bookings"]) for key in lead_order], "cancellation_rate")
bar_chart("cancellation_by_channel.svg", "TA/TO combines scale with the highest cancellation rate", "Cancellation rate by distribution channel", rate_items(METRICS["by_distribution_channel"]), "cancellation_rate", "#6f4a37")
bar_chart("cancellation_by_customer_type.svg", "Transient bookings are the clearest high-risk segment", "Cancellation rate by customer type", rate_items(METRICS["by_customer_type"]), "cancellation_rate", "#9b774c")
repeat_items = [(key, value["repeated_guest_rate"] * 100, value["bookings"]) for key, value in METRICS["repeated_guest_by_distribution_channel"].items()]
bar_chart("repeated_guest_by_channel.svg", "Direct and Corporate lead on repeat-guest share", "Corrected calculation using distribution_channel, not market_segment", repeat_items, "repeated_guest_rate", "#39785b")
