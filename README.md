# Casa delle Montagne

A small Django application for managing handmade soap products, ingredients, recipes, and printable labels.

The project began as a simple tool for a hobby soap maker who sells occasionally at local markets and fairs. The immediate aim is to make it easy to maintain product formulations and generate consistent ingredient labels without relying on Django Admin for normal use.

## Current status

This is an early development version intended for local, single-user use.

Current features include:

- ingredient management;
- product management;
- recipe/formulation entry;
- active/inactive product status for seasonal soaps;
- dynamic recipe rows while editing a product;
- creation of new ingredients from within the product workflow;
- `g`, `kg`, `ml`, `l`, `tsp`, `tbsp`, and `each` units;
- 70 × 50 mm landscape label preview;
- Casa delle Montagne branding on the web interface and labels;
- macOS launcher scripts for opening and stopping the local application.

Stock management, production batches, sales, and automated updating are planned but are not yet part of the application.

## Technology

- Python
- Django
- SQLite
- Django templates
- minimal JavaScript
- local browser-based interface

The application is deliberately kept simple so that it can run on an ordinary desktop computer and remain easy to maintain.

## Development setup

Clone the repository:

```bash
git clone https://github.com/emkayoh/casa-delle-montagne.git
cd casa-delle-montagne
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply the database migrations:

```bash
python manage.py migrate
```

Create a Django superuser if required for development or administration:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

Django Admin remains available at:

```text
http://127.0.0.1:8000/admin/
```

but the intention is that normal day-to-day use should not require access to Admin.

## Main workflow

The current application is centred on three related concepts:

```text
Ingredient
    ↓
Recipe ingredient
    ↓
Product
```

A product has a structured recipe made from reusable ingredient records. The same structured data is used to generate the ingredient list shown on the label.

This avoids maintaining a recipe and a separate free-text label declaration that could later become inconsistent.

## Product status

Products can be marked active or inactive from the product list.

This is intended for seasonal products such as Christmas soaps: inactive products remain visible and editable, but can be clearly distinguished from products currently being offered.

## Labels

The current label format is:

```text
70 mm × 50 mm
landscape
```

The label uses the Casa delle Montagne artwork together with product-specific information such as:

- product name;
- description;
- ingredient declaration;
- nominal weight.

The precise layout is still being refined through user feedback.

## macOS launcher

The repository includes:

```text
run_app.sh
stop_app.sh
launcher.applescript.example
```

These can be used to create a clickable macOS application launcher that starts the local Django server and opens the app in the default browser.

Detailed instructions are in:

```text
docs/macos_launcher.md
```

The current macOS launcher uses Django's development server and is intended only for local development and testing.

## Planned Ubuntu installation

The intended live installation is an Ubuntu 24 desktop machine.

The likely production arrangement is:

```text
Ubuntu login
    ↓
systemd user service
    ↓
local application server
    ↓
127.0.0.1 on a dedicated port
    ↓
desktop launcher opens browser
```

The production setup will probably use Gunicorn rather than Django's `runserver`.

## Planned development

Likely future additions include:

- basic stock management for ingredients and finished products;
- stock movements rather than manually maintained totals;
- production batches;
- recipe versioning where needed;
- printable multi-label sheets;
- backup and update workflow;
- GitHub-based application updates;
- Ubuntu desktop launcher and managed service.

The project is intentionally being developed incrementally from real user feedback rather than trying to anticipate every possible requirement in advance.

## Repository notes

Local data and generated runtime files should not be committed.

The `.gitignore` excludes items such as:

```text
.venv/
db.sqlite3
.env
logs/
.soapbook.pid
*.app/
Casa.iconset/
Casa.icns
```

The SQLite database is deliberately local so that user data is not stored in the public repository.

## Documentation

Project documentation is kept under:

```text
docs/
```

At present this includes the macOS launcher procedure.

## Development approach

This is a small hobby project rather than a commercial product. The priorities are:

- keep the interface straightforward;
- avoid unnecessary infrastructure;
- make common tasks possible without Django Admin;
- preserve a clean data model that can grow if the user's needs expand;
- use real user feedback to determine what gets built next.
