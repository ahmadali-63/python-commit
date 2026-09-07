import os
import subprocess
import random
from datetime import datetime, timedelta

# ================= CONFIGURATION =================
TOTAL_COMMITS = 200   # Exact total commits to create
DAYS_BACK = 365       # Spread across the past 365 days (1 year)
# =================================================

def run_git_commit(commit_date_str, commit_num):
    # Update log file
    with open("activity.log", "a") as f:
        f.write(f"Commit #{commit_num} - {commit_date_str}\n")
    
    # Stage the file
    subprocess.run(["git", "add", "activity.log"], check=True, stdout=subprocess.DEVNULL)
    
    # Set Git author and committer dates
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_date_str
    env["GIT_COMMITTER_DATE"] = commit_date_str
    
    commit_msg = f"Update log entry #{commit_num} ({commit_date_str.split()[0]})"
    subprocess.run(
        ["git", "commit", "-m", commit_msg, "--date", commit_date_str],
        env=env,
        check=True,
        stdout=subprocess.DEVNULL
    )

def main():
    print(f"🚀 Generating exactly {TOTAL_COMMITS} commits across the last {DAYS_BACK} days...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DAYS_BACK)
    total_seconds_range = int((end_date - start_date).total_seconds())
    
    # Generate 200 random timestamps and sort them in chronological order
    commit_timestamps = []
    for _ in range(TOTAL_COMMITS):
        random_seconds = random.randint(0, total_seconds_range)
        random_date = start_date + timedelta(seconds=random_seconds)
        
        # Adjust hours to normal working hours (9 AM - 10 PM)
        adjusted_time = random_date.replace(
            hour=random.randint(9, 22),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        commit_timestamps.append(adjusted_time)
    
    # Sort so commit history flows forward in time
    commit_timestamps.sort()
    
    # Execute all 200 commits
    for index, commit_time in enumerate(commit_timestamps, start=1):
        date_str = commit_time.strftime("%Y-%m-%d %H:%M:%S")
        run_git_commit(date_str, index)
        
        if index % 25 == 0 or index == TOTAL_COMMITS:
            print(f"  ⚡ Progress: {index}/{TOTAL_COMMITS} commits created...")

    print("\n✅ Done! Exactly 200 commits created successfully.")
    print("👉 Push them now by running:")
    print("   git push origin main")

if __name__ == "__main__":
    main()