import xml.etree.ElementTree as ET
import os
import sys

try:
    tree = ET.parse('artifacts/test-results-3.11/test_results/unit-test-results.xml')
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
        if os.path.exists('artifacts/test-results-3.11/tests/reports/coverage_unit.xml'):
            cov_tree = ET.parse('artifacts/test-results-3.11/tests/reports/coverage_unit.xml')
            cov_root = cov_tree.getroot()
            coverage = float(cov_root.get('line-rate', 0)) * 100
    except:
        pass
    print(f"- **Total Tests**: {total}")
    print(f"- **Passed**: {passed} ✅")
    print(f"- **Failed**: {failures} ❌")
    print(f"- **Errors**: {errors} 🔥")
    if total > 0:
        print(f"- **Pass Rate**: {passed * 100 // total}%")
    print("")
    with open('/tmp/unit_3.11.txt', 'w') as tf:
        tf.write(f"{total},{passed},{failures},{errors},{coverage}")
except Exception as e:
    print(f"❌ Error processing Python 3.11 results: {e}\n")