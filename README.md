# Cloudflare A-Record Auto-Updater

A small Python utility that:

1. Fetches your public IP  
2. Creates or updates an A-record in Cloudflare for a given subdomain  
3. Can be scheduled via cron to run every 10 minutes and at reboot

---


## ⚙️ Installation

**Clone this repo**  
```bash
   git clone git@github.com:jansoft54/FreeDynDNS.git
   cd FreeDynDNS
   chmod +x setup_cron.sh
   ```

**Create & activate a virtual environment & install dependencies**
```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
```
## 🔐 Configuration
**Create a ```.env``` file in the project root**
```bash
# .env
    CF_API_TOKEN=eyJhbGciOiJIUzI1Ni…      # your scoped Cloudflare API token
    CF_ZONE_ID=0123456789abcdef…          # your Cloudflare Zone ID
    API_BASE_URL=https://api.cloudflare.com/client/v4
    CF_DOMAIN=sub.yourdomain.com          # the subdomain to update, e.g. "foo.example.com"
```
## 🚀 Usage
```bash
./setup_cron.sh /full/path/to/FreeDynDNS/main.py /full/path/to/FreeDynDNS/main.log
```


