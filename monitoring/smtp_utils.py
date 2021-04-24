import smtplib
from .config_loader import load_config
from .timestamp import timestamp

config = load_config()

def send_alert(p_subject, p_msg):
    smtp_server = config['smtp']['smtp_server']
    smtp_user = config['smtp']['smtp_user']
    smtp_password = config['smtp']['smtp_password']

    if not (smtp_server or smtp_user or smtp_password):
        return False

    smtp_from = config['smtp']['mail_from']
    smtp_to = config['smtp']['mail_to']
    smtp_subject = "*** ALERT " + p_subject
    msg = f"From: {smtp_from}\n"
    for i in smtp_to:
        msg += f"To: {i}\n"
    msg += f"Subject: {smtp_subject}\n\n"
    msg += f"{p_msg}"
    print(msg)

    try:
        mail = smtplib.SMTP_SSL(smtp_server)
        mail.login(smtp_user, smtp_password)
        mail.sendmail(smtp_from, smtp_to, msg)
        return True
    except Exception as ex:
        print("Send mail failed")
        print(str(ex))
        return False
