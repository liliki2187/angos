#!/usr/bin/env python3
"""Push all local files to GitHub repo via Git Trees API (single commit)."""
import base64, json, urllib.request, sys, os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT_DIR, ".env.local")


def load_env_file(path):
    env = {}
    if not os.path.exists(path):
        return env
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip().strip('"').strip("'")
    return env


ENV = load_env_file(ENV_PATH)
TOKEN = os.environ.get("GITHUB_TOKEN") or ENV.get("GITHUB_TOKEN")
if not TOKEN:
    raise RuntimeError(f"GITHUB_TOKEN not found in env or {ENV_PATH}")

REPO = "daydreamerguan/angus"
BRANCH = "main"
LOCAL_DIR = "/home/admin/.openclaw/workspace/project"
COMMIT_MSG = "feat: switch to Godot 4.3 - project skeleton and CI\n\n- Remove Unity configs\n- Add Godot project (project.godot, Main.tscn)\n- Add export presets (Linux/Win/Mac/HTML5)\n- Add Godot CI workflow\n- Update docs"

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github.v3+json",
}

def api(method, path, data=None):
    url = f"https://api.github.com/repos/{REPO}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

# 1. Get HEAD
ref = api("GET", f"/git/refs/heads/{BRANCH}")
head_sha = ref["object"]["sha"]
print(f"HEAD: {head_sha}")

commit = api("GET", f"/git/commits/{head_sha}")
tree_sha = commit["tree"]["sha"]
print(f"TREE: {tree_sha}")

# 2. Collect files
files = []
skip_dirs = {".git", ".openclaw", "__pycache__"}
for root, dirs, filenames in os.walk(LOCAL_DIR):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for fn in filenames:
        fpath = os.path.join(root, fn)
        relpath = os.path.relpath(fpath, LOCAL_DIR)
        files.append((relpath, fpath))

print(f"Files: {len(files)}")

# 3. Create blobs and build tree
tree_entries = []
for relpath, fpath in sorted(files):
    with open(fpath, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    blob = api("POST", "/git/blobs", {"content": content, "encoding": "base64"})
    mode = "100755" if (relpath == "scripts/export.sh") else "100644"
    tree_entries.append({"path": relpath, "mode": mode, "type": "blob", "sha": blob["sha"]})
    print(f"  blob: {relpath}")

# 4. Create tree
new_tree = api("POST", "/git/trees", {"base_tree": tree_sha, "tree": tree_entries})
new_tree_sha = new_tree["sha"]
print(f"NEW TREE: {new_tree_sha}")

# 5. Create commit
new_commit = api("POST", "/git/commits", {
    "message": COMMIT_MSG,
    "tree": new_tree_sha,
    "parents": [head_sha],
})
commit_sha = new_commit["sha"]
print(f"COMMIT: {commit_sha}")

# 6. Update ref
api("PATCH", f"/git/refs/heads/{BRANCH}", {"sha": commit_sha})
print("PUSH OK")
