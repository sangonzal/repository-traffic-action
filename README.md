# Repository Traffic GitHub Action

Github action that can be used to store repository traffic and clones past the default 2 week period. It pulls traffic and clones data from the GitHub API v3 and stores it into a csv file, which can be commited to your repository or uploaded elsewhere. 

# Usage

## Setting up permissions
You'll first need to create a personal access token (PAT) so the action can access the GitHub API. 

You can generate a PAT by going to 
Settings -> Developer Settings -> Personal Access Tokens -> Generate new token. You will need to grant "repo" permission. For more in depth instructions, see the [GitHub documentation](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

After you have generated the PAT, go to the "Settings" tab of the repository, click on New Secret, name the secret "TRAFFIC_ACTION_TOKEN" and copy the PAT into the box.

## Create a work flow

Create a `workflow.yml` file and place in your `.github/workflows` folder. You can reference the action from this workflow. The only required parameter is setting the PAT that was generated when setting up the permissions.
```yaml
    steps:
    # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
    - uses: actions/checkout@v2
    
    # Calculates traffic and clones and stores in CSV file
    - name: Repository Traffic 
      id: traffic
      uses: sangonzal/repository-traffic-action@v0.1.1
      env:
        TRAFFIC_ACTION_TOKEN: ${{ secrets.TRAFFIC_ACTION_TOKEN }} 
```

This actions does not store the generated data anywhere by default. It temporarily stores it in `${GITHUB_WORKPLACE}/traffic`, but unless it's exported it will be lost. You can integrate other actions into the workflow to upload data elsewhere. Below are two example.

 ### Sample workflow that runs weekly and commits files to repository.

```yaml
on:
  schedule: 
    # runs once a week on sunday
    - cron: "55 23 * * 0"
    
jobs:
  # This workflow contains a single job called "traffic"
  traffic:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
    # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
    - uses: actions/checkout@v2
    
    # Calculates traffic and clones and stores in CSV file
    - name: GitHub traffic 
      id: traffic
      uses: sangonzal/repository-traffic-action@v0.1.1
      env:
        TRAFFIC_ACTION_TOKEN: ${{ secrets.TRAFFIC_ACTION_TOKEN }} 
     
    # Commits files to repository
    - name: Commit changes
      uses: EndBug/add-and-commit@v4
      with:
        author_name: Santiago Gonzalez
        message: "GitHub traffic"
        add: "./traffic/*"
        ref: "traffic"  # commits to branch "traffic" 
```
### Sample workflow that runs weekly and uploads files to S3.
 
If you'd like to avoid commiting the data to the repository, you can use another action to upload elsewhere. For example, you could upload to S3 using the [S3 Sync action](https://github.com/marketplace/actions/s3-sync) .

```yaml
on:
  schedule: 
    # runs once a week on sunday
    - cron: "55 23 * * 0"
    
jobs:
  # This workflow contains a single job called "traffic"
  traffic:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
    # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
    - uses: actions/checkout@v2
    
    # Calculates traffic and clones and stores in CSV file
    - name: Repository Traffic 
      id: traffic
      uses: sangonzal/repository-traffic-action@v0.1.1
      env:
        TRAFFIC_ACTION_TOKEN: ${{ secrets.TRAFFIC_ACTION_TOKEN }} 
     
     # Upload to S3
    - name: S3 Sync
      uses: jakejarvis/s3-sync-action@v0.5.1
      with:
        args: --acl public-read --follow-symlinks --delete
      env:
        AWS_S3_BUCKET: ${{ secrets.AWS_S3_BUCKET }}
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        SOURCE_DIR: 'traffic'
```