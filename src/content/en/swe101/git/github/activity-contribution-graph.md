---
label: "Activity"
subtitle: "Contribution graph"
group: "GitHub"
order: 4
---
GitHub activity
The grid below mirrors the **public contribution calendar** on your GitHub profile (daily activity levels 0–4). Squares **appear gradually** after the data loads. Hover a cell for the date and count.

To change which username is loaded, set **`VITE_GITHUB_USERNAME`** for the front-end and optionally **`GITHUB_CONTRIBUTIONS_USER`** on the server (defaults match this site). Data is proxied through **`/api/github-contributions`** and cached for about an hour.

## 1. How it maps to the site menu
This page is a normal study topic: open **GitHub** in the hero menu, select **Activity**, then scroll the article. The graph mounts when you land on the topic so the animation runs each visit.
