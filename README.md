# Vizit Africa Backend

The **Vizit Africa Backend** is the server-side application that powers the Vizit Africa tourism booking platform.  
It provides APIs and core business logic to connect travelers with verified vendors offering tourism-related services across Africa.

## 🌍 Project Overview

Vizit Africa is a digital tourism ecosystem designed to simplify travel planning by allowing users to discover, book, and manage tourism services such as:

- Hotels and accommodations  
- Tours and travel experiences  
- Car rentals  
- Local guides and tour operators  

The backend is responsible for handling authentication, data management, business rules, and secure communication between the frontend and the database.

## 🧩 Key Features

- **User Management**
  - User registration and authentication
  - Role-based access control (Tourist, Vendor, Admin)

- **Vendor Management**
  - Vendor onboarding and approval
  - Management of vendor services and availability

- **Service Management**
  - CRUD operations for tourism services
  - Location-based service listings

- **Booking System**
  - Service booking and reservation tracking
  - Booking status management

- **Administration**
  - Vendor approval workflows
  - Platform monitoring and moderation

## 🛠 Technology Stack

- **Backend Framework:** Django / Django REST Framework  
- **Database:** PostgreSQL (or SQLite for development)  
- **Authentication:** Token-based authentication (JWT or session-based)  
- **Environment Management:** Python virtual environment  
- **Version Control:** Git & GitHub  

## 📂 Project Structure

vizitAfricaBackend/
│
├── accounts/ # User authentication and account management
├── services/ # Tourism services and vendor offerings
├── bookings/ # Booking and reservation logic
├── vizitAfricaBackend/ # Core project configuration
├── manage.py
└── README.md


## 🚀 Getting Started

1. Clone the repository  
   ```bash
   git clone https://github.com/Solvit-Africa-Training-Center/vizit-africa-backend.git

2. python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py runserver


