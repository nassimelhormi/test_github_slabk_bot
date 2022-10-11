from utils.github import GithubClient
import asyncio


def main():
    github_client = GithubClient()
    asyncio.run(github_client.get_open_pr("nassimelhormi", "test_github_slabk_bot"))


if __name__ == '__main__':
    main()
