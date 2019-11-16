"""
    play the sound file
"""
import playsound

# output_filename2 = ".mp3"
# output_filepath = "E:\\pycode\\DTLD\\output\\"


def play(act_id, play_path):
    """

    :param act_id:
    :param play_path:
    :return:
    """
    playsound.playsound(play_path + str(act_id) + ".mp3")