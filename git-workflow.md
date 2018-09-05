# Workflow

## Step 1: Clone an Assignment

4. Open a terminal and type the command:

    ```bash
    git clone repo_url
    ```
 where `repo_url` is the URL you copied in the previous step.
5. You will see a new folder with this repo. Open the notebook file that it is in this repo and make changes. Also, save any newly created files to this folder.

## Step 2: Push the Repo Back to Github

You've made changes and are ready to submit them or share them for collaboration. Type the following commands in order to push your changes back to the `master` branch. (Expert git users will argue with the wisdom of my advice. But let's do this for now.)

```bash
git add .
```

```bash
git status
```

```bash
git commit -am 'insert a comment about your changes'
```

```bash
git push origin master
```

Now, I will be able to also clone your repo, make changes, and push back to github.

### Video Demonstration of Steps 1 and 2

https://youtu.be/p3SwaoDEGH0

## Step 3: Pull the Repo and Push Back to Github

Suppose that you pushed your changes back to github, and then I (Dr. Titus) clone your repo, make changes, and push back to github. On your hard drive, there is an older version, and on github there is a newer version. You need to replace your version with the newer version from github. Thus, in the terminal, navigate to the folder of your repo and type this command.

```bash
git pull
```

This will **replace** your version with the one that it on github. *This has potential for disaster!* What if you lose valuable work? You may want to copy the file before pulling, just to have a backup. Also, you should always pull before making changes so that your version and a collaborator's version are not different versions being developed in parallel.

(When github is used for large collaborations, one never commits to the master branch. Rather, collaborators create different branches and the project owner looks at differences and merges the code.)

When you have finished making changes, you can issue these commands to push to master on github.

```bash
git add .
```

```bash
git status
```

```bash
git commit -am 'insert a comment about your changes'
```

```bash
git push origin master
```

