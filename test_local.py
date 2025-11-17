#!/usr/bin/env python3
"""
Local Test Script for Image Monitoring
Use this to test the image checker locally before deploying to GitHub Actions
"""

import os
import sys

# Set test environment variables
# Replace these with your actual Twilio credentials for testing
os.environ["TWILIO_SID"] = "your_twilio_sid_here"
os.environ["TWILIO_AUTH"] = "your_twilio_auth_token_here"
os.environ["TWILIO_FROM"] = "+15551234567"  # Your Twilio number
os.environ["TWILIO_TO"] = "+15559876543"    # Your phone number

def test_without_sms():
    """Test the script without actually sending SMS"""
    print("🧪 Running test WITHOUT sending SMS...\n")
    
    # Temporarily replace the send_sms function
    import scripts.check_images as checker
    
    original_send_sms = checker.send_sms
    
    def mock_send_sms(message):
        print("\n" + "="*50)
        print("📱 MOCK SMS (not actually sent):")
        print("="*50)
        print(message)
        print("="*50 + "\n")
        return True
    
    checker.send_sms = mock_send_sms
    
    try:
        checker.check_urls()
    finally:
        checker.send_sms = original_send_sms

def test_with_sms():
    """Test the script including actual SMS sending"""
    print("🧪 Running test WITH actual SMS...\n")
    
    response = input("This will send a real SMS. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Test cancelled.")
        return
    
    import scripts.check_images as checker
    checker.check_urls()

def main():
    print("="*60)
    print("IMAGE MONITOR - LOCAL TEST UTILITY")
    print("="*60)
    print()
    print("Choose test mode:")
    print("1. Test WITHOUT sending SMS (recommended)")
    print("2. Test WITH sending actual SMS")
    print("3. Exit")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        test_without_sms()
    elif choice == "2":
        # Check if credentials are set
        if (os.environ["TWILIO_SID"] == "your_twilio_sid_here" or
            os.environ["TWILIO_AUTH"] == "your_twilio_auth_token_here"):
            print("\n⚠️  Error: Please update Twilio credentials in this file first!")
            sys.exit(1)
        test_with_sms()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
