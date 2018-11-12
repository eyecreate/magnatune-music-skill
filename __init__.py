from mycroft import MycroftSkill, intent_file_handler


class MagnatuneMusic(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('music.magnatune.intent')
    def handle_music_magnatune(self, message):
        self.speak_dialog('music.magnatune')


def create_skill():
    return MagnatuneMusic()

