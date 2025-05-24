#!/usr/bin/env python3
import os
import sys
import requests
from dotenv import load_dotenv


load_dotenv()  
CF_API_TOKEN = os.getenv('CF_API_TOKEN')
CF_ZONE_ID   = os.getenv('CF_ZONE_ID')
API_BASE_URL = os.getenv('API_BASE_URL')
CF_DOMAIN = os.getenv('CF_DOMAIN')



def get_public_ip():
    for url in ("https://api.ipify.org?format=json",
                "https://icanhazip.com"):
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            if "json" in r.headers.get("Content-Type", ""):
                return r.json().get("ip")
            return r.text.strip()
        except Exception:
            continue
    raise RuntimeError("Could not determine public IP")

def update_cloudflare_dns():
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type":  "application/json",
    }
    params = {"type": "A", "name": CF_DOMAIN}
    r = requests.get(f"{API_BASE_URL}/zones/{CF_ZONE_ID}/dns_records", headers=headers, params=params)
    data = r.json()
    if not data.get("success"):
        print("Failed to fetch DNS records:", data)
        sys.exit(1)
    results = data.get("result", [])
    public_ip = get_public_ip()
    print(f"Found public IP to be: {public_ip}")

    if len(results) != 0:
        rec = results[0]
        if rec["content"] == public_ip:
            print(f"No change needed; '{CF_DOMAIN}' is already {public_ip}.")
            sys.exit(0)

        update_payload = {
            "type":    "A",
            "name":    CF_DOMAIN,
            "content": public_ip,
            "ttl":     rec.get("ttl", 1),      
            "proxied": rec.get("proxied", False) 
        }
        u = requests.put(f"{API_BASE_URL}/zones/{CF_ZONE_ID}/dns_records/{rec['id']}",
                        headers=headers, json=update_payload)
        udata = u.json()
        if udata.get("success"):
            print(f"Updated '{CF_DOMAIN}' → {public_ip}")
        else:
            print("Update failed:", udata)
            sys.exit(1)
    else:
        create_payload = {
            "type":    "A",
            "name":    CF_DOMAIN,
            "content": "127.0.0.1",
            "ttl":     1,        # 1 = 'automatic'
            "proxied": False     # change to True if you want Cloudflare proxy
        }
        c = requests.post(f"{API_BASE_URL}/zones/{CF_ZONE_ID}/dns_records",
                        headers=headers, json=create_payload)
        cdata = c.json()
        if cdata.get("success"):
            print(f"Created A record '{CF_DOMAIN}' → {"127.0.0.1"}")
        else:
            print("Creation failed:", cdata)
            sys.exit(1)
if __name__ == "__main__":
    update_cloudflare_dns()