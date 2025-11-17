# 📸 GitHub Image Automation Project

Automatically monitor specified URLs for new image uploads and receive SMS notifications via Twilio when changes are detected.

## 🎯 Overview

This project uses GitHub Actions to:
- Check a list of URLs every 30 minutes for new or updated images
- Track image changes using SHA-256 content hashing
- Send SMS alerts via Twilio when changes are detected
- Maintain state across checks even though GitHub Actions runners are ephemeral

## ✨ Features

- ⏰ **Automatic scheduling**: Runs every 30 minutes via GitHub Actions
- 🔍 **Smart detection**: Uses content hashing to detect actual changes
- 📱 **SMS notifications**: Instant alerts via Twilio
- 💾 **Persistent state**: Tracks seen images across workflow runs
- 🔒 **Secure**: All credentials stored as GitHub Secrets
- 📊 **Logging**: Detailed output for each check
- 🎯 **Manual trigger**: Can be triggered manually from GitHub UI

## 📋 Requirements

- A GitHub account (free tier works fine)
- A Twilio account ([sign up for free trial](https://www.twilio.com/try-twilio))
- URLs of images you want to monitor

## 🚀 Setup Instructions

### 1. Clone or Create This Repository

```bash
git clone https://github.com/YOUR_USERNAME/Github-image-automation-project.git
cd Github-image-automation-project
```

Or create a new repository with these files.

### 2. Get Twilio Credentials

1. Sign up at [twilio.com](https://www.twilio.com/try-twilio)
2. Go to your [Twilio Console](https://console.twilio.com/)
3. Note down:
   - **Account SID** (found on dashboard)
   - **Auth Token** (found on dashboard)
   - **Twilio Phone Number** (get one from Phone Numbers → Manage → Buy a number)
   - **Your Phone Number** (where you want to receive SMS)

### 3. Configure GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add these four secrets:

| Secret Name | Value | Example |
|------------|-------|---------|
| `TWILIO_SID` | Your Account SID | `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `TWILIO_AUTH` | Your Auth Token | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `TWILIO_FROM` | Your Twilio phone number | `+15551234567` |
| `TWILIO_TO` | Your personal phone number | `+15559876543` |

> ⚠️ **Important**: Phone numbers must include country code (e.g., `+1` for US)

### 4. Configure URLs to Monitor

Edit `scripts/check_images.py` and update the `URLS` list:

```python
URLS = [
    "https://example.com/gallery/photo1.jpg",
    "https://mysite.com/uploads/latest.png",
    "https://cdn.example.com/images/banner.jpg",
    # Add your URLs here
]
```

### 5. Push to GitHub

```bash
git add .
git commit -m "Configure image monitoring URLs"
git push origin main
```

### 6. Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. If prompted, click **"I understand my workflows, go ahead and enable them"**
3. The workflow will now run automatically every 30 minutes

## 🎮 Usage

### Automatic Mode

Once set up, the system runs automatically:
- Checks run every 30 minutes
- You'll receive SMS when new/changed images are detected
- State is saved after each check

### Manual Trigger

To run a check immediately:

1. Go to **Actions** tab
2. Click **"Check Images Every 30 Minutes"** workflow
3. Click **"Run workflow"** button
4. Click the green **"Run workflow"** button in the dropdown

### View Logs

1. Go to **Actions** tab
2. Click on any workflow run
3. Click on the **"check"** job to see detailed logs

## 📁 Project Structure

```
Github-image-automation-project/
├── .github/
│   └── workflows/
│       └── check_images.yml       # GitHub Actions workflow
├── scripts/
│   ├── check_images.py            # Main Python script
│   └── state.json                 # Tracks seen images (auto-updated)
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore patterns
└── README.md                      # This file
```

## 🔧 How It Works

1. **Scheduling**: GitHub Actions cron triggers the workflow every 30 minutes
2. **Fetching**: Script downloads content from each configured URL
3. **Hashing**: Calculates SHA-256 hash of the content
4. **Comparison**: Compares with previous hash stored in `state.json`
5. **Detection**: If hash differs or URL is new, marks as changed
6. **Notification**: Sends SMS via Twilio with list of changed URLs
7. **State Update**: Saves new hashes and commits back to repository

## 🛠️ Customization

### Change Check Frequency

Edit `.github/workflows/check_images.yml`:

```yaml
schedule:
  - cron: "*/15 * * * *"  # Every 15 minutes
  # - cron: "0 * * * *"   # Every hour
  # - cron: "0 9,17 * * *" # 9 AM and 5 PM daily
```

### Customize SMS Message

Edit `scripts/check_images.py`, line ~95:

```python
msg = f"🔔 Custom Alert!\n\nImages changed at:\n\n"
msg += "\n".join([f"• {url}" for url in changed])
```

### Add Request Headers

If URLs require authentication:

```python
headers = {
    "User-Agent": "Mozilla/5.0",
    "Authorization": "Bearer YOUR_TOKEN"
}
r = requests.get(url, timeout=30, headers=headers)
```

## 🐛 Troubleshooting

### Workflow Not Running

- Check that Actions are enabled in repo settings
- Verify the workflow file is in `.github/workflows/`
- Check the Actions tab for error messages

### No SMS Received

- Verify all Twilio secrets are correctly set
- Check Twilio console for error messages
- Ensure phone numbers include country code (e.g., `+1`)
- Verify Twilio account has sufficient credits

### False Positives

If you get notifications even when images haven't changed:
- The image might be dynamically generated
- Server might add timestamps or metadata
- Consider using image comparison instead of content hashing

### State Not Persisting

- Ensure the workflow has `contents: write` permission
- Check that git commit step completes successfully
- Review workflow logs for push errors

## 📊 Monitoring & Logs

Each workflow run provides:
- ✅ Successfully checked URLs
- 🆕 Newly detected URLs
- 🔄 Changed content
- ❌ Errors (timeouts, 404s, etc.)
- 📨 SMS delivery confirmation

## 🔐 Security Best Practices

- ✅ Never commit Twilio credentials to code
- ✅ Use GitHub Secrets for all sensitive data
- ✅ Regularly rotate Twilio Auth Token
- ✅ Use Twilio's webhook validation if extending this project
- ✅ Review GitHub Actions logs regularly

## 💡 Advanced Ideas

### Monitor Entire Directories

Modify script to parse HTML directory listings and check all images:

```python
from bs4 import BeautifulSoup

def get_images_from_directory(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return [img['src'] for img in soup.find_all('img')]
```

### Image Metadata Comparison

Instead of hashing entire content, check image dimensions or EXIF:

```python
from PIL import Image
import io

img = Image.open(io.BytesIO(r.content))
metadata = f"{img.size}_{img.format}"
```

### Multiple Notification Channels

Add email, Slack, Discord, or webhooks alongside SMS.

## 📄 License

MIT License - Feel free to use and modify for your needs.

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📞 Support

- Check [GitHub Actions documentation](https://docs.github.com/actions)
- Review [Twilio Python SDK docs](https://www.twilio.com/docs/libraries/python)
- Open an issue in this repository

---

**Made with ❤️ for automated image monitoring**
