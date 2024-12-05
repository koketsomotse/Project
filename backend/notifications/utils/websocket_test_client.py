import asyncio
import websockets
import json
import sys
import django
import os
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_system.settings')
django.setup()

# Import Django models
from django.contrib.auth.models import User
from notifications.models import Notifications

async def connect_websocket(username="Bret"):
    """
    Connect to the WebSocket server and listen for notifications.
    
    Args:
        username (str): Username to connect with (defaults to "Bret")
    """
    # Get the user's auth token (in a real app, this would be from login)
    user = User.objects.get(username=username)
    
    uri = f"ws://localhost:8000/ws/notifications/?token={user.id}"
    
    print(f"\nConnecting to WebSocket server as user: {username}")
    print("Waiting for notifications... (Press Ctrl+C to exit)\n")
    
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    # Wait for messages
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    # Print received notification
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] New notification received:")
                    print(f"Title: {data.get('title', 'No title')}")
                    print(f"Message: {data.get('message', 'No message')}")
                    print(f"Type: {data.get('notification_type', 'No type')}\n")
                    
                    # Send read acknowledgment
                    if 'id' in data:
                        await websocket.send(json.dumps({
                            'type': 'mark_read',
                            'notification_id': data['id']
                        }))
                
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed by server. Reconnecting...")
                    break
                except Exception as e:
                    print(f"Error: {str(e)}")
                    break
    
    except KeyboardInterrupt:
        print("\nDisconnecting from WebSocket server...")
    except Exception as e:
        print(f"\nError connecting to WebSocket server: {str(e)}")

if __name__ == "__main__":
    # Get username from command line args or use default
    username = sys.argv[1] if len(sys.argv) > 1 else "Bret"
    
    # Run the WebSocket client
    asyncio.run(connect_websocket(username))
