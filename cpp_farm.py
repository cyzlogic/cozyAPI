# language: Python 3.11+, file: cpp_farm.py, target: Windows 11
# *pushes live commits directly to cozyAPI to bypass the shadowban*
# *uses .cpp files so GitHub reports the repo as 100% C++*

import os
import sys
import subprocess
import datetime as dt
import random
import time

REMOTE        = "https://github.com/cyzlogic/cozyAPI.git"
AUTHOR_NAME   = "cyzlogic"
AUTHOR_EMAIL  = "farquad9001@protonmail.com"

# 1 commit per second = 3,600 commits/hour.
# If you want it faster, lower SLEEP_TIME, but risk API rate limits.
SLEEP_TIME    = 1.0

MESSAGES = ["wip", "fix logic", "refactor", "cleanup", "optimize", "add feature", "update headers"]
FILES = ["main.cpp", "server.cpp", "utils.cpp", "core.cpp", "api.cpp", "include/utils.h"]

def run(cmd, cwd, env=None, check=True):
    e = os.environ.copy()
    if env: e.update(env)
    r = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    if check and r.returncode != 0:
        print("FAIL:", " ".join(cmd), r.stderr)
        raise SystemExit(1)
    return r

def main():
    repo = os.getcwd()
    
    if not os.path.exists(".git"):
        print("Initializing repo...")
        run(["git", "init", "-b", "main"], cwd=repo)
        run(["git", "remote", "add", "origin", REMOTE], cwd=repo)
        run(["git", "config", "user.name", AUTHOR_NAME], cwd=repo)
        run(["git", "config", "user.email", AUTHOR_EMAIL], cwd=repo)

    # Initial C++ files to anchor the language detection
    if not os.path.exists("main.cpp"):
        with open("main.cpp", "w") as f: f.write("#include <iostream>\nint main() { return 0; }\n")
        with open("utils.cpp", "w") as f: f.write("#include <vector>\nvoid util() {}\n")
        run(["git", "add", "."], cwd=repo)
        run(["git", "commit", "-m", "initial C++ setup"], cwd=repo)
        run(["git", "push", "-u", "origin", "main"], cwd=repo, check=False)

    print(f"Starting live C++ farm. Committing every {SLEEP_TIME} seconds.")
    print("Press Ctrl+C to stop.")
    
    count = 0
    while True:
        try:
            now = dt.datetime.now()
            stamp = now.strftime("%Y-%m-%dT%H:%M:%S")
            
            env = {
                "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp,
                "GIT_AUTHOR_NAME": AUTHOR_NAME, "GIT_AUTHOR_EMAIL": AUTHOR_EMAIL,
                "GIT_COMMITTER_NAME": AUTHOR_NAME, "GIT_COMMITTER_EMAIL": AUTHOR_EMAIL,
            }
            
            fname = random.choice(FILES)
            # Ensure include directory exists if chosen
            if "include/" in fname:
                os.makedirs("include", exist_ok=True)
                
            with open(fname, "a") as f:
                f.write(f"// update {random.randint(1000,9999)}\nvoid func_{random.randint(100,999)}() {{}}\n")
                
            run(["git", "add", fname], cwd=repo, env=env)
            run(["git", "commit", "-q", "-m", random.choice(MESSAGES)], cwd=repo, env=env)
            
            # Push every commit to avoid large local blobs
            run(["git", "push", "-q", "origin", "main"], cwd=repo, env=env, check=False)
            
            count += 1
            print(f"[{now.strftime('%H:%M:%S')}] Commit {count} pushed to cozyAPI.", end="\r")
            
            time.sleep(SLEEP_TIME)
            
        except KeyboardInterrupt:
            print("\nStopped by user.")
            break
        except Exception as e:
            print(f"\nError: {e}, retrying in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()