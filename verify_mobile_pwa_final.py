from playwright.sync_api import sync_playwright

def verify_mobile_pwa():
    with sync_playwright() as p:
        # Simulate an iPhone 12 Pro
        iphone = p.devices['iPhone 12 Pro']
        browser = p.chromium.launch()
        context = browser.new_context(**iphone)
        page = context.new_page()

        try:
            print("Accessing http://127.0.0.1:5000/ ...")
            page.goto("http://127.0.0.1:5000/")

            # Check for PWA manifest link
            manifest_link = page.locator('link[rel="manifest"]')
            if manifest_link.count() > 0:
                print("SUCCESS: Manifest link found.")
            else:
                print("FAILED: Manifest link not found.")

            # Check for Service Worker registration script
            content = page.content()
            if "serviceWorker.register" in content:
                print("SUCCESS: Service Worker registration script found.")
            else:
                print("FAILED: Service Worker registration script not found.")

            # Verify Service Worker URL in registration
            if "/sw.js" in content:
                print("SUCCESS: Service Worker registered at root path.")
            else:
                print("FAILED: Service Worker path incorrect in registration.")

            page.screenshot(path="verification_mobile_pwa_final.png")
            print("Screenshot saved to verification_mobile_pwa_final.png")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_mobile_pwa()
