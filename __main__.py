# TODO make in-file replacement a flag option
# TODO output total count of cards uploaded

if __name__ == '__main__':
    import analyzer, sys
    from pathlib import Path

    path = Path(sys.argv[1])
    analyzer.analyze(path)
    with open(path, "r") as f:
        lines = analyzer.replace_with_note_formatting(f.readlines())
    with open(path, "w") as f:
        f.writelines(lines)
