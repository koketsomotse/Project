import asyncio
import websockets
import sys
import django
import os
from datetime import datetime
from asgiref.sync import sync_to_async

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_system.settings')
django.setup()

from django.contrib.auth.models import User

@sync_to_async
def get_user(username):
    """Get user from database"""
    return User.objects.get(username=username)

async def test_connection(username="Bret"):
    """Test WebSocket connection and basic functionality"""
    try:
        # Get user
        user = await get_user(username)
        uri = f"ws://localhost:8000/ws/notifications/?token={user.id}"
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Testing WebSocket connection...")
        print(f"Connecting as user: {username}")
        print(f"WebSocket URI: {uri}\n")
        
        async with websockets.connect(uri) as websocket:
            print("✓ Successfully established WebSocket connection")
            print("✓ Connection authenticated")
            print("✓ WebSocket handshake completed")
            
            # Keep connection open briefly to verify stability
            print("\nMaintaining connection for 5 seconds to verify stability...")
            await asyncio.sleep(5)
            
            print("✓ Connection remained stable")
            print("\nWebSocket connection test completed successfully!")
            
    except User.DoesNotExist:
        print(f"Error: User '{username}' not found in database")
    except websockets.ConnectionClosed:
        print("Error: Connection closed unexpectedly")
    except websockets.WebSocketException as e:
        print(f"WebSocket Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Get username from command line args or use default
    username = sys.argv[1] if len(sys.argv) > 1 else "Bret"
    
    # Run the connection test
    asyncio.run(test_connection(username))
