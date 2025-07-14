import sys
import xml.etree.ElementTree as ET


def main(xml_path):
    print("## Coverage Report\n")
    print("| File | Statements | Missed | Coverage |")
    print("|------|------------|--------|----------|")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    total_stmts = total_miss = 0
    file_data = {}

    # Group classes/functions by file
    for package in root.findall(".//package"):
        for class_elem in package.findall("class"):
            filename = class_elem.attrib.get("filename")
            if filename not in file_data:
                file_data[filename] = {"classes": [], "functions": []}
            # Class-level coverage
            class_name = class_elem.attrib.get("name")
            stmts = int(class_elem.attrib.get("lines-valid") or class_elem.attrib.get("statements") or 0)
            covered = int(class_elem.attrib.get("lines-covered") or 0)
            miss = stmts - covered
            cover = 100 if stmts == 0 else int(100 * covered / stmts)
            file_data[filename]["classes"].append({
                "name": class_name,
                "stmts": stmts,
                "miss": miss,
                "cover": cover
            })

    # Function-level coverage (if available)
    for method_elem in root.findall(".//method"):
        filename = method_elem.attrib.get("filename")
        if not filename:
            continue
        if filename not in file_data:
            file_data[filename] = {"classes": [], "functions": []}
        func_name = method_elem.attrib.get("name")
        stmts = int(method_elem.attrib.get("lines-valid") or method_elem.attrib.get("statements") or 0)
        covered = int(method_elem.attrib.get("lines-covered") or 0)
        miss = stmts - covered
        cover = 100 if stmts == 0 else int(100 * covered / stmts)
        file_data[filename]["functions"].append({
            "name": func_name,
            "stmts": stmts,
            "miss": miss,
            "cover": cover
        })

    # File-level summary
    for file_elem in root.findall(".//class") + root.findall(".//file"):
        filename = file_elem.attrib.get("filename")
        stmts = int(file_elem.attrib.get("lines-valid") or file_elem.attrib.get("statements") or 0)
        covered = int(file_elem.attrib.get("lines-covered") or 0)
        miss = stmts - covered
        cover = 100 if stmts == 0 else int(100 * covered / stmts)
        print(f"| `{filename}` | {stmts} | {miss} | {cover}% |")
        total_stmts += stmts
        total_miss += miss
    if total_stmts:
        total_cover = int(100 * (total_stmts - total_miss) / total_stmts)
        print(f"| **TOTAL** | {total_stmts} | {total_miss} | **{total_cover}%** |\n")

    # Per-file, per-class/function breakdown
    for filename, details in file_data.items():
        print(f"\n<details><summary><strong>{filename}</strong> - Class & Function Coverage</summary>\n")
        if details["classes"]:
            print("\n**Classes:**\n")
            print("| Class | Statements | Missed | Coverage |")
            print("|-------|------------|--------|----------|")
            for c in details["classes"]:
                print(f"| `{c['name']}` | {c['stmts']} | {c['miss']} | {c['cover']}% |")
        if details["functions"]:
            print("\n**Functions:**\n")
            print("| Function | Statements | Missed | Coverage |")
            print("|----------|------------|--------|----------|")
            for f in details["functions"]:
                print(f"| `{f['name']}` | {f['stmts']} | {f['miss']} | {f['cover']}% |")
        print("\n</details>\n")

if __name__ == "__main__":
    main(sys.argv[1]) 