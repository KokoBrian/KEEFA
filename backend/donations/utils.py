import requests
from django.conf import settings

# ----- Helper Functions -----

def get_mpesa_access_token():
    """Get OAuth access token from Safaricom Daraja API."""
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def initiate_mpesa_stk_push(donation):
    """Initiate M-Pesa STK push transaction for the given donation."""
    access_token = get_mpesa_access_token()
    if not access_token:
        raise Exception("Failed to get M-Pesa access token")

    stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    timestamp = donation.created.strftime('%Y%m%d%H%M%S')
    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    import base64
    password_str = shortcode + passkey + timestamp
    password = base64.b64encode(password_str.encode()).decode()

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(donation.amount),
        "PartyA": donation.phone_number,
        "PartyB": shortcode,
        "PhoneNumber": donation.phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": f"Donation-{donation.id}",
        "TransactionDesc": "Donation Payment"
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(stk_push_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"M-Pesa STK Push failed: {response.text}")