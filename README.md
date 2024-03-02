Ecommerce-API 
==============================
## Installation

    Python 3.x is required. If you don't have Python 3.x or higher, download the appropriate package and install:

* Then, Git clone this repo to your PC
    ```bash
        $ git clone https://github.com/Shehbaazsk/Ecommerce-api.git
    ```

* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```bash
            $ cd core
        ```
    2. Create and fire up your virtual environment:
        ```bash
            $ python3 -m venv venv
            $ source venv/bin/activate
        ```
    3. Install the dependencies needed to run the app:
        ```bash
            $ pip install -r requirements.txt
        ```
    4. Make those migrations work
        ```bash
            $ python manage.py makemigrations
            $ python manage.py migrate
        ```
    5. Seed databasew with fixtures:
        ```bash
            $ python manage.py loaddata ./fixtures/*.json
        ```

* #### Run It
    Fire up the server using this one simple command:
    ```bash
        $ python manage.py runserver
    ```