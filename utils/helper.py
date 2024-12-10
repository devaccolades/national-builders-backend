import requests
import logging
logger = logging.getLogger(__name__)

def send_to_qleads_api(enquiry,client_ip):
    # Prepare the data to be sent to Qleads API
    payload = {
        "Name": f"{enquiry.first_name} {enquiry.last_name}" if enquiry.first_name and enquiry.last_name else "NA",
        "Email": enquiry.email if enquiry.email else "NA",
        "Phone": str(enquiry.phone) if enquiry.phone else "NA",
        "Country": "India",  
        "City": "",  
        "Referral": "Project Enquiry" if enquiry.project else "Contact Enquiry", 
        "LandingPage": "https://nationalbuilders.in/", 
        "IP": str(client_ip),
        "CreatedTime": enquiry.enquiry_date.strftime('%d/%m/%Y %H:%M:%S'),
        "Project": enquiry.project.name if enquiry.project else "NA",  
        "ChatTranscript": "", 
        "Title": "NA",
        "Utm_Source": "NA",
        "Utm_Medium": "NA",
        "Utm_Campaign": "NA",
        "BHK": str(enquiry.project.bedrooms) if enquiry.project and enquiry.project.bedrooms else "NA",
        "Budget": "NA",
        "Remarks1": enquiry.message if enquiry.message else "NA",
        "Remarks2": "NA", 
        "IncomingSource": "Website" 
    }

    # API endpoint
    api_url = "https://quadraleads.in:8580/api/qleads"

    # Send POST request to Qleads API
    try:
        response = requests.post(api_url, json=payload)

        # Check for a successful response
        if response.json().get('Status') == "Success": 
            logger.info("Enquiry successfully sent to Qleads API")
            return True
        else:
            logger.error(f"Failed to send enquiry to Qleads API: {response.json()}")
            return False
    except Exception as e:
        logger.error(f"An error occurred while sending data to Qleads API: {str(e)}")
        return False


def get_client_ip(request):
    """Function to get the client's IP address from request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0] 
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
