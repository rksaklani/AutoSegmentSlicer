# Git setup – push to GitHub

Use these commands from the **project root** (the folder that contains `README.md`, `CMakeLists.txt`, and now `.gitignore`).

If this is a **new** repo (no `.git` yet):

```bash
git init
git add .
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:rksaklani/AutoSegmentSlicer.git
git push -u origin main
```

If you already have a repo and only need to add the remote and push:

```bash
git remote add origin git@github.com:rksaklani/AutoSegmentSlicer.git
git branch -M main
git push -u origin main
```

**Note:** The project already has a full `README.md`. The one-line `echo "# AutoSegmentSlicer" >> README.md` would append that line to the file; it’s not required. Use `git add .` to add all files (respecting `.gitignore`), or `git add README.md` and other files as needed.
