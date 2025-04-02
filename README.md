# BitTrack

BitTrack is a simple version control system that allows you to manage your repository efficiently using the command line.

## Available Commands

```sh
init       # Initialize a new BitTrack repository
add        # Add all files to the staging area
cat-file   # Display the content of a stored object (-p <object_id>)
status     # Show the current staging status
reset      # Clear the staging area
commit     # Commit staged changes with a message (-m 'message')
log        # Display the commit log
revert     # Revert to a previous commit (<commit_hash>)
help       # Display help information for available commands
```

## Ignoring Files and Folders

You can exclude specific files and folders from being tracked by creating a `.bitignore` file in your repository. Simply list the file and folder names you want to ignore inside this file, similar to `.gitignore` in Git.

**Example:**

```
# Ignore log files  
*.log  

# Ignore temporary files  
temp/  

# Ignore a specific file  
config.json  
```

bit_track/

.gitignore