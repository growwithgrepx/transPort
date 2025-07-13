import xml.etree.ElementTree as ET
import os

try:
    tree = ET.parse('artifacts/selenium-test-results/test_results/selenium-test-results.xml')
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
    print(f"- **Total Tests**: {total}")
    print(f"- **Passed**: {passed} ✅")
    print(f"- **Failed**: {failures} ❌")
    print(f"- **Errors**: {errors} 🔥")
    if total > 0:
        print(f"- **Pass Rate**: {passed * 100 // total}%")
    print("")
    with open('/tmp/selenium.txt', 'w') as tf:
        tf.write(f"{total},{passed},{failures},{errors}")
except Exception as e:
    print(f"❌ Error processing Selenium results: {e}\n")