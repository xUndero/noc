# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Hikvision.DSKV8 config normalizer
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.confdb.normalizer.base import BaseNormalizer, match, ANY, REST
from noc.core.confdb.syntax import DEF, BOOL, CHOICES


class HikvisionNormalizer(BaseNormalizer):
    # config format: table.<entityname>[entityToken].

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

    @match("DeviceInfo", "deviceName", REST)
    def normalize_hostname(self, tokens):
        yield self.make_hostname(" ".join(tokens[2:]))

    @match("Time", "timeZone", ANY)
    def normalize_timezone(self, tokens):
        yield self.make_tz_offset(tz_offset=tokens[2])

    @match("Time", "timeMode", "NTP")
    def normalize_timesource(self, tokens):
        yield self.make_clock_source(source="ntp")

    @match("Time", "NTPServer", ANY, ANY)
    def normalize_ntp_server(self, tokens):
        yield self.make_ntp_server(server=tokens[2])

    @match("Users", "user", ANY, "userLevel", ANY)
    def normalize_username_access_level(self, tokens):
        yield self.make_user_class(username=tokens[2], class_name="level-%s" % tokens[4].lower())

    @match("Users", "user", ANY, "id", ANY)
    def normalize_username_uid(self, tokens):
        yield self.make_user_uid(username=tokens[2], uid=tokens[4])

    @match("Color", "brightnessLevel", ANY)
    def normalize_image_profile_brightness(self, tokens):
        yield self.make_image_brightness(profile_name="1", brightness=tokens[2])

    @match("Color", "contrastLevel", ANY)
    def normalize_image_profile_contrast(self, tokens):
        yield self.make_image_contrast(profile_name="1", contrast=tokens[2])

    @match("Color", "saturationLevel", ANY)
    def normalize_image_profile_saturation(self, tokens):
        yield self.make_image_saturation(profile_name="1", saturation=tokens[2])

    @match("WDR", "mode", ANY)
    def normalize_image_wdr(self, tokens):
        yield self.make_image_wdr_mode(
            profile_name="1", mode={"open": "on", "close": "off", "auto": "auto"}[tokens[2]]
        )

    @match("StreamingChannel", ANY, "enabled", ANY)
    def normalize_stream_enable(self, tokens):
        yield self.make_enable_stream(stream_id=tokens[1], enabled=tokens[3] == "true")

    @match("StreamingChannel", ANY, "Video", "videoResolutionHeight", ANY)
    def normalize_resolution_height(self, tokens):
        yield self.make_video_encoder_resolution_h(stream_id=tokens[1], height=tokens[4])

    @match("StreamingChannel", ANY, "Video", "videoResolutionWidth", ANY)
    def normalize_resolution_width(self, tokens):
        yield self.make_video_encoder_resolution_w(stream_id=tokens[1], width=tokens[4])

    @match("StreamingChannel", ANY, "Video", "videoQualityControlType", ANY)
    def normalize_video_control_mode(self, tokens):
        yield self.make_video_encoder_ratecontrol_mode(stream_id=tokens[1], mode=tokens[4])

    @match("StreamingChannel", ANY, "Video", "vbrUpperCap", ANY)
    @match("StreamingChannel", ANY, "Video", "constantBitRate", ANY)
    def normalize_bitrate(self, tokens):
        yield self.make_video_encoder_bitratelimit(stream_id=tokens[1], bitratelimit=tokens[4])

    @match("StreamingChannel", ANY, "Video", "videoCodecType", ANY)
    def normalize_encoder_compression(self, tokens):
        yield self.make_video_encoder_encoding(
            stream_id=tokens[1], encoding=tokens[4].replace(".", "")
        )

    @match("StreamingChannel", ANY, "Video", "GovLength", ANY)
    def normalize_h264_keyframe_(self, tokens):
        yield self.make_video_encoder_h264_gov_length(stream_id=tokens[1], gov_length=tokens[4])

    @match("StreamingChannel", ANY, "Video", "maxFrameRate", ANY)
    def normalize_h264_framerate_(self, tokens):
        yield self.make_video_encoder_frameratelimit(
            stream_id=tokens[1], frameratelimit=int(tokens[4]) / 100
        )

    @match("StreamingChannel", ANY, "Video", "H264Profile", ANY)
    def normalize_h264_profile(self, tokens):
        yield self.make_video_encoder_h264_profile(stream_id=tokens[1], h264_profile=tokens[4])

    @match("StreamingChannel", ANY, "Audio", "enabled", ANY)
    def normalize_stream_audio_enable(self, tokens):
        yield self.make_enable_audio_stream(stream_id=tokens[1], enabled=tokens[4] == "true")

    @match("StreamingChannel", ANY, "Audio", "audioInputChannelID", ANY)
    def normalize_stream_audio_channel_enable(self, tokens):
        yield self.make_audio_encoder_source(stream_id=tokens[1], source_name=tokens[4])

    @match("StreamingChannel", ANY, "Audio", "audioCompressionType", ANY)
    def normalize_stream_audio_encoder(self, tokens):
        yield self.make_audio_encoder_encoding(stream_id=tokens[1], encoding=tokens[4])

    @match("Overlay", "channelNameOverlay", "enabled", ANY)
    def normalize_overlay_channel_name_enable(self, tokens):
        yield self.make_enable_channel_name_overlay(enabled=tokens[3] == "true")

    @match("Overlay", "DateTimeOverlay", "enabled", ANY)
    def normalize_overlay_datetime_enable(self, tokens):
        yield self.make_enable_datetime_overlay(enabled=tokens[3] == "true")

    @match("Overlay", "TextOverlay", "TextOverlay", ANY, ANY)
    def normalize_overlay_text_text(self, tokens):
        yield self.make_text_overlay_text(index=tokens[3], text=tokens[4])
