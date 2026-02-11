# Push to GitHub

1. **Create the repo on GitHub**  
   If the "New repository" page didn’t open, go to:  
   https://github.com/new?name=cherry-picked-in-endings  
   Click **Create repository** (leave it empty, no README).

2. **Add the remote and push** (replace `YOUR_USERNAME` with your GitHub username):

   ```bash
   cd /Users/leo.lychagin/Downloads/cherry-picked-in-endings
   git remote add origin https://github.com/YOUR_USERNAME/cherry-picked-in-endings.git
   git push -u origin main
   ```

   If you use SSH:

   ```bash
   git remote add origin git@github.com:YOUR_USERNAME/cherry-picked-in-endings.git
   git push -u origin main
   ```

After the first push you can delete this file: `rm PUSH_INSTRUCTIONS.md && git add -A && git commit -m "Remove push instructions" && git push`
