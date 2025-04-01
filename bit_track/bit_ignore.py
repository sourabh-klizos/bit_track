from pathlib import Path
import fnmatch



class BitIgnore:
    IGNORE_FILE = ".bitignore"

    @staticmethod
    def load_ignored_patterns():
        """Load ignore patterns from the .bitignore file."""
        ignore_path = Path.cwd() / BitIgnore.IGNORE_FILE
        patterns = set()

        if ignore_path.exists():
            with ignore_path.open("r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"): 
                        patterns.add(line)
        return patterns

    @staticmethod
    def is_ignored(file_path: Path, ignore_patterns):
        """Check if a file or directory should be ignored."""
        relative_path = file_path.relative_to(Path.cwd())

        for pattern in ignore_patterns:
            # Check for exact match or wildcard match
            if fnmatch.fnmatch(str(relative_path), pattern) or fnmatch.fnmatch(file_path.name, pattern):
                return True

            # Ignore all contents of a folder if the pattern ends with "/"
            if pattern.endswith("/") and str(relative_path).startswith(pattern.rstrip("/")):
                return True

        return False

    @staticmethod
    def list_tracked_files():
        """List all non-ignored files."""
        ignore_patterns = BitIgnore.load_ignored_patterns()
        tracked_files = []

        for file_path in Path.cwd().rglob("*"):
            if ".bit_track" in file_path.parts:  # Always ignore the repo folder
                continue
            if BitIgnore.is_ignored(file_path, ignore_patterns):
                # print(f"Ignoring: {file_path}")
                continue


            tracked_files.append(file_path)

        return tracked_files
