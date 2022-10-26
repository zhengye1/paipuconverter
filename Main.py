from mahjong.RuleSet import RuleSet
from mahjong.util.MAJING_CONSTANT import M_LEAGUE_RULE, A_RULE
from parseTenhou import parseHanchan
import argparse


def createRuleSet(rule):
    if rule == 'A':
        return A_RULE
    if rule == 'M':
        return M_LEAGUE_RULE
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help="name ofinput paipu that need to convert")
    parser.add_argument('--output', type=str, help="name of the output file")
    parser.add_argument('--rule', type=str, help="Rule for the hanchan, valid value is (A) rule, (M) rule, (W)RC rule")

    args = parser.parse_args()
    print(args.rule)
    if args.rule and args.rule not in ["A", "M", "W"]:
        raise argparse.ArgumentTypeError('Rule value valid for (A) rule, (M) rule, (W)RC rule')

    ruleSet = createRuleSet(args.rule)
    fileObj = open(args.input, "r", encoding="utf-8")
    lines = fileObj.read().splitlines()
    fileObj.close()

    with open(args.output, "w", encoding="utf-8") as outfile:
        kobaReport = parseHanchan(lines, ruleSet)
        outfile.write(kobaReport)
