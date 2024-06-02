import asyncio
from playwright.async_api import async_playwright

playwright = None
browser = None
context = None
page = None

async def block_ads(route, request):
    ad_domains = [
        "doubleclick.net",
        "googleadservices.com",
    ]
    for domain in ad_domains:
        if domain in request.url:
            await route.abort()
            return
    await route.continue_()

async def init_browser():
    global playwright, browser, context, page
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    await page.route("**/*", block_ads)
    await page.goto("https://deepai.org/chat", timeout=60000)

async def close_browser():
    global playwright, browser, context, page
    await browser.close()
    await playwright.stop()
    playwright = None
    browser = None
    context = None
    page = None

async def run(prompt):
    global page
    if not page:
        raise ValueError("Browser page is not initialized")
    
    textarea = await page.query_selector_all("textarea[placeholder='Chat with AI...']")
    textarea = textarea[-1]
    button = await page.query_selector("#chatSubmitButton")

    await textarea.fill(prompt)
    await button.click()
    await asyncio.sleep(5)

    container = await page.query_selector_all(".outputBox > .markdownContainer > .markdownContainer")
    html = await container[-1].inner_html()

    return html

# Ensure the browser is initialized at startup
asyncio.run(init_browser())
