Homepage
========

I am currently hosting my homepage at:

[https://hpenedones.me](https://hpenedones.me)

## Automated Link Checking

This repository includes a GitHub Actions workflow that automatically checks for broken links in the website and blog posts.

The link checker runs:
- Weekly on Mondays at 9:00 AM UTC
- On every push to the main/master branch
- Manually via the Actions tab (workflow_dispatch)

If broken links are detected, the workflow will:
1. Fail and show the broken links in the workflow run
2. Create or update a GitHub issue with the "broken-links" label

You can configure which links to exclude by editing `.lychee.toml` in the repository root.
