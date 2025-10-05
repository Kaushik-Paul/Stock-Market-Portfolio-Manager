import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP
from mailjet_rest.client import Client

load_dotenv(override=True)

mcp = FastMCP("email_server")


class EmailBodyArgs(BaseModel):
    message: str = Field(description="A brief message for sending email")


@mcp.tool()
def send_email(args: EmailBodyArgs):
    """Send an email with this brief message"""

    api_key = os.getenv("MAILJET_API_KEY")
    api_secret = os.getenv("MAILJET_API_SECRET")
    from_email = os.getenv("MAILJET_FROM_EMAIL")
    to_email = os.getenv("MAILJET_TO_EMAIL")

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": from_email,
                    "Name": "AI Agents Trader"
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": "Portfolio Owner"
                    }
                ],
                "Subject": "Trade Analysis",
                "TextPart": args.message,
            }
        ]
    }

    result = mailjet.send.create(data=data)
    return {
        "status": "success",
        "response": result.json()
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
