import configparser
import os
import subprocess

from models import FetchEmail


def get_config():
    """
    Read the configuration file.
    :return: configuration parser object.
    """
    config = configparser.ConfigParser()
    config.read("creds/creds.cfg")

    return config


def get_fetch_email(config):
    """
    Connects to email server using settings provided by given config
    object. Returns FetchEmail object.
    :param config: Configparser object that has already parsed a
    configuration file containing server connection information.
    :return: FetchEmail object containing the list of emails.
    """
    fetch = FetchEmail(mail_server=config["GMAIL CREDS"]["SMTP_SERVER"],
                       username=config["GMAIL CREDS"]["FROM"],
                       password=config["GMAIL CREDS"]["FROM_PWD"])
    fetch.fetch_unread_messages()

    return fetch


def start_flask(debug=False):
    os.environ["FLASK_APP"] = "web.py"
    os.environ["FLASK_DEBUG"] = debug
    subprocess.run(["flask", "run"], env=os.environ.copy())
