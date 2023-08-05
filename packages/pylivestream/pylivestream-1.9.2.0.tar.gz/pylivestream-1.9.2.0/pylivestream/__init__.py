from pathlib import Path
from typing import List, Union, Dict, Sequence
import logging
#
from . import stream
from . import utils

__all__ = ['FileIn', 'Microphone', 'SaveDisk', 'Screenshare', 'Webcam']


class Livestream(stream.Stream):

    def __init__(self,
                 inifn: Path, site: str, *,
                 vidsource: str = None,
                 image: Path = None,
                 loop: bool = False,
                 infn: Path = None,
                 caption: str = None,
                 yes: bool = False,
                 timeout: int = None) -> None:
        super().__init__(inifn, site, vidsource=vidsource,
                         image=image, loop=loop,
                         infn=infn, caption=caption, yes=yes,
                         timeout=timeout)

        self.site = site.lower()

        self.osparam()

        self.video_bitrate()

        vidIn: List[str] = self.videoIn()
        vidOut: List[str] = self.videoOut()

        audIn: List[str] = self.audioIn()
        audOut: List[str] = self.audioOut()

        buf: List[str] = self.buffer(self.server)
# %% begin to setup command line
        cmd: List[str] = []
        cmd.append(self.exe)

        cmd += self.loglevel
        cmd += self.yes

#        cmd += self.timelimit  # terminate input after N seconds, IF specified

        cmd += self.queue

        cmd += vidIn + audIn

        if not self.movingimage:  # FIXME: need a different filter chain to caption moving images
            cmd += self.F.drawtext(self.caption)

        cmd += vidOut + audOut
        cmd += buf

        cmd.extend(self.timelimit)  # terminate output after N seconds, IF specified

        streamid: str = self.key if self.key else ''

        self.sink: List[str] = [self.server + streamid]

        self.cmd: List[str] = cmd + self.sink
# %% quick check command, to verify device exists
        # 0.1 seems OK, spurious buffer error on Windows that wasn't helped by any bigger size
        CHECKTIMEOUT = '0.1'

        self.checkcmd: List[str] = ([self.exe] +
                                    self.loglevel + ['-t', CHECKTIMEOUT] +
                                    self.videoIn(quick=True) +
                                    self.audioIn(quick=True) +
                                    ['-t', CHECKTIMEOUT] +  # webcam needs at output
                                    ['-f', 'null', '-']
                                    )

    def startlive(self, sinks: Sequence[str] = None):
        """finally start the stream(s)"""

        self.check_device()

        proc = None
# %% special cases for localhost tests
        if self.key is None and self.site != 'localhost-test':
            if self.site == 'localhost':
                proc = self.F.listener()  # start own RTMP server
            else:
                print('\n', ' '.join(self.cmd), '\n', flush=True)
                return

        if proc is not None and proc.poll() is not None:
            # listener stopped prematurely, probably due to error
            raise RuntimeError(f'listener stopped with code {proc.poll()}')
# %% RUN STREAM
        cmd: List[str]
        if not sinks:  # single stream
            utils.run(self.cmd)
        elif self.movingimage:
            if len(sinks) > 1:
                logging.warning(f'streaming only to {sinks[0]}')

            utils.run(self.cmd)
        elif len(sinks) == 1:
            utils.run(self.cmd)
        else:  # multi-stream output tee
            cmdstem: List[str] = self.cmd[:-3]
            # +global_header is necessary to tee to multiple services
            cmd = cmdstem + ['-flags:v', '+global_header',
                             '-f', 'tee']

            if self.image:
                #  connect image to video stream, audio file to audio stream
                cmd += ['-map', '0:v', '-map', '1:a']
            else:
                if self.vidsource == 'file':
                    # picks first video and audio stream, often correct
                    cmd += ['-map', '0:v', '-map', '0:a:0']
                else:  # device (webcam)
                    # connect video device to video stream,
                    # audio device to audio stream
                    cmd += ['-map', '0:v', '-map', '1:a']

            cmd += ['[f=flv]' + '|[f=flv]'.join(sinks)]  # no double quotes

            utils.run(cmd)

# %% stop the listener before starting the next process, or upon final process closing.
        if proc is not None and proc.poll() is None:
            proc.terminate()
        yield


# %% operators
class Screenshare(Livestream):

    def __init__(self,
                 inifn: Path,
                 websites: Union[str, Sequence[str]],
                 caption: str = None,
                 yes: bool = False,
                 timeout: int = None):

        vidsource = 'screen'

        if isinstance(websites, str):
            websites = [websites]

        streams = {}
        for site in websites:
            streams[site] = Livestream(inifn, site, vidsource=vidsource,
                                       caption=caption, yes=yes, timeout=timeout)

        self.streams: Dict[str, Livestream] = streams

    def golive(self):

        sinks: List[str] = [self.streams[stream].sink[0]
                            for stream in self.streams]

        try:
            next(self.streams[unify_streams(self.streams)].startlive(sinks))
        except StopIteration:
            pass


class Webcam(Livestream):

    def __init__(self,
                 inifn: Path,
                 websites: Union[str, Sequence[str]], *,
                 caption: str = None,
                 yes: bool = False,
                 timeout: int = None):

        vidsource = 'camera'

        if isinstance(websites, str):
            websites = [websites]

        streams = {}
        for site in websites:
            streams[site] = Livestream(inifn, site, vidsource=vidsource,
                                       caption=caption, yes=yes,
                                       timeout=timeout)

        self.streams: Dict[str, Livestream] = streams

    def golive(self):

        sinks: List[str] = [self.streams[stream].sink[0]
                            for stream in self.streams]

        try:
            next(self.streams[unify_streams(self.streams)].startlive(sinks))
        except StopIteration:
            pass


class Microphone(Livestream):

    def __init__(self,
                 inifn: Path,
                 websites: Union[str, Sequence[str]], *,
                 image: Path,
                 caption: str = None,
                 yes: bool = False,
                 timeout: int = None):

        if isinstance(websites, str):
            websites = [websites]

        streams = {}
        for site in websites:
            streams[site] = Livestream(inifn, site, image=image,
                                       loop=True,
                                       caption=caption, yes=yes, timeout=timeout)

        self.streams: Dict[str, Livestream] = streams

    def golive(self):

        sinks: List[str] = [self.streams[stream].sink[0]
                            for stream in self.streams]

        try:
            next(self.streams[unify_streams(self.streams)].startlive(sinks))
        except StopIteration:
            pass


# %% File-based inputs
class FileIn(Livestream):

    def __init__(self,
                 inifn: Path,
                 websites: Union[str, Sequence[str]], *,
                 infn: Path,
                 loop: bool = False,
                 image: Path = None,
                 caption: str = None,
                 yes: bool = False,
                 timeout: int = None):

        vidsource = 'file'

        if isinstance(websites, str):
            websites = [websites]

        streams = {}
        for site in websites:
            streams[site] = Livestream(inifn, site, vidsource=vidsource, image=image,
                                       loop=loop, infn=infn,
                                       caption=caption, yes=yes, timeout=timeout)

        self.streams: Dict[str, Livestream] = streams

    def golive(self):

        sinks: List[str] = [self.streams[stream].sink[0]
                            for stream in self.streams]

        try:
            next(self.streams[unify_streams(self.streams)].startlive(sinks))
        except StopIteration:
            pass


class SaveDisk(stream.Stream):

    def __init__(self,
                 inifn: Path, outfn: Path = None, *,
                 caption: str = None,
                 yes: bool = False,
                 timeout: int = None):
        """
        records to disk screen capture with audio

        if not outfn, just cite command that would have run
        """
        site = 'file'
        vidsource = 'screen'

        super().__init__(inifn, site,
                         vidsource=vidsource, caption=caption, timeout=timeout)

        self.outfn = Path(outfn).expanduser() if outfn else None

        self.osparam()

        vidIn: List[str] = self.videoIn()
        vidOut: List[str] = self.videoOut()

        audIn: List[str] = self.audioIn()
        audOut: List[str] = self.audioOut()

        self.cmd: List[str] = [str(self.exe)]
        self.cmd += vidIn + audIn
        self.cmd += vidOut + audOut

        # ffmpeg relies on suffix for container type, this is a fallback.
        if self.outfn and not self.outfn.suffix:
            self.cmd += ['-f', 'flv']

        self.cmd += [str(self.outfn)]

#        if sys.platform == 'win32':  # doesn't seem to be needed.
#            cmd += ['-copy_ts']

    def save(self):

        if self.outfn:
            utils.run(self.cmd)

        else:
            print('specify filename to save screen capture w/ audio to disk.')


def unify_streams(streams: Dict[str, stream.Stream]) -> str:
    """
    find least common denominator stream settings,
        so "tee" output can generate multiple streams.
    First try: use stream with lowest video bitrate.

    Exploits that Python >= 3.6 has guaranteed dict() ordering.

    fast native Python argmin()
    https://stackoverflow.com/a/11825864
    """
    vid_bw: List[int] = [streams[s].video_kbps for s in streams]

    argmin: int = min(range(len(vid_bw)), key=vid_bw.__getitem__)

    key: str = list(streams.keys())[argmin]

    return key
