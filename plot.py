import json
import src.analyze as analyze

def main():
    with open("analysis/bi_child.json","r") as file:
        bi_child = json.load(file)
    with open("analysis/dev_child.json","r") as file:
        dev_child = json.load(file)
    analyze.plot(dev_child, bi_child)

main()