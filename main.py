from github import Github
from pandas import DataFrame
import matplotlib.pyplot as plt

# Things we will need:
# Github access token
# Repository name


# 1) Download data from GitHub
# 2) Load from csv
# 3) Append data from github to data in csv
# 4) Plot charts
# 5) Write charts to directory
# 6) Write csv to directory


def main():

    github = Github("0ffd446e9445c97b5f742f3f6276d13294fa56aa")

    repo = github.get_repo("AzureAd/microsoft-authentication-library-for-java")

    traffic = repo.get_views_traffic()
    traffic_dict = {}
    for view in traffic['views']:
        traffic_dict[view.timestamp] = [view.count, view.uniques]

    traffic_frame = DataFrame.from_dict(data=traffic_dict, orient="index", columns=["total_views", "unique_views"])
    traffic_frame.to_csv("views.csv")

    clones = repo.get_clones_traffic()
    clones_dict = {}
    for view in clones['clones']:
        clones_dict[view.timestamp] = [view.count, view.uniques]

    clones_frame = DataFrame.from_dict(data=clones_dict, orient="index", columns=["total_clones", "unique_clones"])

    fig, axes = plt.subplots(nrows=2)

    traffic_frame.plot(ax=axes[0])
    clones_frame.plot(ax=axes[1])
    plt.show()
    #print(traffic_frame)


if __name__ == "__main__":
    main()