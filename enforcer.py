import os
import sys
import re

if len(sys.argv) < 3:
    print('Usage: enforcer (rules.txt) (parent_directory)')
    exit(1)

ruleFile = sys.argv[1]
scanDirectory = sys.argv[2]
if scanDirectory[-1] != '\\':
    scanDirectory = scanDirectory + '\\'
print("Rules in '" + ruleFile + "', Searching in '" + scanDirectory + "'")

excludePaths = []
if len(sys.argv) > 3:
    excludePaths = sys.argv[3:]
    print("Exclude Paths: " + str(excludePaths))

unmatchedRules = []
ruleRegex = re.compile(r'\d+(\.\d+)*')
for line in open(ruleFile):
    match = ruleRegex.match(line.strip())
    if match:
        ruleNumber = match.group()
        if ruleNumber in unmatchedRules:
            print("Error: Duplicate rule found: " + ruleNumber)
            exit(3)
        unmatchedRules.append(ruleNumber)
    else:
        print("Invalid rule: " + line)
        exit(2)

print(str(len(unmatchedRules)) + " rules to match")

matchedRules = []
ruleReferenceRegex = re.compile(r'@r\d(\.\d+)*')
fileRegex = re.compile(r'.+(\.(js|txt))')
for file in [f for f in [os.path.join(dp, f) for dp, dn, fn in os.walk(scanDirectory) for f in fn] if fileRegex.search(f)]:
    if file == ruleFile:
        continue
    excluded = False
    for ex in excludePaths:
        if ex in file:
            excluded = True
    if excluded:
        continue
    with open(file) as f:
        for match in ruleReferenceRegex.finditer(f.read()):
            ruleReference = match.group()
            ruleNumber = ruleReference[2:].strip()
            if ruleNumber in unmatchedRules:
                unmatchedRules.remove(ruleNumber)
                matchedRules.append(ruleNumber)
            elif ruleNumber not in matchedRules:
                print("Rule referenced but not in Rules: " + ruleReference + ", '" + ruleNumber + "'")

print(str(len(unmatchedRules)) + " unreferenced rules: ")
for rule in unmatchedRules:
    print(rule)
