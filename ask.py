import asyncio
from playwright.async_api import async_playwright
from scripts import screen_capture, screenshot_path

async def block_ads(route, request):
    # List of common ad-serving domains
    ad_domains = [
        "doubleclick.net",
        "googleadservices.com",
        # Add more ad-serving domains as needed
    ]

    for domain in ad_domains:
        if domain in request.url:
            await route.abort()
            return

    await route.continue_()

async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()

        page = await context.new_page()
        await page.route("**/*", block_ads)
        await page.goto("https://deepai.org/chat", timeout=60000)

        path = "./capture/capture.png"
        await screen_capture(page, path, full_page=True)
        
        stoppers = ["exit", "stop", "quit", "abort"]
        prompt = input("Ask PlayAI: ")

        try:
            while prompt.lower() not in stoppers and prompt:
                textarea = await page.query_selector_all("textarea[placeholder='Chat with AI...']")
                textarea = textarea[-1]
                button = await page.query_selector("#chatSubmitButton")

                await textarea.fill(prompt)
                await button.click()
                await asyncio.sleep(5)

                container = await page.query_selector_all(".outputBox > .markdownContainer > .markdownContainer")
                html = await container[-1].inner_html()
                print(html)

                return html
                await screen_capture(page, path, full_page=True)

                prompt = input("Ask PlayAI: ")
        finally:
            # await screen_capture(page, path, full_page=True)
            # await asyncio.Event().wait()  # Wait indefinitely until you decide to close the browser manually
            await browser.close()
            print("Browser closed")

if __name__ == "__main__":
    asyncio.run(run())
