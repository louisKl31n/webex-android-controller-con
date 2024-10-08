import os
import base64
import pickle
import mimetypes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Scopes pour l'accès Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Obtenir les informations d'authentification OAuth2 et retourner le service Gmail."""
    creds = None
    # Le fichier token.pickle stocke les jetons d'accès utilisateur
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Si aucun jeton disponible ou expiré, obtenir l'autorisation
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/app/creds.json', SCOPES)
            creds = flow.run_local_server(port=8082)

        # Sauvegarder le nouveau jeton pour les futurs usages
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def create_message_with_attachment(sender, to, subject, message_text, file_path):
    """Créer un email avec pièce jointe."""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Ajouter le corps de l'email
    msg = MIMEText(message_text)
    message.attach(msg)

    # Joindre un fichier
    content_type, encoding = mimetypes.guess_type(file_path)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'

    main_type, sub_type = content_type.split('/', 1)
    with open(file_path, 'rb') as fp:
        mime_base = MIMEBase(main_type, sub_type)
        mime_base.set_payload(fp.read())

    encoders.encode_base64(mime_base)
    mime_base.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
    message.attach(mime_base)

    # Encoder le message en base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, user_id, message):
    """Envoyer un email via le service Gmail API."""
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'Message Id: {sent_message["id"]}')
        return sent_message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

if __name__ == '__main__':
    # Obtenez le service Gmail avec OAuth2
    service = get_gmail_service()

    if service:
        sender_email = "qlan001webexbeta@gmail.com"
        recipient_email = "alan.signor.ext@orange.com"
        subject = "Test de mail avec pièce jointe"
        body = "Ceci est un mail de test avec une pièce jointe en utilisant OAuth2."
        file_path = "/app/adbkey"

        # Créer un message avec pièce jointe
        message = create_message_with_attachment(sender_email, recipient_email, subject, body, file_path)

        # Envoyer le message
        send_message(service, "me", message)