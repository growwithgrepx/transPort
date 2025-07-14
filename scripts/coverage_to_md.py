import sys
import xml.etree.ElementTree as ET
from collections import defaultdict


def main(xml_path):
    print("## Coverage Report\n")
    print("| File | Statements | Missed | Coverage |")
    print("|------|------------|--------|----------|")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    total_stmts = total_miss = 0
    file_data = {}
    file_lines = defaultdict(list)

    # Group lines by file for accurate statement/miss counts
    for class_elem in root.findall(".//class"):
        filename = class_elem.attrib.get("filename")
        for line_elem in class_elem.findall("lines/line"):
            file_lines[filename].append(line_elem)

    # File-level summary (sum up <line> elements for each file)
    for filename, lines in file_lines.items():
        stmts = len(lines)
        covered = sum(1 for l in lines if int(l.attrib.get("hits", "0")) > 0)
        miss = stmts - covered
        cover = 100 if stmts == 0 else int(100 * covered / stmts)
        print(f"| `{filename}` | {stmts} | {miss} | {cover}% |")
        total_stmts += stmts
        total_miss += miss

    if total_stmts:
        total_cover = int(100 * (total_stmts - total_miss) / total_stmts)
        print(f"| **TOTAL** | {total_stmts} | {total_miss} | **{total_cover}%** |\n")

    # Per-file, per-class/function breakdown (as before)
    for class_elem in root.findall(".//class"):
        filename = class_elem.attrib.get("filename")
        class_name = class_elem.attrib.get("name")
        # Class-level coverage
        class_lines = class_elem.findall("lines/line")
        stmts = len(class_lines)
        covered = sum(1 for l in class_lines if int(l.attrib.get("hits", "0")) > 0)
        miss = stmts - covered
        cover = 100 if stmts == 0 else int(100 * covered / stmts)
        print(f"\n<details><summary><strong>{filename}</strong> - Class & Function Coverage</summary>\n")
        print("\n**Classes:**\n")
        print("| Class | Statements | Missed | Coverage |")
        print("|-------|------------|--------|----------|")
        print(f"| `{class_name}` | {stmts} | {miss} | {cover}% |")
        # Function-level coverage (if available)
        methods = class_elem.findall("methods/method")
        if methods:
            print("\n**Functions:**\n")
            print("| Function | Statements | Missed | Coverage |")
            print("|----------|------------|--------|----------|")
            for method_elem in methods:
                func_name = method_elem.attrib.get("name")
                func_lines = method_elem.findall("lines/line")
                f_stmts = len(func_lines)
                f_covered = sum(1 for l in func_lines if int(l.attrib.get("hits", "0")) > 0)
                f_miss = f_stmts - f_covered
                f_cover = 100 if f_stmts == 0 else int(100 * f_covered / f_stmts)
                print(f"| `{func_name}` | {f_stmts} | {f_miss} | {f_cover}% |")
        print("\n</details>\n")

if __name__ == "__main__":
    main(sys.argv[1]) 