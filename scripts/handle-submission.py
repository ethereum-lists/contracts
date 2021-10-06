import sys
import re
import json
import os

CONTRACT_ADDRESSES = 'Contract Addresses'
GITHUB_ORG = 'Github Organization'
PROJECT_NAME = 'Project Name'
SECURITY_EMAIL = 'Security Contact Email'
PROJECT_ID = 'Project ID'
NETWORK = 'Network'

def parse(input):
  current_key = None
  current_value = None
  result = {}

  for line in input:
    print(line)
    match = re.match(r'^### (.+)$', line)
    if match:
      if current_key and current_value: 
        result[current_key] = current_value.strip()
      current_key = match.group(1)
      current_value = ""
    elif len(line.strip()) == 0:
      continue
    elif current_key:
      current_value = current_value + "\n" + line.strip()
  
  if current_key and current_value: 
    result[current_key] = current_value.strip()

  if CONTRACT_ADDRESSES in result:
    addresses = result[CONTRACT_ADDRESSES].split("\n")[1:-1]
    result[CONTRACT_ADDRESSES] = [line for line in addresses if len(line.strip())]

  if NETWORK in result:
    match = re.search(r'\((\d+)\)', result[NETWORK])
    result[NETWORK] = match.group(1)

  return result

def put_project(data):
  if not PROJECT_ID in data: raise Exception("Missing project ID")
  if not re.match(r'^[a-z0-9_]+$', data[PROJECT_ID]): raise Exception(f"Invalid project ID: {data[PROJECT_ID]}")

  path = f"projects/{data[PROJECT_ID]}.json"
  project = {}
  if os.path.exists(path):
    with open(path, 'r') as infile: 
      project = json.load(infile)

  if PROJECT_NAME in data: 
    project['name'] = data[PROJECT_NAME]

  if GITHUB_ORG in data:
    if not 'social' in project: project['social'] = {}
    project['social']['github'] = data[GITHUB_ORG]

  if SECURITY_EMAIL in data: 
    if not 'contacts' in project: project['contacts'] = {}
    project['contacts']['security'] = data[SECURITY_EMAIL]
  
  with open(path, 'w') as outfile: 
    json.dump(project, outfile, indent=2)
    print(f"Written {path}: {project}")

def put_contracts(data):
  if CONTRACT_ADDRESSES in data:
    for line in data[CONTRACT_ADDRESSES]:
      if not len(line.strip()): continue
      address, name = (re.split(r'\s+', line.strip(), 1) + [None])[:2]
      put_contract(data, address, name)

def put_contract(data, address, name):
  if not PROJECT_ID in data: raise Exception("Missing project ID")
  if not NETWORK in data: raise Exception("Missing network for contract addresses")
  if not re.match(r'^0x[A-Fa-f0-9]{40}$', address): raise Exception(f"Invalid contract address {address}")
  
  folder = f"contracts/{data[NETWORK]}"
  path = f"{folder}/{address.lower()}.json"
  
  contract = {}
  if os.path.exists(path):
    with open(path, 'r') as infile: 
      contract = json.load(infile)
  
  if not os.path.exists(folder):
    os.mkdir(folder)

  contract["project"] = data[PROJECT_ID]
  if name: contract["name"] = name

  with open(path, 'w') as outfile: 
    json.dump(contract, outfile, indent=2)
    print(f"Written {path}: {contract}")

def main():
  input = sys.stdin.read()
  data = parse(input.split("\n"))
  print(f"Input: {data}")
  put_project(data)
  put_contracts(data)

# Sample run:
# echo -e '### Project ID\n\nproj_id\n\n### Project Name\n\nmy project\n\n### Github Organization\n\norg\n\n### Security Contact Email\n\nfoo@example.com\n\n### Network\n\nEthereum Mainnet (1)\n\n### Contract Addresses\n\n```text\n0xe26067c76fdbe877f48b0a8400cf5db8b47af0fe foo foo\r\n0xd07e72b00431af84ad438ca995fd9a7f0207542d\n```\n' | python3 scripts/handle-submission.py 
if __name__ == "__main__":
  try:
    main()
  except Exception as err:
    print("Error:", err)
    exit(1)