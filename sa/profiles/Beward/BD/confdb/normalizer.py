# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Beward.BD config normalizer
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.confdb.normalizer.base import BaseNormalizer, match, ANY, REST
from noc.core.confdb.syntax import DEF, BOOL, CHOICES

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
    "ulaw": "g711A",
    "alaw": "g711U",
    "16000": "g726",
    "24000": "g726",
    "32000": "g726",
    "40000": "g726",
    "aac_128000": "aac",
}


class BDNormalizer(BaseNormalizer):

    SYNTAX = [
        DEF(
            "system",
            [
                DEF(
                    "clock",
                    [
                        DEF(
                            "source",
                            [
                                DEF(
                                    CHOICES("ntp", "local"),
                                    required=True,
                                    default="local",
                                    name="source",
                                    gen="make_clock_source",
                                )
                            ],
                        ),
                        DEF(
                            "ntp_servers",
                            [
                                DEF(
                                    ANY,
                                    required=False,
                                    name="server",
                                    gen="make_ntp_server",
                                    multi=True,
                                )
                            ],
                        ),
                    ],
                )
            ],
        ),
        DEF(
            "image-sources",
            [
                DEF(
                    ANY,
                    [
                        DEF(
                            "name",
                            [
                                DEF(
                                    BOOL,
                                    required=False,
                                    name="enabled",
                                    gen="make_image_source_name",
                                )
                            ],
                        )
                    ],
                    multi=True,
                    name="video_source",
                    gen="make_video_source",
                )
                # DEF("resolution", [
                #     DEF(ANY, required=False, name="resolution", gen="make_video_source_resolution"),
                # Move to video_source
                #     ]),
            ],
        ),
        DEF(
            "audio-sources",
            [
                DEF(
                    ANY,
                    [
                        DEF(
                            "name",
                            [
                                DEF(
                                    BOOL,
                                    required=False,
                                    name="enabled",
                                    gen="make_audio_source_name",
                                )
                            ],
                        )
                    ],
                    multi=True,
                    name="audio_source",
                    gen="make_audio_source",
                )
            ],
        ),
        DEF(
            "media-profiles",
            [
                DEF(
                    ANY,
                    [
                        DEF(
                            "image-source",
                            [
                                DEF(
                                    "source-name",
                                    [
                                        DEF(
                                            ANY,
                                            required=False,
                                            name="source_name",
                                            gen="make_video_source_profile",
                                        )
                                    ],
                                ),
                                DEF(
                                    "imaging",
                                    [
                                        DEF(
                                            "brightness",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="brightness",
                                                    gen="make_image_brightness",
                                                )
                                            ],
                                        ),
                                        DEF(
                                            "saturation",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="saturation",
                                                    gen="make_image_saturation",
                                                )
                                            ],
                                        ),
                                        DEF(
                                            "contrast",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="contrast",
                                                    gen="make_image_contrast",
                                                )
                                            ],
                                        ),
                                        DEF(
                                            "sharpness",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="sharpness",
                                                    gen="make_image_sharpness",
                                                )
                                            ],
                                        ),
                                        DEF(
                                            "white-balance",
                                            [
                                                DEF(
                                                    "cr-gain",
                                                    [
                                                        DEF(
                                                            ANY,
                                                            required=False,
                                                            name="gain",
                                                            gen="make_image_wb_crgain",
                                                        )
                                                    ],
                                                ),
                                                DEF(
                                                    "gb-gain",
                                                    [
                                                        DEF(
                                                            ANY,
                                                            required=False,
                                                            name="brightness",
                                                            gen="make_image__wb_gbgain",
                                                        )
                                                    ],
                                                ),
                                                DEF(
                                                    "mode",
                                                    [
                                                        DEF(
                                                            CHOICES("auto", "on", "off"),
                                                            required=False,
                                                            name="mode",
                                                            gen="make_image_wb_mode",
                                                        )
                                                    ],
                                                ),
                                            ],
                                        ),
                                        DEF(
                                            "wide-dynamic-range",
                                            [
                                                DEF(
                                                    "level",
                                                    [
                                                        DEF(
                                                            ANY,
                                                            required=False,
                                                            name="level",
                                                            gen="make_image_wdr_level",
                                                        )
                                                    ],
                                                ),
                                                DEF(
                                                    "mode",
                                                    [
                                                        DEF(
                                                            CHOICES("auto", "on", "off"),
                                                            required=False,
                                                            name="mode",
                                                            gen="make_image_wdr_mode",
                                                        )
                                                    ],
                                                ),
                                            ],
                                        ),
                                        DEF(
                                            "black-light-compensation",
                                            [
                                                DEF(
                                                    "enabled",
                                                    [
                                                        DEF(
                                                            BOOL,
                                                            required=False,
                                                            name="enabled",
                                                            gen="make_image_blc_enable",
                                                        )
                                                    ],
                                                ),
                                                DEF(
                                                    "mode",
                                                    [
                                                        DEF(
                                                            ANY,
                                                            required=False,
                                                            name="mode",
                                                            gen="make_image_blc_mode",
                                                        )
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                    required=True,
                    multi=True,
                    name="profile_name",
                )
            ],
        ),
        DEF(
            "encoder_profiles",
            [
                DEF(
                    ANY,
                    [
                        DEF(
                            "source-name",
                            [
                                DEF(
                                    ANY,
                                    required=False,
                                    name="source_name",
                                    gen="make_encoder_source",
                                )
                            ],
                        ),
                        DEF(
                            "enabled",
                            [DEF(BOOL, required=False, name="enabled", gen="make_enable_stream")],
                        ),
                        DEF(
                            "video-encoder",
                            [
                                DEF(
                                    "encoding",
                                    [
                                        DEF(
                                            CHOICES("MJPEG", "H264"),
                                            required=False,
                                            name="encoding",
                                            gen="make_video_encoder_encoding",
                                        )
                                    ],
                                ),
                                DEF(
                                    "resolution",
                                    [
                                        DEF(
                                            "height",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="height",
                                                    gen="make_video_encoder_resolution_h",
                                                )
                                            ],
                                        ),
                                        DEF(
                                            "width",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="width",
                                                    gen="make_video_encoder_resolution_w",
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                                DEF(
                                    "quality",
                                    [
                                        DEF(
                                            ANY,
                                            required=False,
                                            name="quality",
                                            gen="make_video_encoder_quality",
                                        )
                                    ],
                                ),
                                DEF(
                                    "rate-control",
                                    [
                                        DEF(
                                            "mode",
                                            [
                                                DEF(
                                                    CHOICES("VBR", "CBR"),
                                                    required=False,
                                                    name="mode",
                                                    gen="make_video_encoder_ratecontrol_mode",
                                                )
                                            ],
                                        ),
                                        DEF(
                                            "framerate-limit",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="frameratelimit",
                                                    gen="make_video_encoder_frameratelimit",
                                                )
                                            ],
                                        ),
                                        DEF(
                                            "bitrate-limit",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="bitratelimit",
                                                    gen="make_video_encoder_bitratelimit",
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                                # @todo MJPEG profile
                                DEF(
                                    "h264",
                                    [
                                        DEF(
                                            "gov-length",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="gov_length",
                                                    gen="make_video_encoder_h264_gov_length",
                                                )
                                            ],
                                        ),
                                        DEF(
                                            "h264-profile",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="h264_profile",
                                                    gen="make_video_encoder_h264_profile",
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        DEF(
                            "audio-encoder",
                            [
                                DEF(
                                    "enabled",
                                    [
                                        DEF(
                                            BOOL,
                                            required=False,
                                            name="enabled",
                                            gen="make_enable_audio_stream",
                                        )
                                    ],
                                ),
                                DEF(
                                    "source-name",
                                    [
                                        DEF(
                                            ANY,
                                            required=False,
                                            name="source_name",
                                            gen="make_audio_encoder_source",
                                        )
                                    ],
                                ),
                                DEF(
                                    "encoding",
                                    [
                                        DEF(
                                            ANY,
                                            required=False,
                                            name="encoding",
                                            gen="make_audio_encoder_encoding",
                                        )
                                    ],
                                ),
                                DEF(
                                    "bitrate-limit",
                                    [
                                        DEF(
                                            ANY,
                                            required=False,
                                            name="bitratelimit",
                                            gen="make_audio_encoder_bitratelimit",
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                    required=True,
                    multi=True,
                    name="stream_id",
                )
            ],
        ),
        DEF(
            "overlays",
            [
                DEF(
                    "text",
                    [
                        DEF(
                            ANY,
                            [
                                DEF(
                                    "enabled",
                                    [
                                        DEF(
                                            BOOL,
                                            required=False,
                                            name="enabled",
                                            gen="make_enable_text_overlay",
                                        )
                                    ],
                                ),
                                DEF(
                                    "position",
                                    [
                                        DEF(
                                            "X",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="x",
                                                    gen="make_text_overlay_postion_x",
                                                )
                                            ],
                                        ),
                                        DEF(
                                            "Y",
                                            [
                                                DEF(
                                                    ANY,
                                                    required=False,
                                                    name="y",
                                                    gen="make_text_overlay_postion_y",
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                                DEF(
                                    "text",
                                    [
                                        DEF(
                                            ANY,
                                            required=False,
                                            name="text",
                                            gen="make_text_overlay_text",
                                        )
                                    ],
                                ),
                            ],
                            multi=True,
                            required=False,
                            name="index",
                        )
                    ],
                ),
                DEF(
                    "datetime",
                    [
                        DEF(
                            "enabled",
                            [
                                DEF(
                                    BOOL,
                                    required=False,
                                    name="enabled",
                                    gen="make_enable_datetime_overlay",
                                )
                            ],
                        ),
                        DEF(
                            "position",
                            [
                                DEF(
                                    "X",
                                    [
                                        DEF(
                                            ANY,
                                            required=False,
                                            name="x",
                                            gen="make_datetime_overlay_postion_x",
                                        )
                                    ],
                                ),
                                DEF(
                                    "Y",
                                    [
                                        DEF(
                                            ANY,
                                            required=False,
                                            name="y",
                                            gen="make_datetime_overlay_postion_y",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        DEF(
                            "date_format",
                            [
                                DEF(
                                    ANY,
                                    required=False,
                                    name="format",
                                    gen="make_datetime_overlay_date_format",
                                )
                            ],
                        ),
                        DEF(
                            "time_format",
                            [
                                DEF(
                                    ANY,
                                    required=False,
                                    name="format",
                                    gen="make_datetime_overlay_time_format",
                                )
                            ],
                        ),
                    ],
                ),
                DEF(
                    "channel_name",
                    [
                        DEF(
                            "enabled",
                            [
                                DEF(
                                    BOOL,
                                    required=False,
                                    name="enabled",
                                    gen="make_enable_channel_name_overlay",
                                )
                            ],
                        ),
                        DEF(
                            "position",
                            [
                                DEF(
                                    "X",
                                    [
                                        DEF(
                                            ANY,
                                            required=False,
                                            name="x",
                                            gen="make_channel_name_overlay_postion_x",
                                        )
                                    ],
                                ),
                                DEF(
                                    "Y",
                                    [
                                        DEF(
                                            ANY,
                                            required=False,
                                            name="y",
                                            gen="make_channel_name_overlay_postion_y",
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ]

    @match("root", "Network", "HostName", ANY)
    def normalize_hostname(self, tokens):
        yield self.make_hostname(tokens[3])

    @match("root", "Time", "TimeZone", ANY)
    def normalize_timezone(self, tokens):
        yield self.make_tz_offset(tz_offset=tokens[3])

    @match("root", "Time", "SynSource", "NTP")
    def normalize_timesource(self, tokens):
        yield self.make_clock_source(source="ntp")

    @match("root", "Time", "NTP", "Server", REST)
    def normalize_ntp_server(self, tokens):
        yield self.make_ntp_server(server=".".join(tokens[4:]))

    @match("root", "ImageSource", "I0", "Sensor", "Wdr", ANY)
    def normalize_image_wdr(self, tokens):
        yield self.make_image_wdr_mode(profile_name="default", mode=tokens[5])

    @match("root", "ImageSource", "I0", "Sensor", "Backlight", ANY)
    def normalize_image_blc(self, tokens):
        yield self.make_image_blc_enable(profile_name="default", enabled=tokens[5] == "on")

    @match("root", "ImageSource", "I0", "Sensor", "Sharpness", ANY)
    def normalize_image_sharpness(self, tokens):
        yield self.make_image_sharpness(profile_name="default", sharpness=tokens[5])

    @match("root", "ImageSource", "I0", "Sensor", "WhiteBalance", ANY)
    def normalize_image_wb(self, tokens):
        yield self.make_image_wb_mode(profile_name="default", mode=tokens[5])

    @match("root", "Image", "I0", "Appearance", "Resolution", ANY)
    def normalize_resolution(self, tokens):
        r = tokens[5].split(",")
        for index, s in enumerate(["mjpeg", "h264", "h264_2"]):
            height, width = RESOLUTION_MAPPER[r[index]].split("x")
            yield self.make_enable_stream(stream_id=s, enabled=r[index] != "disable")
            yield self.make_video_encoder_resolution_h(stream_id=s, height=height)
            yield self.make_video_encoder_resolution_w(stream_id=s, width=width)
            if s == "mjpeg":
                yield self.make_video_encoder_encoding(stream_id=s, encoding="MJPEG")
            else:
                yield self.make_video_encoder_encoding(stream_id=s, encoding="H264")

    @match("root", "Image", "I0", "RateControl", "H264Mode", ANY)
    def normalize_video_control_mode_h264(self, tokens):
        yield self.make_video_encoder_ratecontrol_mode(stream_id="h264", mode=tokens[5].upper())

    @match("root", "Image", "I0", "RateControl", "H264_2Mode", ANY)
    def normalize_video_control_h264_2(self, tokens):
        yield self.make_video_encoder_ratecontrol_mode(stream_id="h264_2", mode=tokens[5].upper())

    @match("root", "Image", "I0", "Appearance", "H264_2Bitrate", ANY)
    def normalize_bitrate_h264_2(self, tokens):
        yield self.make_video_encoder_bitratelimit(stream_id="h264_2", bitratelimit=tokens[5])

    @match("root", "Image", "I0", "Appearance", "H264Bitrate", ANY)
    def normalize_bitrate_h264(self, tokens):
        yield self.make_video_encoder_bitratelimit(stream_id="h264", bitratelimit=tokens[5])

    @match("root", "Image", "I0", "Appearance", "H264_2VideoKeyFrameInterval", ANY)
    def normalize_keyframe_h264_2(self, tokens):
        yield self.make_video_encoder_h264_gov_length(stream_id="h264_2", gov_length=tokens[5])

    @match("root", "Image", "I0", "Appearance", "H264VideoKeyFrameInterval", ANY)
    def normalize_keyframe_h264(self, tokens):
        yield self.make_video_encoder_h264_gov_length(stream_id="h264", gov_length=tokens[5])

    @match("root", "Audio", "DuplexMode", ANY)
    def normalize_stream_audio_enable(self, tokens):
        yield self.make_enable_audio_stream(stream_id="h264", enabled=tokens[3] != "disable")

    @match("root", "AudioSource", ANY, "BitRate", ANY)
    def normalize_stream_audio_encoder(self, tokens):
        yield self.make_audio_encoder_bitratelimit(stream_id="h264", bitratelimit=tokens[4])
        yield self.make_audio_encoder_encoding(
            stream_id="h264", encoding=AUDIO_CODEC_MAPPER[tokens[4]]
        )
        yield self.make_audio_encoder_source(stream_id="h264", source_name=tokens[2])

    @match("root", "Image", "I0", "Text", "String", REST)
    def normalize_overlay_text_text(self, tokens):
        yield self.make_enable_text_overlay(index="1", enabled=True)
        yield self.make_text_overlay_text(index="1", text=" ".join(tokens[5:]))

    @match("user", ANY)
    def normalize_username(self, tokens):
        tk = tokens[1].split(":")
        if tk[0] != "Username":
            yield self.make_user_class(username=tk[0], class_name=":".join(tk[1:]))
