import os, sys, base64, re, requests, traceback
from github import Github, GithubException, InputGitAuthor

START_SECTION = "<!--START_SECTION:jokes-quotes-->"
END_SECTION = "<!--END_SECTION:jokes-quotes-->"
listReg = f"${START_SECTION}[\\s\\S]+${END_SECTION}"
GH_TOKEN = os.getenv("INPUT_GH_TOKEN")
GH_REPO = os.getenv("INPUT_REPOSITORY")
GH_USERNAME = os.getenv("INPUT_USERNAME")
GH_EMAIL = os.getenv("INPUT_EMAIL")
GH_BRANCH = os.getenv("INPUT_BRANCH")


def getRandomQoutes():
    url: str = "https://api.quotable.io/random"
    data = requests.get(url=url).json()
    return {"quote": data["content"], "author": data["author"]}


def getRandomJokes():
    url: str = "https://v2.jokeapi.dev/joke/Programming?type=twopart"
    data = requests.get(url=url).json()
    return {"question": data["setup"], "answer": data["delivery"]}


def decodeReadme(data: str):
    decodeBytes = base64.b64decode(data)
    return str(decodeBytes, "utf-8")


def generateNewReadme(contents: str, readme: str):
    contentsInReadme = f"{START_SECTION}\n{contents}\n{END_SECTION}"
    return re.sub(listReg, contentsInReadme, readme)


def generateTables():
    jokes = getRandomJokes()
    quotes = getRandomQoutes()
    upper: str = "| Quotes | Jokes |\n| :-----: | :-----: |"
    middle: str = f"| {quotes['quote']} | {jokes['question']}|"
    bottom: str = f"| {quotes['author']} | {jokes['answer']}|"
    return f"{upper}\n{middle}\n{bottom}"


if __name__ == "__main__":
    try:
        if GH_TOKEN is None:
            raise Exception("Please input the token!")

        gh = Github(GH_TOKEN)
        repo = gh.get_repo(f"{GH_USERNAME}/{GH_REPO}")
        contents = repo.get_readme()
        readme = decodeReadme(contents)
        new_readme = generateNewReadme(contents=generateTables(), readme=readme)
        commiter = InputGitAuthor(GH_USERNAME, GH_EMAIL)

        if new_readme != readme:
            repo.update_file(
                path=contents.path,
                message="Updating file",
                content=new_readme,
                sha=contents.sha,
                branch=GH_BRANCH,
                committer=commiter
            )

    except Exception as e:
        traceback.print_exc()
        print(f"Exeception Occured: {str(e)}")
