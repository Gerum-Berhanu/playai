import asyncio
from playwright.async_api import async_playwright

async def run(prompt):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        url = "https://chatgpt.com"
        await page.goto(url)
        
        # Wait for the textarea to appear
        await page.locator("textarea#prompt-textarea").wait_for(timeout=10000)
        textarea = page.locator("textarea#prompt-textarea")
        
        # Wait for the button to appear
        await page.locator("button.absolute.bottom-1\\.5").wait_for(timeout=10000)
        button = page.locator("button.absolute.bottom-1\\.5")

        # Fill textarea, click button, and wait for the response
        await textarea.fill(prompt)
        await asyncio.sleep(1)
        await button.click()
        await page.wait_for_selector("button.rounded-md.p-1.text-token-text-tertiary")

        # Obtain the list of elements
        elements_locator = page.locator(".markdown > p:nth-child(1)")
        elements = await elements_locator.all()
        
        # Obtain the text content of each element
        text_contents = []
        for element in elements:
            text_contents.append(await element.text_content())
        
        # Print the text contents
        last_response = text_contents[-1]
        
        await browser.close()
        return last_response

