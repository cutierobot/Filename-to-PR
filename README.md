# Filename-to-PR
A Azure DevOps Python 3 script that grabs all active PR's that contain the given filename

### Problem Statement

### Python libraries used
- [dotenv](https://pypi.org/project/python-dotenv/)
- [azure-devops-python-api](https://github.com/microsoft/azure-devops-python-api/tree/dev)

### TODO
- [ ] Remove hardcoded repo values and allow to be configurable for different companies/clients

### how to use file
Simply fill in the `.env` with the required values and run in your prefered command line application followed by the filename for which you would like to find active Pull Requests for.

#### Example
```
python3 pr_to_filename.py /path/to/file.html
```
