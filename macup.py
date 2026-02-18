#!/usr/bin/env python3

import requests
import os
from pathlib import Path
import json
import random
import argparse
import sys
import platform

plt = platform.system()

paths = {
    "Linux": "/usr/local/lib/macup",
    "Windows": "%USERPROFILE%\\Documents\\macup"
}

db_path = os.path.join(paths[plt], "mac-vendor.json")

db_mirror_url = "https://maclookup.app/downloads/json-database/get-db"

def main():
    parser = argparse.ArgumentParser(description="macup is a (mostly) offline lookup tool for MAC address prefixes and their respective vendors.")
    parser.add_argument("-i", "--init", action = "store_true", help="Initializes the utility and downloads the database. This is the only time macup requires a network connection.")
    parser.add_argument("-p", "--prefix", help="Specify a prefix and return the vendor associated with that prefix")
    parser.add_argument("-v", "--vendor", help="Specify a vendor and return all associated prefixes")
    parser.add_argument("-r", "--rand", action = "store_true", help="Generate a random prefix and its vendor (for subversion testing purposes)")
    parser.add_argument("-s", "--outfile", default="", help="Save output to file (only with -v, no extension)")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.init:
        init()
    if args.prefix:
        matchPrefix(args.prefix)
    if args.vendor and args.outfile:
        matchVendor(args.vendor, args.outfile)
    if args.vendor:
        matchVendor(args.vendor)
    if args.rand:
        randomPrefix()

# def helpMsg():
#     print("macup is a (mostly) offline lookup tool for MAC address prefixes and their respective vendors.")
#     print("Syntax: macup <-pvrish> <prefix/vendor>")
#     print("Options:")
#     print("-i | Initializes the utility and downloads the database. This is the only time macup requires a network connection.")
#     print("-p | Specify a prefix and return the vendor associated with that prefix")
#     print("-v | Specify a vendor and return all associated prefixes")
#     print("-s | Save output to specified file (only with -v)")
#     print("-r | Generate a random prefix and its vendor (for subversion testing purposes)")
#     print("-h | Display this help message and end execution")

def init():
    try:
        try:
            resDir = Path(paths[plt])
            resDir.mkdir()
        except FileExistsError:
            print("Directory already exists. Ignoring mkdir...")
        print(f"Requesting database from mirror at: {db_mirror_url}")
        response = requests.get(db_mirror_url)
        print(f"Response received! Response status: {response.status_code}")
        if response.status_code == 200:
            print(f"Beginning database write to: {db_path}")
            with open(db_path, "wb") as f:
                print("Writing...")
                f.write(response.content)
                print("Database written!")
        else:
            print(f"Failed to download database. Server responded with status code: {response.status_code}")
    except FileExistsError:
        print("File already exists. Updating...")
        print(f"Removing database found at: {db_path}")
        os.remove(db_path)
        print(f"Requesting database from mirror at: {db_mirror_url}")
        response = requests.get("https://maclookup.app/downloads/json-database/get-db")
        print(f"Response received! Response status: {response.status_code}")
        if response.status_code == 200:
            print(f"Beginning database write to: {db_path}")
            with open(db_path, "wb") as f:
                print("Writing...")
                f.write(response.content)
                print("Database written!")
        else:
            print(f"Failed to download database. Server responded with status code: {response.status_code}")
    except PermissionError:
        print("Permission denied. Please try again, running as root.")
    except Exception as e:
        print(f"An error occurred while attempting to initialize the database: {e}")

def matchPrefix(p):
    try:
        with open(db_path, "r") as f:
            db = json.load(f)
        for record in db:
            if record["macPrefix"] == p:
                print(f"{record["macPrefix"]} | {record["vendorName"]}")
    except FileNotFoundError:
        print("Database not found! Did you initialize macup?")

def matchVendor(v, saveToFileName = ""):
    try:
        with open(db_path, "r") as f:
            db = json.load(f)
        if saveToFileName:
            with open(f"{saveToFileName}.txt", "w") as f:
                for record in db:
                    if v.lower() in record["vendorName"].lower():
                        print(f"{record["macPrefix"]} | {record["vendorName"]}")
                        f.write(f"{record["macPrefix"]} | {record["vendorName"]}\n")
        else:
            for record in db:
                if v.lower() in record["vendorName"].lower():
                    print(f"{record["macPrefix"]} | {record["vendorName"]}")
    except FileNotFoundError:
        print("Database not found! Did you initialize macup?")

def randomPrefix():
    try:
        with open(db_path, "r") as f:
            db = json.load(f)
        randRec = db[random.randint(0, len(db) - 1)]
        print(f"{randRec['macPrefix']} | {randRec['vendorName']}")
    except FileNotFoundError:
        print("Database not found! Did you initialize macup?")

if __name__ == "__main__":
    main()