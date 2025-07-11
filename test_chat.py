#!/usr/bin/env python3
"""
Simple test script to verify chat functionality
"""

import requests
import json

def test_chat_api():
    """Test the chat API with various queries"""
    
    base_url = "http://localhost:5000"
    
    # Test queries
    test_queries = [
        "Show all jobs",
        "Active jobs",
        "Pending jobs",
        "All drivers",
        "Available vehicles",
        "Payment status",
        "Dashboard summary",
        "Help"
    ]
    
    print("Testing Chat API...")
    print("=" * 50)
    
    for query in test_queries:
        try:
            response = requests.post(
                f"{base_url}/api/chat",
                json={"message": query},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Query: '{query}'")
                print(f"Response: {data['response'][:100]}...")
                if data['data']:
                    print(f"Data: {len(data['data'])} records")
                print("-" * 30)
            else:
                print(f"❌ Query: '{query}' - Status: {response.status_code}")
                print(f"Error: {response.text}")
                print("-" * 30)
                
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to server. Make sure the Flask app is running.")
            break
        except Exception as e:
            print(f"❌ Error testing query '{query}': {str(e)}")
            print("-" * 30)

if __name__ == "__main__":
    test_chat_api() 