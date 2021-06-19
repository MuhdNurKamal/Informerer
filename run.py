from datetime import timedelta
from persistence import get_stored_counts, store_counts, log
import time
from slack_sdk.webhook import WebhookClient
from dotenv import load_dotenv
import os
from betterer import get_counts
from humanize import naturaldelta

load_dotenv()


def get_time_to_zero(prev, curr, prev_count, curr_count):
    delta_seconds = 0
    if prev_count <= curr_count:
        delta_seconds = 3.154e8
    else:
        delta_seconds = (curr - prev) / (prev_count - curr_count) * curr_count
    return naturaldelta(timedelta(seconds=delta_seconds))


prev = get_stored_counts()
counts = get_counts()

url = os.environ.get("SLACK_WEBHOOK_URL")
webhook = WebhookClient(url)

reports = [
    {
        "label": "ESLint",
        "prev_count": prev["es"]["count"],
        "count": counts["es"],
        "prev_date": prev["es"]["updatedAt"],
        "logo": ":eslint:",
    },
    {
        "label": "TypeScript",
        "prev_count": prev["ts"]["count"],
        "count": counts["ts"],
        "prev_date": prev["ts"]["updatedAt"],
        "logo": ":typescript:",
    },
]

report_sections = list(
    map(
        lambda report: [
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "{} {}: {:,d}    :small_red_triangle_down: {:,d}".format(
                        report["logo"],
                        report["label"],
                        report["count"],
                        report["prev_count"] - report["count"],
                    ),
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":rocket: Countdown to zero: {}".format(
                        get_time_to_zero(
                            report["prev_date"],
                            time.time(),
                            report["prev_count"],
                            report["count"],
                        ),
                    ),
                },
            },
        ],
        reports,
    )
)

response = webhook.send(
    text="Informerer Report",
    blocks=[
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":tada: This week's Betterer Error Counts :tada:",
            },
        },
    ]
    + [x for y in report_sections for x in y],
)

assert response.status_code == 200
assert response.body == "ok"

store_counts(
    es={"count": counts["es"], "updatedAt": time.time()},
    ts={"count": counts["ts"], "updatedAt": time.time()},
)

log(str({"time": time.time(), "counts": counts}))
