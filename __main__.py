# TODO output total count of cards uploaded

if __name__ == '__main__':
    import analyzer
    from pathlib import Path
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Parse Anki Cards from Notes")
    parser.add_argument("file", help="The file to parse cards from")
    parser.add_argument("-r", "--reformat", help="Replace added card syntax in-file with Markdown formatting",
                        action='store_true',
                        dest="reformat")

    args = parser.parse_args()

    path = Path(args.file)
    analyzer.analyze(path)
    with open(path, "r") as f:
        lines = analyzer.replace_with_note_formatting(f.readlines())
    if args.reformat:
        with open(path, "w") as f:
            f.writelines(lines)
