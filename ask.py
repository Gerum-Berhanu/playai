import asyncio
from playwright.async_api import async_playwright

async def run(prompt):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        url = "https://chatgpt.com"
        await page.goto(url)
        await page.wait_for_selector("textarea#prompt-textarea")
        textarea = await page.locator("textarea#prompt-textarea")
        button = await page.locator("button.absolute.bottom-1\\.5")

        await textarea.fill(prompt)
        await asyncio.sleep(1)
        await button.click()
        await page.wait_for_selector("button.rounded-md.p-1.text-token-text-tertiary")
        elements = await page.locator(".markdown > p:nth-child(1)").all()
        last_response = await elements[-1].text_content()
        await browser.close()
        return last_response