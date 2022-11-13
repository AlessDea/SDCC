# Secure PassWorld


### Applicazione a microservizi per la gestione di password e tool di sicurezza per aziende.

Il password manager offre i seguenti microservizi:

   0. **Login**
        - Permette di:
             - registrarsi ed accedere alla piattaforma;
             - associare utenti alle aziende come impiegati.

   1. **Password Create**
        - Permette di generare una nuova password sicura specificando:
             - tipo (alfanumerica, numerica o solo caratteri);
             - lunghezza;
             - presenza o meno di caratteri speciali.

   2. **Password Manager**
        - Permette di:
             - memorizzare/modificare password create dal microservizio *Password Create*;
             - memorizzare/modificare password create dall'utente;
             - visualizzare le password di un determinato utente.

   3. **Double Authentication**
        - Permette di generare un codice temporaneo (tramite il microservizio *Password Create*) da utilizzare in un secondo stage di autenticazione.

             > *Servizio utilizzabile da siti/applicazioni che scelgono di integrare il sistema come framework di autenticazione a due fattori.*

   4. **Group Manager**
        - Permette alle aziende di creare e gestire gruppi di utenti precedentemente associati come loro impiegati.


   5. **Shared Password**
        - Permette agli utenti appartenenti almeno ad un gruppo, di richiedere agli altri membri una password temporanea.
In particolare, la creazione della password è vincolata all'accettazione di tutti i partecipanti, anche un solo rifiuto nega l'utilizzo del servizio. Una volta generata, la password ha una durata di 24 ore. Terminato il periodo di validità, è necessario inviare una nuova richiesta al gruppo.

             > *Servizio utilizzabile da siti/applicazioni che scelgono di integrare il sistema come framework per l'accesso ad aree riservate.*

   6. **Notification**
        -  Comunicando con gli altri microservizi in modo asincrono tramite *RabbitMQ*, permette di inviare notifiche agli utenti via email e gestisce lo stato delle richieste di *Shared Password*.