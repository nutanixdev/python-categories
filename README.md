# Nutanix Prism Central Category Management Demo

This small demo will create a collection of Prism Central category keys and values that are provided by accompanying JSON file.

## Usage

- Recommended Python version 3.8 or later.  Testing for this script was done with Python 3.8 on Ubuntu Linux 20.04.
- Create and activate a virtual environment:

  ```
  python3.8 -m venv venv
  . venv/bin/activate
  ```

- Install the script dependencies:

  ```
  pip3 install -r requirements.txt
  ```

- Rename `.env.example` to `.env`
- Edit `.env` to match your environment requirements i.e. Prism Central IP address & credentials
- Edit `categories.json` to match the category keys and values you want to create
- Run the script:

  ```
  python ./categories.py
  ```

## Additional Info

By default, this script does not require a verified SSL connection to Prism Central.  If you have configured Prism Central with a valid SSL certificate and require SSL certificate verification in your environment, please comment the following line:

```
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## Screenshot

![Screenshot of Python category management script being run](./screenshot.png?raw=true)

## Disclaimer

Please see the `.disclaimer` file that is distributed with this repository.