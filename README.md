# Digital Wallet

This is a simple digital wallet. 

## Table of Contents

1. [Introduction](#introduction)
2. [Tech Stack](#Tech_Stack)
3. [Installation](#installation)
3. [Limitations](#Limitations)


## Introduction

The purpose is to provide a cloud based wallet, where an individual may fund, transfer and withdraw funds anywhere in the world. The wallet is free and accessable online.

## Tech_Stack

- Django
- Python
- Mariadb
- Javascript
- HTML
- CSS

## Installation

- pip install django
- python manage.py createsuperuser
- python manage.py makemigrations 
- python manage.py migrate
- python manage.py runserver

## Limitations

- After adding transaction history, the UI became terrible on small screens (fixed)
- no real intergration with payment API (will be fixed on next update)
- transaction history should have sender and reciever during money transfer


