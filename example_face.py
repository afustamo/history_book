import requests
import shutil

# Replace 'YOUR_ACCESS_KEY' with your actual Unsplash API access key
access_key = 'NmSzB8-_HJLvigbY75Dey7E2renuTenVNrJwNqYkJQg'
search_query = 'einstein'

# Make the API request
url = f'https://api.unsplash.com/search/photos?query={search_query}&client_id={access_key}'
response = requests.get(url)
data = response.json()

# Check if the request was successful
if response.status_code == 200:
    # Check if there are results
    if 'results' in data and data['results']:
        # Extract the URL of the first image
        image_url = data['results'][0]['urls']['regular']

        # Make a request to download the image
        image_response = requests.get(image_url, stream=True)

        # Check if the request was successful
        if image_response.status_code == 200:
            # Open a local file with the name 'einstein.jpg' for writing in binary mode
            with open('einstein.jpg', 'wb') as f:
                # Write the content of the response to the file
                image_response.raw.decode_content = True
                shutil.copyfileobj(image_response.raw, f)

            print("Image downloaded successfully.")
        else:
            print(f"Failed to download image. Status code: {image_response.status_code}")
    else:
        print("No results found.")
else:
    print(f"Failed to make API request. Status code: {response.status_code}")