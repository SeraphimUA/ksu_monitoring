from monitoring.smtp_utils import send_alert

subject = "Something went wrong"
message = "Can you check the server?"

send_alert(subject, message)
