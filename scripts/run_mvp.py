import subprocess
import sys


def run_command(command: list[str]) -> None:
    print(f"\nRunning: {' '.join(command)}")
    subprocess.run(command, check=True)


def main() -> None:
    run_command([sys.executable, "scripts/init_db.py"])
    run_command([sys.executable, "scripts/seed_base_data.py"])
    run_command([sys.executable, "scripts/seed_demo_data.py"])

    print("\nStarting Sarateal API...")
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


if __name__ == "__main__":
    main()