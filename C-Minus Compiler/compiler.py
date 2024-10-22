from scanner import Scanner
from parse import Parser


def main():
    scanner = Scanner()
    parser = Parser(scanner)

    parser.parse()


if __name__ == '__main__':
    main()
