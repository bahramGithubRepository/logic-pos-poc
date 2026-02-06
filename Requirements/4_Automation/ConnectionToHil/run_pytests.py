import pytest, logging, argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args, pytest_args = parser.parse_known_args()

    print(args.debug)
    

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    print(f"--log-cli-{'level=DEBUG' if args.debug else 'level=INFO'}")
    pytest.main([
        "-v", 
        f"--log-cli-{'level=DEBUG' if args.debug else 'level=INFO'}",
        "tests"
    ])