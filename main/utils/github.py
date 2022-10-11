import requests as requests
import yaml


class GithubClient:
    """
    Client to interact with the GitHub API.
    """
    def __init__(self):
        with open("../config/default.yml", "r") as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

    """
    Get all open pull requests from a given repository.
    """
    async def get_open_pr(self, owner: str, repo: str):

        temp = {}
        results = []
        token = "Bearer " + self.conf["github"]["token"]
        headers = {"Authorization": token}
        url = self.conf["github"]["url"] + "repos/" + owner + "/" + repo + "/pulls"

        pull_requests = requests.get(url=url, headers=headers)
        for pull_request in pull_requests.json():
            if pull_request["state"] == "open":
                temp["title"] = pull_request["title"]
                temp["html_url"] = pull_request["html_url"]
                temp["owner"] = pull_request["user"]["login"]
            results.append(temp)
        return results
