import sys
import xml.etree.ElementTree as ET

def main(xml_path):
    print("## Coverage Report (Markdown Table)\n")
    print("| File | Statements | Missed | Coverage |")
    print("|------|------------|--------|----------|")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    total_stmts = total_miss = 0
    for cls in root.findall(".//class"):
        filename = cls.attrib["filename"]
        stmts = int(cls.attrib["statements"])
        miss = int(cls.attrib["missed"])
        cover = 100 if stmts == 0 else int(100 * (stmts - miss) / stmts)
        print(f"| `{filename}` | {stmts} | {miss} | {cover}% |")
        total_stmts += stmts
        total_miss += miss
    if total_stmts:
        total_cover = int(100 * (total_stmts - total_miss) / total_stmts)
        print(f"| **TOTAL** | {total_stmts} | {total_miss} | **{total_cover}%** |")

if __name__ == "__main__":
    main(sys.argv[1]) 