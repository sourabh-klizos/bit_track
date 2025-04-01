from pathlib import Path
import sys
import zlib


class FileHandler:
    """Handles file operations like creating, writing, and reading files."""

    @staticmethod
    def create_file(file_path: Path, content: str = "") -> None:
        """Creates a file and writes content to it."""
        try:
            file_path.parent.mkdir(
                parents=True, exist_ok=True
            )  # Ensure the directory exists
            file_path.write_text(content)
        except Exception as e:
            print(f"Error creating file {file_path}: {e}")

    @staticmethod
    def read_file(file_path: Path) -> str:
        """Reads content from a file and returns it."""
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            with file_path.open("rb") as f:
                compressed_data = f.read()
            if not compressed_data:
                sys.stdout.write("No files staged.\n")
                return

            try:
                decompressed_data = zlib.decompress(compressed_data).decode()
                obj_ids = []
                if decompressed_data:
                    for line in decompressed_data.splitlines():
                        mode, obj_id, path = line.strip().split(" ", 2)
                        obj_ids.append(obj_id)
                        # sys.stdout.write(f"  {mode} {obj_id} {path}\n")

                    print(obj_ids)
                    return obj_ids

            except zlib.error:
                sys.stdout.write("Error: Corrupted index file.\n")
                return

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

    @staticmethod
    def file_exists(file_path: Path) -> bool:
        """Checks if a file exists."""
        return file_path.exists()
