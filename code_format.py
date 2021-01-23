import re

# Matches markdown formatted code blocks, groups (language, code)
code_block_pattern = r"```(\w*)\n(.*?)\n```"

def format_code_in_html(text):
    from pygments import highlight, lexers
    from pygments.formatters.html import HtmlFormatter

    formatter = HtmlFormatter(linenos='inline', noclasses=True, font_size=16)

    def format_block(match: re.Match):
        lang, code = match.groups()
        lexer = lexers.get_lexer_by_name(lang, stripall=True)
        return highlight(code, lexer, formatter)

    return re.sub(code_block_pattern, format_block, text, flags=re.DOTALL)

text = "".join(open("card.txt", 'r').readlines())
text = format_code_in_html(text)

with open("card.html", "w") as f:
    f.write(text)