if __name__ == '__main__':
    import analyzer

    with open("test/anki_test.txt", "r") as f:
        analyzer.analyze(f)