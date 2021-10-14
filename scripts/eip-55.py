from sys import argv
from getopt import getopt

import os
import re
import eth_utils

# Adapted from https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md
def checksum_encode(addr_str):
  addr = addr_str.lower()[2:]
  checksummed_buffer = ""

  hashed_address = eth_utils.keccak(text=addr).hex()

  for nibble_index, character in enumerate(addr):
    if character in "0123456789":
      checksummed_buffer += character
    elif character in "abcdef":
      hashed_address_nibble = int(hashed_address[nibble_index], 16)
      if hashed_address_nibble > 7:
        checksummed_buffer += character.upper()
      else:
        checksummed_buffer += character
    else:
      raise eth_utils.ValidationError(
        f"Unrecognized hex character {character} at position {nibble_index}"
      )

  return "0x" + checksummed_buffer

def run(file, fix):
  match = re.match(r'^contracts/(\d+)/(0x[a-fA-F0-9]{40})\.json$', file)
  if not match: return f"Invalid file name {file}"
  addr = match.group(2)
  checksummed = checksum_encode(addr)
  if addr == checksummed: return None
  if not fix: return file
  os.rename(file, f"contracts/{match.group(1)}/{checksummed}.json")

def main():
  opts, args = getopt(argv[1:], "f", ["fix"])
  fix = False
  for o, a in opts:
    if o in ["--fix", "-f"]:
      fix = True
  assert args, "Missing input files"

  errs = [run(file, fix) for file in args]
  errs = [err for err in errs if err]
  if errs:
    print("Wrong file names:")
    for err in errs: print(err)
    exit(1)

if __name__ == "__main__":
  try:
    main()
  except Exception as err:
    print("Error:", err)
    exit(1)