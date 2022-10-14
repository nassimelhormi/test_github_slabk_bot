import requests as requests
import yaml
import asyncio
from datetime import datetime


class GithubClient:
    """
    Client to interact with the GitHub API.
    """

    def __init__(self):
        with open("./config/default.yml", "r") as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)
            token = "Bearer " + self.conf["github"]["token"]
            self.headers = {"Authorization": token}

    """
    Get open pull (max 30) requests from a given repository.
    """

    async def get_opened_pr(self, owner: str, repo: str):

        temp = {}
        results = []

        url = self.conf["github"]["url"] + "repos/" + owner + "/" + repo + "/pulls?state='open'"
        pull_requests = requests.get(url=url, headers=self.headers)
        for pull_request in pull_requests.json():
            temp["title"] = pull_request["title"]
            temp["html_url"] = pull_request["html_url"]
            temp["owner"] = pull_request["user"]["login"]
            results.append(temp)
        print(results)
        return results

    """
    Get closed pull requests (30st) from a given repository.
    """

    async def get_closed_pr(self, owner: str, repo: str):

        temp = {}
        results = []

        url = self.conf["github"]["url"] + "repos/" + owner + "/" + repo + "/pulls?state='closed'"
        closed_prs = requests.get(url=url, headers=self.headers)
        for closed_pr in closed_prs.json():
            if closed_pr["base"]["ref"] == "master":
                temp = {
                    "title": closed_pr["title"],
                    "html_url": closed_pr["html_url"],
                    "owner": closed_pr["user"]["login"],
                    "merged_at": closed_pr["merged_at"],
                }
            results.append(temp)
        results = list(filter(None, results))  # remove empty list

        return results

    """
    Get information for a given branch.
    """

    def _get_branch_infos(self, owner: str, repo: str, branch: str):
        url = self.conf["github"]["url"] + "repos/" + owner + "/" + repo + "/branches/" + branch
        res = requests.get(url=url, headers=self.headers)

        return res.json()

    """
    Get pull requests merged in Staging environment (branch master).
    """

    async def get_pr_staging(self, owner: str, repo: str):
        prs = await self.get_closed_pr(owner=owner, repo=repo)
        res_prod = self._get_branch_infos(owner=owner, repo=repo, branch="prod")

        last_merge_date_prod = datetime.strptime(res_prod["commit"]["commit"]["committer"]["date"],
                                                 "%Y-%m-%dT%H:%M:%SZ")

        for pr in prs:
            if datetime.strptime(pr["merged_at"], "%Y-%m-%dT%H:%M:%SZ") >= last_merge_date_prod:
                print(pr)
                print("Prod : " + str(last_merge_date_prod))

        return True
