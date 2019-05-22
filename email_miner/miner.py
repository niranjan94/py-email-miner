import contextlib
import imaplib
import logging
import ssl
from typing import List

from imapclient import IMAPClient, SEEN

from email_miner.email import Email
from email_miner.parse import parse_emails


class Miner:
    """create a new email miner instance that can be used to traverse mails"""

    imap: IMAPClient = None

    def __init__(self, hostname: str,
                 username: str,
                 password: str,
                 port: int = imaplib.IMAP4_SSL_PORT,
                 use_ssl: bool = True,
                 verify: bool = True,
                 log_level: int = None):
        """
        Create a new instance of the miner.

        :param hostname: the hostname of the imap server to connect to
        :param username: the user to login as
        :param password:
        :param port: the port to connect to. (defaults to 993)
        :param use_ssl: whether to use SSL to connect (defaults to True)
        :param verify: whether to verify the SSL certificates (defaults to False)
        """

        if log_level is not None:
            logging.basicConfig(
                format='%(asctime)s - %(levelname)s: %(message)s',
                level=log_level
            )

        ssl_context = ssl.create_default_context()

        if not verify:
            # disable hostname check. certificate may not match hostname.
            ssl_context.check_hostname = False
            # disable certificate authority verification. certificate maybe issued by unknown CA
            ssl_context.verify_mode = ssl.CERT_NONE

        self.imap = IMAPClient(host=hostname, port=port, ssl=use_ssl, ssl_context=ssl_context)
        self.imap.login(username, password)

    @contextlib.contextmanager
    def folder(self, folder_name: str, read_only: bool = True):
        """
        Switch to a specific folder.

        :param folder_name: name of the folder to switch to
        :param read_only: read-only mode will not mark emails as read even after retrieval
        :return:
        """
        try:
            yield self.imap.select_folder(folder_name, read_only)
        finally:
            self.imap.close_folder()

    @contextlib.contextmanager
    def inbox(self, read_only: bool = True):
        """
        Switch to the inbox folder.

        :param read_only: read-only mode will not mark emails as read even after retrieval
        :return:
        """
        try:
            yield self.imap.select_folder('inbox', read_only)
        finally:
            self.imap.close_folder()

    def mark_as_unread(self, message_ids: List[int]):
        """
        Mark the given message IDs as unread by removing the SEEN flag.

        :param message_ids:
        :return:
        """
        self.imap.remove_flags(message_ids, [SEEN])

    def mark_as_read(self, message_ids: List[int]):
        """
        Mark the given message IDs as read by adding the SEEN flag.

        :param message_ids:
        :return:
        """
        self.imap.add_flags(message_ids, [SEEN])

    def get_emails(self, unread_only: bool = True,
                   with_body: bool = False,
                   keep_as_unread: bool = False,
                   in_memory: bool = True) -> List[Email]:
        """
        Get emails from the selected folder.

        :param keep_as_unread: keep any retrieved emails as unread in the mailbox.
        :param unread_only: choose only to retrieve unread mails
        :param with_body: read-only mode will not mark emails as read even after retrieval
        :param in_memory: store the parsed attachments in-memory as bytes or to a temp file locally
        :return:
        """
        ids = self.imap.search('(UNSEEN)' if unread_only else 'ALL')
        flags = ['ENVELOPE', 'FLAGS', 'UID', 'INTERNALDATE']

        if with_body:
            flags.append('BODY[]')

        response = self.imap.fetch(ids, flags)

        try:
            if keep_as_unread:
                self.mark_as_unread(ids)
            else:
                self.mark_as_read(ids)
        except Exception:
            # will throw an exception if folder in read-only mode. so ignore.
            pass

        return parse_emails(response, in_memory)

    def __enter__(self):
        """
        return the instance of the miner for use as a context manager.

        :return:
        """
        return self

    def __exit__(self, *args):
        """
        Close folder and logout on exit when used as a context manager.

        :param args:
        :return:
        """
        if self.imap is not None:
            try:
                self.imap.close_folder()
            except:
                pass
            self.imap.logout()
