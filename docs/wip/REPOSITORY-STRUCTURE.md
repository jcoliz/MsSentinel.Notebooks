# Repository Structure

## Question

How should we structure the repository?

## Context

This repository will be public, intended to demonstrate what and how Sentinel data lake Jupyter notebooks can be used for.

### Multiple files per notebook ###

Each notebook is likely to have

* A design document
* An implementation plan
* The notebook itself
* A job definition

So I was thinking each would need to go into its own folder.

### Challenges with sharing notebooks: ###

Notebooks have an "results" section. This would need to be stripped from anything before being checked in.

Sentinel Data lake Spark environments don't have any environment-specific config. Thus, in order to run a notebook, you would start with this

```
# Configuration - Update this with your workspace name
WORKSPACE_NAME = "MyCompany-SpecialWorkspace12345"
```

But we can't check those into source control that way, instead it needs to say

```
# Configuration - Update this with your workspace name
WORKSPACE_NAME = "<your_workspace_name>"
```

### Requirements ###

1. there needs to be a way to have notebooks we're RUNNING separate from notebooks that are PUBLISHED to the repo. 
2. user who clones the repo with no desire to contribute back could simply clone the repo, change their workspace name, and populate the notebook with details. 
3. In this case, they could never commit this back, but it's OK.

Questions

* Should we have a different location where working notebooks go in the repo, that is held out of source control?
* Or just have a santize script we run before checking in