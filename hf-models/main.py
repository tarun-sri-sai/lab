from argparse import ArgumentParser
from hf.models import update_models
from hf.mcp import cmd_mcp


def main() -> None:
    parser = ArgumentParser(description="hf-models")

    subcommands = parser.add_subparsers(
        dest="command",
        required=True
    )

    models_parser = subcommands.add_parser(
        "models",
        help="models commands"
    )

    models_subcommands = models_parser.add_subparsers(
        dest="models_subcommands",
        required=True
    )

    models_update_subparser = models_subcommands.add_parser(
        "update",
        help="updates models",
    )

    mcp_parser = subcommands.add_parser(
        "mcp",
        help="start the MCP server"
    )
    mcp_parser.set_defaults(func=cmd_mcp)

    models_update_subparser.set_defaults(func=update_models)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
