# Secure PassWorld


### Applicazioni a microservizi per la gestione di password.
Il password manager offre i seguenti microservizi:

   1. **Creazione di una nuova password:**
        - Il microservizio in questione permette di generare in modo automatico una nuova password sicura, anche partendo da informazioni inserite precedentemente dall'utente (Sito, Date, Parole Chiavi).

   2. **Memorizza o modifica password:**
        - Tale microservizio permette la memorizzazione delle password create con il microservizio precedente oppure di password inserite dall'utente. Permette inoltre di modificare le password già presenti.

   3. **Listing password:**
        - Visualizzazione delle password memorizzate o di una password specifica.

   4. **Servizio di doppia autenticazione:**
        - Tale microservizio permette la generazione di un codice temporaneo da utilizzare nel secondo stage di autenticazione.

        > *Servizio utilizzabile per siti/applicazioni che scelgono di utilizzare tale sistema come framework di autenticazione.*

   5. **Generazione password temporanea:**
        - Generazione di password temporanee utilizzabili da utenti ospiti per un certo periodo specificato dal creatore della password.

        > *Servizio utilizzabile per siti/applicazioni che scelgono di utilizzare tale sistema come framework di autenticazione.*

   6. **Generazioni password condivise:**
        - tale microservizio offre la possibilità a due o più utenti di limitare l'accesso ad una password. In particolare, l'utilizzo di una certa password è vincolata all'accettazione di tutti i partecipanti ad essa. Una password di questo tipo viene restituita all'utente solamente se la richiesta viene accettata da tutti i 'partecipanti' a questa password. Una volta ottenute tutte le autorizzazioni la password viene mostrata all'utente richiedente.
        N.B.: la password in questione viene generata in modo temporaneo. Le richieste successive per una password già creata non ne producono una nuova se il periodo di validità non è ancora trascorso.

        > *Servizio utilizzabile per siti/applicazioni che scelgono di utilizzare tale sistema come framework di autenticazione.*
         

> *Tale applicazione offre agli utenti di utilizzarla come framework di autenticazione da integrare in siti o applicazioni. In tal caso gli utlimi tre microservizi possono essere utilizzati.*
