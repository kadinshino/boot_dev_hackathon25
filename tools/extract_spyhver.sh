#!/bin/bash
# Spyhver Message Extractor
# Run in the git repository root

echo "Extracting hidden message from git history..."
echo ""

# Method 1: Extract from commit messages (first word pattern)
echo "Method 1 - Commit message pattern:"
git log --pretty=format:"%s" --reverse | head -47 | awk '{print $2}' | tr '\n' ' '
echo ""
echo ""

# Method 2: Extract from file comments (SPYHVER tags)
echo "Method 2 - File comments:"
for i in {01..47}; do
    grep -h "SPYHVER-$i:" $(find . -name "*.py" -o -name "*.md") 2>/dev/null | awk '{print $3}'
done | tr '\n' ' '
echo ""
echo ""

# Method 3: Extract from commit order
echo "Method 3 - Chronological assembly:"
git log --pretty=format:"%h %s" --reverse | head -47
