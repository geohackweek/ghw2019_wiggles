# Seismic wiggle discriminator

When you see wiggle records of ground motion and there's a spike, what casued it?  We'll 

## Files

* `.gitignore`
<br> Globally ignored files by `git` for the project.
* `environment.yml`
<br> `conda` environment description needed to run this project.
* `README.md`
<br> Description of the project. [Sample](https://geohackweek.github.io/wiki/github_project_management.html#project-guidelines)

## Folders

### `contributors`
A seismology team to provide a data set of wiggles and labels.
A machine learning team to choose what kind of model we should use.
A data format team to convert data into the appropriate format for the machine learning.

Each team member has it's own folder under contributors, where he/she can
work on their contribution. Having a dedicated folder for one-self helps to 
prevent conflicts when merging with master.

### `notebooks`
Notebooks that are considered delivered results for the project should go in
here.

### `scripts`
Helper utilities that are shared with the team

