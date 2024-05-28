from playwright.sync_api import sync_playwright
import time

playwright = sync_playwright().start()

browser = playwright.chromium.launch(headless=False)
page = browser.new_page()
url = "https://chatgpt.com"
page.goto(url)

textarea = page.get_by_placeholder("Message ChatGPT")
button = page.locator("button.absolute.bottom-1\.5")

def message():
    prompt = input("Ask ChatGPT: ")
    while not prompt:
        prompt = input("Ask ChatGPT: ")
    textarea.fill(prompt)
    time.sleep(1)
    button.click()
    time.sleep(10)
    elements = page.locator(".markdown > p:nth-child(1)").all()
    last_response = elements[-1].text_content()
    return last_response

result = message()
print(result)

browser.close()
