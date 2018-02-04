import glob
import os
import sys
import re

if len(sys.argv) == 1:
    print('Usage: enforcer (rules.txt) (parent_directory)')
    exit(1)

ruleFile = sys.argv[1]
scanDirectory = sys.argv[2]

rules = []
ruleRegex = re.compile(r'\d+(\.\d+)*')
for line in open(ruleFile):
    match = ruleRegex.match(line.strip())
    if match:
        ruleNumber = match.group()
        if ruleNumber in rules:
            print("Error: Duplicate rule found: " + ruleNumber)
            exit(3)
        rules.append(ruleNumber)
    else:
        print("Invalid rule: " + line)
        exit(2)

print("Rules: ")
for rule in rules:
    print(rule)

ruleReferenceRegex = re.compile(r'@r\d(\.\d+)*')
fileRegex = re.compile(r'.+(\.(js|txt))')
for file in [f for f in os.listdir(scanDirectory) if fileRegex.search(f)]:
    toRead = scanDirectory + file
    if toRead == ruleFile:
        continue
    print("Processing: " + toRead + "...")
    with open(toRead) as f:
        for match in ruleReferenceRegex.finditer(f.read()):
            ruleReference = match.group()
            print("Found Reference: " + ruleReference)
            ruleNumber = ruleReference[2:].strip()
            print("Rule: " + ruleNumber)
            if ruleNumber in rules:
                rules.remove(ruleNumber)
            else:
                print("Rule referenced but not in Rules: " + ruleReference)

print("Unreferenced Rules: ")
for rule in rules:
    print(rule)
