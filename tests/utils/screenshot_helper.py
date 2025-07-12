import os

def save_debug_artifacts(driver, name):
    os.makedirs("test_screenshots", exist_ok=True)
    driver.save_screenshot(f"test_screenshots/{name}.png")
    with open(f"test_screenshots/{name}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source) 