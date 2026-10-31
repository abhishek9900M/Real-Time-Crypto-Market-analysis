import os
import smtplib
import mimetypes
import pandas as pd

from pathlib import Path
from email.message import EmailMessage
from dotenv import load_dotenv

# Load .env from the same folder as this script
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

loaded = load_dotenv(ENV_FILE, override=True)

print("ENV file:", ENV_FILE)
print("ENV exists:", ENV_FILE.is_file())
print("ENV loaded:", loaded)


def send_report(attachment_path):

    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    receiver = os.getenv("REPORT_TO_EMAIL")

    print("Gmail address found:", bool(sender))
    print("App password found:", bool(password))
    print("Receiver found:", bool(receiver))

    if not sender or not password or not receiver:
        raise ValueError("Gmail configuration is incomplete in .env")
    # Read the complete Excel report
    df = pd.read_excel(attachment_path)

    # Select top 20 rows
    top_20 = df.head(50)

    # Save a separate Excel report
    top_20_path = BASE_DIR / "top_20_market_data.xlsx"
    top_20.to_excel(top_20_path, index=False)

    # Attach the filtered report
    file_path = top_20_path

    if not file_path.is_file():
        raise FileNotFoundError(f"Report not found: {file_path}")
    # Create email
    message = EmailMessage()
    message["Subject"] = "Cryptocurrency Market Report"
    message["From"] = sender
    message["To"] = receiver

    message.set_content(
        "Hello,\n\n"
        "Your latest cryptocurrency market report is attached.\n\n"
        "Regards,\n"
        "Crypto Dashboard Automation"
    )

    # Attach Excel file
    content_type, encoding = mimetypes.guess_type(file_path.name)

    if content_type is None or encoding is not None:
        content_type = "application/octet-stream"

    main_type, sub_type = content_type.split("/", 1)

    with open(file_path, "rb") as file:
        message.add_attachment(
            file.read(),
            maintype=main_type,
            subtype=sub_type,
            filename=file_path.name
        )

    # Connect to Gmail SMTP
    # Clean credentials (removes normal AND non-breaking spaces, quotes, newlines)
    clean_password = "".join(password.split()).strip("'\"")
    sender = sender.strip().strip("'\"")

    # Gmail over SSL (port 465) is more reliable than STARTTLS on 587
    import ssl
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=30) as server:
        # remove once it works
        server.login(sender, clean_password)
        server.send_message(message)

    print("Email report sent successfully!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit(
            'Usage: python email_report.py "reports/market_data.xlsx"'
        )

    send_report(sys.argv[1])

