import email
import imaplib
import os


class Bill:
    def __init__(self, start_date, end_date, category, total):
        self.start_date = start_date
        self.end_date = end_date
        self.service_period = self.end_date - self.start_date
        self.category = category
        self.total = total
        self.cost_per_day = self.get_cost_per_day()

    def get_cost_per_day(self):
        return self.total / self.service_period.days

    def split_cost_by_days(self, num_days):
        return self.total / num_days


class FetchEmail:
    """Based on https://stackoverflow.com/a/27556667"""

    connection = None
    error = None

    def __init__(self, mail_server, username, password):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)
        self.connection.select(readonly=False)  # so we can mark mails as read
        self.emails = []

    def close_connection(self):
        """
        Close the connection to the IMAP server
        """
        self.connection.close()

    def fetch_unread_messages(self):
        """
        Retrieve unread messages
        """
        result, messages = self.connection.search(None, 'ALL')
        if result == "OK":
            for message in messages[0].split():
                try:
                    ret, data = self.connection.fetch(message, '(RFC822)')
                except:
                    print("No new emails to read.")
                    self.close_connection()
                    exit()

                msg = email.message_from_bytes(data[0][1])
                if not isinstance(msg, str):
                    self.emails.append(msg)

    def save_attachment(self, msg, download_folder="/tmp"):
        """
        Given a message, save its attachments to the specified
        download folder (default is /tmp)

        return: file path to attachment
        """
        att_path = "No attachment found."
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            att_path = os.path.join(download_folder, filename)

            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

        print("[!] Saved attachment!")
        return att_path
