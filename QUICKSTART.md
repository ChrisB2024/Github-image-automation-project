# Quick Setup Guide

## ⚡ 5-Minute Setup

### Step 1: Get Twilio Credentials (2 minutes)

1. Go to [twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Sign up (free trial gives you credit)
3. From your dashboard, copy:
   - Account SID
   - Auth Token
4. Get a phone number: **Phone Numbers → Manage → Buy a number**

### Step 2: Configure GitHub Secrets (1 minute)

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** four times to add:

```
TWILIO_SID       → Your Account SID
TWILIO_AUTH      → Your Auth Token
TWILIO_FROM      → +15551234567 (your Twilio number)
TWILIO_TO        → +15559876543 (your phone number)
```

### Step 3: Add Your URLs (1 minute)

Edit `scripts/check_images.py`, line 12:

```python
URLS = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
]
```

### Step 4: Push & Deploy (1 minute)

```bash
git add .
git commit -m "Initial setup"
git push origin main
```

### Step 5: Enable & Test

1. Go to **Actions** tab
2. Click **"Check Images Every 30 Minutes"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Watch it run!

## ✅ Verification

You should receive an SMS within ~1 minute because all URLs are new on first run.

## 🎯 Next Steps

- Monitor the Actions tab for automatic runs every 30 minutes
- Check your SMS when images change
- Review workflow logs for detailed information

## 🆘 Common Issues

**No SMS received?**
- Check Twilio console for delivery status
- Verify phone numbers include country code (+1 for US)
- Check GitHub Actions logs for errors

**Workflow not running?**
- Enable Actions in repo Settings
- Check workflow file syntax
- Verify cron expression

**State not saving?**
- Ensure workflow has `contents: write` permission
- Check git commit step in logs

---

Need help? Check the full README.md or open an issue!
