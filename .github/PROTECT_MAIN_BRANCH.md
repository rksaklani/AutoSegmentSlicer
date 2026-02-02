# Protect the `main` branch

GitHub recommends protecting `main` so it can't be force-pushed or deleted, and (optionally) so status checks must pass before merging.

## One-time setup (do this in GitHub)

1. Open: **https://github.com/rksaklani/AutoSegmentSlicer/settings/branches**
2. Under **Branch protection rules**, click **Add rule** (or **Add branch protection rule**).
3. In **Branch name pattern**, enter: `main`
4. Enable what you want, for example:
   - **Require a pull request before merging** (optional)
   - **Require status checks to pass before merging** (optional; use if you want CI to pass first)
   - **Do not allow bypassing the above settings**
   - **Restrict who can push to matching branches** (optional)
5. Click **Create** (or **Save changes**).

After this, the "Your main branch isn't protected" notice will go away.
