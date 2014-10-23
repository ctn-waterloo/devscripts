#/usr/bin/env bash
# Run this from the nengo directory, on the branch you want to update.
# This should work whenever we force push master; just change OLD_MASTER.

OLD_MASTER="76f8053076d30"

# Get most recent commit from old master
OLD=$(git rev-list --reverse $OLD_MASTER.. | head -n 1)
MSG=$(git show $OLD~1 --format="%s" --no-patch)

# Get the hash of that commit from new master
NEW=$(git log --grep "$MSG" master --format="%H")

# Do the rebase super clean-like
git rebase --onto $NEW $OLD~1
