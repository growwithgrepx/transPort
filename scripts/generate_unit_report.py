import xml.etree.ElementTree as ET
import os
import sys

if __name__ == "__main__":
    # Optionally allow passing a custom XML path as an argument
    import argparse
    parser = argparse.ArgumentParser(description="Generate a summary report from a unit test XML file.")
    parser.add_argument('--xml', type=str, default='artifacts/test-results-3.11/test_results/unit-test-results.xml', help='Path to unit test XML results')
    parser.add_argument('--cov', type=str, default='artifacts/test-results-3.11/tests/reports/coverage_unit.xml', help='Path to coverage XML (optional)')
    parser.add_argument('--out', type=str, default='/tmp/unit_3.11.txt', help='Output summary file')
    args = parser.parse_args()

    try:
        tree = ET.parse(args.xml)
        root = tree.getroot()
        if root.tag == 'testsuites':
            total = sum(int(suite.get('tests', 0)) for suite in root.findall('testsuite'))
            failures = sum(int(suite.get('failures', 0)) for suite in root.findall('testsuite'))
            errors = sum(int(suite.get('errors', 0)) for suite in root.findall('testsuite'))
        else:
            total = int(root.get('tests', 0))
            failures = int(root.get('failures', 0))
            errors = int(root.get('errors', 0))
        passed = total - failures - errors
        coverage = 0
        try:
            if os.path.exists(args.cov):
                cov_tree = ET.parse(args.cov)
                cov_root = cov_tree.getroot()
                coverage = float(cov_root.get('line-rate', 0)) * 100
        except:
            pass
        print(f"- **Total Tests**: {total}")
        print(f"- **Passed**: {passed} \u2705")
        print(f"- **Failed**: {failures} \u274c")
        print(f"- **Errors**: {errors} \ud83d\udd25")
        if total > 0:
            print(f"- **Pass Rate**: {passed * 100 // total}%")
        print("")
        with open(args.out, 'w') as tf:
            tf.write(f"{total},{passed},{failures},{errors},{coverage}")
    except Exception as e:
        print(f"\u274c Error processing results: {e}\n")