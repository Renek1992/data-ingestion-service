"""
slack alerting module.
"""
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.config import AppConfig


def send_slack_message(app_config: AppConfig, error_msg: str, severity: str):
    if app_config.environment == 'prod':
        slack_token = app_config.slack_token
        channel_id = 'C046G6M036Z'

        severity_specs = {
            "info": {
                "emoji": ":thought_balloon:",
                "color": "#b0b0ae"
            },
            "warn": {
                "emoji": ":warning:",
                "color": "#f7bd1e"
            },
            "error": {
                "emoji": ":alert-flash:",
                "color": "#f24444"
            }
        }

        attachment = [
            {
                "color": severity_specs[severity]['color'],
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{severity_specs[severity]['emoji']} | {severity} message",
                            "emoji": True
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Log Message:*\n{error_msg}"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*AWS Lambda Name:*\n{os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'test_function')}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*AWS Region:*\n{os.environ.get('AWS_REGION', 'test_region')}"
                            }
                        ]
                    }
                ]
            }
        ]

        client = WebClient(token=slack_token)

        try:
            client.chat_postMessage(
                channel=channel_id, 
                attachments=attachment,
                text="Notification from DW Ingestion App"
            )

        except SlackApiError as e:
            raise e
    else:
        pass
        


if __name__== "__main__":
    error = "test error test error test error test error test error test error test error test error test error test error"
    severity = "error"
    send_slack_message(error_msg=error, severity=severity)
