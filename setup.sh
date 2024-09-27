#!/bin/bash

# Prompt for environment variables
echo "Please enter your secret key:"
read SECRET_KEY
echo "Please enter your MAIL_USERNAME:"
read MAIL_USERNAME
echo "Please enter your MAIL_PASSWORD:"
read MAIL_PASSWORD


# Create the .env file
cat <<EOL > .env
SECRET_KEY=$SECRET_KEY
SQLALCHEMY_TRACK_MODIFICATIONS=False
MAIL_USERNAME=$MAIL_USERNAME
MAIL_PASSWORD=$MAIL_PASSWORD
EOL

# Notify the user
echo ".env file created successfully."
