#!/usr/bin/env python3
import re
import argparse
import jwt
import time
from datetime import datetime
from colorama import Fore, Style, init


def extract_jwt_tokens(log_text):
    jwt_pattern = r'\beyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\b'
    tokens = re.findall(jwt_pattern, log_text)
    return tokens

def parse_jwt(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    except jwt.DecodeError:
        return None

def is_token_valid(exp_epoch):
    current_time = time.time()
    return exp_epoch > current_time

def main():
    init(autoreset=True)

    parser = argparse.ArgumentParser(description="Extracts JWTs from a file and displays valid tokens.")
    parser.add_argument("file", help="pass path to file containing tokens. For example, output from office_tokens bof in CS C2 logs")
    
    args = parser.parse_args()
    
    with open(args.file, 'r') as f:
        log_text = f.read()
    
    tokens = extract_jwt_tokens(log_text)
    
    for token in tokens:
        parsed_token = parse_jwt(token)
        if parsed_token and 'exp' in parsed_token:
            exp_epoch = parsed_token['exp']
            if is_token_valid(exp_epoch):
                exp_time = datetime.fromtimestamp(exp_epoch).strftime('%Y-%m-%d %H:%M:%S')
                aud = parsed_token.get('aud', 'No audience')
                scopes = parsed_token.get('scp', 'No scopes')
                tenant_id = parsed_token.get('tid', 'No tenantId')
                upn = parsed_token.get('upn', 'No UPN')

                print(f"{Fore.CYAN}{Style.BRIGHT}Token: {Style.NORMAL}{token}")
                print(f"{Fore.GREEN}{Style.BRIGHT}Expiration Time: {Style.NORMAL}{exp_time}")
                print(f"{Fore.YELLOW}{Style.BRIGHT}Tenant ID: {Style.NORMAL}{tenant_id}")
                print(f"{Fore.YELLOW}{Style.BRIGHT}UPN: {Style.NORMAL}{upn}")
                print(f"{Fore.GREEN}{Style.BRIGHT}Audience: {Style.NORMAL}{aud}")
                print(f"{Fore.GREEN}{Style.BRIGHT}AScopes: {Style.NORMAL}{scopes}\n")
   

if __name__ == "__main__":
    main()
