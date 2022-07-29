from parseTenhou import parseHanchan

if __name__ == "__main__":
    fileObj = open("paipu.txt", "r", encoding="utf-8")
    lines = fileObj.read().splitlines()
    fileObj.close()

    with open("SegaSammy_No1.json", "w", encoding="utf-8") as outfile:
        kobaReport = parseHanchan(lines)
        outfile.write(kobaReport)
