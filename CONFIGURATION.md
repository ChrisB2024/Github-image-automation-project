# Configuration Template

## URLs to Monitor

Copy and paste this template into `scripts/check_images.py` (line 12):

```python
# Direct image URLs
URLS = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.png",
    "https://cdn.example.com/photo.webp",
]

# Or use a configuration file approach:
# import json
# with open('config.json') as f:
#     config = json.load(f)
#     URLS = config['urls']
```

## GitHub Secrets Checklist

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `TWILIO_SID` | Account SID from Twilio dashboard | `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `TWILIO_AUTH` | Auth Token from Twilio dashboard | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `TWILIO_FROM` | Your Twilio phone number with country code | `+15551234567` |
| `TWILIO_TO` | Recipient phone number with country code | `+15559876543` |

## Schedule Options

Edit `.github/workflows/check_images.yml` (line 6):

```yaml
# Every 30 minutes (default)
- cron: "*/30 * * * *"

# Every 15 minutes
- cron: "*/15 * * * *"

# Every hour
- cron: "0 * * * *"

# Every 6 hours
- cron: "0 */6 * * *"

# Every day at 9 AM UTC
- cron: "0 9 * * *"

# Every weekday at 9 AM and 5 PM UTC
- cron: "0 9,17 * * 1-5"

# Every Monday at 8 AM UTC
- cron: "0 8 * * 1"
```

## SMS Message Customization

Edit `scripts/check_images.py` (around line 95):

```python
# Default message
msg = f"🔔 Image Monitor Alert!\n\nNew or updated images detected at:\n\n"
msg += "\n".join([f"• {url}" for url in changed])

# Compact message
msg = f"🔔 {len(changed)} image(s) changed: {', '.join(changed[:3])}"

# Detailed message with timestamp
from datetime import datetime
msg = f"🔔 Alert at {datetime.now().strftime('%I:%M %p')}\n\n"
msg += f"{len(changed)} changes detected:\n"
msg += "\n".join([f"{i+1}. {url}" for i, url in enumerate(changed)])

# Custom branding
msg = f"🖼️ [Your Brand] Image Update\n\n"
msg += "The following images have been updated:\n\n"
msg += "\n".join([f"→ {url}" for url in changed])
```

## Advanced Configuration

### Add Request Headers

For URLs requiring authentication or special headers:

```python
# In check_images.py, around line 67
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; ImageMonitor/1.0)",
    "Accept": "image/*",
    # Add authentication if needed:
    # "Authorization": "Bearer YOUR_TOKEN",
}

r = requests.get(url, timeout=30, headers=headers)
```

### Filter by Content Type

Only alert for specific image types:

```python
# After the request
content_type = r.headers.get('Content-Type', '')
if not content_type.startswith('image/'):
    print(f"  ⚠️ Not an image: {content_type}")
    continue
```

### Minimum File Size

Ignore tiny images (like tracking pixels):

```python
# After getting the content
if len(r.content) < 1024:  # Less than 1KB
    print(f"  ⚠️ File too small, skipping")
    continue
```

### Retry on Failure

Add retry logic for flaky connections:

```python
from time import sleep

max_retries = 3
for attempt in range(max_retries):
    try:
        r = requests.get(url, timeout=30)
        break
    except requests.exceptions.RequestException as e:
        if attempt < max_retries - 1:
            sleep(2 ** attempt)  # Exponential backoff
            continue
        raise
```

## Testing Configuration

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Test without SMS
python test_local.py
# Choose option 1

# Test with SMS (requires credentials in test_local.py)
python test_local.py
# Choose option 2
```

## Environment Variables for Local Testing

Create `.env` file (not committed to git):

```bash
TWILIO_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_FROM=+15551234567
TWILIO_TO=+15559876543
```

Then use python-dotenv:

```python
# At top of check_images.py
from dotenv import load_dotenv
load_dotenv()
```

And add to requirements.txt:
```
python-dotenv>=1.0.0
```

---

**Tip**: Start with a few test URLs and the default 30-minute schedule, then customize once everything works!
