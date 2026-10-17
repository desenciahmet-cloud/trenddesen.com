import urllib.request
import time
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://trenddesen.com/"
marker = "runway-sticky-container"

print(f"Waiting for live deployment with marker '{marker}' on trenddesen.com...")
for attempt in range(1, 40):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (DeploymentChecker)"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            if marker in content:
                print(f"DEPLOYMENT ACTIVE on attempt {attempt}! (Found marker)")
                break
            else:
                print(f"Attempt {attempt}: Marker not yet live. Waiting 10s...")
    except Exception as e:
        print(f"Attempt {attempt}: Request error: {e}")
    time.sleep(10)
