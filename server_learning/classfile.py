class TestClass:
    def __init__(self, start_board) -> None:
        self.start_board = start_board
        self.empty_data_to_send = "empty"

    # def __str__(self) -> str:
    #     ret_str = ""
    #     for row in self.start_board:
    #         for tup in row:
    #             ret_str += f"({tup[0]}, {tup[1]}) "
    #         ret_str += '\n'
    #     return ret_str