# pylint: disable=unexpected-keyword-arg
import os

import click
import requests
from furl import furl


@click.command()
@click.option(
    "--drone-token",
    required=True,
)
@click.option(
    "--target",
    required=True,
)
def command(drone_token, target):
    drone_build_link = os.getenv("DRONE_BUILD_LINK")
    f = furl(drone_build_link)
    drone_server_url = f.url.replace(f.pathstr, "")
    f.url.replace(f.pathstr, "")
    http = requests.Session()
    http.headers.update({"Authorization": f"Bearer {drone_token}"})
    repo = os.getenv("DRONE_REPO")
    build_number = os.getenv("DRONE_BUILD_NUMBER")
    url = f"{drone_server_url}/api/repos/{repo}/builds/{build_number}/promote?target={target}"
    res = http.post(url)
    res.raise_for_status()
    new_deployment_number = res.json()["number"]
    deployment_link = f"{drone_server_url}/{repo}/{new_deployment_number}"
    click.echo(f"Deployed {repo}@{build_number} to {target}")
    click.echo(f"Link to new deployment: {deployment_link}")


run = lambda: command(auto_envvar_prefix="PLUGIN")
