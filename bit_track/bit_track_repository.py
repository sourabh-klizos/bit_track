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
    heads_dir = refs_dir/ "heads"
    main_file = heads_dir / "main"





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
            cls.heads_dir.mkdir()
            cls.main_file.touch()
            

            cls.head_file.write_text("ref: refs/heads/main\n")
            # cls.config_file.write_text(
            #     "[core]\n\trepositoryformatversion = 0\n\tfilemode = false\n\tbare = false\n"
            # )
            cls.index_file.touch()


            cls.set_user_config()

            sys.stdout.write(f"Initialized empty BitTrack repository in {cls.bt_dir}\n")
        except Exception as e:
            sys.stdout.write(f"Error initializing repository: {e}\n")


    @classmethod
    def set_user_config(cls):
        """Ask for user name and email and save it to config."""
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        
        config_content = cls.config_file.read_text() if cls.config_file.exists() else ""
        config_content += f"\n[user]\n\tname = {name}\n\temail = {email}\n"
        cls.config_file.write_text(config_content)
        sys.stdout.write("User configuration saved successfully.\n")

        # print(cls.get_user_config())


    @classmethod
    def get_user_config(cls):
        """Retrieve user name and email from config."""
        if not cls.config_file.exists():
            return None, None

        config_content = cls.config_file.read_text()
        name, email = None, None

        for line in config_content.splitlines():
            if line.startswith("\tname = "):
                name = line.split("= ")[1].strip()
            elif line.startswith("\temail = "):
                email = line.split("= ")[1].strip()

        return name, email

