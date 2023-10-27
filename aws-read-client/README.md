# Prerequisites
In order to run this the following prerequisites must be met:

## Boto3
Install Boto3 by running `pip install boto3`

## AWS Command Line Interface (CLI)
Install AWS CLI by using the instructionsin the link: https://aws.amazon.com/cli/

## User and keys
The CLI requires a valid user, as well as an access key and a secret access key. Users can be set up in the AWS IAM console, and the access key is visible there. The secret access key is as far as I know only available during user creation since it's, well, secret. If the secret key has been lost, a new user might have to be created.

Configure the keys by editing the `~/.aws/credentials` and `~/.aws/config` files with the following:
```
# ~/.aws/credentials
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

# ~/.aws/config
region = eu-central-1
```

These values can also be set by running `aws configure`.

You are now ready to go!