######################
#
# If black has the starting move, the result has to be flipped(negated *-1)
# since we are gonna use white as the perspective in the Tsetlin Machine
#
# python-chess is licensed under the GPL 3 (or any later version at your option).
# Check out LICENSE.txt for the full text.
# Github: https://github.com/niklasf/python-chess
#
######################

import chess.syzygy

with chess.syzygy.open_tablebase("data/syzygy/regular") as tablebase:
    board = chess.Board("8/2K5/4B3/3N4/8/8/4k3/8 b - - 0 1")
    print(board.is_valid())
    print(tablebase.probe_wdl(board)*-1)