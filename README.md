# langchain-google-tool

#### gitignore  안될경우
git rm -r --cached .

- rm is the remove command

- r will allow recursive removal

– cached will only remove files from the index. Your files will still be there.

- The .indicates that all files will be untracked.

git add .

git commit -m ".gitignore fix"



#### Remove all  commits - secret inclcuded
- 1️⃣ Switch to a new orphan branch (no history)
git checkout --orphan fresh-start

- 2️⃣ Stage all files
git add .

- 3️⃣ Commit as the fresh starting point
git commit -m "Fresh start: remove all history and sensitive files"

- 4️⃣ Delete the old main branch (local only)
git branch -D main

- 5️⃣ Rename the fresh branch to main
git branch -m main

- 6️⃣ Add secrets to .gitignore to avoid future accidents
echo "langchain-gmail-toolkit/token.json" >> .gitignore
echo "langchain-google-calendar-toolkit/token.json" >> .gitignore
echo "langchain-gmail-toolkit/credentials.json" >> .gitignore

- 7️⃣ Stage and commit the .gitignore update
git add .gitignore
git commit -m "Add .gitignore to exclude sensitive files"

- 8️⃣ Force-push to GitHub (this overwrites the repo history)
git push -f origin main
