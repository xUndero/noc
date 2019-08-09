# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Beward.BD config normalizer
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.confdb.normalizer.base import BaseNormalizer, match, ANY, REST

RESOLUTION_MAPPER = {
    "2048x2048": "2048x2048",
    "1080p": "1920x1080",
    "sxga": "1280x1024",
    "quadvga": "1280x960",
    "720p": "1280x720",
    ("d1", "ntsc"): "720x480",
    ("d1", "pal"): "720x576",
    "d1": "720x576",
    "vga": "640x480",
    "qvga": "320x240",
    ("cif", "ntsc"): "252x240",
    ("cif", "pal"): "352x288",
    "cif": "352x288",
    "qcif": "176x144",
    "disable": "0x0",
}

AUDIO_CODEC_MAPPER = {
    "ulaw": "g711a",
    "alaw": "g711u",
    "16000": "g726",
    "24000": "g726",
    "32000": "g726",
    "40000": "g726",
    "aac_128000": "aac",
}


class BDNormalizer(BaseNormalizer):
    @match("root", "Network", "HostName", ANY)
    def normalize_hostname(self, tokens):
        yield self.make_hostname(tokens[3])

    @match("root", "Time", "TimeZone", ANY)
    def normalize_timezone(self, tokens):
        yield self.make_tz_offset(tz_name="", tz_offset=tokens[3])

    @match("root", "Time", "SynSource", "NTP")
    def normalize_timesource(self, tokens):
        yield self.make_clock_source(source="ntp")

    @match("root", "Time", "NTP", "Server", REST)
    def normalize_ntp_server(self, tokens):
        yield self.make_ntp_server_address(name="0", address=".".join(tokens[4:]))

    @match("root", "ImageSource", "I0", "Sensor", "Wdr", ANY)
    def normalize_image_wdr(self, tokens):
        yield self.make_video_wide_dynamic_range_admin_status(
            name="default", admin_status=tokens[5] != "off"
        )

    @match("root", "ImageSource", "I0", "Sensor", "Backlight", ANY)
    def normalize_image_blc(self, tokens):
        yield self.make_video_black_light_compensation_admin_status(
            name="default", admin_status=tokens[5] == "on"
        )

    @match("root", "ImageSource", "I0", "Sensor", "Sharpness", ANY)
    def normalize_image_sharpness(self, tokens):
        yield self.make_video_sharpness(name="default", sharpness=tokens[5])

    @match("root", "ImageSource", "I0", "Sensor", "WhiteBalance", ANY)
    def normalize_image_wb(self, tokens):
        yield self.make_video_white_balance_admin_status(
            name="default", admin_status=tokens[5] != "off"
        )
        if tokens[5] == "auto":
            yield self.make_video_white_balance_auto(name="default")

    @match("root", "Image", "I0", "Appearance", "Resolution", ANY)
    def normalize_resolution(self, tokens):
        r = tokens[5].split(",")
        for index, s in enumerate(["mjpeg", "h264", "h264_2"]):
            height, width = RESOLUTION_MAPPER[r[index]].split("x")
            yield self.make_media_streams_video_admin_status(
                name=s, admin_status=r[index] != "disable"
            )
            yield self.make_media_streams_video_resolution_height(name=s, height=height)
            yield self.make_media_streams_video_resolution_width(name=s, width=width)
            yield self.make_stream_rtsp_path(name=s, path="/%s" % s)
            if s == "mjpeg":
                yield self.make_media_streams_video_codec_mpeg4(name=s)
            else:
                yield self.make_media_streams_video_codec_h264(name=s)

    @match("root", "Image", "I0", "RateControl", "H264Mode", ANY)
    def normalize_video_control_mode_h264(self, tokens):
        self.set_context("h264_use_vbr", tokens[5] == "vbr")
        # yield self.make_video_encoder_ratecontrol_mode(name="h264", mode=tokens[5].upper())
        yield

    @match("root", "Image", "I0", "RateControl", "H264_2Mode", ANY)
    def normalize_video_control_h264_2(self, tokens):
        self.set_context("h264_2_use_vbr", tokens[5] == "vbr")
        yield
        # yield self.make_video_encoder_ratecontrol_mode(name="h264_2", mode=tokens[5].upper())

    @match("root", "Image", "I0", "Appearance", "H264_2Bitrate", ANY)
    def normalize_bitrate_h264_2(self, tokens):
        if self.get_context("h264_2_use_vbr"):
            yield self.make_media_streams_video_rate_control_vbr_max_bitrate(
                name="h264_2", max_bitrate=tokens[5]
            )
        else:
            yield self.make_media_streams_video_rate_control_cbr_bitrate(
                name="h264_2", bitrate=tokens[5]
            )

    @match("root", "Image", "I0", "Appearance", "H264Bitrate", ANY)
    def normalize_bitrate_h264(self, tokens):
        if self.get_context("h264_use_vbr"):
            yield self.make_media_streams_video_rate_control_vbr_max_bitrate(
                name="h264", max_bitrate=tokens[5]
            )
        else:
            yield self.make_media_streams_video_rate_control_cbr_bitrate(
                name="h264", bitrate=tokens[5]
            )

    @match("root", "Image", "I0", "Appearance", "H264_2VideoKeyFrameInterval", ANY)
    def normalize_keyframe_h264_2(self, tokens):
        yield self.make_media_streams_video_codec_h264_profile_gov_length(
            name="h264_2", gov_length=tokens[5]
        )

    @match("root", "Image", "I0", "Appearance", "H264VideoKeyFrameInterval", ANY)
    def normalize_keyframe_h264(self, tokens):
        yield self.make_media_streams_video_codec_h264_profile_gov_length(
            name="h264", gov_length=tokens[5]
        )

    @match("root", "Audio", "DuplexMode", ANY)
    def normalize_stream_audio_enable(self, tokens):
        yield self.make_media_streams_audio_admin_status(
            name="h264", admin_status=tokens[3] != "disable"
        )

    @match("root", "AudioSource", ANY, "BitRate", ANY)
    def normalize_stream_audio_encoder(self, tokens):
        #  yield self.make_audio_encoder_bitratelimit(name="h264", bitratelimit=tokens[4])
        yield self.make_media_streams_audio_codec(name="h264", codec=AUDIO_CODEC_MAPPER[tokens[4]])

    @match("root", "Image", "I0", "Text", "String", REST)
    def normalize_overlay_text_text(self, tokens):
        yield self.make_media_streams_overlay_status(overlay_name="1", admin_status=True)
        yield self.make_media_streams_overlay_text(overlay_name="1", text=" ".join(tokens[5:]))

    @match("user", ANY)
    def normalize_username(self, tokens):
        tk = tokens[1].split(":")
        if tk[0] != "Username":
            yield self.make_user_class(username=tk[0], class_name=":".join(tk[1:]))
