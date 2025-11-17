"""
Image Monitor Script
Checks specified URLs for new image uploads and sends SMS notifications via Twilio
"""

import os
import json
import hashlib
import requests
from twilio.rest import Client

# List of URLs to monitor
# Add your image URLs here
URLS = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/folder/photo.png",
    # Add more URLs here
]

STATE_FILE = "scripts/state.json"

def load_state():
    """Load the previous state (image hashes) from file"""
    if not os.path.exists(STATE_FILE):
        return {}
    
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: state.json is corrupted. Starting fresh.")
        return {}

def save_state(state):
    """Save the current state (image hashes) to file"""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def hash_content(content):
    """Generate SHA-256 hash of content"""
    return hashlib.sha256(content).hexdigest()

def send_sms(message):
    """Send SMS notification via Twilio"""
    try:
        client = Client(
            os.environ["TWILIO_SID"],
            os.environ["TWILIO_AUTH"]
        )

        message_result = client.messages.create(
            body=message,
            from_=os.environ["TWILIO_FROM"],
            to=os.environ["TWILIO_TO"]
        )
        
        print(f"SMS sent successfully! SID: {message_result.sid}")
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

def check_urls():
    """Check all URLs for changes and send notifications"""
    state = load_state()
    changed = []
    errors = []

    print(f"Checking {len(URLS)} URLs for changes...\n")

    for url in URLS:
        print(f"Checking: {url}")
        try:
            # Set timeout to avoid hanging
            r = requests.get(url, timeout=30)
            
            if r.status_code != 200:
                error_msg = f"Failed with status {r.status_code}"
                print(f"  ❌ {error_msg}")
                errors.append(f"{url}: {error_msg}")
                continue

            # Calculate hash of the content
            content_hash = hash_content(r.content)
            
            # Check if this is a new image or if content changed
            if url not in state:
                print(f"  🆕 New URL detected!")
                changed.append(url)
                state[url] = content_hash
            elif state[url] != content_hash:
                print(f"  🔄 Content changed!")
                changed.append(url)
                state[url] = content_hash
            else:
                print(f"  ✓ No changes")

        except requests.exceptions.Timeout:
            error_msg = "Request timeout"
            print(f"  ❌ {error_msg}")
            errors.append(f"{url}: {error_msg}")
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            print(f"  ❌ Error: {error_msg}")
            errors.append(f"{url}: {error_msg}")
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"  ❌ {error_msg}")
            errors.append(f"{url}: {error_msg}")

    # Send SMS if any changes detected
    if changed:
        print(f"\n{'='*50}")
        print(f"📸 {len(changed)} image(s) changed or newly detected!")
        print(f"{'='*50}\n")
        
        msg = f"🔔 Image Monitor Alert!\n\nNew or updated images detected at:\n\n"
        msg += "\n".join([f"• {url}" for url in changed])
        
        if errors:
            msg += f"\n\n⚠️ {len(errors)} error(s) occurred during check."
        
        send_sms(msg)
    else:
        print(f"\n{'='*50}")
        print("✅ No changes detected")
        print(f"{'='*50}\n")

    # Report errors if any
    if errors:
        print(f"\n⚠️ Errors encountered:")
        for error in errors:
            print(f"  • {error}")

    # Save updated state
    save_state(state)
    print(f"\n✓ State saved to {STATE_FILE}")


if __name__ == "__main__":
    print("="*50)
    print("IMAGE MONITOR - Starting Check")
    print("="*50)
    print()
    
    check_urls()
    
    print()
    print("="*50)
    print("IMAGE MONITOR - Check Complete")
    print("="*50)
