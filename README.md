# Project 4: Item Catalog
### by Yashwanth Manchikatla
This project is a part of Udacity [Full Stack Web Developer Nanodegree program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).
## Description
This project is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates categories and their items. OAuth2 provides authentication for further CRUD functionality on the application.This application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## PreRequisites
 - python 2.x
 - Vagrant
 - VirtualBox
 - SQLite 3.9.2
 - Flask 0.9
 - SQLAlchemy 1.0.12
 - Google+ Client Secrets(client_secrets.json)

## Features
 - All items are grouped into categories
 - User registration system
 - User authentication with google+ account
 - Any user can see all categories, items and item description
 - Registered users can add,update and delete items
## Usage
 - To create database:
```sh
$ python database_setup.py
```
 - To populate database with seed data
```sh
$ python lotsofcategories.py
```
 - Run the application:
```sh
$ python project.py
```
 - Navigate to http://localhost:5000