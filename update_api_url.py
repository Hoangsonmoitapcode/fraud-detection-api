#!/usr/bin/env python3
"""
Script to update API URL in documentation files after deployment
Usage: python update_api_url.py https://your-actual-api-url.up.railway.app
"""

import sys
import os
import re

def update_api_url(new_url):
    """Update API URL in all documentation files"""
    
    if not new_url.startswith('https://'):
        print("❌ URL must start with https://")
        return False
    
    # Remove trailing slash
    new_url = new_url.rstrip('/')
    
    # Files to update
    files_to_update = [
        'API_USAGE_GUIDE.md',
        'FOR_USERS.md',
        'DEPLOYMENT_STEPS.md',
        'DEPLOYMENT_SUMMARY.md'
    ]
    
    # URL patterns to replace
    patterns = [
        r'https://your-api-url\.up\.railway\.app',
        r'https://your-api-domain\.com',
        r'https://your-fraud-api\.railway\.app',
        r'https://your-url',
        r'your-api-url\.up\.railway\.app',
        r'your-api-domain\.com'
    ]
    
    updated_files = 0
    
    for filename in files_to_update:
        if not os.path.exists(filename):
            print(f"⚠️  File not found: {filename}")
            continue
            
        try:
            # Read file
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Replace all patterns
            for pattern in patterns:
                content = re.sub(pattern, new_url, content)
            
            # Write back if changed
            if content != original_content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Updated: {filename}")
                updated_files += 1
            else:
                print(f"📄 No changes needed: {filename}")
                
        except Exception as e:
            print(f"❌ Error updating {filename}: {e}")
    
    print(f"\n🎉 Updated {updated_files} files with new API URL: {new_url}")
    
    # Show next steps
    print("\n📋 Next steps:")
    print(f"1. Test your API: curl {new_url}/health")
    print(f"2. Check docs: {new_url}/docs")
    print(f"3. Share FOR_USERS.md with your users")
    print(f"4. Your API is ready at: {new_url}")
    
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python update_api_url.py https://your-actual-api-url.up.railway.app")
        print("\nExample:")
        print("python update_api_url.py https://fraud-detection-api-production-1234.up.railway.app")
        sys.exit(1)
    
    new_url = sys.argv[1]
    
    print(f"🔄 Updating API URL to: {new_url}")
    print("=" * 60)
    
    success = update_api_url(new_url)
    
    if success:
        print("\n✅ URL update completed successfully!")
    else:
        print("\n❌ URL update failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
