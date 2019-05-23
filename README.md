<img width=100 src="https://res.cloudinary.com/niranjan94/image/upload/c_scale,w_200/v1558590706/mine_caxqwq.png">

<hr>

`email-miner` makes it easy to mine IMAP mailboxes in a simple pythonic way. It's a thin-wrapper around the awesome [IMAPClient](https://github.com/mjs/imapclient) library.

### Installation

`email-miner` is listed on [PyPI](https://pypi.org/project/email-miner/) and can be installed with pip:

```bash
pip install email-miner
```

### Example

```python
from email_miner.miner import Miner

# miner acts as a context manager to ensure connections are closed
with Miner('imap.gmail.com', 'john@gmail.com', 'xyzzy') as client:

    # folder switching as a context manager to ensure folder is closed
    with client.inbox(read_only=True):
    
        # get emails from the selected folder as a list
        emails = client.get_emails(unread_only=True, with_body=True)
       
        for email in emails:
            print('Subject:', email.subject)
            print('From:', email.from_addresses)
            print('To:', email.to_addresses)
            
            # the body is already parsed 
            # and the attachments can be accessed directly
            for attachment in email.attachments:
                
                print('Attachment type:', attachment.content_type)
                print('Attachment name:', attachment.file_name)
                
                with open(attachment.file_name, 'wb') as file:
                    file.write(attachment.file_content)
```

### License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

```
MIT License

Copyright (c) 2019 Niranjan Rajendran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

