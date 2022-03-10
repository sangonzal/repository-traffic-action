import pandas as pd
from github import Github


class RepoStats:

    def get_views(self, views_path):

        views = self.repo.get_views_traffic()
        view_counts = self._get_counts(views, "views")
        return self._create_dataframe(view_counts, "views", views_path)

    def get_clones(self, clones_path):
        clones = self.repo.get_clones_traffic()
        clone_counts = self._get_counts(clones, "clones")
        return self._create_dataframe(clone_counts, "clones", clones_path)

    def __init__(self, repo_name, token) -> None:
        print("Repository name: ", repo_name)

        github = Github(token)
        self.repo = github.get_repo(repo_name)

    def _get_counts(self, data, metric_type):

        total_column = "total_{}".format(metric_type)
        unique_column = "unique_{}".format(metric_type)

        counts = {}
        for view in data[metric_type]:
            counts[view.timestamp] = {
                total_column: view.count, unique_column: view.uniques}
        return counts

    def _create_dataframe(self, data, metric_type, file_path):

        total_column = "total_{}".format(metric_type)
        unique_column = "unique_{}".format(metric_type)

        try:
            print("Attempt to read existing metrics for: ", metric_type)
            old_data = pd.read_csv(file_path, index_col="_date", parse_dates=[
                "_date"]).to_dict(orient="index")
            updated_dict = self.merge_dict(old_data, data, metric_type)
            dataframe = pd.DataFrame.from_dict(
                data=updated_dict, orient="index", columns=[total_column, unique_column])
        except:
            print("No existing metrics for: ", metric_type)
            dataframe = pd.DataFrame.from_dict(
                data=data, orient="index", columns=[total_column, unique_column])

        dataframe.index.name = "_date"
        return dataframe

    def _merge_dict(self, old_data, new_data, metric_type):
        
        total_column = "total_{}".format(metric_type)
        unique_column = "unique_{}".format(metric_type)
        
        print("Merging data for: ", metric_type)
        
        for key in new_data:
            if key not in old_data:
                old_data[key] = new_data[key]
            else:
                if new_data[key][total_column] > old_data[key][total_column] or new_data[key][unique_column] > old_data[key][unique_column]:
                    old_data[key] = new_data[key]
        return old_data
