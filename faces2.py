import requests
import webbrowser

# Unsplash API parameters
params = {
    'query': 'mussolini',  # Adjust the query to your needs
    'per_page': 1,  # Increase the number of results to display
}

# Add your Unsplash API access key to the Authorization header
headers = {
    'Authorization': 'Client-ID NmSzB8-_HJLvigbY75Dey7E2renuTenVNrJwNqYkJQg',
}

try:
    # Make the API request
    response = requests.get('https://api.unsplash.com/search/photos', params=params, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if there are any results
        if data['results']:
            print('Choose the correct image:')
            
            # Display the results with indices
            for i, result in enumerate(data['results']):
                print(f"{i + 1}. {result['urls']['regular']}")

            # Prompt the user to enter the index of the desired image
            selected_index = int(input('Enter the number corresponding to the correct image: '))
            
            # Open the URL of the selected result in the default web browser
            webbrowser.open(data['results'][selected_index - 1]['urls']['regular'])
        else:
            print('No results found.')
    else:
        print('Failed to make API request. Status code:', response.status_code)

except Exception as e:
    print('An error occurred:', str(e))
