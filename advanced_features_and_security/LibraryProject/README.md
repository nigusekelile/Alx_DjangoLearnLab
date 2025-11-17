# Django Permissions and Groups Setup

## Overview
This Django application implements a comprehensive permission and group system to control access to various parts of the application. The system uses Django's built-in authentication system with custom permissions and groups.

## Custom Permissions
The following custom permissions have been added to the CustomUser model:

- `can_view`: Permission to view user profiles
- `can_create`: Permission to create new users
- `can_edit`: Permission to edit user profiles
- `can_delete`: Permission to delete users

## Groups
Three default groups have been created with the following permissions:

### 1. Viewers
- `can_view`: Can view user profiles

### 2. Editors
- `can_view`: Can view user profiles
- `can_create`: Can create new users
- `can_edit`: Can edit user profiles

### 3. Admins
- `can_view`: Can view user profiles
- `can_create`: Can create new users
- `can_edit`: Can edit user profiles
- `can_delete`: Can delete users

## Setup Instructions

### 1. Run Migrations
After updating the models, run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
