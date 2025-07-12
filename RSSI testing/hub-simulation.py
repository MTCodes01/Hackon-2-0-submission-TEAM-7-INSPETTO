import asyncio
import aiohttp

async def fetch_data(url, headers):
    async with aiohttp.ClientSession() as session:
        # Remove the incorrect params, credentials are handled through headers
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data

async def send_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers={"Content-Type": "application/json"}) as response:
            if response.status == 201:
                print("Data sent successfully")
            else:
                print(f"Failed to send data. Status: {response.status}")

async def main():
    source_url = "https://api-tracking.hard-softwerk.com/rssi-data/E4E1129BDB4D"  # Source API URL
    destination_url = "http://127.0.0.1:8000/api/hub-logs/"  # Destination API URL
    
    # Fix the headers - use proper Authorization header format
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNyZWVkZXZzczA1QGdtYWlsLmNvbSIsInVzZXJfdHlwZSI6IlN1cGVyIEFkbWluIiwib3JnIjoiSFNXIiwiaWF0IjoxNzUyMjk1MTg4LCJleHAiOjE3NTQ4ODcxODh9.zh2N0L1R-yT3hOKR8zZY_dholLhTulyg6Nzz19TrU4o",  # Changed from "auth" to "Authorization"
        "Content-Type": "application/json"  # Often required for APIs
    }
    
    # Configuration
    delay_seconds = 5  # How often to fetch data (in seconds)
    max_iterations = None  # Set to a number to limit iterations, or None for infinite
    
    iteration = 0
    
    while max_iterations is None or iteration < max_iterations:
        try:
            print(f"--- Iteration {iteration + 1} ---")
            
            # Fetch data from the source URL
            data = await fetch_data(source_url, headers)
            
            if data and 'error' not in data:
                print("Fetched data:", data)
                data_to_send = {
                    'timestamp': data['hubReadings'][0]['lastSeen'],
                    'hub': data['hubReadings'][0]['hubId'],
                    'chip': data['macAddress'],
                    'rssi': data['hubReadings'][0]['rssi'],
                }

                # Send the fetched data to the destination URL
                await send_data(destination_url, data_to_send)
            else:
                print("Error fetching data:", data)
                
        except Exception as e:
            print(f"Error in iteration {iteration + 1}: {e}")
        
        iteration += 1
        
        # Wait before next iteration (skip on last iteration if max_iterations is set)
        if max_iterations is None or iteration < max_iterations:
            print(f"Waiting {delay_seconds} seconds before next fetch...")
            await asyncio.sleep(delay_seconds)

if __name__ == "__main__":
    asyncio.run(main())