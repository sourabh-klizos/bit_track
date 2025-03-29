from pathlib import Path
import sys



class BitTrackRepository:
    @staticmethod
    def init():
        """Initialize a BitTrack repository in the current directory."""
        try:
            worktree = Path.cwd()
            bt_dir = worktree / ".bit_track"

            if bt_dir.exists():
                sys.stdout.write("A BitTrack repository already exists here.\n")
                return

            bt_dir.mkdir()
            (bt_dir / "objects").mkdir()
            (bt_dir / "refs").mkdir()

            (bt_dir / "HEAD").write_text("ref: refs/heads/main\n")
            (bt_dir / "config").write_text("""[core]\n	repositoryformatversion = 0\n	filemode = false\n	bare = false\n""")
            (bt_dir / "index").touch()

            sys.stdout.write(f"Initialized empty BitTrack repository in {bt_dir}\n")
        except Exception as e:
            sys.stdout.write(f"Error initializing repository: {e}\n")
