import inspect
import os
from argparse import Namespace
from mcp.server.mcpserver.exceptions import InvalidSignature
from mcp.server.mcpserver import MCPServer
from pydantic import PydanticUserError
from huggingface_hub import HfApi

mcp = MCPServer("huggingface")
hf_api = HfApi(token=os.environ["HF_TOKEN"])


def make_tool(name, method):
    sig = inspect.signature(method)

    def tool(**kwargs):
        return method(**kwargs)

    tool.__name__ = name
    tool.__doc__ = inspect.getdoc(method) or f"Execute HfApi.{name}"
    tool.__signature__ = sig

    return tool


def cmd_mcp(_: Namespace) -> None:
    eligible_tools = set([
        "get_organization_overview",
        "get_user_overview",
        "list_user_repos",
        "list_organization_members",
        "list_organization_followers",
        "list_user_followers",
        "list_repo_likers",
        "list_liked_repos",
        "get_dataset_leaderboard",
        "get_discussion_details",
        "list_repo_commits",
        "list_papers",
    ])

    for name, method in inspect.getmembers(hf_api, predicate=callable):
        if name not in eligible_tools:
            continue

        mcp.tool(name=name)(make_tool(name, method))

    mcp.run()
