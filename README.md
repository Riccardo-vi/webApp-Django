# RepairDesk - Gestione Ticket di Riparazione

Una web application Django per la gestione centralizzata di ticket di assistenza tecnica e riparazione dispositivi. RepairDesk consente ai clienti di aprire segnalazioni, ai tecnici di gestire gli interventi e ai manager di supervisionare l'intero workflow.

## 🎯 Caratteristiche Principali

### Gestione Ticket Completa
- **Apertura ticket** - I clienti possono segnalare problemi sui loro dispositivi
- **Tracking stato** - Sistema di stato con 3 livelli: *Aperto*, *In lavorazione*, *Chiuso*
- **Priorità** - Classificazione per urgenza: *Bassa*, *Media*, *Alta*
- **Assegnazione tecnici** - Manager assegna i ticket ai tecnici disponibili
- **Data di chiusura prevista** - Tracciamento delle scadenze

### Gestione Dispositivi
- **Inventario dispositivi** - Registrazione brand, modello, numero seriale
- **Associazione cliente** - Ogni dispositivo è collegato al proprietario
- **Storico ticket** - Visualizzazione di tutti gli interventi su un dispositivo

### Controllo Accessi Granulare
L'app implementa un sistema RBAC (Role-Based Access Control) con tre ruoli:

| Ruolo | Permessi | Accesso |
|-------|----------|---------|
| **Customer** | Aprire ticket, visualizzare propri ticket | Solo dispositivi e ticket personali |
| **Technician** | Modificare ticket assegnati, visualizzare stato | Solo ticket a loro assegnati |
| **Manager** | CRUD completo ticket e dispositivi, dashboard | Vista globale dell'intero sistema |

### Interfaccia Utente
- **Tema scuro/chiaro** - Toggle tema con persistent storage in sessione
- **Paginazione** - Liste con pagina di 5 elementi
- **Ricerca avanzata** - Filtro per titolo, descrizione, marca e modello dispositivo
- **Responsive design** - Interfaccia adattiva con HTML/CSS

## 🏗️ Architettura

```
webApp-Django/
├── manage.py                    # Entry point Django
├── repairdesk/                  # Configurazione principale del progetto
│   ├── settings.py              # Configurazione Django (DB, app, middleware)
│   ├── urls.py                  # Router globale (login, logout, inclusione app core)
│   └── wsgi.py                  # WSGI application per deployment
├── core/                        # Applicazione principale
│   ├── models.py                # Modelli ORM: Ticket, Device
│   ├── views.py                 # CBV e funzioni vista (business logic)
│   ├── urls.py                  # Router interno app core
│   ├── forms.py                 # Form Django con validazione custom
│   ├── admin.py                 # Configurazione admin Django
│   ├── apps.py                  # Configurazione app
│   ├── migrations/              # Cronologia modifiche database
│   └── templates/core/          # Template HTML
│       ├── home.html            # Homepage pubblica
│       ├── login.html           # Pagina login
│       ├── ticket_list.html     # Lista ticket (filtri, ricerca)
│       ├── ticket_detail.html   # Dettagli singolo ticket
│       ├── ticket_form.html     # Form creazione/modifica ticket
│       ├── my_tickets.html      # Ticket del cliente loggato
│       ├── device_list.html     # Lista dispositivi
│       ├── device_detail.html   # Dettagli dispositivo
│       ├── device_form.html     # Form creazione/modifica dispositivo
│       ├── device_confirm_delete.html  # Conferma eliminazione dispositivo
│       └── manager_dashboard.html      # Dashboard manager
├── static/                      # File statici
│   ├── css/                     # Fogli di stile
│   └── js/                      # JavaScript frontend
└── db.sqlite3                   # Database SQLite (sviluppo)
```

### Flusso di Dati

1. **Request HTTP** → URL routing in `repairdesk/urls.py` + `core/urls.py`
2. **View** → CBV/funzione elabora la logica (autorizzazione, queryset filtrato)
3. **Form** → Validazione dati e custom checks (es. data passato)
4. **Model** → Persistenza in SQLite tramite Django ORM
5. **Template** → Rendering HTML con context data
6. **Response** → HTML + CSS/JS per il browser

### Modelli Dati

#### Device
```python
- owner: ForeignKey(User)          # Proprietario dispositivo
- brand: CharField(50)             # Marca (es. "Apple", "Samsung")
- model: CharField(50)             # Modello (es. "iPhone 13", "Galaxy S21")
- serial_number: CharField(100)    # Numero seriale (UNIQUE)
```

#### Ticket
```python
- title: CharField(100)            # Titolo segnalazione
- description: TextField()         # Descrizione dettagliata
- device: ForeignKey(Device)       # Dispositivo interessato
- customer: ForeignKey(User)       # Cliente che ha aperto il ticket
- technician: ForeignKey(User, null=True)  # Tecnico assegnato
- status: Choice[OPEN, IN_PROGRESS, CLOSED]
- priority: Choice[LOW, MEDIUM, HIGH]
- created_at: DateTimeField        # Data creazione (auto)
- updated_at: DateTimeField        # Ultima modifica (auto)
- expected_close_date: DateField   # Scadenza prevista
```

## 🚀 Come Avviare

### Prerequisiti
- Python 3.8+
- pip
- Virtualenv (consigliato)

### Setup Ambiente di Sviluppo

```bash
# Clone del repository
git clone https://github.com/Riccardo-vi/webApp-Django.git
cd webApp-Django

# Creazione ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate  # Windows

# Installazione dipendenze
pip install django==4.2.11

# Migrazione database
python manage.py migrate

# Creazione superuser (admin)
python manage.py createsuperuser
# Inserisci username, email, password

# Avvio server di sviluppo
python manage.py runserver
```

Server disponibile su: **http://localhost:8000**

### Creazione Utenti e Gruppi

Per utilizzare l'app con i vari ruoli, accedi a `/admin`:

```bash
# 1. Accedi a http://localhost:8000/admin con le credenziali superuser

# 2. Crea i gruppi (Groups):
#    - Customer
#    - Technician
#    - Manager

# 3. Crea utenti di test e assegna ai gruppi rispettivi
```

### Comandi Utili

```bash
# Creare nuove migrazioni dopo modifiche ai model
python manage.py makemigrations

# Applicare migrazioni
python manage.py migrate

# Accedere alla shell interattiva Django
python manage.py shell

# Raccogliere file statici (per production)
python manage.py collectstatic
```

## 📋 Flusso di Utilizzo

### Per un Customer (Cliente)

1. **Registrazione/Login** → `/login` con credenziali
2. **Registrare dispositivo** → `/devices/create`
   - Inserisce marca, modello, numero seriale
3. **Aprire ticket** → `/tickets/create`
   - Seleziona il dispositivo
   - Descrive il problema
   - ⚠️ Non può impostare stato, priorità, tecnico (rimossi dal form in `forms.py`)
4. **Monitorare ticket** → `/my-tickets`
   - Visualizza i propri ticket in tempo reale
   - Vede lo stato di avanzamento

### Per un Technician (Tecnico)

1. **Login** → `/login`
2. **Visualizzare assegnazioni** → `/tickets`
   - Vede SOLO i ticket a lui assegnati
3. **Dettagli ticket** → `/tickets/<id>`
   - Visualizza tutte le informazioni
4. **Aggiornare ticket** → `/tickets/<id>/edit`
   - Modifica stato (es. OPEN → IN_PROGRESS → CLOSED)
   - Aggiorna priorità se necessario
   - ⚠️ Può modificare solo ticket assegnati (check in `TicketUpdateView.get_object()`)

### Per un Manager

1. **Login** → `/login`
2. **Dashboard Manager** → `/manager-dashboard`
   - Vista completa di TUTTI i ticket
3. **Gestione Ticket** → `/tickets`
   - Filtri per stato e ricerca avanzata
4. **Assegnazione tecnici** → `/tickets/<id>/edit`
   - Seleziona il tecnico per il ticket
   - Imposta data di chiusura prevista
5. **Gestione dispositivi** → `/devices`
   - CRUD dispositivi (aggiunge, modifica, elimina)
   - Accesso a tutti i dispositivi in sistema

## 🔐 Sicurezza e Validazione

### Validazioni Custom (models.py)

```python
# Data chiusura non può essere nel passato
if expected_close_date < today():
    raise ValidationError("La data prevista di chiusura non può essere nel passato.")

# Ticket chiuso deve avere tecnico assegnato
if status == 'CLOSED' and technician is None:
    raise ValidationError("Un ticket chiuso deve avere un tecnico assegnato.")
```

### Controllo Accessi

- **PermissionRequiredMixin** - Verifica permessi classe (`add_ticket`, `change_ticket`)
- **LoginRequiredMixin** - Richiede autenticazione
- **get_object() override** - Verifica logica autorizzazione per singolo oggetto
- **PermissionDenied** - Solleva eccezione se accesso non autorizzato

### Protezioni Django Built-in

- CSRF token su form
- Session-based authentication
- Password hashing con PBKDF2
- SQLite injection prevention (ORM parametrizzato)

## 🎨 Frontend

### File Static
- **CSS** - Responsive layout, tema chiaro/scuro
- **HTML Templates** - Django template language (DTL) con context processor
- **JavaScript** - Interattività frontend (toggle tema, validazioni lato client)

### Session Variables
```python
# Conteggio visite
request.session['visits']

# Preferenza tema
request.session['theme']  # 'light' o 'dark'
```

## 📊 Configurazione Django (settings.py)

| Setting | Valore |
|---------|--------|
| LANGUAGE_CODE | `IT-it` (Italiano) |
| TIME_ZONE | `UTC` |
| DEBUG | `True` (sviluppo) |
| DATABASE | SQLite (`db.sqlite3`) |
| INSTALLED_APPS | admin, auth, sessions, messages, staticfiles, **core** |
| LOGIN_URL | `login` |
| LOGIN_REDIRECT_URL | `home` |
| LOGOUT_REDIRECT_URL | `home` |

⚠️ **Nota Sicurezza**: `SECRET_KEY` è esposta in settings.py. Per production:
- Usare variabili d'ambiente
- Disattivare `DEBUG`
- Configurare `ALLOWED_HOSTS`
- Usare database PostgreSQL/MySQL

## 🧪 Testing (Consigliato)

Creare file `tests.py`:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Device, Ticket

class TicketTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        device = Device.objects.create(
            owner=user, brand='Apple', model='iPhone', serial_number='12345'
        )
    
    def test_ticket_creation(self):
        # Test creazione ticket
        pass
```

Eseguire test:
```bash
python manage.py test core
```

## 🔍 Troubleshooting

| Problema | Soluzione |
|----------|-----------|
| ModuleNotFoundError: django | `pip install django==4.2.11` |
| TemplateDoesNotExist | Verificare percorsi in `templates/core/` |
| PermissionDenied accesso ticket | Verificare gruppo utente in admin |
| Form mostra campi non voluti | Controllare logica `TicketForm.__init__()` |
| Database locked | `rm db.sqlite3` e refare migrazioni |

## 📚 Risorse Utili

- [Django 4.2 Documentation](https://docs.djangoproject.com/en/4.2/)
- [Django ORM Query](https://docs.djangoproject.com/en/4.2/topics/db/queries/)
- [Class-Based Views](https://docs.djangoproject.com/en/4.2/topics/class-based-views/)
- [Authentication & Permissions](https://docs.djangoproject.com/en/4.2/topics/auth/)

## 📝 Licenza

Questo progetto è un'esercitazione educativa ("esame").

## 👤 Autore

**Riccardo-vi** - [GitHub](https://github.com/Riccardo-vi)

---

**Ultima modifica**: Settembre 2026

Per domande o contributi, aprire un Issue o Pull Request nel repository.
