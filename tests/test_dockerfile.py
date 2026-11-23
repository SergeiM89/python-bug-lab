from pathlib import Path


def test_dockerfile_copies_existing_requirements_from_context():
    project_root = Path(__file__).resolve().parents[1]
    dockerfile = (project_root / "Dockerfile").read_text()
    instructions = [line.split() for line in dockerfile.splitlines()]

    assert ["COPY", "requirements.txt", "."] in instructions
    assert (project_root / "requirements.txt").is_file()
