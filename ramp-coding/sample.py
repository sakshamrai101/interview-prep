import requests 

BASE_URL = 'https://api.ramp-simulation.internal/v1' 

def fetch_data(endpoint: string):

    url = f"{BASE_URL}{endpoint}"
    print(f"Hitting endpoint: {url}")


    response = requests.get(url)
    print(f"Response recieved: {response.status_code}")

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Non-200 status code recieved for endpoint: {endpoint}")
        return None 


def run_ledger_crawl():

    # 1. Initialise variables to keep track of our final answer. 
    net_volume = 0.0

    # 2. Get our starting point 
    start_data = fetch_data("/user/start")

    if not start_date:
        print("[CRITICAL] Could not fetch starting point")
        return 0.0

    # 3. Extract the next page endpoint from the dictionary
    current_endpoint = start_date["next_step"]

    # Keep looping as long as the current_endpoint has a valid string 
    while current_endpoint is not None:
        print(f"Processing page: {current_endpoint}")
        page_data = fetch_data(current_endpoint)

        if not page_date:
            print(f"Failed to load data from {current_endpoint}, stopping loop.")
            break

        
        # Extract the list of transactions and the next page cursor 
        transactions = page_data.get("data", [])
        pagination = page_data.get("pagination", {})

        # 4. Process every transaction on this page:
        for tx in transactions:
            tx_id = tx.get("id")
            status = tx.get("status")
            amount = tx.get("amount", 0.0)


            print(f"Processing transaction: {tx_id} with status: {status} and amount: {tx_amount}")

            # We only care about SETTLED transactions: 
            if status == 'SETTLED':
                details_endpoint = tx.get("details_endpoint")

                # Fetch the details of the transaction for inner fees:
                print(f"Fetching details for transaction: {tx_id}")
                details_data = fetch_data(details_endpoint)

                fee = 0.0
                if details_data:
                    fee = details_data.get("fee", 0.0)
                    print(f"Found fee: {fee} for transaction: {tx_id}")
                
                # Calculate the net volume:
                tx_net = amount - fee
                net_volume += tx_net 
                print(f"Added net_volume: {tx_net} to total net_volume: {net_volume}")
        
        # 5. Update the pointer to the next page:
        current_endpoint = pagination.get('next_cursor')
        
    return net_volume












