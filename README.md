# Consumer Car Care Inspection System

A comprehensive web-based inspection management system built with Django for Consumer Car Care.

## Project Overview

This system helps manage vehicle inspections with the following key features:
- Inspection ticket management
- Inspector assignment
- Inspection scheduling with calendar integration

## Technologies Used

- Python 3.x
- Django 5.1.7
- SQLite (default database)
- HTML/CSS for front-end

## Project Structure

```
C3-/
├── config/              # Project configuration directory
│   ├── settings.py      # Django settings
│   ├── urls.py          # Main URL routing
│   └── wsgi.py/asgi.py  # WSGI/ASGI configuration
├── inspection/          # Main inspection app
│   ├── admin.py         # Admin panel configuration
│   ├── models.py        # Data models
│   ├── views.py         # View functions
│   ├── urls.py          # URL routing for inspection app
│   └── templates/       # HTML templates
│       └── inspection/  # App-specific templates
├── inventory/           # Inventory management app
│   ├── admin.py
│   ├── models.py
│   └── views.py
├── manage.py            # Django command-line utility
└── requirements.txt     # Project dependencies
```

## Features Implemented

### 1. Inspection Ticket Management
- View list of all inspection tickets
- Filter and search functionality
- Create new inspection tickets
- View ticket details and status

### 2. Inspector Assignment
- View list of available inspectors
- Assign inspectors to inspection tickets
- Track inspector status

### 3. Inspection Scheduling
- Calendar view for scheduling
- Date and time selection
- Schedule management

## Models

### Inspector
- Name
- Phone
- Status
- Address

### InspectionTicket
- Ticket number
- Inspection type
- Company
- Vehicle make
- VIN
- Priority
- Tag
- Status

### InspectionSchedule
- Ticket (FK to InspectionTicket)
- Inspection date
- Inspection time
- Duration
- Notes

## Setup Instructions

1. Clone the repository:
```
git clone <repository-url>
cd C3-
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Apply migrations:
```
python manage.py migrate
```

4. Create a superuser:
```
python manage.py createsuperuser
```

5. Run the development server:
```
python manage.py runserver
```

6. Navigate to http://127.0.0.1:8000 in your browser

## Usage

### Admin Interface
- Access the admin interface at http://127.0.0.1:8000/admin/
- Use it to manage all data models directly

### Main Application
- Inspection tickets list: http://127.0.0.1:8000/inspection/tickets/
- Assign inspector: http://127.0.0.1:8000/inspection/assign-inspector/
- Schedule inspection: http://127.0.0.1:8000/inspection/schedule-inspection/<ticket_id>/
- Create new ticket: http://127.0.0.1:8000/inspection/create-ticket/

## Screenshots

The application implements the following views:

1. Inspection Tickets List - Displays all inspection tickets with their details and status

![inspection-ticket](https://raw.githubusercontent.com/IfeanyiAyadiuno/C3-/main/Screenshots/inspection-ticket.png)

2. Inspector Assignment - Interface for assigning inspectors to tickets

![inspeciton-assign](https://raw.githubusercontent.com/IfeanyiAyadiuno/C3-/main/Screenshots/inspeciton-assign.png)

3. Inspection Scheduling - Calendar interface for scheduling inspections

![inspeciton-booking](https://raw.githubusercontent.com/IfeanyiAyadiuno/C3-/main/Screenshots/inspeciton-booking.png)

