from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # ✅ Added
import json
import os

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Headless mode for silent scraping
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  # ✅ Updated

def get_test_details(url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-catalogue-training-calendar__row")))

        description = ""
        job_levels = ""
        languages = ""
        test_type = ""
        remote_testing = ""
        downloads = []

        rows = driver.find_elements(By.CSS_SELECTOR, ".product-catalogue-training-calendar__row")
        for row in rows:
            try:
                if "Description" in row.text:
                    description = row.find_element(By.TAG_NAME, "p").text.strip()
                elif "Job levels" in row.text:
                    job_levels = row.find_element(By.TAG_NAME, "p").text.strip()
                elif "Languages" in row.text:
                    languages = row.find_element(By.TAG_NAME, "p").text.strip()
                elif "Test Type" in row.text:
                    test_type = row.find_element(By.CSS_SELECTOR, ".product-catalogue__key").text.strip()
                elif "Remote Testing" in row.text:
                    remote_testing = row.find_element(By.CSS_SELECTOR, ".catalogue__circle").text.strip()
                if "Downloads" in row.text:
                    download_links = driver.find_elements(By.CSS_SELECTOR, ".product-catalogue__download-title a")
                    for link in download_links:
                        downloads.append(link.get_attribute("href"))
            except Exception as e:
                print(f"Error extracting data from {url}: {e}")

        return {
            "description": description,
            "job_levels": job_levels,
            "languages": languages,
            "test_type": test_type,
            "remote_testing": remote_testing,
            "downloads": downloads
        }
    except Exception as e:
        print(f"Error fetching details from {url}: {e}")
        return {}

def scrape_main_catalog():
    driver.get("https://www.shl.com/solutions/products/product-catalog/")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".custom__table-wrapper")))

    rows = driver.find_elements(By.CSS_SELECTOR, ".custom__table-wrapper table tbody tr[data-course-id]")
    print(f"Found {len(rows)} rows in the catalog page.")

    # Collect all basic info before navigation
    basic_info_list = []
    for i, row in enumerate(rows, start=1):
        try:
            test_id = row.get_attribute("data-course-id")
            name_elem = row.find_element(By.CSS_SELECTOR, "td.custom__table-heading__title a")
            name = name_elem.text.strip()
            link = name_elem.get_attribute("href")

            basic_info_list.append({
                "id": test_id,
                "name": name,
                "url": link
            })
        except Exception as e:
            print(f"Error collecting row {i}: {e}")
            continue

    print(f"Collected {len(basic_info_list)} basic entries. Now fetching details...")

    results = []

    for i, info in enumerate(basic_info_list, start=1):
        try:
            print(f"Processing {i}: {info['name']}")
            test_details = get_test_details(info['url'])

            if test_details:
                results.append({
                    "id": info['id'],
                    "category": "Pre-packaged Job Solutions",
                    "name": info['name'],
                    "url": info['url'],
                    **test_details
                })
            else:
                print(f"Failed to fetch details for {info['name']}")
        except Exception as e:
            print(f"Error fetching details for {info['name']}: {e}")

    print(f"Total tests scraped: {len(results)}")

    with open("shl_catalog.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print("✅ Catalog data has been scraped and saved successfully.")

try:
    scrape_main_catalog()
finally:
    driver.quit()
