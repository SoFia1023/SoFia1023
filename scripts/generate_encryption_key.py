#!/usr/bin/env python
"""
Script to generate a secure encryption key salt for the application.
This script should be run once to generate a salt for your environment.
"""
import secrets
import argparse
from typing import Optional


def generate_encryption_key_salt(length: int = 32) -> str:
    """
    Generate a secure random string suitable for use as an encryption key salt.
    
    Args:
        length: Length of the salt in bytes (default: 32)
        
    Returns:
        A secure random hex string
    """
    return secrets.token_hex(length)


def main() -> None:
    """
    Main function to parse arguments and generate the encryption key salt.
    """
    parser = argparse.ArgumentParser(
        description="Generate a secure encryption key salt for the application"
    )
    parser.add_argument(
        "--length", 
        type=int, 
        default=32,
        help="Length of the salt in bytes (default: 32)"
    )
    args = parser.parse_args()
    
    salt = generate_encryption_key_salt(args.length)
    
    print("\n=== ENCRYPTION KEY SALT ===")
    print(f"\n{salt}\n")
    print("Add this to your .env file as:")
    print(f"ENCRYPTION_KEY_SALT={salt}")
    print("\nWARNING: Keep this value secret and secure!")
    print("Do not commit it to version control or share it publicly.")
    print("If this value is lost, all encrypted data will be unrecoverable.\n")


if __name__ == "__main__":
    main()
