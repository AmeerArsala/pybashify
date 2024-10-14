# Run this after updating the pyproject.toml

version=$(python3 scripts/helpers/read-version.py)

pixi install
pixi install -e dev

git status
git add pyproject.toml
git add pixi.lock

git commit -m "[UPDATE] v$version"

# Must happen after or else will point to a previous commit
git tag "v$version"

git push origin main "v$version"
