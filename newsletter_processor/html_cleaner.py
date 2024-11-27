from html.parser import HTMLParser
import re


class HTMLCleaner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content = []

    def handle_data(self, data):
        self.text_content.append(data)

    def get_text(self):
        return ''.join(self.text_content).strip()


def remove_html_tags(input_html: str) -> str:
    cleaner = HTMLCleaner()
    cleaner.feed(input_html)
    return cleaner.get_text()


def fix_json_input(body: str) -> str:
    regex = r'"input":\s*"(.*)"'
    match = re.search(regex, body)
    if match:
        fixed_input = match.group(1).replace('"', '\\"')
        return re.sub(regex, f'"input": "{fixed_input}"', body)
    return body
