import subprocess
import sys


def main() -> None:
    print("\nStarting Sarateal API (stateless, no database)...")
    print("Open API docs at: http://127.0.0.1:8000/docs")

    run_command(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--reload",
        ]
    )


def run_command(command: list[str]) -> None:
    print(f"\nRunning: {' '.join(command)}")
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()