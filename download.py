# Downloads and creates source directory for problem (C++)

from bs4 import BeautifulSoup
import os
import wget
import shutil
import urllib
import sys

namespaces = []  # written to "main.cpp"
subdirectories = []  # written to "CMakeLists.txt"


def createDirectory(dirName):  # return True if directory created successfully
    try:
        os.mkdir(dirName)
        return True
    except:
        return False


def copyTemplate(dirName):  # return True if template copied successfully
    try:
        shutil.copytree("template", dirName)
        return True
    except:
        return False


def getChallengeNames(domainLink):
    challengeNames = []

    page = urllib.request.urlopen(domainLink)
    soup = BeautifulSoup(page)

    # <a ... data-analytics="ChallengeListChallengeName" ... data-attr1="two-strings" ...>

    all_links = soup.find_all("a")
    for link in all_links:
        if link.get("data-analytics") == "ChallengeListChallengeName":
            challengeNames.append(link.get("data-attr1"))

    return challengeNames


def getChallenge(domainName, challengeName):

    domainDir = domainName
    challengeLink = "https://www.hackerrank.com/challenges/" + challengeName + "/problem"
    challengePDFLink = "https://www.hackerrank.com/rest/contests/master/challenges/" + \
        challengeName + "/download_pdf?language=English"
    challengeDir = domainName + "/" + challengeName

    createDirectory(domainDir)

    copyTemplate(challengeDir)

    wget.download(challengePDFLink, out=challengeDir)

    # review this code if template/main.cpp is modified
    with open(challengeDir + "/main.cpp") as f:
        lines = f.readlines()

    lines[0] = "// " + challengeLink + "\n"
    lines[7] = "namespace " + challengeName.replace('-', '') + "\n"

    with open(challengeDir + "/main.cpp", mode="w") as f:
        f.writelines(lines)

    # review this code if template/CMakeLists.txt is modified
    with open(challengeDir + "/CMakeLists.txt") as f:
        lines = f.readlines()

    lines[1] = "project(" + challengeName.replace('-', '') + ")\n"

    with open(challengeDir + "/CMakeLists.txt", mode="w") as f:
        f.writelines(lines)

    namespaces.append(challengeName.replace('-', ''))
    subdirectories.append(challengeDir)


def getDomain(domainLink, domainName):
    challengeNames = getChallengeNames(domainLink)
    for challengeName in challengeNames:
        getChallenge(domainName, challengeName) # adds to namespaces, subdirectories


def createCMakeLists():  # uses subdirectories
    lines = []
    lines.append("cmake_minimum_required(VERSION 3.14)\n")
    lines.append("project(main)\n")
    lines.append("\n")

    for subdirectory in subdirectories:
        lines.append("add_subdirectory(" + subdirectory + ")\n")

    lines.append("\nadd_executable(main main.cpp)\n")

    with open("CMakeLists.txt", mode="w") as f:
        f.writelines(lines)


def createMainCpp():  # uses subdirectories, namespaces
    lines = []

    for subdirectory in subdirectories:
        lines.append("#include \"" + subdirectory + "/main.cpp\"" + "\n")

    lines.append("\n")
    lines.append("int main()\n")
    lines.append("{\n")

    for namespace in namespaces:
        lines.append("    " + namespace + "::test();\n")

    lines.append("    return 0;\n")
    lines.append("}\n")

    with open("main.cpp", mode="w") as f:
        f.writelines(lines)


if __name__ == "__main__":

    # Examples of "domains":
    #
    # https://www.hackerrank.com/domains/cpp?badge_type=cpp
    # https://www.hackerrank.com/domains/python?badge_type=python
    # https://www.hackerrank.com/contests/projecteuler/challenges
    # https://www.hackerrank.com/interview/interview-preparation-kit/dictionaries-hashmaps/challenges

    getDomain(sys.argv[1], sys.argv[2])

    createCMakeLists()
    createMainCpp()
