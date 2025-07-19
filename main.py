#!/usr/bin/env python3
import requests
import datetime
import json
import sys

def ping_server(url, server_name):
    """
    Ping a server and return detailed response information
    
    Args:
        url: The URL to ping
        server_name: Name of the server for logging
    
    Returns:
        dict: Response information
    """
    try:
        print(f"{datetime.datetime.now()}: Pinging {server_name} at {url}")
        
        # Make the request with timeout
        response = requests.get(url, timeout=30)
        
        # Get response details
        response_info = {
            "server": server_name,
            "url": url,
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "timestamp": datetime.datetime.now().isoformat(),
            "success": response.status_code == 200
        }
        
        # Try to parse JSON response
        try:
            response_data = response.json()
            response_info["response_data"] = response_data
        except json.JSONDecodeError:
            response_info["response_data"] = response.text
        
        # Print results
        if response.status_code == 200:
            print(f"✅ {server_name} is alive (Status: {response.status_code})")
            print(f"   Response time: {response_info['response_time']:.3f}s")
            
            # Print additional info if available
            if "response_data" in response_info and isinstance(response_info["response_data"], dict):
                data = response_info["response_data"]
                if "message" in data:
                    print(f"   Message: {data['message']}")
                if "uptime" in data:
                    print(f"   Uptime: {data['uptime']:.1f}s")
        else:
            print(f"⚠️ {server_name} returned unexpected status code: {response.status_code}")
            
        return response_info
        
    except requests.exceptions.Timeout:
        error_msg = f"❌ {server_name} request timed out after 30 seconds"
        print(error_msg)
        return {
            "server": server_name,
            "url": url,
            "error": "timeout",
            "timestamp": datetime.datetime.now().isoformat(),
            "success": False
        }
        
    except requests.exceptions.ConnectionError:
        error_msg = f"❌ {server_name} connection failed - server may be down"
        print(error_msg)
        return {
            "server": server_name,
            "url": url,
            "error": "connection_error",
            "timestamp": datetime.datetime.now().isoformat(),
            "success": False
        }
        
    except Exception as e:
        error_msg = f"❌ {server_name} error: {str(e)}"
        print(error_msg)
        return {
            "server": server_name,
            "url": url,
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat(),
            "success": False
        }

def ping_all_servers():
    """
    Ping both servers and provide summary
    """
    # Server configurations
    servers = [
        {
            "name": "Node.js API Server",
            "url": "https://make-it-rag.onrender.com/ping"  # Replace with your actual Node.js server URL
        },
        {
            "name": "Python AI Server", 
            "url": "https://make-it-rag-1.onrender.com/ping"
        }
    ]
    
    print("=" * 60)
    print("SERVER PING MONITORING")
    print("=" * 60)
    
    results = []
    
    # Ping each server
    for server in servers:
        result = ping_server(server["url"], server["name"])
        results.append(result)
        print()  # Add spacing between servers
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    successful_pings = sum(1 for r in results if r["success"])
    total_servers = len(results)
    
    print(f"Servers responding: {successful_pings}/{total_servers}")
    
    if successful_pings == total_servers:
        print("🎉 All servers are healthy!")
        return 0
    else:
        print("⚠️ Some servers are not responding")
        return 1

if __name__ == "__main__":
    try:
        exit_code = ping_all_servers()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nPing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1) 
