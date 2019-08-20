"""
Manages aspects of the Dominion Energy bill.
"""
import re


def process_gas_bill_email(fetch):
    """
    Searchs for Dominion Energy gas bill email among list of email
    objects contained in the given FetchEmail object. If found,
    save the attachment and return it.
    :param fetch: FetchEmail object.
    :return: Float representing the total amount due for the bill.
    """
    for email in fetch.emails:
        email_subject = email['subject']
        email_from = email['from']
        if email_from == "paperlessbill@domenergyuteb.com" and \
                email_subject == "Your Dominion Energy Gas Bill is Ready to View":
            msg = email.get_payload()[0].as_string()

            amt_pat = re.compile(r"Amount Due: </span><br>[\s]+[\S]+[\s]+[\S]+[\s][\S]+[\s][\S]+[\s][\S]+[\s][\S]+"
                                 r"[\s][\S]+[\s][\S]+[\s]+[\S]\">\$(?P<amt_due>\d{2,3}\.\d{2})", re.MULTILINE)
            amt_due = re.search(amt_pat, msg)
            amt_due = float(amt_due.group("amt_due"))

    return amt_due
