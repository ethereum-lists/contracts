from sys import argv
from getopt import getopt

import os
import json
import csv

def formataddr(addr):
  if not addr: return None
  return addr.replace('\\x', '0x')

def makedata(row, source):
  project, name = row["namespace"], row["name"]
  if not project: return None
  factory = formataddr(row["factory"] if "factory" in row else None)
  data = { "project": project, "features": {} }
  if name: data["name"] = name
  if source: data["source"] = source
  if factory: data["features"]["factory"] = factory
  if not data["features"]: del(data["features"])
  return data

def run(inputfile, source, dryrun=False):
  with open(inputfile, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      if not "chain" in row or not "address" in row: continue
      address, chain = formataddr(row["address"]), row["chain"]
      if not address or not chain: continue
      
      path = f"contracts/{chain}/{address}.json"
      if os.path.exists(path): continue

      data = makedata(row, source)
      if not data: continue

      if dryrun: 
        print(data)
      else:
        with open(path, 'w') as outfile: 
          json.dump(data, outfile, indent=2)
          print(f" written {path}")


def main():
  opts, args = getopt(argv[1:], "ns:", ["dry-run", "source="])
  source = 'dune'
  dryrun = False
  for o, a in opts:
    if o in ["--source", "-s"]:
      source = a
    elif o in ["-n", "--dry-run"]:
      dryrun = True
  assert args, "Missing input files"
  for file in args:
    print(f"Importing {file}...")
    run(file, source, dryrun)
  
if __name__ == "__main__":
  try:
    main()
  except Exception as err:
    print("Error:", err)
    exit(1)