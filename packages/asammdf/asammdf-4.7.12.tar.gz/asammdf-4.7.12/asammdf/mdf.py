# -*- coding: utf-8 -*-
""" common MDF file format module """

import csv
import logging
import os
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from copy import deepcopy
from functools import reduce
from struct import unpack
from shutil import copy
from warnings import warn

import numpy as np
from numpy.core.defchararray import encode, decode
from pandas import DataFrame

from .blocks.mdf_v2 import MDF2
from .blocks.mdf_v3 import MDF3
from .blocks.mdf_v4 import MDF4
from .signal import Signal
from .blocks.utils import (
    CHANNEL_COUNT,
    MERGE_LOW,
    MERGE_MINIMUM,
    MdfException,
    matlab_compatible,
    validate_memory_argument,
    validate_version_argument,
    MDF2_VERSIONS,
    MDF3_VERSIONS,
    MDF4_VERSIONS,
    SUPPORTED_VERSIONS,
    randomized_string,
    is_file_like,
    count_channel_groups,
    UINT16_u,
    UINT64_u,
    debug_channel,
    UniqueDB,
)
from .blocks.v2_v3_blocks import Channel as ChannelV3
from .blocks.v2_v3_blocks import HeaderBlock as HeaderV3
from .blocks.v2_v3_blocks import ChannelConversion as ChannelConversionV3
from .blocks.v2_v3_blocks import ChannelExtension
from .blocks.v4_blocks import SourceInformation
from .blocks.v4_blocks import ChannelConversion as ChannelConversionV4
from .blocks.v4_blocks import Channel as ChannelV4
from .blocks.v4_blocks import HeaderBlock as HeaderV4
from .blocks.v4_blocks import ChannelArrayBlock, EventBlock
from .blocks import v4_constants as v4c
from .blocks import v2_v3_constants as v23c

PYVERSION = sys.version_info[0]

logger = logging.getLogger("asammdf")


if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    warn("Minimum Python version warning: asammdf 5.0 will only support Python >= 3.6")


__all__ = ["MDF", "SUPPORTED_VERSIONS"]


class MDF(object):
    """Unified access to MDF v3 and v4 files. Underlying _mdf's attributes and
    methods are linked to the `MDF` object via *setattr*. This is done to expose
    them to the user code and for performance considerations.

    Parameters
    ----------
    name : string | BytesIO
        mdf file name (if provided it must be a real file name) or
        file-like object
    memory : str
        memory option; default `full`:

        * if *full* the data group binary data block will be loaded in RAM
        * if *low* the channel data is read from disk on request, and the
          metadata is loaded into RAM
        * if *minimum* only minimal data is loaded into RAM

    version : string
        mdf file version from ('2.00', '2.10', '2.14', '3.00', '3.10', '3.20',
        '3.30', '4.00', '4.10', '4.11'); default '4.10'
    callback : function
        keyword only argument: function to call to update the progress; the
        function must accept two arguments (the current progress and maximum
        progress value)
    use_display_names : bool
        keyword only argument: for MDF4 files parse the XML channel comment to
        search for the display name; XML parsing is quite expensive so setting
        this to *False* can decrease the loading times very much; default
        *False*

    """

    _terminate = False

    def __init__(self, name=None, memory="full", version="4.10", **kwargs):
        if name:
            memory = validate_memory_argument(memory)
            if is_file_like(name):
                file_stream = name
            else:
                if os.path.isfile(name):
                    file_stream = open(name, "rb")
                else:
                    raise MdfException('File "{}" does not exist'.format(name))
            file_stream.seek(0)
            magic_header = file_stream.read(3)
            if magic_header != b"MDF":
                raise MdfException('"{}" is not a valid ASAM MDF file'.format(name))
            file_stream.seek(8)
            version = file_stream.read(4).decode("ascii").strip(" \0")
            if not version:
                file_stream.read(16)
                version = unpack("<H", file_stream.read(2))[0]
                version = str(version)
                version = "{}.{}".format(version[0], version[1:])
            if version in MDF3_VERSIONS:
                self._mdf = MDF3(name, memory, **kwargs)
            elif version in MDF4_VERSIONS:
                self._mdf = MDF4(name, memory, **kwargs)
            elif version in MDF2_VERSIONS:
                self._mdf = MDF2(name, memory, **kwargs)
            else:
                message = (
                    '"{}" is not a supported MDF file; ' '"{}" file version was found'
                )
                raise MdfException(message.format(name, version))

        else:
            version = validate_version_argument(version)
            memory = validate_memory_argument(memory)
            if version in MDF2_VERSIONS:
                self._mdf = MDF3(version=version, memory=memory, **kwargs)
            elif version in MDF3_VERSIONS:
                self._mdf = MDF3(version=version, memory=memory, **kwargs)
            elif version in MDF4_VERSIONS:
                self._mdf = MDF4(version=version, memory=memory, **kwargs)
            else:
                message = (
                    '"{}" is not a supported MDF file version; '
                    "Supported versions are {}"
                )
                raise MdfException(message.format(version, SUPPORTED_VERSIONS))

        # link underlying _mdf attributes and methods to the new MDF object
        for attr in set(dir(self._mdf)) - set(dir(self)):
            setattr(self, attr, getattr(self._mdf, attr))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _transfer_events(self, other):
        def get_scopes(event, events):
            if event.scopes:
                return event.scopes
            else:
                if event.parent is not None:
                    return get_scopes(events[event.parent], events)
                elif event.range_start is not None:
                    return get_scopes(events[event.range_start], events)
                else:
                    return event.scopes

        if other.version >= "4.00":
            for event in other.events:
                if self.version >= "4.00":
                    new_event = deepcopy(event)
                    event_valid = True
                    for i, ref in enumerate(new_event.scopes):
                        try:
                            dg_cntr, ch_cntr = ref
                            try:
                                (self.groups[dg_cntr]["channels"][ch_cntr])
                            except:
                                event_valid = False
                        except TypeError:
                            dg_cntr = ref
                            try:
                                (self.groups[dg_cntr]["channel_group"])
                            except:
                                event_valid = False
                    # ignore attachments for now
                    for i in range(new_event["attachment_nr"]):
                        key = "attachment_{}_addr".format(i)
                        event[key] = 0
                    if event_valid:
                        self.events.append(new_event)
                else:
                    ev_type = event["event_type"]
                    ev_range = event["range_type"]
                    ev_base = event["sync_base"]
                    ev_factor = event["sync_factor"]

                    timestamp = ev_base * ev_factor

                    try:
                        comment = ET.fromstring(
                            event.comment.replace(
                                ' xmlns="http://www.asam.net/mdf/v4"', ""
                            )
                        )
                        pre = comment.find(".//pre_trigger_interval")
                        if pre is not None:
                            pre = float(pre.text)
                        else:
                            pre = 0.0
                        post = comment.find(".//post_trigger_interval")
                        if post is not None:
                            post = float(post.text)
                        else:
                            post = 0.0
                        comment = comment.find(".//TX")
                        if comment is not None:
                            comment = comment.text
                        else:
                            comment = ""

                    except:
                        pre = 0.0
                        post = 0.0
                        comment = event.comment

                    if comment:
                        comment += ": "

                    if ev_range == v4c.EVENT_RANGE_TYPE_BEGINNING:
                        comment += "Begin of "
                    elif ev_range == v4c.EVENT_RANGE_TYPE_END:
                        comment += "End of "
                    else:
                        comment += "Single point "

                    if ev_type == v4c.EVENT_TYPE_RECORDING:
                        comment += "recording"
                    elif ev_type == v4c.EVENT_TYPE_RECORDING_INTERRUPT:
                        comment += "recording interrupt"
                    elif ev_type == v4c.EVENT_TYPE_ACQUISITION_INTERRUPT:
                        comment += "acquisition interrupt"
                    elif ev_type == v4c.EVENT_TYPE_START_RECORDING_TRIGGER:
                        comment += "measurement start trigger"
                    elif ev_type == v4c.EVENT_TYPE_STOP_RECORDING_TRIGGER:
                        comment += "measurement stop trigger"
                    elif ev_type == v4c.EVENT_TYPE_TRIGGER:
                        comment += "trigger"
                    else:
                        comment += "marker"

                    scopes = get_scopes(event, other.events)
                    if scopes:
                        for i, ref in enumerate(scopes):
                            event_valid = True
                            try:
                                dg_cntr, ch_cntr = ref
                                try:
                                    (self.groups[dg_cntr])
                                except:
                                    event_valid = False
                            except TypeError:
                                dg_cntr = ref
                                try:
                                    (self.groups[dg_cntr])
                                except:
                                    event_valid = False
                            if event_valid:

                                self.add_trigger(
                                    dg_cntr,
                                    timestamp,
                                    pre_time=pre,
                                    post_time=post,
                                    comment=comment,
                                )
                    else:
                        for i, _ in enumerate(self.groups):
                            self.add_trigger(
                                i,
                                timestamp,
                                pre_time=pre,
                                post_time=post,
                                comment=comment,
                            )

        else:
            for trigger_info in other.iter_get_triggers():
                comment = trigger_info["comment"]
                timestamp = trigger_info["time"]
                group = trigger_info["group"]

                if self.version < "4.00":
                    self.add_trigger(
                        group,
                        timestamp,
                        pre_time=trigger_info["pre_time"],
                        post_time=trigger_info["post_time"],
                        comment=comment,
                    )
                else:
                    if timestamp:
                        ev_type = v4c.EVENT_TYPE_TRIGGER
                    else:
                        ev_type = v4c.EVENT_TYPE_START_RECORDING_TRIGGER
                    event = EventBlock(
                        event_type=ev_type,
                        sync_base=int(timestamp * 10 ** 9),
                        sync_factor=10 ** -9,
                        scope_0_addr=0,
                    )
                    event.comment = comment
                    event.scopes.append(group)
                    self.events.append(event)

    def _excluded_channels(self, index):
        """ get the indexes list of channels that are excluded when processing
        teh channel group. The candiates for exlusion are the master channel
        (since it is retrieved as `Signal` timestamps), structure channel
        composition component channels (since they are retrieved as fields in
        the `Signal` samples recarray) and channel dependecies (mdf version 3)
        / channel array axes

        Parameters
        ----------
        index : int
            channel group index

        Returns
        -------
        excluded_channels : set
            set of excluded channels

        """

        group = self.groups[index]

        excluded_channels = set()
        master_index = self.masters_db.get(index, -1)
        excluded_channels.add(master_index)

        channels = group["channels"]
        channel_group = group["channel_group"]

        if self.version in MDF2_VERSIONS + MDF3_VERSIONS:
            for dep in group["channel_dependencies"]:
                if dep is None:
                    continue
                for gp_nr, ch_nr  in dep.referenced_channels:
                    if gp_nr == index:
                        excluded_channels.add(ch_nr)
        else:
            if channel_group["flags"] & v4c.FLAG_CG_BUS_EVENT:
                where = self.whereis("CAN_DataFrame")
                for dg_cntr, ch_cntr in where:
                    if dg_cntr == index:
                        break
                else:
                    raise MdfException("CAN_DataFrame not found in group " + str(index))
                channel = channels[ch_cntr]
                excluded_channels.add(ch_cntr)
                if group["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
                    stream = self._file
                else:
                    stream = self._tempfile
                if self.memory == "minimum":
                    channel = ChannelV4(
                        address=channel, stream=stream, load_metadata=False
                    )
                frame_bytes = range(
                    channel["byte_offset"],
                    channel["byte_offset"] + channel["bit_count"] // 8,
                )
                for i, channel in enumerate(channels):
                    if self.memory == "minimum":
                        channel = ChannelV4(
                            address=channel, stream=stream, load_metadata=False
                        )
                    if channel["byte_offset"] in frame_bytes:
                        excluded_channels.add(i)

            for dependencies in group["channel_dependencies"]:
                if dependencies is None:
                    continue
                if all(not isinstance(dep, ChannelArrayBlock) for dep in dependencies):
                    for channel in dependencies:
                        excluded_channels.add(channels.index(channel))
                else:
                    for dep in dependencies:
                        for gp_nr, ch_nr in dep.referenced_channels:
                            if gp_nr == index:
                                excluded_channels.add(ch_nr)

        return excluded_channels

    def _included_channels(self, index):
        """ get the minimum channels needed to extract all information from the
        channel group (for example keep onl the structure channel and exclude the
        strucutre fields channels)

        Parameters
        ----------
        index : int
            channel group index

        Returns
        -------
        included_channels : set
            set of excluded channels

        """

        group = self.groups[index]

        included_channels = set(range(len(group["channels"])))
        master_index = self.masters_db.get(index, None)
        if master_index is not None:
            included_channels.remove(master_index)

        channels = group["channels"]

        if self.version in MDF2_VERSIONS + MDF3_VERSIONS:
            for dep in group["channel_dependencies"]:
                if dep is None:
                    continue
                for gp_nr, ch_nr in dep.referenced_channels:
                    if gp_nr == index:
                        included_channels.add(ch_nr)
        else:
            if group.get("CAN_logging", False):
                where = (
                    self.whereis("CAN_DataFrame")
                    + self.whereis("CAN_ErrorFrame")
                    + self.whereis("CAN_RemoteFrame")
                )
                for dg_cntr, ch_cntr in where:
                    if dg_cntr == index:
                        break
                else:
                    raise MdfException("CAN_DataFrame or CAN_ErrorFrame not found in group " + str(index))
                channel = channels[ch_cntr]
                if group["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
                    stream = self._file
                else:
                    stream = self._tempfile
                if self.memory == "minimum":
                    channel = ChannelV4(
                        address=channel, stream=stream, load_metadata=False
                    )
                frame_bytes = range(
                    channel["byte_offset"],
                    channel["byte_offset"] + channel["bit_count"] // 8,
                )
                for i, channel in enumerate(channels):
                    if self.memory == "minimum":
                        channel = ChannelV4(
                            address=channel, stream=stream, load_metadata=False
                        )
                    if channel["byte_offset"] in frame_bytes:
                        included_channels.remove(i)

                if group.get("CAN_database", False):
                    dbc_addr = group["dbc_addr"]
                    message_id = group["message_id"]
                    can_msg = self._dbc_cache[dbc_addr].frameById(message_id)

                    for i, _ in enumerate(can_msg.signals, 1):
                        included_channels.add(-i)

            for dependencies in group["channel_dependencies"]:
                if dependencies is None:
                    continue
                if all(not isinstance(dep, ChannelArrayBlock) for dep in dependencies):
                    for _, ch_nr in dependencies:
                        try:
                            included_channels.remove(ch_nr)
                        except KeyError:
                            pass
                else:
                    for dep in dependencies:
                        for gp_nr, ch_nr in dep.referenced_channels:
                            if gp_nr == index:
                                try:
                                    included_channels.remove(ch_nr)
                                except KeyError:
                                    pass

        return included_channels

    def __contains__(self, channel):
        """ if *'channel name'* in *'mdf file'* """
        return channel in self.channels_db

    def __iter__(self):
        """ iterate over all the channels found in the file; master channels
        are skipped from iteration

        """

        for signal in self.iter_channels():
            yield signal

    def convert(self, version, memory=None):
        """convert *MDF* to other version

        Parameters
        ----------
        version : str
            new mdf file version from ('2.00', '2.10', '2.14', '3.00', '3.10',
            '3.20', '3.30', '4.00', '4.10', '4.11'); default '4.10'
        memory : str
            memory option; default *full*

        Returns
        -------
        out : MDF
            new *MDF* object

        """
        version = validate_version_argument(version)
        if memory is None:
            memory = self.memory
        else:
            memory = validate_memory_argument(memory)

        out = MDF(version=version, memory=memory)
        name, _ = os.path.splitext(self.name)
        _, ext = os.path.splitext(out.name)
        out.name = '{}.converted_to_{}{}'.format(name, version, ext)

        out.header.start_time = self.header.start_time

        groups_nr = len(self.groups)

        if self._callback:
            self._callback(0, groups_nr)

        cg_nr = -1

        # walk through all groups and get all channels
        for i, group in enumerate(self.groups):
            encodings = [None, ]
            included_channels = self._included_channels(i)
            if included_channels:
                cg_nr += 1
            else:
                continue

            parents, dtypes = self._prepare_record(group)
            group["parents"], group["types"] = parents, dtypes

            data = self._load_data(group)
            for idx, fragment in enumerate(data):
                if dtypes.itemsize:
                    group["record"] = np.core.records.fromstring(
                        fragment[0], dtype=dtypes
                    )
                    group["record"].setflags(write=False)
                else:
                    group["record"] = None

                # the first fragment triggers and append that will add the
                # metadata for all channels
                if idx == 0:
                    sigs = []
                    for j in included_channels:
                        sig = self.get(
                            group=i,
                            index=j,
                            data=fragment,
                            raw=True,
                            ignore_invalidation_bits=True,
                            copy_master=False,
                        )
                        if version < "4.00":
                            if sig.samples.dtype.kind == "S":
                                encodings.append(sig.encoding)
                                strsig = self.get(
                                    group=i,
                                    index=j,
                                    samples_only=True,
                                    ignore_invalidation_bits=True,
                                )[0]
                                sig.samples = sig.samples.astype(strsig.dtype)
                                del strsig
                                if sig.encoding != "latin-1":

                                    if sig.encoding == "utf-16-le":
                                        sig.samples = sig.samples.view(np.uint16).byteswap().view(sig.samples.dtype)
                                        sig.samples = encode(decode(sig.samples, "utf-16-be"), "latin-1")
                                    else:
                                        sig.samples = encode(decode(sig.samples, sig.encoding), "latin-1")
                            else:
                                encodings.append(None)
                        if not sig.samples.flags.writeable:
                            sig.samples = sig.samples.copy()
                        sigs.append(sig)
                    source_info = "Converted from {} to {}"

                    if sigs:
                        out.append(
                            sigs,
                            source_info.format(self.version, version),
                            common_timebase=True,
                        )
                        new_group = out.groups[-1]
                        new_channel_group = new_group["channel_group"]
                        old_channel_group = group["channel_group"]
                        new_channel_group.comment = old_channel_group.comment
                        if version >= "4.00":
                            new_channel_group["path_separator"] = ord(".")
                            if self.version >= "4.00":
                                new_channel_group.acq_name = old_channel_group.acq_name
                                new_channel_group.acq_source = (
                                    old_channel_group.acq_source
                                )
                    else:
                        break

                # the other fragments will trigger onl the extension of
                # samples records to the data block
                else:
                    sigs = [(self.get_master(i, data=fragment, copy_master=False), None)]

                    for j in included_channels:
                        sig = self.get(
                            group=i,
                            index=j,
                            data=fragment,
                            raw=True,
                            samples_only=True,
                            ignore_invalidation_bits=True,
                        )

                        if version < "4.00":
                            encoding = encodings[j]
                            samples = sig[0]
                            if encoding:
                                if encoding != "latin-1":

                                    if encoding == "utf-16-le":
                                        samples = samples.view(np.uint16).byteswap().view(samples.dtype)
                                        samples = encode(decode(samples, "utf-16-be"), "latin-1")
                                    else:
                                        samples = encode(decode(samples, encoding), "latin-1")
                                    sig.samples = samples

                        if not sig[0].flags.writeable:
                            sig = sig[0].copy(), sig[1]
                        sigs.append(sig)
                    out.extend(cg_nr, sigs)

                del group["record"]

            if self._callback:
                self._callback(i + 1, groups_nr)

            if self._terminate:
                return

        out._transfer_events(self)
        if self._callback:
            out._callback = out._mdf._callback = self._callback
        return out

    def cut(self, start=None, stop=None, whence=0, version=None, memory=None, include_ends=True):
        """cut *MDF* file. *start* and *stop* limits are absolute values
        or values relative to the first timestamp depending on the *whence*
        argument.

        Parameters
        ----------
        start : float
            start time, default *None*. If *None* then the start of measurement
            is used
        stop : float
            stop time, default *None*. If *None* then the end of measurement is
            used
        whence : int
            how to search for the start and stop values

            * 0 : absolute
            * 1 : relative to first timestamp
        version : str
            new mdf file version from ('2.00', '2.10', '2.14', '3.00', '3.10',
            '3.20', '3.30', '4.00', '4.10', '4.11'); default *None* and in this
            case the original file version is used
        memory : str
            memory option; default *None* and in this case the original file
            memory option is used
        include_ends : bool
            include the *start* and *stop* timestamps after cutting the signal.
            If *start* and *stop* are found in the original timestamps, then
            the new samples will be computed using interpolation. Default *True*

        Returns
        -------
        out : MDF
            new MDF object

        """
        if memory is None:
            memory = self.memory
        else:
            memory = validate_memory_argument(memory)

        if version is None:
            version = self.version
        else:
            version = validate_version_argument(version)

        out = MDF(version=version, memory=memory)
        name, _ = os.path.splitext(self.name)
        _, ext = os.path.splitext(out.name)
        out.name = '{}.cut_to_{}{}'.format(name, version, ext)

        out.header.start_time = self.header.start_time

        if whence == 1:
            timestamps = []
            for i, group in enumerate(self.groups):
                fragment = next(self._load_data(group))
                master = self.get_master(i, fragment)
                if master.size:
                    timestamps.append(master[0])
                del master

            if timestamps:
                first_timestamp = np.amin(timestamps)
            else:
                first_timestamp = 0
            if start is not None:
                start += first_timestamp
            if stop is not None:
                stop += first_timestamp

        out.header.start_time = self.header.start_time

        groups_nr = len(self.groups)

        if self._callback:
            self._callback(0, groups_nr)

        cg_nr = -1

        # walk through all groups and get all channels
        for i, group in enumerate(self.groups):
            included_channels = self._included_channels(i)
            if included_channels:
                cg_nr += 1
            else:
                continue

            data = self._load_data(group)
            parents, dtypes = self._prepare_record(group)
            group["parents"], group["types"] = parents, dtypes

            idx = 0
            for fragment in data:
                if dtypes.itemsize:
                    group["record"] = np.core.records.fromstring(
                        fragment[0], dtype=dtypes
                    )
                    group["record"].setflags(write=False)
                else:
                    group["record"] = None
                master = self.get_master(i, fragment)
                if not len(master):
                    continue

                needs_cutting = True

                # check if this fragement is within the cut interval or
                # if the cut interval has ended
                if start is None and stop is None:
                    fragment_start = None
                    fragment_stop = None
                    start_index = 0
                    stop_index = len(master)
                    needs_cutting = False
                elif start is None:
                    fragment_start = None
                    start_index = 0
                    if master[0] > stop:
                        break
                    else:
                        fragment_stop = min(stop, master[-1])
                        stop_index = np.searchsorted(
                            master, fragment_stop, side="right"
                        )
                        if stop_index == len(master):
                            needs_cutting = False
                elif stop is None:
                    fragment_stop = None
                    if master[-1] < start:
                        continue
                    else:
                        fragment_start = max(start, master[0])
                        start_index = np.searchsorted(
                            master, fragment_start, side="left"
                        )
                        stop_index = len(master)
                        if start_index == 0:
                            needs_cutting = False
                else:
                    if master[0] > stop:
                        break
                    elif master[-1] < start:
                        continue
                    else:
                        fragment_start = max(start, master[0])
                        start_index = np.searchsorted(
                            master, fragment_start, side="left"
                        )
                        fragment_stop = min(stop, master[-1])
                        stop_index = np.searchsorted(
                            master, fragment_stop, side="right"
                        )
                        if start_index == 0 and stop_index == len(master):
                            needs_cutting = False

                # the first fragment triggers and append that will add the
                # metadata for all channels
                if idx == 0:
                    sigs = []
                    for j in included_channels:
                        sig = self.get(
                            group=i,
                            index=j,
                            data=fragment,
                            raw=True,
                            ignore_invalidation_bits=True,
                            copy_master=False,
                        )
                        if needs_cutting:
                            sig = sig.cut(fragment_start, fragment_stop, include_ends)

                        if not sig.samples.flags.writeable:
                            sig.samples = sig.samples.copy()
                        sigs.append(sig)

                    if sigs:
                        if start:
                            start_ = "{}s".format(start)
                        else:
                            start_ = "start of measurement"
                        if stop:
                            stop_ = "{}s".format(stop)
                        else:
                            stop_ = "end of measurement"
                        out.append(
                            sigs,
                            "Cut from {} to {}".format(start_, stop_),
                            common_timebase=True,
                        )
                    else:
                        break

                    idx += 1

                # the other fragments will trigger onl the extension of
                # samples records to the data block
                else:
                    if needs_cutting:
                        sigs = [(master[start_index:stop_index].copy(), None)]
                    else:
                        sigs = [(master, None)]

                    for j in included_channels:
                        sig = self.get(
                            group=i,
                            index=j,
                            data=fragment,
                            raw=True,
                            samples_only=True,
                            ignore_invalidation_bits=True,
                        )
                        if needs_cutting:
                            if sig[1] is not None:
                                sig = (
                                    sig[0][start_index:stop_index],
                                    sig[1][start_index:stop_index],
                                )
                            else:
                                sig = sig[0][start_index:stop_index], None
                            if not sig[0].flags.writeable:
                                sig = sig[0].copy(), sig[1]
                        sigs.append(sig)

                    if sigs:
                        out.extend(cg_nr, sigs)

                    idx += 1

                del group["record"]

            # if the cut interval is not found in the measurement
            # then append an empty data group
            if idx == 0:

                self.configure(read_fragment_size=1)
                sigs = []

                fragment = next(self._load_data(group))

                fragment = (fragment[0], -1, None)

                for j in included_channels:
                    sig = self.get(
                        group=i,
                        index=j,
                        data=fragment,
                        raw=True,
                        ignore_invalidation_bits=True,
                    )
                    sig.samples = sig.samples[:0]
                    sig.timestamps = sig.timestamps[:0]
                    sigs.append(sig)

                if start:
                    start_ = "{}s".format(start)
                else:
                    start_ = "start of measurement"
                if stop:
                    stop_ = "{}s".format(stop)
                else:
                    stop_ = "end of measurement"
                out.append(
                    sigs,
                    "Cut from {} to {}".format(start_, stop_),
                    common_timebase=True,
                )

                self.configure(read_fragment_size=0)

            if self._callback:
                self._callback(i + 1, groups_nr)

            if self._terminate:
                return

        out._transfer_events(self)
        if self._callback:
            out._callback = out._mdf._callback = self._callback
        return out

    def export(self, fmt, filename=None, **kargs):
        """ export *MDF* to other formats. The *MDF* file name is used is
        available, else the *filename* argument must be provided.

        Parameters
        ----------
        fmt : string
            can be one of the following:

            * `csv` : CSV export that uses the ";" delimiter. This option
              will generate a new csv file for each data group
              (<MDFNAME>_DataGroup_<cntr>.csv)

            * `hdf5` : HDF5 file output; each *MDF* data group is mapped to
              a *HDF5* group with the name 'DataGroup_<cntr>'
              (where <cntr> is the index)

            * `excel` : Excel file output (very slow). This option will
              generate a new excel file for each data group
              (<MDFNAME>_DataGroup_<cntr>.xlsx)

            * `mat` : Matlab .mat version 4, 5 or 7.3 export. If
              *single_time_base==False* the channels will be renamed in the mat
              file to 'D<cntr>_<channel name>'. The channel group
              master will be renamed to 'DM<cntr>_<channel name>'
              ( *<cntr>* is the data group index starting from 0)

            * `pandas` : export all channels as a single pandas DataFrame

            * `parquet` : export to Apache parquet format

        filename : string
            export file name

        **kwargs

            * `single_time_base`: resample all channels to common time base,
              default *False* (pandas export is by default single based)
            * `raster`: float time raster for resampling. Valid if
              *single_time_base* is *True* and for *pandas*
              export
            * `time_from_zero`: adjust time channel to start from 0
            * `use_display_names`: use display name instead of standard channel
              name, if available.
            * `empty_channels`: behaviour for channels without samples; the
              options are *skip* or *zeros*; default is *zeros*
            * `format`: only valid for *mat* export; can be '4', '5' or '7.3',
              default is '5'
            * `oned_as`: only valid for *mat* export; can be 'row' or 'column'

        Returns
        -------
        dataframe : pandas.DataFrame
            only in case of *pandas* export

        """

        header_items = ("date", "time", "author", "department", "project", "subject")

        if fmt != "pandas" and filename is None and self.name is None:
            message = (
                "Must specify filename for export"
                "if MDF was created without a file name"
            )
            logger.warning(message)
            return

        single_time_base = kargs.get("single_time_base", False)
        raster = kargs.get("raster", 0)
        time_from_zero = kargs.get("time_from_zero", True)
        use_display_names = kargs.get("use_display_names", True)
        empty_channels = kargs.get("empty_channels", "zeros")
        format = kargs.get("format", "5")
        oned_as = kargs.get("oned_as", "row")

        name = filename if filename else self.name

        if fmt == "parquet":
            try:
                from fastparquet import write as write_parquet
            except ImportError:
                logger.warning(
                    "fastparquet not found; export to parquet is unavailable"
                )
                return

        elif fmt == "hdf5":
            try:
                from h5py import File as HDF5
            except ImportError:
                logger.warning("h5py not found; export to HDF5 is unavailable")
                return

        elif fmt == "excel":
            try:
                import xlsxwriter
            except ImportError:
                logger.warning("xlsxwriter not found; export to Excel unavailable")
                return

        elif fmt == "mat":
            if format == "7.3":
                try:
                    from hdf5storage import savemat
                except ImportError:
                    logger.warning(
                        "hdf5storage not found; export to mat v7.3 is unavailable"
                    )
                    return
            else:
                try:
                    from scipy.io import savemat
                except ImportError:
                    logger.warning("scipy not found; export to mat is unavailable")
                    return

        if single_time_base or fmt in ("pandas", "parquet"):
            mdict = OrderedDict()
            units = OrderedDict()
            comments = OrderedDict()
            masters = [self.get_master(i) for i in range(len(self.groups))]
            master = reduce(np.union1d, masters)

            if raster and len(master):
                if len(master) > 1:
                    num = float(
                        np.float32((master[-1] - master[0]) / raster)
                    )
                    if num.is_integer():
                        master = np.linspace(
                            master[0],
                            master[-1],
                            int(num),
                        )
                    else:
                        master = np.arange(master[0], master[-1], raster, dtype=np.float64)

            if time_from_zero and len(master):
                mdict["time"] = master - master[0]
            else:
                mdict["time"] = master

            units["time"] = "s"
            comments["time"] = ""

            used_names = UniqueDB()
            used_names.get_unique_name("time")

            for i, grp in enumerate(self.groups):
                if self._terminate:
                    return

                included_channels = self._included_channels(i)

                data = self._load_data(grp)

                if PYVERSION == 2:
                    data = b"".join(str(d[0]) for d in data)
                else:
                    data = b"".join(d[0] for d in data)
                data = (data, 0, None)

                for j in included_channels:
                    sig = self.get(
                        group=i,
                        index=j,
                        data=data,
                    ).interp(master)

                    if len(sig.samples.shape) > 1:
                        arr = [sig.samples]
                        types = [(sig.name, sig.samples.dtype, sig.samples.shape[1:])]
                        sig.samples = np.core.records.fromarrays(arr, dtype=types)

                    if use_display_names:
                        channel_name = sig.display_name or sig.name
                    else:
                        channel_name = sig.name

                    channel_name = used_names.get_unique_name(channel_name)

                    if len(sig):
                        mdict[channel_name] = sig.samples
                        units[channel_name] = sig.unit
                        comments[channel_name] = sig.comment
                    else:
                        if empty_channels == "zeros":
                            mdict[channel_name] = np.zeros(
                                len(master), dtype=sig.samples.dtype
                            )
                            units[channel_name] = sig.unit
                            comments[channel_name] = sig.comment

        if fmt == "hdf5":
            if not name.endswith(".hdf"):
                name += ".hdf"

            if single_time_base:
                with HDF5(name, "w") as hdf:
                    # header information
                    group = hdf.create_group(os.path.basename(name))

                    if self.version in MDF2_VERSIONS + MDF3_VERSIONS:
                        for item in header_items:
                            group.attrs[item] = self.header[item]

                    # save each data group in a HDF5 group called
                    # "DataGroup_<cntr>" with the index starting from 1
                    # each HDF5 group will have a string attribute "master"
                    # that will hold the name of the master channel

                    for channel in mdict:
                        samples = mdict[channel]
                        unit = units[channel]
                        comment = comments[channel]

                        dataset = group.create_dataset(channel, data=samples)
                        unit = unit.replace("\0", "")
                        if unit:
                            dataset.attrs["unit"] = unit
                        comment = comment.replace("\0", "")
                        if comment:
                            dataset.attrs["comment"] = comment

            else:
                with HDF5(name, "w") as hdf:
                    # header information
                    group = hdf.create_group(os.path.basename(name))

                    if self.version in MDF2_VERSIONS + MDF3_VERSIONS:
                        for item in header_items:
                            group.attrs[item] = self.header[item]

                    # save each data group in a HDF5 group called
                    # "DataGroup_<cntr>" with the index starting from 1
                    # each HDF5 group will have a string attribute "master"
                    # that will hold the name of the master channel
                    for i, grp in enumerate(self.groups):
                        if self._terminate:
                            return
                        group_name = r"/" + "DataGroup_{}".format(i + 1)
                        group = hdf.create_group(group_name)

                        master_index = self.masters_db.get(i, -1)

                        data = self._load_data(grp)

                        if PYVERSION == 2:
                            data = b"".join(str(d[0]) for d in data)
                        else:
                            data = b"".join(d[0] for d in data)
                        data = (data, 0, None)

                        for j, _ in enumerate(grp["channels"]):
                            sig = self.get(group=i, index=j, data=data)
                            name = sig.name
                            if j == master_index:
                                group.attrs["master"] = name
                            dataset = group.create_dataset(name, data=sig.samples)
                            unit = sig.unit.replace("\0", "")
                            if unit:
                                dataset.attrs["unit"] = unit
                            comment = sig.comment.replace("\0", "")
                            if comment:
                                dataset.attrs["comment"] = comment

        elif fmt == "excel":

            if single_time_base:
                if not name.endswith(".xlsx"):
                    name += ".xlsx"
                message = 'Writing excel export to file "{}"'.format(name)
                logger.info(message)

                workbook = xlsxwriter.Workbook(name)
                sheet = workbook.add_worksheet("Channels")

                for col, (channel_name, channel_unit) in enumerate(units.items()):
                    if self._terminate:
                        return
                    samples = mdict[channel_name]
                    sig_description = "{} [{}]".format(channel_name, channel_unit)
                    sheet.write(0, col, sig_description)
                    try:
                        sheet.write_column(1, col, samples.astype(str))
                    except:
                        vals = [str(e) for e in sig.samples]
                        sheet.write_column(1, col, vals)

                workbook.close()

            else:
                while name.endswith(".xlsx"):
                    name = name[:-5]

                count = len(self.groups)

                for i, grp in enumerate(self.groups):
                    if self._terminate:
                        return
                    message = "Exporting group {} of {}".format(i + 1, count)
                    logger.info(message)

                    data = self._load_data(grp)

                    if PYVERSION == 2:
                        data = b"".join(str(d[0]) for d in data)
                    else:
                        data = b"".join(d[0] for d in data)
                    data = (data, 0, None)

                    master_index = self.masters_db.get(i, None)
                    if master_index is not None:
                        master = self.get(group=i, index=master_index, data=data)

                        if raster and len(master):
                            raster_ = np.arange(
                                master[0], master[-1], raster, dtype=np.float64
                            )
                            master = master.interp(raster_)
                        else:
                            raster_ = None
                    else:
                        master = None
                        raster_ = None

                    if time_from_zero:
                        master.samples -= master.samples[0]

                    group_name = "DataGroup_{}".format(i + 1)
                    wb_name = "{}_{}.xlsx".format(name, group_name)
                    workbook = xlsxwriter.Workbook(wb_name)

                    sheet = workbook.add_worksheet(group_name)

                    if master is not None:

                        sig_description = "{} [{}]".format(master.name, master.unit)
                        sheet.write(0, 0, sig_description)
                        sheet.write_column(1, 0, master.samples.astype(str))

                        offset = 1
                    else:
                        offset = 0

                    for col, _ in enumerate(grp["channels"]):
                        if self._terminate:
                            return
                        if col == master_index:
                            offset -= 1
                            continue

                        sig = self.get(group=i, index=col, data=data)
                        if raster_ is not None:
                            sig = sig.interp(raster_)

                        sig_description = "{} [{}]".format(sig.name, sig.unit)
                        sheet.write(0, col + offset, sig_description)

                        try:
                            sheet.write_column(1, col + offset, sig.samples.astype(str))
                        except:
                            vals = [str(e) for e in sig.samples]
                            sheet.write_column(1, col + offset, vals)

                    workbook.close()

        elif fmt == "csv":

            if single_time_base:
                if not name.endswith(".csv"):
                    name += ".csv"
                message = 'Writing csv export to file "{}"'.format(name)
                logger.info(message)
                with open(name, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)

                    names_row = [
                        "{} [{}]".format(channel_name, channel_unit)
                        for (channel_name, channel_unit) in units.items()
                    ]
                    writer.writerow(names_row)

                    vals = [samples for samples in mdict.values()]

                    if self._terminate:
                        return

                    for idx, row in enumerate(zip(*vals)):
                        writer.writerow(row)

            else:

                while name.endswith(".csv"):
                    name = name[:-4]

                count = len(self.groups)
                for i, grp in enumerate(self.groups):
                    if self._terminate:
                        return
                    message = "Exporting group {} of {}".format(i + 1, count)
                    logger.info(message)
                    data = self._load_data(grp)

                    if PYVERSION == 2:
                        data = b"".join(str(d[0]) for d in data)
                    else:
                        data = b"".join(d[0] for d in data)
                    data = (data, 0, None)

                    group_name = "DataGroup_{}".format(i + 1)
                    group_csv_name = "{}_{}.csv".format(name, group_name)
                    with open(group_csv_name, "w") as csvfile:
                        writer = csv.writer(csvfile)

                        master_index = self.masters_db.get(i, None)
                        if master_index is not None:
                            master = self.get(group=i, index=master_index, data=data)

                            if raster and len(master):
                                raster_ = np.arange(
                                    master[0], master[-1], raster, dtype=np.float64
                                )
                                master = master.interp(raster_)
                            else:
                                raster_ = None
                        else:
                            master = None
                            raster_ = None

                        if time_from_zero:
                            if master is None:
                                pass
                            elif len(master):
                                master.samples -= master.samples[0]

                        ch_nr = len(grp["channels"])
                        if master is None:
                            channels = [
                                self.get(group=i, index=j, data=data)
                                for j in range(ch_nr)
                            ]
                        else:
                            if raster_ is not None:
                                channels = [
                                    self.get(group=i, index=j, data=data).interp(
                                        raster_
                                    )
                                    for j in range(ch_nr)
                                    if j != master_index
                                ]
                            else:
                                channels = [
                                    self.get(group=i, index=j, data=data)
                                    for j in range(ch_nr)
                                    if j != master_index
                                ]

                        if raster_ is not None:
                            cycles = len(raster_)
                        else:
                            cycles = grp["channel_group"]["cycles_nr"]

                        if empty_channels == "zeros":
                            for channel in channels:
                                if not len(channel):
                                    channel.samples = np.zeros(
                                        cycles, dtype=channel.samples.dtype
                                    )

                        if master is not None:
                            names_row = [master.name]
                            vals = [master.samples]
                        else:
                            names_row = []
                            vals = []
                        names_row += [
                            "{} [{}]".format(ch.name, ch.unit) for ch in channels
                        ]
                        writer.writerow(names_row)

                        vals += [ch.samples for ch in channels]

                        for idx, row in enumerate(zip(*vals)):
                            writer.writerow(row)

        elif fmt == "mat":

            if not name.endswith(".mat"):
                name = name + ".mat"

            if not single_time_base:
                mdict = {}

                master_name_template = "DGM{}_{}"
                channel_name_template = "DG{}_{}"
                used_names = UniqueDB()

                for i, grp in enumerate(self.groups):
                    if self._terminate:
                        return

                    included_channels = self._included_channels(i)

                    master_index = self.masters_db.get(i, -1)

                    if master_index >= 0:
                        included_channels.add(master_index)
                    data = self._load_data(grp)

                    if PYVERSION == 2:
                        data = b"".join(str(d[0]) for d in data)
                    else:
                        data = b"".join(d[0] for d in data)
                    data = (data, 0, None)

                    for j in included_channels:
                        sig = self.get(group=i, index=j, data=data)
                        if j == master_index:
                            channel_name = master_name_template.format(i, sig.name)
                        else:
                            if use_display_names:
                                channel_name = sig.display_name or sig.name
                            else:
                                channel_name = sig.name
                            channel_name = channel_name_template.format(i, channel_name)

                        channel_name = matlab_compatible(channel_name)
                        channel_name = used_names.get_unique_name(channel_name)

                        if sig.samples.dtype.names:
                            sig.samples.dtype.names = [
                                matlab_compatible(name)
                                for name in sig.samples.dtype.names
                            ]

                        mdict[channel_name] = sig.samples
            else:
                used_names = UniqueDB()
                new_mdict = {}
                for channel_name, samples in mdict.items():
                    channel_name = matlab_compatible(channel_name)
                    channel_name = used_names.get_unique_name(channel_name)

                    new_mdict[channel_name] = samples
                mdict = new_mdict

            if format == "7.3":

                savemat(
                    name,
                    mdict,
                    long_field_names=True,
                    format="7.3",
                    delete_unused_variables=False,
                    oned_as=oned_as,
                )
            else:
                savemat(
                    name,
                    mdict,
                    long_field_names=True,
                    oned_as=oned_as,
                )

        elif fmt in ("pandas", "parquet"):
            if fmt == "pandas":
                return DataFrame.from_dict(mdict)
            else:
                if not name.endswith(".parquet"):
                    name = name + ".parquet"
                write_parquet(name, DataFrame.from_dict(mdict))

        else:
            message = (
                'Unsopported export type "{}". '
                'Please select "csv", "excel", "hdf5", "mat" or "pandas"'
            )
            message.format(fmt)
            logger.warning(message)

    def filter(self, channels, memory=None, version=None):
        """ return new *MDF* object that contains only the channels listed in
        *channels* argument

        Parameters
        ----------
        channels : list
            list of items to be filtered; each item can be :

                * a channel name string
                * (channel name, group index, channel index) list or tuple
                * (channel name, group index) list or tuple
                * (None, group index, channel index) list or tuple

        version : str
            new mdf file version from ('2.00', '2.10', '2.14', '3.00', '3.10',
            '3.20', '3.30', '4.00', '4.10', '4.11'); default *None* and in this
            case the original file version is used
        memory : str
            memory option; default *None* and in this case the original file
            memory option is used

        Returns
        -------
        mdf : MDF
            new *MDF* file

        Examples
        --------
        >>> from asammdf import MDF, Signal
        >>> import numpy as np
        >>> t = np.arange(5)
        >>> s = np.ones(5)
        >>> mdf = MDF()
        >>> for i in range(4):
        ...     sigs = [Signal(s*(i*10+j), t, name='SIG') for j in range(1,4)]
        ...     mdf.append(sigs)
        ...
        >>> filtered = mdf.filter(['SIG', ('SIG', 3, 1), ['SIG', 2], (None, 1, 2)])
        >>> for gp_nr, ch_nr in filtered.channels_db['SIG']:
        ...     print(filtered.get(group=gp_nr, index=ch_nr))
        ...
        <Signal SIG:
                samples=[ 1.  1.  1.  1.  1.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        <Signal SIG:
                samples=[ 31.  31.  31.  31.  31.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        <Signal SIG:
                samples=[ 21.  21.  21.  21.  21.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        <Signal SIG:
                samples=[ 12.  12.  12.  12.  12.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">

        """

        if memory is None:
            memory = self.memory
        else:
            memory = validate_memory_argument(memory)

        if version is None:
            version = self.version
        else:
            version = validate_version_argument(version)

        # group channels by group index
        gps = {}

        for item in channels:
            if isinstance(item, (list, tuple)):
                if len(item) not in (2, 3):
                    raise MdfException(
                        "The items used for filtering must be strings, "
                        "or they must match the first 3 argumens of the get "
                        "method"
                    )
                else:
                    group, index = self._validate_channel_selection(*item)
                    if group not in gps:
                        gps[group] = {index}
                    else:
                        gps[group].add(index)
            else:
                name = item
                group, index = self._validate_channel_selection(name)
                if group not in gps:
                    gps[group] = {index}
                else:
                    gps[group].add(index)

        # see if there are exluded channels in the filter list
        for group_index, indexes in gps.items():
            grp = self.groups[group_index]
            included_channels = set(indexes)
            for index in indexes:
                if self.version in MDF2_VERSIONS + MDF3_VERSIONS:
                    dep = grp["channel_dependencies"][index]
                    if dep:
                        for gp_nr, ch_nr in dep.referenced_channels:
                            if gp_nr == group:
                                included_channels.remove(ch_nr)
                else:
                    dependencies = grp["channel_dependencies"][index]
                    if dependencies is None:
                        continue
                    if all(
                        not isinstance(dep, ChannelArrayBlock) for dep in dependencies
                    ):
                        channels = grp["channels"]
                        for channel in dependencies:
                            included_channels.add(channels.index(channel))
                    else:
                        for dep in dependencies:
                            for gp_nr, ch_nr in dep.referenced_channels:
                                if gp_nr == group:
                                    included_channels.remove(ch_nr)

            gps[group_index] = included_channels

        mdf = MDF(version=version, memory=memory)
        name, _ = os.path.splitext(self.name)
        _, ext = os.path.splitext(mdf.name)
        mdf.name = '{}.filtered_to_{}{}'.format(name, version, ext)

        mdf.header.start_time = self.header.start_time

        if self.name:
            origin = os.path.basename(self.name)
        else:
            origin = "New MDF"

        groups_nr = len(gps)

        if self._callback:
            self._callback(0, groups_nr)

        # append filtered channels to new MDF
        for new_index, (group_index, indexes) in enumerate(gps.items()):
            if version < "4.00":
                encodings = [None, ]

            group = self.groups[group_index]

            data = self._load_data(group)
            parents, dtypes = self._prepare_record(group)
            group["parents"], group["types"] = parents, dtypes

            for idx, fragment in enumerate(data):

                if dtypes.itemsize:
                    group["record"] = np.core.records.fromstring(
                        fragment[0], dtype=dtypes
                    )
                    group["record"].setflags(write=False)
                else:
                    group["record"] = None

                # the first fragment triggers and append that will add the
                # metadata for all channels
                if idx == 0:
                    sigs = []
                    for j in indexes:
                        sig = self.get(
                            group=group_index,
                            index=j,
                            data=fragment,
                            raw=True,
                            ignore_invalidation_bits=True,
                            copy_master=False,
                        )
                        if version < "4.00":
                            if sig.samples.dtype.kind == "S":
                                encodings.append(sig.encoding)
                                strsig = self.get(
                                    group=group_index,
                                    index=j,
                                    samples_only=True,
                                    ignore_invalidation_bits=True,
                                )[0]
                                sig.samples = sig.samples.astype(strsig.dtype)
                                del strsig
                                if sig.encoding != "latin-1":

                                    if sig.encoding == "utf-16-le":
                                        sig.samples = sig.samples.view(np.uint16).byteswap().view(sig.samples.dtype)
                                        sig.samples = encode(decode(sig.samples, "utf-16-be"), "latin-1")
                                    else:
                                        sig.samples = encode(decode(sig.samples, sig.encoding), "latin-1")
                            else:
                                encodings.append(None)
                        if not sig.samples.flags.writeable:
                            sig.samples = sig.samples.copy()
                        sigs.append(sig)

                    source_info = "Signals filtered from <{}>".format(origin)

                    if sigs:
                        mdf.append(sigs, source_info, common_timebase=True)
                    else:
                        break

                # the other fragments will trigger onl the extension of
                # samples records to the data block
                else:
                    sigs = [(self.get_master(group_index, data=fragment, copy_master=False), None)]

                    for j in indexes:
                        sig = self.get(
                            group=group_index,
                            index=j,
                            data=fragment,
                            samples_only=True,
                            raw=True,
                            ignore_invalidation_bits=True,
                        )
                        if version < "4.00":
                            encoding = encodings[j]
                            samples = sig[0]
                            if encoding:
                                if encoding != "latin-1":

                                    if encoding == "utf-16-le":
                                        samples = samples.view(np.uint16).byteswap().view(samples.dtype)
                                        samples = encode(decode(samples, "utf-16-be"), "latin-1")
                                    else:
                                        samples = encode(decode(samples, encoding), "latin-1")
                                    sig.samples = samples
                        sigs.append(sig)

                    if sigs:
                        mdf.extend(new_index, sigs)

                del group["record"]

            if self._callback:
                self._callback(new_index + 1, groups_nr)

            if self._terminate:
                return

        mdf._transfer_events(self)
        if self._callback:
            mdf._callback = mdf._mdf._callback = self._callback
        return mdf

    def iter_get(
        self,
        name=None,
        group=None,
        index=None,
        raster=None,
        samples_only=False,
        raw=False,
    ):
        """ iterator over a channel

        This is usefull in case of large files with a small number of channels.

        If the *raster* keyword argument is not *None* the output is
        interpolated accordingly

        Parameters
        ----------
        name : string
            name of channel
        group : int
            0-based group index
        index : int
            0-based channel index
        raster : float
            time raster in seconds
        samples_only : bool
            if *True* return only the channel samples as numpy array; if
                *False* return a *Signal* object
        raw : bool
            return channel samples without appling the conversion rule; default
            `False`

        """
        gp_nr, ch_nr = self._validate_channel_selection(name, group, index)

        grp = self.groups[gp_nr]

        data = self._load_data(grp)

        for fragment in data:
            yield self.get(
                group=gp_nr,
                index=ch_nr,
                raster=raster,
                samples_only=samples_only,
                data=fragment,
                raw=raw,
            )

    @staticmethod
    def concatenate(files, version="4.10", memory="full", sync=True, **kwargs):
        """ concatenates several files. The files
        must have the same internal structure (same number of groups, and same
        channels in each group)

        Parameters
        ----------
        files : list | tuple
            list of *MDF* file names or *MDF* instances
        version : str
            merged file version
        memory : str
            memory option; default *full*
        sync : bool
            sync the files based on the start of measurement, default *True*

        Returns
        -------
        concatenate : MDF
            new *MDF* object with concatenated channels

        Raises
        ------
        MdfException : if there are inconsistencies between the files

        """
        if not files:
            raise MdfException("No files given for merge")

        callback = kwargs.get("callback", None)
        if callback:
            callback(0, 100)

        versions = []
        if sync:
            timestamps = []
            for file in files:
                if isinstance(file, MDF):
                    timestamps.append(file.header.start_time)
                    versions.append(file.version)
                else:
                    with open(file, "rb") as mdf:
                        mdf.seek(64)
                        blk_id = mdf.read(2)
                        if blk_id == b"HD":
                            header = HeaderV3
                            versions.append('3.00')
                        else:
                            versions.append('4.00')
                            blk_id += mdf.read(2)
                            if blk_id == b"##HD":
                                header = HeaderV4
                            else:
                                raise MdfException(
                                    '"{}" is not a valid MDF file'.format(file)
                                )

                        header = header(address=64, stream=mdf)

                        timestamps.append(header.start_time)

            oldest = timestamps[0]
            offsets = [
                (timestamp - oldest).total_seconds()
                for timestamp in timestamps
            ]
            offsets = [offset if offset > 0 else 0 for offset in offsets]

        else:
            file = files[0]
            if isinstance(file, MDF):
                oldest = file.header.start_time
                versions.append(file.version)
            else:
                with open(file, "rb") as mdf:
                    mdf.seek(64)
                    blk_id = mdf.read(2)
                    if blk_id == b"HD":
                        versions.append('3.00')
                        header = HeaderV3
                    else:
                        versions.append('4.00')
                        blk_id += mdf.read(2)
                        if blk_id == b"##HD":
                            header = HeaderV4
                        else:
                            raise MdfException(
                                '"{}" is not a valid MDF file'.format(file)
                            )

                    header = header(address=64, stream=mdf)

                    oldest = header.start_time

            offsets = [0 for _ in files]

        sizes = set()
        for file in files:
            if isinstance(file, MDF):
                if file.version < '4.00':
                    ch_count = sum(
                        len(group['channels'])
                        for group in file.groups
                    )
                else:
                    ch_count = sum(
                        len(group['channels']) - sum(
                                len(dep)
                                for dep in group['channel_dependencies']
                                if dep and not isinstance(dep[0], ChannelArrayBlock)
                            )
                        for group in file.groups
                    )
                info = len(file.groups), ch_count
            else:
                with open(file, "rb") as mdf:
                    info = count_channel_groups(mdf, include_channels=True)
            sizes.add(info)

        if len(sizes) > 1:
            message = "Can't merge files: difference in number of data groups"
            raise MdfException(message)

        groups_nr, _ = sizes.pop()

        last_timestamps = [
            None
            for _ in range(groups_nr)
        ]

        version = validate_version_argument(version)

        memory = validate_memory_argument(memory)

        merged = MDF(version=version, memory=memory, callback=callback)
        _, ext = os.path.splitext(merged.name)
        merged.name = 'Concatenated_to_{}{}'.format(version, ext)

        merged.header.start_time = oldest

        for mdf_index, (offset, mdf) in enumerate(zip(offsets, files)):
            if not isinstance(mdf, MDF):
                mdf = MDF(mdf, memory=memory)

            cg_nr = -1

            for i, group in enumerate(mdf.groups):
                included_channels = mdf._included_channels(i)
                if included_channels:
                    cg_nr += 1
                else:
                    continue
                channels_nr = len(group["channels"])

                if memory == "minimum":
                    y_axis = MERGE_MINIMUM
                else:
                    y_axis = MERGE_LOW

                idx = np.searchsorted(CHANNEL_COUNT, channels_nr, side='right') - 1
                if idx < 0:
                    idx = 0
                read_size = y_axis[idx]

                idx = 0
                last_timestamp = last_timestamps[i]
                first_timestamp = None
                original_first_timestamp = None

                if read_size:
                    mdf.configure(read_fragment_size=int(read_size))

                parents, dtypes = mdf._prepare_record(group)
                group["parents"], group["types"] = parents, dtypes

                data = mdf._load_data(group)

                for fragment in data:

                    if dtypes.itemsize:
                        group["record"] = np.core.records.fromstring(
                            fragment[0], dtype=dtypes
                        )
                        group["record"].setflags(write=False)
                    else:
                        group["record"] = None

                    if mdf_index == 0 and idx == 0:
                        encodings = [None, ]
                        signals = []
                        for j in included_channels:
                            sig = mdf.get(
                                group=i,
                                index=j,
                                data=fragment,
                                raw=True,
                                ignore_invalidation_bits=True,
                                copy_master=False,
                            )

                            if version < "4.00":
                                if sig.samples.dtype.kind == "S":
                                    encodings.append(sig.encoding)
                                    strsig = mdf.get(
                                        group=i,
                                        index=j,
                                        samples_only=True,
                                        ignore_invalidation_bits=True,
                                    )[0]
                                    sig.samples = sig.samples.astype(strsig.dtype)
                                    del strsig
                                    if sig.encoding != "latin-1":

                                        if sig.encoding == "utf-16-le":
                                            sig.samples = sig.samples.view(np.uint16).byteswap().view(sig.samples.dtype)
                                            sig.samples = encode(decode(sig.samples, "utf-16-be"), "latin-1")
                                        else:
                                            sig.samples = encode(decode(sig.samples, sig.encoding), "latin-1")
                                else:
                                    encodings.append(None)

                            if not sig.samples.flags.writeable:
                                sig.samples = sig.samples.copy()
                            signals.append(sig)

                        if signals and len(signals[0]):
                            if offset > 0:
                                timestamps = sig[0].timestamps + offset
                                for sig in signals:
                                    sig.timestamps = timestamps
                            last_timestamp = signals[0].timestamps[-1]
                            first_timestamp = signals[0].timestamps[0]
                            original_first_timestamp = first_timestamp

                        if signals:
                            merged.append(signals, common_timebase=True)
                        else:
                            break
                        idx += 1
                    else:
                        master = mdf.get_master(i, fragment)

                        if len(master):
                            if original_first_timestamp is None:
                                original_first_timestamp = master[0]
                            if offset > 0:
                                master = master + offset
                            if last_timestamp is None:
                                last_timestamp = master[-1]
                            else:
                                if last_timestamp >= master[0]:
                                    if len(master) >= 2:
                                        delta = master[1] - master[0]
                                    else:
                                        delta = 0.001
                                    master -= master[0]
                                    master += last_timestamp + delta
                                last_timestamp = master[-1]

                            signals = [(master, None)]

                            for j in included_channels:
                                sig = mdf.get(
                                    group=i,
                                    index=j,
                                    data=fragment,
                                    raw=True,
                                    samples_only=True,
                                    ignore_invalidation_bits=True,
                                )

                                signals.append(sig)

                                if version < '4.00':
                                    encoding = encodings[j]
                                    samples = sig[0]
                                    if encoding:
                                        if encoding != "latin-1":

                                            if encoding == "utf-16-le":
                                                samples = samples.view(np.uint16).byteswap().view(samples.dtype)
                                                samples = encode(decode(samples, "utf-16-be"), "latin-1")
                                            else:
                                                samples = encode(decode(samples, encoding), "latin-1")
                                            sig.samples = samples

                            if signals:
                                merged.extend(cg_nr, signals)

                            if first_timestamp is None:
                                first_timestamp = master[0]
                        idx += 1

                    del group["record"]

                last_timestamps[i] = last_timestamp
                if first_timestamp is not None:
                    merged.groups[-1]['channel_group'].comment += (
                        "{}s to {}s concatenated from channel group {} of \"{}\" with first time stamp at {}s\n".format(
                            first_timestamp, last_timestamp, i, os.path.basename(mdf.name), original_first_timestamp
                        )
                    )
                else:
                    merged.groups[-1]['channel_group'].comment += (
                        "there were no samples in channel group {} of \"{}\"\n".format(
                            i, os.path.basename(mdf.name)
                        )
                    )

            if callback:
                callback(i + 1, groups_nr)

            if MDF._terminate:
                return

            merged._transfer_events(mdf)

        return merged

    @staticmethod
    def merge(files, version="4.10", memory="full", sync=True, **kwargs):
        """ concatenates several files. The files
        must have the same internal structure (same number of groups, and same
        channels in each group)

        Parameters
        ----------
        files : list | tuple
            list of *MDF* file names or *MDF* instances
        version : str
            merged file version
        memory : str
            memory option; default *full*
        sync : bool
            sync the files based on the start of measurement, default *True*

        Returns
        -------
        concatenate : MDF
            new *MDF* object with concatenated channels

        Raises
        ------
        MdfException : if there are inconsistencies between the files

        """
        return MDF.concatenate(files, version, memory, sync, **kwargs)

    @staticmethod
    def stack(files, version="4.10", memory="full", sync=True, **kwargs):
        """ stack several files and return the stacked *MDF* object

        Parameters
        ----------
        files : list | tuple
            list of *MDF* file names or *MDF* instances
        version : str
            merged file version
        memory : str
            memory option; default *full*
        sync : bool
            sync the files based on the start of measurement, default *True*

        Returns
        -------
        stacked : MDF
            new *MDF* object with stacked channels

        """
        if not files:
            raise MdfException("No files given for stack")

        version = validate_version_argument(version)
        memory = validate_memory_argument(memory)

        callback = kwargs.get("callback", None)

        stacked = MDF(version=version, memory=memory, callback=callback)
        _, ext = os.path.splitext(stacked.name)
        stacked.name = 'Stacked_to_{}{}'.format(version, ext)

        files_nr = len(files)

        if callback:
            callback(0, files_nr)

        if sync:
            timestamps = []
            for file in files:
                if isinstance(file, MDF):
                    timestamps.append(file.header.start_time)
                else:
                    with open(file, "rb") as mdf:
                        mdf.seek(64)
                        blk_id = mdf.read(2)
                        if blk_id == b"HD":
                            header = HeaderV3
                        else:
                            blk_id += mdf.read(2)
                            if blk_id == b"##HD":
                                header = HeaderV4
                            else:
                                raise MdfException(
                                    '"{}" is not a valid MDF file'.format(file)
                                )

                        header = header(address=64, stream=mdf)

                        timestamps.append(header.start_time)

            oldest = min(timestamps)
            offsets = [(timestamp - oldest).total_seconds() for timestamp in timestamps]

            stacked.header.start_time = oldest
        else:
            offsets = [0 for file in files]

        cg_nr = -1
        for offset, mdf in zip(offsets, files):
            if not isinstance(mdf, MDF):
                mdf = MDF(mdf, memory)

            for i, group in enumerate(mdf.groups):
                idx = 0
                if version < "4.00":
                    encodings = [None, ]
                included_channels = mdf._included_channels(i)
                if included_channels:
                    cg_nr += 1
                else:
                    continue

                parents, dtypes = mdf._prepare_record(group)
                group["parents"], group["types"] = parents, dtypes

                data = mdf._load_data(group)

                for fragment in data:

                    if dtypes.itemsize:
                        group["record"] = np.core.records.fromstring(
                            fragment[0], dtype=dtypes
                        )
                        group["record"].setflags(write=False)
                    else:
                        group["record"] = None
                    if idx == 0:
                        signals = []
                        for j in included_channels:
                            sig = mdf.get(
                                group=i,
                                index=j,
                                data=fragment,
                                raw=True,
                                ignore_invalidation_bits=True,
                                copy_master=False,
                            )

                            if version < "4.00":
                                if sig.samples.dtype.kind == "S":
                                    encodings.append(sig.encoding)
                                    strsig = mdf.get(
                                        group=i,
                                        index=j,
                                        samples_only=True,
                                        ignore_invalidation_bits=True,
                                    )[0]
                                    sig.samples = sig.samples.astype(strsig.dtype)
                                    del strsig
                                    if sig.encoding != "latin-1":

                                        if sig.encoding == "utf-16-le":
                                            sig.samples = sig.samples.view(np.uint16).byteswap().view(sig.samples.dtype)
                                            sig.samples = encode(decode(sig.samples, "utf-16-be"), "latin-1")
                                        else:
                                            sig.samples = encode(decode(sig.samples, sig.encoding), "latin-1")
                                else:
                                    encodings.append(None)

                            if not sig.samples.flags.writeable:
                                sig.samples = sig.samples.copy()
                            signals.append(sig)

                        if signals:
                            if sync:
                                timestamps = signals[0].timestamps + offset
                                for sig in signals:
                                    sig.timestamps = timestamps
                            stacked.append(signals, common_timebase=True)
                        idx += 1
                    else:
                        master = mdf.get_master(i, fragment)
                        if sync:
                            master = master + offset
                        if len(master):

                            signals = [(master, None)]

                            for j in included_channels:
                                sig = mdf.get(
                                        group=i,
                                        index=j,
                                        data=fragment,
                                        raw=True,
                                        samples_only=True,
                                        ignore_invalidation_bits=True,
                                    )
                                signals.append(sig)

                                if version < "4.00":
                                    encoding = encodings[j]
                                    samples = sig[0]
                                    if encoding:
                                        if encoding != "latin-1":

                                            if encoding == "utf-16-le":
                                                samples = samples.view(np.uint16).byteswap().view(samples.dtype)
                                                samples = encode(decode(samples, "utf-16-be"), "latin-1")
                                            else:
                                                samples = encode(decode(samples, encoding), "latin-1")
                                            sig.samples = samples

                            if signals:
                                stacked.extend(cg_nr, signals)
                        idx += 1

                    del group["record"]

                stacked.groups[-1]['channel_group'].comment = (
                    "stacked from channel group {} of \"{}\"".format(
                        i, os.path.basename(mdf.name)
                    )
                )

            if callback:
                callback(idx, files_nr)

            if MDF._terminate:
                return

        return stacked

    def iter_channels(self, skip_master=True):
        """ generator that yields a *Signal* for each non-master channel

        Parameters
        ----------
        skip_master : bool
            do not yield master channels; default *True*

        """
        for i, group in enumerate(self.groups):
            try:
                master_index = self.masters_db[i]
            except KeyError:
                master_index = -1

            for j, _ in enumerate(group["channels"]):
                if skip_master and j == master_index:
                    continue
                yield self.get(group=i, index=j)

    def iter_groups(self):
        """ generator that yields channel groups as pandas DataFrames. If there
        are multiple occurences for the same channel name inside a channel
        group, then a counter will be used to make the names unique
        (<original_name>_<counter>)

        """

        for i, group in enumerate(self.groups):
            yield self.get_group(i)

    def resample(self, raster, memory=None, version=None):
        """ resample all channels using the given raster

        Parameters
        ----------
        raster : float
            time raster is seconds
        version : str
            new mdf file version from ('2.00', '2.10', '2.14', '3.00', '3.10',
            '3.20', '3.30', '4.00', '4.10', '4.11'); default *None* and in this
            case the original file version is used
        memory : str
            memory option; default *None* and in this case the original file
            memory option is used

        Returns
        -------
        mdf : MDF
            new *MDF* with resampled channels

        """

        if memory is None:
            memory = self.memory
        else:
            memory = validate_memory_argument(memory)

        if version is None:
            version = self.version
        else:
            version = validate_version_argument(version)

        mdf = MDF(version=version, memory=memory)
        name, _ = os.path.splitext(self.name)
        _, ext = os.path.splitext(mdf.name)
        mdf.name = '{}.resampled_with_raster_{}s_to_{}{}'.format(name, raster, version, ext)

        mdf.header.start_time = self.header.start_time

        groups_nr = len(self.groups)

        if self._callback:
            self._callback(0, groups_nr)

        # walk through all groups and get all channels
        cg_nr = -1
        for i, group in enumerate(self.groups):
            if version < "4.00":
                encodings = [None, ]
            included_channels = self._included_channels(i)
            if included_channels:
                cg_nr += 1
            else:
                continue

            data = self._load_data(group)
            for idx, fragment in enumerate(data):

                if idx == 0:
                    sigs = []
                    for j in included_channels:
                        sig = self.get(
                            group=i,
                            index=j,
                            data=fragment,
                            raw=True,
                            raster=raster,
                            ignore_invalidation_bits=True,
                        )
                        if version < "4.00":
                            if sig.samples.dtype.kind == "S":
                                encodings.append(sig.encoding)
                                strsig = self.get(
                                    group=i,
                                    index=j,
                                    samples_only=True,
                                    ignore_invalidation_bits=True,
                                )[0]
                                sig.samples = sig.samples.astype(strsig.dtype)
                                del strsig
                                if sig.encoding != "latin-1":

                                    if sig.encoding == "utf-16-le":
                                        sig.samples = sig.samples.view(np.uint16).byteswap().view(sig.samples.dtype)
                                        sig.samples = encode(decode(sig.samples, "utf-16-be"), "latin-1")
                                    else:
                                        sig.samples = encode(decode(sig.samples, sig.encoding), "latin-1")
                            else:
                                encodings.append(None)

                        if not sig.samples.flags.writeable:
                            sig.samples = sig.samples.copy()
                        sigs.append(sig)

                    if sigs:
                        mdf.append(
                            sigs,
                            "Resampled to {}s".format(raster),
                            common_timebase=True,
                        )
                    else:
                        break

                else:
                    sigs = [(self.get_master(i, data=fragment, raster=raster), None)]

                    for j in included_channels:
                        sig = self.get(
                            group=i,
                            index=j,
                            data=fragment,
                            raw=True,
                            samples_only=True,
                            raster=raster,
                            ignore_invalidation_bits=True,
                        )

                        if version < "4.00":
                            encoding = encodings[j]
                            samples = sig[0]
                            if encoding:
                                if encoding != "latin-1":

                                    if encoding == "utf-16-le":
                                        samples = samples.view(np.uint16).byteswap().view(samples.dtype)
                                        samples = encode(decode(samples, "utf-16-be"), "latin-1")
                                    else:
                                        samples = encode(decode(samples, encoding), "latin-1")
                                    sig.samples = samples

                        if not sig[0].flags.writeable:
                            sig = sig[0].copy(), sig[1]
                        sigs.append(sig)

                    if sigs:
                        mdf.extend(cg_nr, sigs)

            if self._callback:
                self._callback(cg_nr + 1, groups_nr)

            if self._terminate:
                return

        mdf._transfer_events(self)
        if self._callback:
            mdf._callback = mdf._mdf._callback = self._callback
        return mdf

    def select(self, channels, dataframe=False, record_offset=0):
        """ retreiv the channels listed in *channels* argument as *Signal*
        objects

        Parameters
        ----------
        channels : list
            list of items to be filtered; each item can be :

                * a channel name string
                * (channel name, group index, channel index) list or tuple
                * (channel name, group index) list or tuple
                * (None, group index, channel index) lsit or tuple

        dataframe: bool
            return a pandas DataFrame instead of a list of *Signals*; in this
            case the signals will be interpolated using the union of all
            timestamps

        Returns
        -------
        signals : list
            list of *Signal* objects based on the input channel list

        Examples
        --------
        >>> from asammdf import MDF, Signal
        >>> import numpy as np
        >>> t = np.arange(5)
        >>> s = np.ones(5)
        >>> mdf = MDF()
        >>> for i in range(4):
        ...     sigs = [Signal(s*(i*10+j), t, name='SIG') for j in range(1,4)]
        ...     mdf.append(sigs)
        ...
        >>> # select SIG group 0 default index 1 default, SIG group 3 index 1, SIG group 2 index 1 default and channel index 2 from group 1
        ...
        >>> mdf.select(['SIG', ('SIG', 3, 1), ['SIG', 2],  (None, 1, 2)])
        [<Signal SIG:
                samples=[ 1.  1.  1.  1.  1.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        , <Signal SIG:
                samples=[ 31.  31.  31.  31.  31.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        , <Signal SIG:
                samples=[ 21.  21.  21.  21.  21.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        , <Signal SIG:
                samples=[ 12.  12.  12.  12.  12.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        ]

        """

        # group channels by group index
        gps = {}

        indexes = []

        for item in channels:
            if isinstance(item, (list, tuple)):
                if len(item) not in (2, 3):
                    raise MdfException(
                        "The items used for filtering must be strings, "
                        "or they must match the first 3 argumens of the get "
                        "method"
                    )
                else:
                    group, index = self._validate_channel_selection(*item)
                    indexes.append((group, index))
                    if group not in gps:
                        gps[group] = {index}
                    else:
                        gps[group].add(index)
            else:
                name = item
                group, index = self._validate_channel_selection(name)
                indexes.append((group, index))
                if group not in gps:
                    gps[group] = {index}
                else:
                    gps[group].add(index)

        signal_parts = {}
        for group in gps:
            grp = self.groups[group]
            data = self._load_data(grp, record_offset=record_offset)
            parents, dtypes = self._prepare_record(grp)
            grp["parents"], grp["types"] = parents, dtypes

            for fragment in data:
                if dtypes.itemsize:
                    grp["record"] = np.core.records.fromstring(
                        fragment[0], dtype=dtypes
                    )
                    grp["record"].setflags(write=False)
                else:
                    grp["record"] = None
                for index in gps[group]:
                    signal = self.get(
                        group=group,
                        index=index,
                        data=fragment,
                        copy_master=False,
                    )
                    if (group, index) not in signal_parts:
                        signal_parts[(group, index)] = [signal]
                    else:
                        signal_parts[(group, index)].append(signal)
                del grp["record"]

        signals = []
        for pair in indexes:
            parts = signal_parts[pair]
            signal = Signal(
                np.concatenate([part.samples for part in parts]),
                np.concatenate([part.timestamps for part in parts]),
                unit=parts[0].unit,
                name=parts[0].name,
                comment=parts[0].comment,
                raw=parts[0].raw,
                conversion=parts[0].conversion,
            )
            signals.append(signal)

        if dataframe:
            times = [s.timestamps for s in signals]
            t = reduce(np.union1d, times).flatten().astype(np.float64)
            signals = [s.interp(t) for s in signals]

            pandas_dict = {"time": t}
            for sig in signals:
                pandas_dict[sig.name] = sig.samples

            signals = DataFrame.from_dict(pandas_dict)

        return signals

    def whereis(self, channel):
        """ get ocurrences of channel name in the file

        Parameters
        ----------
        channel : str
            channel name string

        Returns
        -------
        ocurrences : tuple


        Examples
        --------
        >>> mdf = MDF(file_name)
        >>> mdf.whereis('VehicleSpeed') # "VehicleSpeed" exists in the file
        ((1, 2), (2, 4))
        >>> mdf.whereis('VehicleSPD') # "VehicleSPD" doesn't exist in the file
        ()

        """
        if channel in self:
            return tuple(self.channels_db[channel])
        else:
            return tuple()

    @staticmethod
    def scramble(name, memory="low"):
        """ scramble text blocks and keep original file structure

        Parameters
        ----------
        name : str
            file name
        memory : str
            memory option; default *'low'*

        """

        memory = validate_memory_argument(memory)
        mdf = MDF(name, memory=memory)
        texts = {}

        if mdf.version >= "4.00":
            Channel = ChannelV4
            ChannelConversion = ChannelConversionV4

            stream = mdf._file

            if mdf.header["comment_addr"]:
                stream.seek(mdf.header["comment_addr"] + 8)
                size = UINT64_u(stream.read(8))[0] - 24
                texts[mdf.header["comment_addr"]] = randomized_string(size)

            for fh in mdf.file_history:
                addr = fh["comment_addr"]
                if addr and addr not in texts:
                    stream.seek(addr + 8)
                    size = UINT64_u(stream.read(8))[0] - 24
                    texts[addr] = randomized_string(size)

            for ev in mdf.events:
                for addr in (ev["comment_addr"], ev["name_addr"]):
                    if addr and addr not in texts:
                        stream.seek(addr + 8)
                        size = UINT64_u(stream.read(8))[0] - 24
                        texts[addr] = randomized_string(size)

            for gp in mdf.groups:

                addr = gp["data_group"]["comment_addr"]
                if addr and addr not in texts:
                    stream.seek(addr + 8)
                    size = UINT64_u(stream.read(8))[0] - 24
                    texts[addr] = randomized_string(size)

                cg = gp["channel_group"]
                for addr in (cg["acq_name_addr"], cg["comment_addr"]):
                    if cg["flags"] & v4c.FLAG_CG_BUS_EVENT:
                        continue

                    if addr and addr not in texts:
                        stream.seek(addr + 8)
                        size = UINT64_u(stream.read(8))[0] - 24
                        texts[addr] = randomized_string(size)

                    source = cg["acq_source_addr"]
                    if source:
                        source = SourceInformation(address=source, stream=stream)
                        for addr in (
                            source["name_addr"],
                            source["path_addr"],
                            source["comment_addr"],
                        ):
                            if addr and addr not in texts:
                                stream.seek(addr + 8)
                                size = UINT64_u(stream.read(8))[0] - 24
                                texts[addr] = randomized_string(size)

                for ch in gp["channels"]:
                    if mdf.memory == "minimum":
                        ch = Channel(address=ch, stream=stream, load_metadata=False)

                    for addr in (ch["name_addr"], ch["unit_addr"], ch["comment_addr"]):
                        if addr and addr not in texts:
                            stream.seek(addr + 8)
                            size = UINT64_u(stream.read(8))[0] - 24
                            texts[addr] = randomized_string(size)

                    source = ch["source_addr"]
                    if source:
                        source = SourceInformation(address=source, stream=stream)
                        for addr in (
                            source["name_addr"],
                            source["path_addr"],
                            source["comment_addr"],
                        ):
                            if addr and addr not in texts:
                                stream.seek(addr + 8)
                                size = UINT64_u(stream.read(8))[0] - 24
                                texts[addr] = randomized_string(size)

                    conv = ch["conversion_addr"]
                    if conv:
                        conv = ChannelConversion(address=conv, stream=stream)
                        for addr in (
                            conv["name_addr"],
                            conv["unit_addr"],
                            conv["comment_addr"],
                        ):
                            if addr and addr not in texts:
                                stream.seek(addr + 8)
                                size = UINT64_u(stream.read(8))[0] - 24
                                texts[addr] = randomized_string(size)
                        if conv["conversion_type"] == v4c.CONVERSION_TYPE_ALG:
                            addr = conv["formula_addr"]
                            if addr and addr not in texts:
                                stream.seek(addr + 8)
                                size = UINT64_u(stream.read(8))[0] - 24
                                texts[addr] = randomized_string(size)

                        if conv.referenced_blocks:
                            for key, block in conv.referenced_blocks.items():
                                if block:
                                    if block["id"] == b"##TX":
                                        addr = block.address
                                        if addr not in texts:
                                            stream.seek(addr + 8)
                                            size = block["block_len"] - 24
                                            texts[addr] = randomized_string(size)
            mdf.close()

            if name.lower().endswith(".mf4"):
                dst = name[:-4] + ".scrambled.mf4"
            else:
                dst = name + ".scrambled.mf4"

            copy(name, dst)

            with open(dst, "rb+") as mdf:
                for addr, bts in texts.items():
                    mdf.seek(addr + 24)
                    mdf.write(bts)

        else:
            Channel = ChannelV3
            ChannelConversion = ChannelConversionV3

            stream = mdf._file

            if mdf.header["comment_addr"]:
                stream.seek(mdf.header["comment_addr"] + 2)
                size = UINT16_u(stream.read(2))[0] - 4
                texts[mdf.header["comment_addr"] + 4] = randomized_string(size)
            texts[36 + 0x40] = randomized_string(32)
            texts[68 + 0x40] = randomized_string(32)
            texts[100 + 0x40] = randomized_string(32)
            texts[132 + 0x40] = randomized_string(32)

            for gp in mdf.groups:

                cg = gp["channel_group"]
                addr = cg["comment_addr"]

                if addr and addr not in texts:
                    stream.seek(addr + 2)
                    size = UINT16_u(stream.read(2))[0] - 4
                    texts[addr + 4] = randomized_string(size)

                if gp["trigger"]:
                    addr = gp["trigger"]["text_addr"]
                    if addr:
                        stream.seek(addr + 2)
                        size = UINT16_u(stream.read(2))[0] - 4
                        texts[addr + 4] = randomized_string(size)

                for ch in gp["channels"]:
                    if mdf.memory == "minimum":
                        ch = Channel(address=ch, stream=stream, load_metadata=False)

                    for key in ("long_name_addr", "display_name_addr", "comment_addr"):
                        addr = ch.get(key, 0)
                        if addr and addr not in texts:
                            stream.seek(addr + 2)
                            size = UINT16_u(stream.read(2))[0] - 4
                            texts[addr + 4] = randomized_string(size)

                    texts[ch.address + 26] = randomized_string(32)
                    texts[ch.address + 58] = randomized_string(128)

                    source = ch["source_addr"]
                    if source:
                        source = ChannelExtension(address=source, stream=stream)
                        if source["type"] == v23c.SOURCE_ECU:
                            texts[source.address + 12] = randomized_string(80)
                            texts[source.address + 92] = randomized_string(32)
                        else:
                            texts[source.address + 14] = randomized_string(36)
                            texts[source.address + 50] = randomized_string(36)

                    conv = ch["conversion_addr"]
                    if conv:
                        texts[conv + 22] = randomized_string(20)

                        conv = ChannelConversion(address=conv, stream=stream)

                        if conv["conversion_type"] == v23c.CONVERSION_TYPE_FORMULA:
                            texts[conv + 36] = randomized_string(conv["block_len"] - 36)

                        if conv.referenced_blocks:
                            for key, block in conv.referenced_blocks.items():
                                if block:
                                    if block["id"] == b"TX":
                                        addr = block.address
                                        if addr and addr not in texts:
                                            stream.seek(addr + 2)
                                            size = UINT16_u(stream.read(2))[0] - 4
                                            texts[addr + 4] = randomized_string(size)
            mdf.close()

            if name.lower().endswith(".mdf"):
                dst = name[:-4] + ".scrambled.mdf"
            else:
                dst = name + ".scrambled.mdf"

            copy(name, dst)

            with open(dst, "rb+") as mdf:
                for addr, bts in texts.items():
                    mdf.seek(addr)
                    mdf.write(bts)

    def get_group(self, index):
        """ get channel group as pandas DataFrames. If there are multiple
        occurences for the same channel name, then a counter will be used to
        make the names unique (<original_name>_<counter>)

        Parameters
        ----------
        index : int
            channel group index

        Returns
        -------
        df : pandas.DataFrame

        """

        group = self.groups[index]

        i = index

        master_index = self.masters_db.get(i, -1)

        if master_index >= 0:
            master_name = self.get_channel_name(i, master_index)
        else:
            master_name = "Idx"

        master = []

        names = [
            self.get_channel_name(i, j)
            for j, _ in enumerate(group["channels"])
            if j != master_index
        ]

        sigs = [
            []
            for j, _ in enumerate(group["channels"])
            if j != master_index
        ]

        data = self._load_data(group)
        for fragment in data:

            master.append(self.get_master(i, data=fragment, copy_master=False))

            idx = 0
            for j, _ in enumerate(group["channels"]):
                if j == master_index:
                    continue
                sigs[idx].append(
                    self.get(group=i, index=j, data=fragment, samples_only=True)[0]
                )
                idx += 1

        pandas_dict = {master_name: np.concatenate(master)}

        used_names = UniqueDB()
        used_names.get_unique_name(master_name)
        for name, sig in zip(names, sigs):
            name = used_names.get_unique_name(name)
            pandas_dict[name] = np.concatenate(sig)

        try:
            return DataFrame.from_dict(pandas_dict)
        except:
            debug_channel(self, group, None, None)
            raise

if __name__ == "__main__":
    pass
