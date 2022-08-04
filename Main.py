from parseTenhou import parseHanchan
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help="name ofinput paipu that need to convert")
    parser.add_argument('--output', type=str, help="name of the output file")
    args = parser.parse_args()
    fileObj = open(args.input, "r", encoding="utf-8")
    lines = fileObj.read().splitlines()
    fileObj.close()

    with open(args.output, "w", encoding="utf-8") as outfile:
        kobaReport = parseHanchan(lines)
        outfile.write(kobaReport)
