if __name__ == '__main__':
    import analyzer, sys

    with open(sys.argv[1], "r") as f:
        analyzer.analyze(f)