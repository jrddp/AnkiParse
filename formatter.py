import re
from pathlib import Path

# TODO add image parsing, then to be stored using ankiConnect
# TODO allow default code langs based on deck

image_pattern = r"!\[(.*)\]\((.+)\)"


def format_newlines(text):
    return text.replace("\n", "<br \\>")


def format_bold_and_italics(text):
    # Replace **words** with HTML emboldening
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", str(text))
    # Replace *words* with HTML italicizing
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", str(text))

    # Revert * italics changes within math blocks
    text = re.sub(r"(\\[([].*)<i>(.*?)</i>(?=.*\\[)\]])", r"\1*\2*", str(text))
    # Revert ** bold changes within math blocks
    text = re.sub(r"(\\[([].*)<b>(.*?)</b>(?=.*\\[)\]])", r"\1**\2**", str(text))

    return text


def format_latex_to_mathjax(text):
    # Replaces $$ANYTHING$$ with \[ANYTHING\]
    text = re.sub(r"\$\$(.*?)\$\$", r"\[\1\]", str(text))
    # Replaces $ANYTHING$ with \(ANYTHING\)
    text = re.sub(r"\$(.*?)\$", r"\(\1\)", str(text))
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
        return "<center><table><tbody><tr><td>" + highlight(code, lexer,
                                                            formatter) + "</td></tr></tbody></table></center>"

    return re.sub(code_block_pattern, format_block, text, flags=re.DOTALL)

def format_images(text):
    from cards import saved_image_prefix
    # Converts all markdown formatted images to HTML formatting, modified by $saved_image_prefix
    text = re.sub(image_pattern, fr'<img src="{saved_image_prefix}\2" alt="\1">', str(text))
    return text


def format_everything(text: str):
    return format_newlines(
        format_bold_and_italics(
            format_latex_to_mathjax(
                format_code_blocks(
                    format_images(
                    text.strip()
                )))))


def get_image_paths(text: str):
    return [match[1] for match in re.findall(image_pattern, text)]