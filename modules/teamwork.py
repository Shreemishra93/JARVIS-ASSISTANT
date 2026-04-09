"""
Teamwork.com Task Reader Module
Reads tasks assigned to you from Teamwork.com using API token.
"""
import requests
from datetime import datetime


class TeamworkService:
    def __init__(self, site_name, api_token):
        """
        Args:
            site_name: Your Teamwork subdomain (e.g., 'fountaindigital')
            api_token: Teamwork API token (twp_xxx)
        """
        self.base_url = f"https://{site_name}.teamwork.com"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }
        self._user_id = None

    def _get_my_user_id(self):
        """Fetch the authenticated user's ID."""
        if self._user_id:
            return self._user_id
        url = f"{self.base_url}/me.json"
        try:
            resp = requests.get(url, headers=self.headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            self._user_id = data.get("person", {}).get("id", "")
            return self._user_id
        except requests.RequestException:
            return ""

    def get_my_tasks(self, include_completed=False):
        """Fetch tasks assigned to the authenticated user."""
        user_id = self._get_my_user_id()
        url = f"{self.base_url}/tasks.json"
        params = {
            "sort": "duedate",
        }
        if user_id:
            params["responsible-party-id"] = user_id
        if not include_completed:
            params["filter"] = "anytime"
            params["includeCompletedTasks"] = "false"

        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            tasks = data.get("todo-items", [])
            return [
                {
                    "id": t["id"],
                    "title": t["content"],
                    "project": t.get("project-name", "No Project"),
                    "due_date": t.get("due-date", "No deadline"),
                    "priority": t.get("priority", "none"),
                    "status": "completed" if t.get("completed") else "active",
                    "tasklist": t.get("todo-list-name", ""),
                }
                for t in tasks
            ]
        except requests.RequestException as e:
            return [{"error": f"Could not fetch tasks: {e}"}]

    def get_upcoming_tasks(self, days=7):
        """Fetch tasks due within the next N days."""
        tasks = self.get_my_tasks()
        if tasks and "error" in tasks[0]:
            return tasks

        upcoming = []
        today = datetime.now().date()
        for t in tasks:
            if t["due_date"] and t["due_date"] != "No deadline":
                try:
                    due = datetime.strptime(t["due_date"], "%Y%m%d").date()
                    days_left = (due - today).days
                    if 0 <= days_left <= days:
                        t["days_left"] = days_left
                        upcoming.append(t)
                except ValueError:
                    pass
        return upcoming

    def format_report(self, tasks):
        """Format tasks into a printable report."""
        if not tasks:
            return "  No tasks found."
        lines = []
        for i, t in enumerate(tasks, 1):
            if "error" in t:
                lines.append(f"  {t['error']}")
                continue
            due = t["due_date"] if t["due_date"] != "No deadline" else "No deadline"
            priority_marker = {"high": "!!!", "medium": "!!", "low": "!"}.get(t["priority"], "")
            lines.append(
                f"  {i}. [{t['project']}] {t['title']} "
                f"(Due: {due}) {priority_marker}"
            )
        return "\n".join(lines)

    def get_spoken_summary(self, tasks):
        """Return a brief spoken summary."""
        if not tasks:
            return "You have no pending tasks. Well done, Sir."
        valid = [t for t in tasks if "error" not in t]
        if not valid:
            return "I couldn't connect to Teamwork at the moment."

        high_priority = [t for t in valid if t.get("priority") == "high"]
        summary = f"You have {len(valid)} pending tasks."
        if high_priority:
            summary += f" {len(high_priority)} are high priority."
        summary += f" Your top task is: {valid[0]['title']}."
        return summary
