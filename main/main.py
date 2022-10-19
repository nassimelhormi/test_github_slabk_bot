from utils.github import GithubClient
from utils.slack import SlackClient
from repos.list import repos
import asyncio


def main():
    github_client = GithubClient()
    slack_client = SlackClient()

    message = ""
    prs = []
    for repo in repos:
        prs.append(asyncio.run(github_client.get_pr_staging("nassimelhormi", repo)))

    for pr in prs:
        for info in pr:
            message += info["html_url"] + "\n"

    slack_client.send_slack_message(message="Hello <!here> we have those PRs in staging this week : \n" + message)


if __name__ == '__main__':
    main()
