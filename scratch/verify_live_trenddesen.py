import asyncio
from playwright.async_api import async_playwright

async def verify_live_trenddesen():
    async with async_playwright() as p:
        # 1. Desktop Verification
        print("1. Launching desktop browser for https://trenddesen.com...")
        browser = await p.chromium.launch(headless=True)
        desktop_ctx = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await desktop_ctx.new_page()
        
        await page.goto("https://trenddesen.com", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Scroll down 800px into the patterns
        print("Scrolling desktop down 800px...")
        await page.mouse.wheel(0, 800)
        await page.wait_for_timeout(1000)
        
        # Click a pattern
        cards = page.locator("#patternGrid .pattern-card")
        await cards.nth(7).click()
        await page.wait_for_timeout(800)
        
        desktop_shot = "C:/Users/user/.gemini/antigravity/brain/776a1e7f-45ba-411e-a13d-a67503f8911b/live_trenddesen_desktop.png"
        await page.screenshot(path=desktop_shot)
        print(f"Desktop screenshot saved to {desktop_shot}")
        await browser.close()
        
        # 2. Mobile Verification (iPhone 14, 390x844)
        print("2. Launching mobile browser (iPhone 14, 390x844)...")
        browser_mob = await p.chromium.launch(headless=True)
        mob_ctx = await browser_mob.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        )
        mob_page = await mob_ctx.new_page()
        await mob_page.goto("https://trenddesen.com", wait_until="networkidle")
        await mob_page.wait_for_timeout(1000)
        
        # Scroll down 600px into patterns
        print("Scrolling mobile down 600px into patterns...")
        await mob_page.mouse.wheel(0, 600)
        await mob_page.wait_for_timeout(1000)
        
        # Click a pattern
        mob_cards = mob_page.locator("#patternGrid .pattern-card")
        await mob_cards.nth(9).click()
        await mob_page.wait_for_timeout(800)
        
        mob_shot = "C:/Users/user/.gemini/antigravity/brain/776a1e7f-45ba-411e-a13d-a67503f8911b/live_trenddesen_mobile.png"
        await mob_page.screenshot(path=mob_shot)
        print(f"Mobile screenshot saved to {mob_shot}")
        await browser_mob.close()
        
        print("LIVE VERIFICATION COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(verify_live_trenddesen())
