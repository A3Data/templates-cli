import requests
import getpass
import socket
import platform
import os
import json
import yaml

TELEMETRY_ENDPOINT = "https://a3workflow.mtttecnologia.com.br/webhook/52ff1099-dbab-41a4-a1e1-4631467d3ec1"


def username_github() -> str:
    gh_config_path = os.path.expanduser("~/.config/gh/hosts.yml")

    if not os.path.exists(gh_config_path):
        return None

    with open(gh_config_path, "r") as file:
        config = yaml.safe_load(file)

    github_info = config.get("github.com")
    # print(github_info)
    if not github_info or "user" not in github_info:
        return None
    return github_info["user"]


def send_telemetry(data: dict) -> None:
    template_name = data.get("template_name", "unknown")
    code = data.get("code", "")

    payload = {
        "user_info": {
            "user": getpass.getuser(),
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "cwd": os.getcwd(),
            "github_username": username_github() or "unknown",
        },
        "template": template_name,
        "metadata": data or {},
        "code": code or "",
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(
            TELEMETRY_ENDPOINT, data=json.dumps(payload), headers=headers, timeout=5
        )
        return response.json() if response.content else {"status": "success"}
    except Exception as e:
        pass
