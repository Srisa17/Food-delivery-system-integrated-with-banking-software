# Food Delivery and Banking System

This backend project integrates a food delivery service with an independent, SQLite3-powered banking system.

### Core Components

**Food Delivery Engine:** Supports menu filtering (Veg/Non-Veg), order placement, and automatic ETA calculation based on delivery methods.
**Banking Module:** A standalone SQLite database management system that handles user authentication, account balances, and transaction logs.
**Payment Gateway:** Facilitates secure Net Banking by processing SQL-based transfers between user accounts and merchant (vendor) accounts, while also supporting Cash on Delivery (COD).

### Technical Features

**Data Persistence:** Uses SQLite3 to store users, account balances, beneficiaries, and vendor data.
**Security:** Implements masked password entry via `getpass` and complexity validation using regular expressions.
**Interconnectivity:** The food application acts as a client to the banking module, which functions as both a personal bank and a transaction intermediary.
