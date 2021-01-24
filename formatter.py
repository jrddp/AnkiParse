import re


def format_newlines(text):
    return text.replace("\n", "<br \\>")


def format_latex_to_mathjax(text):
    import re

    # Replaces $ANYTHING$ with \(ANYTHING\)
    text = re.sub(r"\$(.*?)\$", r"\(\1\)", str(text))
    # Replaces $$ANYTHING$$ with \[ANYTHING\]
    text = re.sub(r"\$\$(.*?)\$\$", r"\[\1\]", str(text))
    return text


# Matches markdown formatted code blocks, groups are (language, code)
code_block_pattern = r"```(\w*)\n(.*?)\n```"


def format_code_blocks(text):
    from pygments import highlight, lexers
    from pygments.formatters.html import HtmlFormatter

    formatter = HtmlFormatter(linenos='inline', noclasses=True, font_size=16)

    def format_block(match: re.Match):
        lang, code = match.groups()
        lexer = lexers.get_lexer_by_name(lang, stripall=True)
        return "<center><table><tbody><tr><td>" + highlight(code, lexer, formatter) + "</td></tr></tbody></table></center>"

    return re.sub(code_block_pattern, format_block, text, flags=re.DOTALL)


def format_everything(text):
    return format_newlines(
        format_latex_to_mathjax(
            format_code_blocks(text)))
