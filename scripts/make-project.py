from sys import argv

import os
import json

def makeproject(project):
  if not project: return None
  name = " ".join(project.split("_")).title()
  return { "name": name }

def main():
  projects = argv[1:]
  for project in projects:
    path = f"projects/{project}.json"
    if os.path.exists(path): continue
    
    data = makeproject(project)
    if not data: continue
    with open(path, 'w') as outfile: 
      json.dump(data, outfile, indent=2)
      print(f" written {path}")

if __name__ == "__main__":
  try:
    main()
  except Exception as err:
    print("Error:", err)
    exit(1)