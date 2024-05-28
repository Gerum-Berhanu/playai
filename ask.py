from playwright.sync_api import sync_playwright
import time

def run(prompt):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    url = "https://chatgpt.com"
    page.goto(url)
    page.wait_for_selector("textarea#prompt-textarea")
    textarea = page.locator("textarea#prompt-textarea")
    button = page.locator("button.absolute.bottom-1\\.5")

    textarea.fill(prompt)
    time.sleep(1)
    button.click()
    page.wait_for_selector("button.rounded-md.p-1.text-token-text-tertiary")
    elements = page.locator(".markdown > p:nth-child(1)").all()
    last_response = elements[-1].text_content()
    browser.close()
    return last_response

if __name__ == "__main__":
    run()