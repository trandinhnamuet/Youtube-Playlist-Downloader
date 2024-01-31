from pytube import YouTube as _YouTube

from pytube.innertube import InnerTube


class YouTube(_YouTube):
    @property
    def vid_info(self):
        """Parse the raw vid info and return the parsed result.

        :rtype: Dict[Any, Any]
        """
        if self._vid_info:
            return self._vid_info

        innertube = InnerTube(client='ANDROID', use_oauth=self.use_oauth,
                              allow_cache=self.allow_oauth_cache)

        innertube_response = innertube.player(self.video_id)
        self._vid_info = innertube_response
        return self._vid_info
