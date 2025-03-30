from pathlib import Path
import sys



# class BitTrackRepository:
    # @staticmethod
    # def init():
    #     """Initialize a BitTrack repository in the current directory."""
    #     try:
    #         worktree = Path.cwd()
    #         bt_dir = worktree / ".bit_track"

    #         if bt_dir.exists():
    #             sys.stdout.write("A BitTrack repository already exists here.\n")
    #             return

    #         bt_dir.mkdir()
    #         (bt_dir / "objects").mkdir()
    #         (bt_dir / "refs").mkdir()

    #         (bt_dir / "HEAD").write_text("ref: refs/heads/main\n")
    #         (bt_dir / "config").write_text("""[core]\n	repositoryformatversion = 0\n	filemode = false\n	bare = false\n""")
    #         (bt_dir / "index").touch()

    #         sys.stdout.write(f"Initialized empty BitTrack repository in {bt_dir}\n")
    #     except Exception as e:
    #         sys.stdout.write(f"Error initializing repository: {e}\n")


class BitTrackRepository:
    """Manage paths for a BitTrack repository and allow initialization."""

    worktree = Path.cwd()
    bt_dir = worktree / ".bit_track"
    objects_dir = bt_dir / "objects"
    refs_dir = bt_dir / "refs"
    head_file = bt_dir / "HEAD"
    config_file = bt_dir / "config"
    index_file = bt_dir / "index"

    @classmethod
    def init(cls):
        """Initialize a BitTrack repository in the current directory."""
        try:
            if cls.bt_dir.exists():
                sys.stdout.write("A BitTrack repository already exists here.\n")
                return

            cls.bt_dir.mkdir()
            cls.objects_dir.mkdir()
            cls.refs_dir.mkdir()

            cls.head_file.write_text("ref: refs/heads/main\n")
            cls.config_file.write_text(
                "[core]\n\trepositoryformatversion = 0\n\tfilemode = false\n\tbare = false\n"
            )
            cls.index_file.touch()

            sys.stdout.write(f"Initialized empty BitTrack repository in {cls.bt_dir}\n")
        except Exception as e:
            sys.stdout.write(f"Error initializing repository: {e}\n")
