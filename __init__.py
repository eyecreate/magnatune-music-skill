from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.audioservice import AudioService
from .api import get_session, Album, Artist


class MagnatuneMusic(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.audio_service = None
        
    def start_magnatune_playback(self,result):
        speakback = dict()
        self.audio_service = AudioService(self.bus)
        speakback['artist'] = result.artist.name
        speakback['album'] = result.name
        self.speak_dialog('music.magnatune',speakback)
        self.audio_service.stop()
        self.audio_service.play('http://he3.magnatune.com/music/'+result.artist.name+'/'+result.name+'/'+result.sku+'_spoken_128.mp3')

    @intent_file_handler('music.magnatune.intent')
    def handle_music_magnatune(self, message):
        media = message.data['media']
        session = get_session()
        query = session.query(Album)
        query = query.filter(getattr(Album, 'name').like('%' + media + '%'))
        results = query.all()
        if query.count() > 0:
            self.start_magnatune_playback(results[0])
        else:
            self.speak_dialog('not-found')
            
    @intent_file_handler('artist.magnatune.intent')
    def handle_artist_magnatune(self,message):
        artist = message.data['artist']
        session = get_session()
        query = session.query(Album)
        query = query.join(Artist).filter(Artist.name.like('%' + artist + '%'))
        results = query.all()
        if query.count() > 0:
            self.start_magnatune_playback(results[0])
        else:
            self.speak_dialog('not-found')
            
    @intent_file_handler('stop-music.magnatune.intent')
    def handle_stop_music(self,message):
        self.audio_service = AudioService(self.bus)
        self.audio_service.stop()
        
    @intent_file_handler('pause-music.magnatune.intent')
    def handle_pause_music(self,message):
        self.audio_service = AudioService(self.bus)
        self.audio_service.pause()
        
    @intent_file_handler('resume-music.magnatune.intent')
    def handle_resume_music(self,message):
        self.audio_service = AudioService(self.bus)
        self.audio_service.resume()


def create_skill():
    return MagnatuneMusic()

