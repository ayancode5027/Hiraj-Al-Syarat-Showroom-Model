# Hiraj Al Sayarat Al Jadeed – Smart Car Showroom Management System

## Overview

The **Hiraj Al Sayarat Al Jadeed Smart Car Showroom Management System** is a web-based application developed using **Python**, **Streamlit**, and **SQLite**. The system helps car showrooms efficiently manage vehicle inventory, customer inquiries, test-drive bookings, and sales operations.

Designed for **Hiraj Al Sayarat Al Jadeed** in **Makkah, Saudi Arabia**, the application provides a modern digital showroom experience with support for both **Arabic** and **English** languages.

---

## Features

### Vehicle Inventory Management

* Add, edit, and delete vehicle records
* Manage new and used vehicles
* Store vehicle images and descriptions
* Track stock availability

### Customer Inquiry Management

* Collect customer leads and inquiries
* Direct WhatsApp contact integration
* Lead tracking and follow-up support

### Test Drive Booking

* Customers can schedule test drives
* Store booking information in the database
* Manage appointment records efficiently

### Finance Calculator

* Calculate estimated monthly payments
* Support down payment and loan duration inputs
* Assist customers in purchase planning

### Role-Based Authentication

#### Administrator

* Manage vehicles
* View bookings
* View customer leads
* Manage users

#### Salesperson

* View inventory
* Manage inquiries
* View bookings
* Track customer leads

### Bilingual Support

* English Language
* Arabic Language
* Dynamic language switching

### Dashboard & Analytics

* Total vehicles
* Available vehicles
* Customer leads
* Test drive requests
* Inventory statistics

---

## Supported Vehicle Brands

* Toyota
* Hyundai
* Kia
* Nissan
* BMW
* Mercedes-Benz

---

## Technology Stack

| Component       | Technology         |
| --------------- | ------------------ |
| Frontend        | Streamlit          |
| Backend         | Python             |
| Database        | SQLite             |
| IDE             | Visual Studio Code |
| Version Control | GitHub             |
| Deployment      | Streamlit Cloud    |

---

## Database Structure

### Users Table

* id
* username
* password
* role

### Cars Table

* id
* brand
* model
* year
* condition
* price
* engine
* transmission
* fuel_type
* color
* stock
* image_url
* description

### Bookings Table

* id
* name
* phone
* car
* date
* time

### Leads Table

* id
* name
* phone
* car

---

## Advantages

* Easy inventory management
* Faster customer handling
* Improved sales tracking
* Secure authentication
* Responsive user interface
* Efficient booking management
* Bilingual support

---

## Future Enhancements

* Online vehicle payments
* AI-powered vehicle recommendations
* Vehicle comparison system
* Email notifications
* QR code vehicle listings
* Mobile application support
* Cloud database integration
* Advanced analytics and reporting

---

## Contact

**WhatsApp:** +966543346930

---
