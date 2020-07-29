from github import Github
import os
import pandas as pd
import matplotlib.pyplot as plt

repo_name = os.environ["GITHUB_REPOSITORY"]
github = Github(os.environ["INSIGHTS_ACTION_TOKEN"])
print("Repository name: ", repo_name)
print("Token: ", os.environ["INSIGHTS_ACTION_TOKEN"])
repo = github.get_repo(repo_name)


workplace_path = "{}/{}".format(os.environ["GITHUB_WORKSPACE"], "insights")
if not os.path.exists(workplace_path):
    os.makedirs(workplace_path)
print("Workplace path: ", workplace_path)

views_path = "{}/{}".format(workplace_path, "views.csv")
clones_path = "{}/{}".format(workplace_path,"clones.csv")
plots_path = "{}/{}".format(workplace_path,"plots.png")


def main():
    # Traffic stats
    traffic = repo.get_views_traffic()
    traffic_dict = {}
    for view in traffic['views']:
        traffic_dict[view.timestamp] = {"total_views": view.count, "unique_views": view.uniques}
    
    try:
        old_traffic_data = pd.read_csv(views_path, index_col="_date", parse_dates=["_date"]).to_dict(orient="index")
        updated_dict = {**old_traffic_data, **traffic_dict}
        traffic_frame = pd.DataFrame.from_dict(data=updated_dict, orient="index", columns=["total_views", "unique_views"])
    except:
        traffic_frame = pd.DataFrame.from_dict(data=traffic_dict, orient="index", columns=["total_views", "unique_views"])
    
    traffic_frame.index.name = "_date"
    traffic_frame.to_csv(views_path)


    # Clones stats
    clones = repo.get_clones_traffic()
    clones_dict = {}
    for view in clones['clones']:
        clones_dict[view.timestamp] = {"total_clones": view.count, "unique_clones": view.uniques}

    try:
        old_clone_data = pd.read_csv(clones_path, index_col="_date", parse_dates=["_date"]).to_dict(orient="index")
        updated_clones_dict = {**old_clone_data, **clones_dict}
        clones_frame = pd.DataFrame.from_dict(data=updated_clones_dict, orient="index", columns=["total_clones", "unique_clones"])
    except:
        clones_frame = pd.DataFrame.from_dict(data=traffic_dict, orient="index", columns=["total_clones", "unique_clones"])
        
    clones_frame.index.name = "_date"
    clones_frame.to_csv(clones_path)

    # Plots
    _, axes = plt.subplots(nrows=2)

    traffic_weekly = traffic_frame.resample("W").sum()
    clones_weekly = traffic_frame.resample("W").sum()
    traffic_weekly.plot(ax=axes[0])
    clones_weekly.plot(ax=axes[1])
    plt.savefig(plots_path)


if __name__ == "__main__":
    main()