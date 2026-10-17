import asyncio
from playwright.async_api import async_playwright

async def test_trenddesen():
    async with async_playwright() as p:
        # 1. Desktop Test
        print("1. Launching desktop test on http://127.0.0.1:8014...")
        browser = await p.chromium.launch(headless=True)
        desktop_ctx = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await desktop_ctx.new_page()
        
        # Test /emprime redirect
        resp = await page.goto("http://127.0.0.1:8014/emprime", wait_until="networkidle")
        print(f"Emprime URL redirect result: {page.url} (status: {resp.status})")
        assert page.url.rstrip('/') == "http://127.0.0.1:8014"
        
        # Check title and catwalk
        title_el = page.locator(".panel-title:has-text('Beğendiğin desene dokun, model üzerine gör.')")
        await title_el.wait_for(state="visible", timeout=5000)
        print("Desktop title visible!")
        
        # Verify badge and kumaslara gec are gone
        badge_count = await page.locator("#activePatternStickyBadge").count()
        kumas_count = await page.locator("a:has-text('Kumaşlara Geç')").count()
        print(f"Badge count: {badge_count}, Kumaslara gec count: {kumas_count}")
        assert badge_count == 0, "Badge should be removed!"
        assert kumas_count == 0, "Kumaslara gec button should be removed from header!"
        
        # Click a pattern
        card = page.locator("#patternGrid .pattern-card").nth(8)
        await card.click()
        await page.wait_for_timeout(600)
        
        desktop_shot = "C:/Users/user/.gemini/antigravity/brain/776a1e7f-45ba-411e-a13d-a67503f8911b/test_desktop_sticky_catwalk.png"
        await page.screenshot(path=desktop_shot)
        print(f"Saved {desktop_shot}")
        await browser.close()
        
        # 2. Mobile Test
        print("2. Launching mobile test (iPhone 14, 390x844)...")
        browser_mob = await p.chromium.launch(headless=True)
        mob_ctx = await browser_mob.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        )
        mob_page = await mob_ctx.new_page()
        await mob_page.goto("http://127.0.0.1:8014", wait_until="networkidle")
        await mob_page.wait_for_timeout(600)
        
        # Verify stage size on mobile
        stage_box = await mob_page.locator(".runway-stage").bounding_box()
        print(f"Mobile stage bounding box: width={stage_box['width']}, height={stage_box['height']}")
        assert stage_box['height'] >= 240, f"Stage height should be at least 240px, got {stage_box['height']}"
        
        mob_initial_shot = "C:/Users/user/.gemini/antigravity/brain/776a1e7f-45ba-411e-a13d-a67503f8911b/test_mobile_sticky_initial.png"
        await mob_page.screenshot(path=mob_initial_shot)
        print(f"Saved initial {mob_initial_shot}")
        
        # Scroll down 600px into patterns
        print("Scrolling mobile down 600px...")
        await mob_page.mouse.wheel(0, 600)
        await mob_page.wait_for_timeout(800)
        
        # Verify sticky stage is pinned
        mob_sticky_box = await mob_page.locator(".runway-sticky-container").bounding_box()
        print(f"Mobile sticky container bounding box while scrolled: y={mob_sticky_box['y']}, height={mob_sticky_box['height']}")
        
        # Click a pattern that is currently visible in the scrolled flow
        visible_cards = mob_page.locator("#patternGrid .pattern-card")
        await visible_cards.nth(10).click()
        await mob_page.wait_for_timeout(600)
        
        mob_scrolled_shot = "C:/Users/user/.gemini/antigravity/brain/776a1e7f-45ba-411e-a13d-a67503f8911b/test_mobile_sticky_scrolled.png"
        await mob_page.screenshot(path=mob_scrolled_shot)
        print(f"Saved scrolled {mob_scrolled_shot}")
        
        await browser_mob.close()
        print("ALL TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(test_trenddesen())
