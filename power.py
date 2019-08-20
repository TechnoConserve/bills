"""
Manages aspects of the Rocky Mountain Power bill.
"""
import pikepdf
import re
import textract
from datetime import datetime

from utils import get_config


def process_power_bill_pdf(pdf_path):
    """
    Given the file path to a readable Rocky Mountain Power pdf bill,
    return the service period and amount due.
    :param pdf_path: File path to Rocky Mountain Power pdf bill.
    :return: The amount due as a floating point number, as well
    as the start and end of the service period as datetime objects.
    """

    text = textract.process(pdf_path).decode("utf-8")
    amt_pat = re.compile(r"AMOUNT DUE:\s+^\$(?P<amt_due>\d{2,3}\.\d{2})", re.MULTILINE)
    period_pat = re.compile(r"AMOUNT USED\sTHIS MONTH\s\s^\d+\s\s(?P<service_start>\w{3}\s\d{1,2},\s\d{4})"
                            r"\s\s(?P<service_end>\w{3}\s\d{1,2},\s\d{4})", re.MULTILINE)
    amt_due = re.search(amt_pat, text)
    service_period = re.search(period_pat, text)

    amt_due = float(amt_due.group("amt_due"))
    service_start = datetime.strptime(service_period.group("service_start"), "%b %d, %Y")
    service_end = datetime.strptime(service_period.group("service_end"), "%b %d, %Y")

    return amt_due, service_start, service_end


def decrypt_power_pdf(attachment, save_path="/tmp/power_bill.pdf"):
    config = get_config()
    with pikepdf.open(attachment, password=config["POWER"]["PASSWORD"]) as pdf:
        print("[!] Decrypting pdf...")
        pdf.save(save_path)

    return save_path


def process_power_bill_email(fetch, download_folder="/tmp"):
    """
    Searchs for Rocky Mountain Power bill email among list of email
    objects contained in the given FetchEmail object. If found,
    save the attachment and return it.
    :param download_folder: File path to save attachments.
    :param fetch: FetchEmail object.
    :return: Path to attachment file.
    """
    for email in fetch.emails:
        email_subject = email['subject']
        email_from = email['from']
        if email_from == "accountnotices@rockymountainpower.net" and \
                email_subject == "Your Rocky Mountain Power bill is attached":
            attachment = fetch.save_attachment(email, download_folder)

            return attachment
