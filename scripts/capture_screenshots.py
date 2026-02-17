import asyncio
import os
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to the frontend
        print("Navigating to http://localhost:5173...")
        try:
            await page.goto("http://localhost:5173", timeout=60000)

            # Wait for content to load
            # await page.wait_for_selector("main", timeout=10000)

            # Take screenshot of desktop view
            print("Taking desktop screenshot...")
            await page.screenshot(path="docs/screenshots/desktop_feed.png", full_page=True)

            # Take screenshot of mobile view
            print("Taking mobile screenshot...")
            await page.set_viewport_size({"width": 375, "height": 812})
            await page.screenshot(path="docs/screenshots/mobile_feed.png", full_page=True)

            print("Screenshots captured successfully!")

        except Exception as e:
            print(f"Error capturing screenshots: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    # Ensure docs/screenshots exists
    os.makedirs("docs/screenshots", exist_ok=True)
    asyncio.run(run())
