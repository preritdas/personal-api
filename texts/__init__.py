"""
Sending text messages back.
"""
# External
import nexmo

# Project
import keys


sms = nexmo.Sms(
    key = keys.Nexmo.api_key,
    secret = keys.Nexmo.api_secret
)


def send_message(content: str, recipient: str, sandbox: bool = False) -> bool:
    """
    Send a text message. Returns True if the request succeeded, or False if it failed.
    """
    assert isinstance(recipient, str)

    if sandbox:
        return True

    vonage_res = sms.send_message(
        {
            "type": "unicode",
            "from": keys.Nexmo.sender,
            "to": recipient,
            "text": str(content)
        }
    )

    return True if vonage_res["messages"][0]["status"] == "0" else False
