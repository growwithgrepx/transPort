import sys
import xml.etree.ElementTree as ET

def main(xml_path):
    print("## Coverage Report\n")
    print("| File | Statements | Missed | Coverage |")
    print("|------|------------|--------|----------|")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    total_stmts = total_miss = 0
    # coverage.py XML puts files under <packages>/<package>/<class> or <packages>/<package>/<file>
    for file_elem in root.findall(".//class") + root.findall(".//file"):
        filename = file_elem.attrib.get("filename")
        # Try both coverage.py v4 and v5+ attributes
        stmts = int(file_elem.attrib.get("lines-valid") or file_elem.attrib.get("statements") or 0)
        covered = int(file_elem.attrib.get("lines-covered") or 0)
        miss = stmts - covered
        cover = 100 if stmts == 0 else int(100 * covered / stmts)
        print(f"| `{filename}` | {stmts} | {miss} | {cover}% |")
        total_stmts += stmts
        total_miss += miss
    if total_stmts:
        total_cover = int(100 * (total_stmts - total_miss) / total_stmts)
        print(f"| **TOTAL** | {total_stmts} | {total_miss} | **{total_cover}%** |")

if __name__ == "__main__":
    main(sys.argv[1]) 