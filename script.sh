NAME="Abhijith K"

# 1. remove the macOS junk and ignore it going forward
git rm --cached .DS_Store 2>/dev/null; printf '\n.DS_Store\n' >> .gitignore

# 2. add a marketplace manifest so the repo is installable as a marketplace
cat > .claude-plugin/marketplace.json <<'JSON'
{
  "name": "architecture-from-codebase",
  "owner": { "name": "Abhijith K", "url": "https://github.com/super-wisdom" },
  "plugins": [
    {
      "name": "architecture-from-codebase",
      "description": "Reverse-engineer any codebase into a self-contained HTML architecture reference with annotated diagrams, source links, and observed-vs-inferred provenance.",
      "category": "engineering",
      "source": "."
    }
  ]
}
JSON

# 3. fill in every placeholder across all files
perl -pi -e "s/YOUR_HANDLE/super-wisdom/g; s/YOUR_MARKETPLACE/architecture-from-codebase/g; s/NAME_PLACEHOLDER/$NAME/g; s/\\QYOUR NAME\\E/$NAME/g" \
  README.md CHANGELOG.md LICENSE .claude-plugin/plugin.json .claude-plugin/marketplace.json

# 4. verify nothing is left, then validate JSON
grep -rn "YOUR_\|YOUR NAME\|NAME_PLACEHOLDER" . --include=*.md --include=*.json && echo "!! placeholders remain" || echo "clean"
python3 -c "import json;[json.load(open(f)) for f in ['.claude-plugin/plugin.json','.claude-plugin/marketplace.json']];print('json valid')"

# 5. (optional but recommended) test the install locally before pushing
claude plugin marketplace add .    # then: claude plugin install architecture-from-codebase@architecture-from-codebase

# 6. commit & push
git add -A && git commit -m "Fill placeholders, add marketplace.json, drop .DS_Store" && git push
