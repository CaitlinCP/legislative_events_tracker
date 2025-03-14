import os
import requests
import time
import json

API_KEY = os.environ["OPEN_STATES_API_KEY"]

class fetchBills():
    """
    Generates an API Key to pull bill information from the Open States API.
    """
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v3.openstates.org/bills?"

    def make_bills_request(self, state, session, per_page, page, *args):
        # if args:
        #     # Filter which fields are returned by the API
        #     included = "&include=" + "&include=".join(args)
    
        response = requests.get(self.base_url, {'apikey': API_KEY, 'page': page, 
                                                'jurisdiction': state, 'per_page': per_page, 
                                                'included': args, 'session': session})

        if response.status_code in (400, 422):
            raise ValueError(response.json())

        elif response.status_code == '504':
            raise TimeoutError(response.json())
        
        return response
    
    def pull_bills(self, state, session, per_page, count, *args):
        results = []
        page = 1

        print("Pulling bills from page 1")

        # Make initial response to test API availability, determine
        # max number of pages to pull
        initial_response = self.make_bills_request(
            state, session, per_page, page, args)

        if initial_response.status_code == 200:

            max_pages = initial_response.json()['pagination']['max_page']
            results.extend(initial_response.json()['results'])

            pages_to_pull = count / per_page

            timeout_errors = 0

            page += 1

            while  page <= pages_to_pull and page <= max_pages:

                print(f"Pulling bills from page {page}")

                if timeout_errors == 5:
                    print("Maximum number of timeout errors exceeded.")
                    break

                try:
                    response = self.make_bills_request(state, session, per_page, page, args)
                    page += 1

                    # If there's been a successful pull, 
                    # reset timeout errors counter

                    timeout_errors = 0
                    results.extend(response.json()['results'])
                
                except TimeoutError:
                    print("Timeout error. Waiting 5 seconds.")
                    timeout_errors += 1
                    time.sleep(5)
                    continue

                time.sleep(1)

        else:
            raise Exception(initial_response.json())
        
        return results


    def pull_bill_data(self, filepath):
        
        with open(filepath, 'r') as f:
            json_string = f.read()
            data = json.loads(json_string)
        
        for bill in data:
            url = bill['openstates_url']
            
            yield url


    def write_results(self, results, filepath):
        with open(filepath, 'w') as f:
            json_as_str = json.dumps(results)
            f.write(json_as_str)

class fetchEvents():
    """
    Generates an API Key to pull event information from the Open States API.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v3.openstates.org/events?"
    
    def make_events_request(self, state, before, after, per_page, page, *args):
        """
        https://v3.openstates.org/events?jurisdiction=Colorado&deleted=false&before=04-13-2025&after=03-14-2025&require_bills=false&include=links&include=sources&include=media&include=documents&include=participants&include=agenda&page=1&per_page=20
        """
        
        response = requests.get(self.base_url, {'apikey': API_KEY, 'page':page,
                                    'jurisdiction':state, 'per_page': per_page,
                                    'included': args, 'before': before, 'after': after, 
                                    'require_bills':'false','include':['links','sources','media','documents','participants','agenda']})

        if response.status_code in (400,422):
            raise ValueError(response.json())
        
        elif response.status_code == '504':
            raise TimeoutError(response.json())

        return response

    def pull_events(self, state, before, after, count=100, per_page=20, *args):
        results = []
        page = 1

        print("Pulling Events from page 1")

        # Make initial response to test API availability, determine
        # max number of pages to pull

        initial_response = self.make_events_request(
            state, before, after, per_page, page, args
        )

        if initial_response.status_code == 200:
            
            max_pages = initial_response.json()['pagination']['max_page']
            results.extend(initial_response.json()['results'])

            pages_to_pull = count / per_page

            timeout_errors = 0

            page += 1

            while page <= pages_to_pull and page <= max_pages:

                print(f"Pulling bills from page {page}")

                if timeout_errors >= 5:
                    print("Maximum number of timeout erros exceeded")
                    break

                try:
                    response = self.make_events_request(state, before, after, per_page, page, args)
                    page += 1

                    # If there's been a successful pull, 
                    # reset timeout errors counter

                    timeout_errors = 0
                    results.extend(response.json()['results'])
                
                except TimeoutError:
                    print("Timeout error. Waiting 5 seconds.")
                    timeout_errors += 1
                    time.sleep(5)
                    continue

                time.sleep(1)

        else:
            raise Exception(initial_response.json())
        
        return results

    def pull_event_data(self, filepath):

        with open(filepath, 'r') as f:
            json_string = f.read()
            data = json.loads(json_string)

        for event in data:
            url = event['openstates_url']

            yield url
    
    def get_bill_list(self, related_entities):
        bill_data = []

        for entity in related_entities:
            if entity['entity_type'] == 'bill':
                bill_data.append((entity.get('name', ''), 
                                  entity.get('bill', '').get('title', ''), 
                                  entity.get('bill', '').get('id', '')))
        
        return bill_data

    def parse_event_data(self, response: list):
        results = []

        for record in response:
            name = record.get('name', '')
            committee = record.get('participants', [])[0].get('name')
            description = record.get('description', '')
            start_date = record.get('start_date', '')
            status = record.get('status', '')

            if record.get('agenda', [])[0].get('related_entities', ''):
                bill_data = self.get_bill_list(
                    record.get('agenda', [])[0].get('related_entities', ''))
            else:
                bill_data = None
            location = record.get('location', '').get('name', '')

            results.append({
                'name': name, 'committee': committee,
                'description': description, 'start_date': start_date,
                'status': status, 'bill_data': bill_data,
                'location': location
                })
        
        return results
    
    def handle_request(self, state, before, after, count=100, per_page=20, *args):
        response = self.pull_events(state, before, after, count, per_page, *args)
        parsed = self.parse_event_data(response)

        return parsed
            
    def write_results(self, results, filepath):
        with open(filepath, 'w') as f:
            json_as_str = json.dumps(results)
            f.write(json_as_str)

