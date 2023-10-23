from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.git.git_client_base import GitClientBase
from azure.devops.v7_1.git.models import GitPullRequest, GitCommitRef,GitPullRequestSearchCriteria
import sys
import os
from dotenv import load_dotenv

load_dotenv()


organization = os.getenv('ORGANIZATION')
project = os.getenv('PROJECT')
personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')
organization_url = os.getenv('ORGANIZATION_URL')
print_array = []

class Wrapper:    
	def __init__(self,filename):        
		self.filename:str = filename        
		self.prs = []

	def append(self, prID):
		self.prs.append(prID)

	def getPRList(self):
		return self.prs
	
	def getFilename(self) -> str:
		return self.filename;


def findWrapper(filename:chr, wrap:[Wrapper]):
	for item in wrap:
		if item.getFilename() == filename:
			return item
	return None

# (wrapper for wrapper in container if wrapper.getFilename() is change["item"]["path"])

# get users to pick which repo
def getRepoId(clientBase: GitClientBase, project):
	switch = {
		1: 'fr-database',
		2: 'fr-playwright',
		3: 'forensic-register',
		4: 'ClientPortal-React',
	}

	print(f'Which Repo would you like to view active filechanges for:\n')
	print(f'[1] fr-database\n')
	print(f'[2] fr-playwright\n')
	print(f'[3] forensic-register\n')
	print(f'[4] ClientPortal-React\n')
	print(f'[5] All Repo changes\n')
	repo_name = int(input(": "))

	if repo_name >= 5: return None
	
	repo_id = GitClientBase.get_repository(clientBase, str(switch.get(repo_name)), project)
	return repo_id.id

# for search criteria for pull requests by project
def searchCriteria(repo_id):
	if repo_id is None: return None
	return GitPullRequestSearchCriteria(repository_id=repo_id)


def filterPRs(activePRs: [GitPullRequest], clientBase: GitClientBase) -> [Wrapper]:

	container:[Wrapper] = [] 
	filenamesArray = []

	# for all active PR's in our choosen repository list the files its changing
	for pr in activePRs:
		pull_request_id = pr.pull_request_id
		repository_id = pr.repository.id
		repository_name = pr.repository.name


		print_array.append(f'[{repository_name}] pull request "{pr.title}"')

		# get all commits done in the PR
		commits:[GitCommitRef] = GitClientBase.get_pull_request_commits(clientBase, repository_id, pull_request_id, project)

		for commit in commits:
			commit_id = commit.commit_id

			commit_changes = GitClientBase.get_changes(clientBase, commit_id,repository_id)

			for change in commit_changes.changes:
				
				if change['item']['gitObjectType'] != 'tree': 
					if change["item"]["path"] in filenamesArray:
						tempWrapper:Wrapper = findWrapper(change["item"]["path"], container)
						tempWrapper.append(pr.title)
					else:
						tempWrapper = Wrapper(change["item"]["path"])
						tempWrapper.append(pr.title)
						filenamesArray.append(change["item"]["path"])
						container.append(tempWrapper)
	# for file in container:
	# 	print(f'{file.getFilename()}: {file.getPRList()}')
	return container


def main():
	if len(sys.argv) < 2:
		print('No Filename provided, cancelling execution')
		return ''
	

	credentials = BasicAuthentication('', personal_access_token)
	clientBase = GitClientBase(base_url=organization_url, creds=credentials)

	repo_id = getRepoId(clientBase, project)

	# get all active PR's in the repo
	activePRs: [GitPullRequest] = GitClientBase.get_pull_requests_by_project(self=clientBase, project=project, search_criteria=searchCriteria(repo_id))

	# TODO apply Conor suggestion of put filename in and returns active PR that have changes for it
	temp = sys.argv[1] if len(sys.argv) > 1 else ''
	# print(temp)
	# return

	wrappedNodes:[Wrapper] = filterPRs(activePRs, clientBase)
	wrap = findWrapper(temp, wrappedNodes)
	print(wrap.getPRList())



	filename = "ActivePR_for_file.txt"

	with open(filename, 'a') as file:
		for line in print_array:
			file.write(line + '\n')

if __name__ == "__main__":
    main()

# # Create a connection to the org
# credentials = BasicAuthentication('', personal_access_token)
# connection = Connection(base_url=organization_url, creds=credentials)

# # Get a client (the "core" client provides access to projects, teams, etc)
# core_client = connection.clients.get_core_client()

# clientBase = GitClientBase(base_url=organization_url, creds=credentials)

# activePRs: [GitPullRequest] = GitClientBase.get_pull_requests_by_project(self=clientBase, project='filenames with active PRs', search_criteria=None)

# for pr in activePRs:
#     # print(pr.title)
#     print(f'pull request "{pr.title}"')
#     pull_request_id = pr.pull_request_id
#     repository_id = pr.repository.id

#     commits:[GitCommitRef] = GitClientBase.get_pull_request_commits(clientBase, repository_id, pull_request_id, 'filenames with active PRs')

#     for commit in commits:
#         commit_id = commit.commit_id

#         commit_changes = GitClientBase.get_changes(clientBase, commit_id,repository_id)

#         for change in commit_changes.changes:
#             if change['item']['gitObjectType'] != 'tree': print(f'\t{change["item"]["path"]}')
