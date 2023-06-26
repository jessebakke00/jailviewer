import requests

endpoint = "http://localhost:8000/api/inmates/"

get_response = requests.post(endpoint, json={
  'book_id':'2',
  'first_name':'Jesse',
  'middle_name':'Cole',
  'last_name': 'Bakke',
  'race': 'W',
  'sex':'M',
  'booking_date':'05/01/2023',
  'release_date':'05/02/2023'
  })

print(get_response.json())