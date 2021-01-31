if __name__ == '__main__':
    import analyzer, sys
    from pathlib import Path

    path = Path(sys.argv[1])
    analyzer.analyze(path)