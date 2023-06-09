# Gitignore creator/updater
This script will create or update a .gitignore file in the current directory. It will also create a .gitignore file in the current directory if one does not exist.


# How does this work?
1. It will scan all files recursively and if it finds a file (or folder) that matches a key in `config.json`, it will fetch the corresponding gitignore data and aggregate everything into a single `.gitignore` file.
2. If the `.gitignore` file already exists, it will update it with the new data.
3. Only unique data will be added to the `.gitignore` file.
4. The data will be sanitized: No empty lines or comments.
5. The data will be sorted alphabetically.


# How to use
```shell
python gitignore.py <target folder to create the .gitignore>
```

In Windows, you can some something like this to run the script:
```shell
python c:\path\to\script\gitignore.py %cd%
```
In this command, `%cd%` is the current directory.

## Example
In the root directory of this project, run the following command:
```shell
python gitignore.py .
```
or 
```shell
python gitignore.py %cd%
```

The output will be:
```text
Generating .gitignore...
Scanning files...
[.idea] Adding .idea related data to .gitignore...
[.idea] Fetching gitignore data...
[.idea] Gitignore data fetched successfully. Caching 77 lines of raw data...
[.py] Adding .py related data to .gitignore...
[.py] Fetching gitignore data...
[.py] Gitignore data fetched successfully. Caching 160 lines of raw data...
Dumping .gitignore...
The .gitignore already exists. Merging with the new data...
Writing 106 lines to .gitignore...
Done! Elapsed time: 0:00:00.272479
```

The resulting `.gitignore` file is the one I'm using in this project.
