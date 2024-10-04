import os
import base64
import google.auth
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

TOKEN_FILE = 'token.json'

# Charger les credentials OAuth 2.0
creds = Credentials.from_authorized_user_file(TOKEN_FILE, scopes=['https://mail.google.com/'])


# Rafraîchir le token s'il est expiré
if creds.expired:
    creds.refresh(google.auth.transport.requests.Request())

# Créer le message avec pièce jointe
def create_message_with_attachment(sender, to, subject, body_text, file_path):
    # Créer le conteneur du message MIME
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Ajouter le texte du corps du message
    body = MIMEText(body_text)
    message.attach(body)

    # Traiter la pièce jointe
    filename = os.path.basename(file_path)
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Encoder la pièce jointe en base64
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')

    # Attacher la pièce jointe au message
    message.attach(part)

    # Encoder le message complet en base64 pour Gmail
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return 

# Envoyer le message via SMTP avec OAuth 2.0
def send_email_with_attachment(sender, to, subject, body_text, file_path):
    # Créer le message avec pièce jointe
    raw_message = create_message_with_attachment(sender, to, subject, body_text, file_path)

    # Connexion au serveur SMTP de Gmail
    smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_conn.ehlo()
    smtp_conn.starttls()
    smtp_conn.ehlo()

    # Créer la chaîne d'authentification OAuth 2.0
    auth_string = f'user={creds.client_id}\1auth=Bearer {creds.token}\1\1'
    smtp_conn.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(auth_string.encode()).decode())

    # Envoyer le message
    smtp_conn.sendmail(sender, to, base64.urlsafe_b64decode(raw_message.encode()))
    smtp_conn.quit()
