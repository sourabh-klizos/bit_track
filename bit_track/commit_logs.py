from bit_track.bit_track_repository import BitTrackRepository



class BitTrackLogs():

    main_file = BitTrackRepository.main_file

    @staticmethod
    def read_commit_pointer():

        with BitTrackLogs.main_file.open("r") as file:
            pointer = file.read().strip()
            print("pointer   ", pointer)
            return pointer 

    @staticmethod
    def generate_index_log(main_file: str, index_log: str):

        latest_commit = BitTrackLogs.read_commit_pointer()

