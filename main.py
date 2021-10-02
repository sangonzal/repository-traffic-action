import os
import json
from repostats import RepoStats
import matplotlib.pyplot as plt
import requests


def main():
    repo_name=os.environ["GITHUB_REPOSITORY"]
    repo_stats = RepoStats(
        repo_name, os.environ["TRAFFIC_ACTION_TOKEN"])

    workplace_path = "{}/{}".format(os.environ["GITHUB_WORKSPACE"], "traffic")
    if not os.path.exists(workplace_path):
        os.makedirs(workplace_path)
    print("Workplace path: ", workplace_path)

    views_path = "{}/{}".format(workplace_path, "views.csv")
    clones_path = "{}/{}".format(workplace_path, "clones.csv")
    plots_path = "{}/{}".format(workplace_path, "plots.png")

    views_frame = repo_stats.get_views(views_path)
    clones_frame = repo_stats.get_clones(clones_path)
    
    if os.environ["UPLOAD_KEY"]:
        upload(repo_name, views_frame, clones_frame, os.environ["UPLOAD_KEY"])
    else: 
        views_frame.to_csv(views_path)
        clones_frame.to_csv(clones_path)
        create_plots(views_frame, clones_frame, plots_path)

def upload(repo_name, views_frame, clones_frame, api_key):
    data ={repo_name: views_frame.join(clones_frame, how='outer').to_json(orient='index')}
    print(requests.put("http://localhost:3000/api/upload", json = json.loads(json.dumps(data))))


def create_plots(views_frame, clones_frame, plots_path):
    fig, axes = plt.subplots(nrows=2)
    fig.tight_layout(h_pad=6)

    # Consider letting users configure plots
    # traffic_weekly = traffic_frame.resample("W", label="left").sum().tail(12)
    # clones_weekly = clones_frame.resample("W", label="left").sum().tail(12)
    if not views_frame.empty:
        views_frame.tail(30).plot(ax=axes[0])
    if not clones_frame.empty:
        clones_frame.tail(30).plot(ax=axes[1])
    plt.savefig(plots_path)


if __name__ == "__main__":
    main()
