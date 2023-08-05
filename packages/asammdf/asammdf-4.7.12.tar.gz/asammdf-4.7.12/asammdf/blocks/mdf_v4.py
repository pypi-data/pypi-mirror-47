"""
ASAM MDF version 4 file format module
"""

from __future__ import division, print_function

import logging
import xml.etree.ElementTree as ET
import os
import sys
from collections import defaultdict
from copy import deepcopy
from functools import reduce
from hashlib import md5
from itertools import chain
from math import ceil
from struct import unpack
from tempfile import TemporaryFile
from zlib import decompress

from numpy import (
    arange,
    array,
    array_equal,
    bool,
    concatenate,
    dtype,
    flip,
    float32,
    float64,
    frombuffer,
    interp,
    linspace,
    nonzero,
    ones,
    packbits,
    roll,
    transpose,
    uint8,
    uint16,
    uint64,
    union1d,
    unpackbits,
    zeros,
    uint32,
    fliplr,
    searchsorted,
    full,
)

from numpy.core.records import fromarrays, fromstring
from canmatrix.formats import loads
from pandas import DataFrame

from . import v4_constants as v4c
from ..signal import Signal
from .conversion_utils import conversion_transfer
from .utils import (
    UINT8_u,
    UINT16_u,
    UINT32_u,
    UINT32_uf,
    UINT64_u,
    FLOAT64_u,
    CHANNEL_COUNT,
    CONVERT_LOW,
    CONVERT_MINIMUM,
    ChannelsDB,
    MdfException,
    SignalSource,
    as_non_byte_sized_signed_int,
    fix_dtype_fields,
    fmt_to_datatype_v4,
    get_fmt_v4,
    UniqueDB,
    get_text_v4,
    debug_channel,
    extract_cncomment_xml,
    validate_memory_argument,
    validate_version_argument,
    count_channel_groups,
    info_to_datatype_v4,
    is_file_like,
    sanitize_xml,
)
from .v4_blocks import (
    AttachmentBlock,
    Channel,
    ChannelArrayBlock,
    ChannelConversion,
    ChannelGroup,
    DataBlock,
    DataGroup,
    DataList,
    DataZippedBlock,
    EventBlock,
    FileHistory,
    FileIdentificationBlock,
    HeaderBlock,
    HeaderList,
    SampleReductionBlock,
    SourceInformation,
    TextBlock,
)
from ..version import __version__


MASTER_CHANNELS = (v4c.CHANNEL_TYPE_MASTER, v4c.CHANNEL_TYPE_VIRTUAL_MASTER)
COMMON_SIZE = v4c.COMMON_SIZE
COMMON_u = v4c.COMMON_u

PYVERSION = sys.version_info[0]
if PYVERSION == 2:
    # pylint: disable=W0622
    from .utils import bytes

    # pylint: enable=W0622

logger = logging.getLogger("asammdf")

__all__ = ["MDF4"]


class MDF4(object):
    """The *header* attibute is a *HeaderBlock*.

    The *groups* attribute is a list of dicts, each one with the following keys:

    * ``data_group`` - DataGroup object
    * ``channel_group`` - ChannelGroup object
    * ``channels`` - list of Channel objects (when *memory* is *full* or *low*) or addresses
      (when *memory* is *minimum*) with the same order as found in the mdf file
    * ``channel_dependencies`` - list of *ChannelArrayBlock* in case of channel arrays;
      list of Channel objects (when *memory* is *full* or *low*) or addresses
      (when *memory* is *minimum*) in case of structure channel composition
    * ``data_block`` - DataBlock object when *memory* is *full* else address of
      data block
    * ``data_location``- integer code for data location (original file, temporary file or
      memory)
    * ``data_block_addr`` - list of raw samples starting addresses, for *low* and *minimum*
      memory options
    * ``data_block_type`` - list of codes for data block type
    * ``data_block_size`` - list of raw samples block size
    * ``sorted`` - sorted indicator flag
    * ``record_size`` - dict that maps record ID's to record sizes in bytes (including invalidation bytes)
    * ``param`` - row size used for tranposizition, in case of tranposed zipped blockss


    Parameters
    ----------
    name : string
        mdf file name (if provided it must be a real file name) or
        file-like object
    memory : str
        memory optimization option; default `full`

        * if *full* the data group binary data block will be memorised in RAM
        * if *low* the channel data is read from disk on request, and the
          metadata is memorized into RAM
        * if *minimum* only minimal data is memorized into RAM

    version : string
        mdf file version ('4.00', '4.10', '4.11'); default '4.10'
    callback : function
        keyword only argument: function to call to update the progress; the
        function must accept two arguments (the current progress and maximum
        progress value)
    use_display_names : bool
        keyword only argument: for MDF4 files parse the XML channel comment to
        search for the display name; XML parsing is quite expensive so setting
        this to *False* can decrease the loading times very much; default
        *False*
    skip_record_preparation : bool
        keyword only argument: only valid if memory='minimum'; this is used to
        optimise the concatenate method


    Attributes
    ----------
    attachments : list
        list of file attachments
    channels_db : dict
        used for fast channel access by name; for each name key the value is a
        list of (group index, channel index) tuples
    events : list
        list event blocks
    file_comment : TextBlock
        file comment TextBlock
    file_history : list
        list of (FileHistory, TextBlock) pairs
    groups : list
        list of data group dicts
    header : HeaderBlock
        mdf file header
    identification : FileIdentificationBlock
        mdf file start block
    masters_db : dict
        used for fast master channel access; for each group index key the value
         is the master channel index
    memory : str
        memory optimization option
    name : string
        mdf file name
    version : str
        mdf version

    """

    _terminate = False

    def __init__(self, name=None, memory="full", version="4.10", **kwargs):
        memory = validate_memory_argument(memory)

        self.groups = []
        self.header = None
        self.identification = None
        self.file_history = []
        self.name = name
        self.memory = memory
        self.channels_db = ChannelsDB()
        self.can_logging_db = {}
        self.masters_db = {}
        self.attachments = []
        self._attachments_cache = {}
        self.file_comment = None
        self.events = []

        self._attachments_map = {}
        self._ch_map = {}
        self._master_channel_cache = {}
        self._master_channel_metadata = {}
        self._invalidation_cache = {}
        self._si_map = {}
        self._file_si_map = {}
        self._cc_map = {}
        self._file_cc_map = {}
        self._cg_map = {}
        self._dbc_cache = {}

        self._tempfile = TemporaryFile()
        self._file = None

        self._read_fragment_size = 0 * 2 ** 20
        self._write_fragment_size = 4 * 2 ** 20
        self._use_display_names = kwargs.get("use_display_names", False)
        self._skip_record_preparation = kwargs.get("skip_record_preparation", False)
        self._single_bit_uint_as_bool = False

        # make sure no appended block has the address 0
        self._tempfile.write(b"\0")

        self._callback = kwargs.get("callback", None)

        if name:
            if is_file_like(name):
                self._file = name
                self.name = "From_FileLike.mf4"
                self._from_filelike = True
            else:
                self._file = open(self.name, "rb")
                self._from_filelike = False
            self._read()

        else:
            self._from_filelike = False
            self.name = "From_Scratch.mf4"
            version = validate_version_argument(version)
            self.header = HeaderBlock()
            self.identification = FileIdentificationBlock(version=version)
            self.version = version

    def _check_finalised(self):
        flags = self.identification["unfinalized_standard_flags"]
        if flags & 1:
            message = (
                "Unfinalised file {}:"
                "Update of cycle counters for CG/CA blocks required"
            )
            message = message.format(self.name)
            logger.warning(message)
        elif flags & 1 << 1:
            message = (
                "Unfinalised file {}:" "Update of cycle counters for SR blocks required"
            )
            message = message.format(self.name)
            logger.warning(message)
        elif flags & 1 << 2:
            message = (
                "Unfinalised file {}:" "Update of length for last DT block required"
            )
            message = message.format(self.name)
            logger.warning(message)
        elif flags & 1 << 3:
            message = (
                "Unfinalised file {}:" "Update of length for last RD block required"
            )
            message = message.format(self.name)
            logger.warning(message)
        elif flags & 1 << 4:
            message = (
                "Unfinalised file {}:"
                "Update of last DL block in each chained list"
                "of DL blocks required"
            )
            message = message.format(self.name)
            logger.warning(message)
        elif flags & 1 << 5:
            message = (
                "Unfinalised file {}:"
                "Update of cg_data_bytes and cg_inval_bytes "
                "in VLSD CG block required"
            )
            message = message.format(self.name)
            logger.warning(message)
        elif flags & 1 << 6:
            message = (
                "Unfinalised file {}:"
                "Update of offset values for VLSD channel required "
                "in case a VLSD CG block is used"
            )
            message = message.format(self.name)
            logger.warning(message)

    def _read(self):

        stream = self._file
        memory = self.memory
        dg_cntr = 0

        cg_count, _ = count_channel_groups(stream)
        if self._callback:
            self._callback(0, cg_count)
        current_cg_index = 0

        self.identification = FileIdentificationBlock(stream=stream)
        version = self.identification["version_str"]
        self.version = version.decode("utf-8").strip(" \n\t\0")

        if self.version >= "4.10":
            self._check_finalised()

        self.header = HeaderBlock(address=0x40, stream=stream)

        # read file history
        fh_addr = self.header["file_history_addr"]
        while fh_addr:
            history_block = FileHistory(address=fh_addr, stream=stream)
            self.file_history.append(history_block)
            fh_addr = history_block["next_fh_addr"]

        # read attachments
        at_addr = self.header["first_attachment_addr"]
        index = 0
        while at_addr:
            at_block = AttachmentBlock(address=at_addr, stream=stream)
            self._attachments_map[at_addr] = index
            self.attachments.append(at_block)
            at_addr = at_block["next_at_addr"]
            index += 1

        # go to first date group and read each data group sequentially
        dg_addr = self.header["first_dg_addr"]

        while dg_addr:
            new_groups = []
            group = DataGroup(address=dg_addr, stream=stream)
            record_id_nr = group["record_id_len"]

            # go to first channel group of the current data group
            cg_addr = group["first_cg_addr"]

            cg_nr = 0

            cg_size = {}

            while cg_addr:
                cg_nr += 1

                grp = {}

                grp["channels"] = []
                grp["logging_channels"] = []
                grp["data_block"] = None
                grp["channel_dependencies"] = []
                grp["signal_data"] = []
                grp["reduction_blocks"] = []
                grp["reduction_data_block"] = []
                if memory == "minimum" and not self._skip_record_preparation:
                    grp["temp_channels"] = []

                # read each channel group sequentially
                block = ChannelGroup(address=cg_addr, stream=stream)
                self._cg_map[cg_addr] = dg_cntr
                channel_group = grp["channel_group"] = block

                grp["record_size"] = cg_size

                if channel_group["flags"] & v4c.FLAG_CG_VLSD:
                    # VLDS flag
                    record_id = channel_group["record_id"]
                    cg_size[record_id] = 0
                elif channel_group["flags"] & v4c.FLAG_CG_BUS_EVENT:
                    bus_type = channel_group.acq_source["bus_type"]
                    if bus_type == v4c.BUS_TYPE_CAN:
                        grp["CAN_logging"] = True
                        message_name = channel_group.acq_name

                        comment = channel_group.acq_source.comment
                        comment_xml = ET.fromstring(comment)
                        common_properties = comment_xml.find(".//common_properties")
                        for e in common_properties:
                            name = e.get("name")
                            if name == "ChannelNo":
                                grp["CAN_id"] = "CAN{}".format(e.text)
                                break

                        if message_name == "CAN_DataFrame":
                            # this is a raw CAN bus logging channel group
                            # it will be later processed to extract all
                            # signals to new groups (one group per CAN message)
                            grp["raw_can"] = True

                        elif message_name in ("CAN_ErrorFrame", "CAN_RemoteFrame"):
                            # for now ignore bus logging flag
                            pass
                        else:
                            comment = channel_group.comment
                            if comment:

                                comment_xml = ET.fromstring(sanitize_xml(comment))
                                can_msg_type = comment_xml.find(".//TX").text
                                if can_msg_type is not None:
                                    can_msg_type = can_msg_type.strip(" \t\r\n")
                                else:
                                    can_msg_type = "CAN_DataFrame"
                                if can_msg_type == "CAN_DataFrame":
                                    common_properties = comment_xml.find(
                                        ".//common_properties"
                                    )
                                    message_id = -1
                                    for e in common_properties:
                                        name = e.get("name")
                                        if name == "MessageID":
                                            message_id = int(e.text)
                                            break

                                    if message_id > 0:
                                        if message_id > 0x80000000:
                                            message_id -= 0x80000000
                                            grp["extended_id"] = True
                                        else:
                                            grp["extended_id"] = False
                                        grp["message_name"] = message_name
                                        grp["message_id"] = message_id

                                else:
                                    message = "Invalid bus logging channel group metadata: {}".format(
                                        comment
                                    )
                                    logger.warning(message)
                            else:
                                message = "Unable to get CAN message information since channel group @{} has no metadata".format(
                                    hex(channel_group.address)
                                )
                                logger.warning(message)
                    else:
                        # only CAN bus logging is supported
                        pass
                    samples_size = channel_group["samples_byte_nr"]
                    inval_size = channel_group["invalidation_bytes_nr"]
                    record_id = channel_group["record_id"]
                    cg_size[record_id] = samples_size + inval_size
                else:

                    samples_size = channel_group["samples_byte_nr"]
                    inval_size = channel_group["invalidation_bytes_nr"]
                    record_id = channel_group["record_id"]
                    cg_size[record_id] = samples_size + inval_size

                if record_id_nr:
                    grp["sorted"] = False
                else:
                    grp["sorted"] = True

                data_group = DataGroup(address=dg_addr, stream=stream)
                grp["data_group"] = data_group

                # go to first channel of the current channel group
                ch_addr = channel_group["first_ch_addr"]
                ch_cntr = 0
                neg_ch_cntr = -1

                # Read channels by walking recursively in the channel group
                # starting from the first channel
                self._read_channels(ch_addr, grp, stream, dg_cntr, ch_cntr, neg_ch_cntr)

                if memory == "minimum" and not self._skip_record_preparation:
                    grp["parents"], grp["types"] = self._prepare_record(grp)
                    del grp["temp_channels"]

                cg_addr = channel_group["next_cg_addr"]
                dg_cntr += 1

                current_cg_index += 1
                if self._callback:
                    self._callback(current_cg_index, cg_count)

                if self._terminate:
                    self.close()
                    return

                new_groups.append(grp)

            # store channel groups record sizes dict in each
            # new group data belong to the initial unsorted group, and add
            # the key 'sorted' with the value False to use a flag;
            # this is used later if memory is 'low' or 'minimum'

            if memory == "full":
                grp["data_location"] = v4c.LOCATION_MEMORY
                dat_addr = group["data_block_addr"]

                if record_id_nr == 0:
                    size = channel_group["samples_byte_nr"]
                    size += channel_group["invalidation_bytes_nr"]
                    size *= channel_group["cycles_nr"]
                else:
                    size = 0
                    for gp in new_groups:
                        cg = gp["channel_group"]
                        if cg["flags"] & v4c.FLAG_CG_VLSD:
                            total_vlsd_bytes = (cg["invalidation_bytes_nr"] << 32) + cg[
                                "samples_byte_nr"
                            ]
                            size += total_vlsd_bytes + cg["cycles_nr"] * (
                                record_id_nr + 4
                            )
                        else:
                            size += (
                                cg["samples_byte_nr"]
                                + record_id_nr
                                + cg["invalidation_bytes_nr"]
                            ) * cg["cycles_nr"]

                data = self._read_data_block(address=dat_addr, stream=stream, size=size)
                data = next(data)

                if record_id_nr == 0:
                    grp = new_groups[0]
                    grp["data_location"] = v4c.LOCATION_MEMORY
                    grp["data_block"] = DataBlock(data=data)

                    info = {
                        "data_block_addr": [],
                        "data_block_type": 0,
                        "data_size": [],
                        "data_block_size": [],
                        "param": 0,
                    }
                    grp.update(info)
                else:
                    cg_data = defaultdict(list)
                    if record_id_nr == 1:
                        _unpack_stuct = UINT8_u
                    elif record_id_nr == 2:
                        _unpack_stuct = UINT16_u
                    elif record_id_nr == 4:
                        _unpack_stuct = UINT32_u
                    elif record_id_nr == 8:
                        _unpack_stuct = UINT64_u
                    else:
                        message = "invalid record id size {}"
                        raise MdfException(message.format(record_id_nr))

                    i = 0
                    while i < size:
                        (rec_id, ) = _unpack_stuct(data[i : i + record_id_nr])
                        # skip record id
                        i += record_id_nr
                        rec_size = cg_size[rec_id]
                        if rec_size:
                            rec_data = data[i : i + rec_size]
                            cg_data[rec_id].append(rec_data)
                        else:
                            (rec_size, ) = UINT32_u(data[i : i + 4])
                            rec_data = data[i : i + rec_size + 4]
                            cg_data[rec_id].append(rec_data)
                            i += 4
                        i += rec_size
                    for grp in new_groups:
                        grp["data_location"] = v4c.LOCATION_MEMORY
                        record_id = grp["channel_group"]["record_id"]
                        data = b"".join(cg_data[record_id])
                        grp["channel_group"]["record_id"] = 1
                        grp["data_block"] = DataBlock(data=data)

                        info = {
                            "data_block_addr": [],
                            "data_block_type": 0,
                            "data_size": [],
                            "data_block_size": [],
                            "param": 0,
                        }
                        grp.update(info)
            else:
                address = group["data_block_addr"]

                info = self._get_data_blocks_info(
                    address=address, stream=stream, block_type=b"##DT"
                )

                for grp in new_groups:
                    grp["data_location"] = v4c.LOCATION_ORIGINAL_FILE
                    grp.update(info)

            # sample reduction blocks
            if memory == "full":
                addr = grp["channel_group"]["first_sample_reduction_addr"]
                while addr:
                    reduction_block = SampleReductionBlock(address=addr, stream=stream)
                    address = reduction_block["data_block_addr"]

                    grp["reduction_blocks"].append(reduction_block)

                    data = self._read_data_block(
                        address=address, stream=stream, size=size
                    )

                    data = next(data)

                    grp["reduction_data_block"].append(DataBlock(data=data, type="RD"))

                    addr = reduction_block["next_sr_addr"]
            else:
                addr = grp["channel_group"]["first_sample_reduction_addr"]

                while addr:

                    reduction_block = SampleReductionBlock(address=addr, stream=stream)
                    address = reduction_block["data_block_addr"]

                    grp["reduction_blocks"].append(reduction_block)

                    grp["reduction_data_block"].append(
                        self._get_data_blocks_info(
                            address=address, stream=stream, block_type=b"##RD"
                        )
                    )

                    addr = reduction_block["next_sr_addr"]

            self.groups.extend(new_groups)

            dg_addr = group["next_dg_addr"]

        # all channels have been loaded so now we can link the
        # channel dependencies and load the signal data for VLSD channels
        for grp in self.groups:
            for dep_list in grp["channel_dependencies"]:
                if not dep_list:
                    continue

                for dep in dep_list:
                    if isinstance(dep, ChannelArrayBlock):
                        conditions = (
                            dep["ca_type"] == v4c.CA_TYPE_LOOKUP,
                            dep["links_nr"] == 4 * dep["dims"] + 1,
                        )
                        if not all(conditions):
                            continue

                        for i in range(dep["dims"]):
                            ch_addr = dep["scale_axis_{}_ch_addr".format(i)]
                            ref_channel = self._ch_map[ch_addr]
                            dep.referenced_channels.append(ref_channel)
                    else:
                        break

            if self.memory == "full":
                sig_data_list = grp["signal_data"]
                for i, signal_data_addr in enumerate(sig_data_list):

                    sig_data_list[i] = self._load_signal_data(
                        address=signal_data_addr, stream=stream
                    )

        # append indexes of groups that contain raw CAN bus logging and
        # store signals and metadata that will be used to create the new
        # groups.
        raw_can = []
        processed_can = []
        for i, group in enumerate(self.groups):
            if group.get("CAN_logging", False):
                if group["CAN_id"] not in self.can_logging_db:
                    self.can_logging_db[group["CAN_id"]] = {}
                message_id = group.get("message_id", None)
                if message_id is not None:
                    self.can_logging_db[group["CAN_id"]][message_id] = i
            else:
                continue

            if group.get("raw_can", False):
                can_ids = self.get(
                    "CAN_DataFrame.ID", group=i, ignore_invalidation_bits=True
                )
                all_can_ids = sorted(set(can_ids.samples))
                payload = self.get(
                    "CAN_DataFrame.DataBytes",
                    group=i,
                    samples_only=True,
                    ignore_invalidation_bits=True,
                )[0]

                _sig = self.get("CAN_DataFrame", group=i, ignore_invalidation_bits=True)

                attachment = _sig.attachment
                if attachment and attachment[1].lower().endswith(("dbc", "arxml")):
                    attachment, at_name = attachment

                    raw_can.append(i)

                    import_type = "dbc" if at_name.lower().endswith("dbc") else "arxml"
                    db = loads(
                        attachment.decode("utf-8"), importType=import_type, key="db"
                    )["db"]

                    board_units = set(bu.name for bu in db.boardUnits)

                    cg_source = group["channel_group"].acq_source

                    for message_id in all_can_ids:
                        self.can_logging_db[group["CAN_id"]][message_id] = i
                        sigs = []
                        can_msg = db.frameById(message_id)

                        for transmitter in can_msg.transmitters:
                            if transmitter in board_units:
                                break
                        else:
                            transmitter = ""
                        message_name = can_msg.name

                        source = SignalSource(
                            transmitter,
                            can_msg.name,
                            "",
                            v4c.SOURCE_BUS,
                            v4c.BUS_TYPE_CAN,
                        )

                        idx = nonzero(can_ids.samples == message_id)[0]
                        data = payload[idx]
                        t = can_ids.timestamps[idx].copy()
                        if can_ids.invalidation_bits is not None:
                            invalidation_bits = can_ids.invalidation_bits[idx]
                        else:
                            invalidation_bits = None

                        for signal in sorted(can_msg.signals, key=lambda x: x.name):

                            sig_vals = self.get_can_signal(
                                "CAN{}.{}.{}".format(
                                    group["CAN_id"], can_msg.name, signal.name
                                ),
                                db=db,
                                ignore_invalidation_bits=True,
                            ).samples

                            conversion = ChannelConversion(
                                a=float(signal.factor),
                                b=float(signal.offset),
                                conversion_type=v4c.CONVERSION_TYPE_LIN,
                            )
                            conversion.unit = signal.unit or ""
                            sigs.append(
                                Signal(
                                    sig_vals,
                                    t,
                                    name=signal.name,
                                    conversion=conversion,
                                    source=source,
                                    unit=signal.unit,
                                    raw=True,
                                    invalidation_bits=invalidation_bits,
                                )
                            )

                        processed_can.append(
                            [sigs, message_id, message_name, cg_source, group["CAN_id"]]
                        )
                else:
                    at_name = attachment[1] if attachment else ""
                    message = 'Expected .dbc or .arxml file as CAN channel attachment but got "{}"'.format(
                        at_name
                    )
                    logger.warning(message)
                    grp["CAN_database"] = False
                    raw_can.append(i)
                    sigs = []
                    cg_source = group["channel_group"].acq_source

                    for message_id in all_can_ids:

                        source = SignalSource(
                            "", "", "", v4c.SOURCE_BUS, v4c.BUS_TYPE_CAN
                        )

                        idx = nonzero(can_ids.samples == message_id)[0]
                        data = payload[idx]
                        t = can_ids.timestamps[idx]
                        if can_ids.invalidation_bits is not None:
                            invalidation_bits = can_ids.invalidation_bits[idx]
                        else:
                            invalidation_bits = None

                        sigs.append(
                            Signal(
                                data,
                                t,
                                name="CAN_DataFrame.DataBytes",
                                source=source,
                                raw=True,
                                invalidation_bits=invalidation_bits,
                            )
                        )
                        processed_can.append(
                            [sigs, message_id, "", cg_source, group["CAN_id"]]
                        )

        # delete the groups that contain raw CAN bus logging and also
        # delete the channel entries from the channels_db. Update data group
        # index for the remaining channel entries. Append new data groups
        if raw_can:
            for index in reversed(raw_can):
                self.groups.pop(index)

            excluded_channels = []
            for name, db_entry in self.channels_db.items():
                new_entry = []
                for i, entry in enumerate(db_entry):
                    new_group_index = entry[0]
                    if new_group_index in raw_can:
                        continue
                    for index in raw_can:
                        if new_group_index > index:
                            new_group_index += 1
                        else:
                            break
                    new_entry.append((new_group_index, entry[1]))
                if new_entry:
                    self.channels_db[name] = new_entry
                else:
                    excluded_channels.append(name)
            for name in excluded_channels:
                del self.channels_db[name]

            for sigs, message_id, message_name, cg_source, can_id in processed_can:
                self.append(
                    sigs, "Extracted from raw CAN bus logging", common_timebase=True
                )
                group = self.groups[-1]
                group["CAN_database"] = message_name != ""
                group["CAN_logging"] = True
                group["CAN_id"] = can_id
                if message_id > 0:
                    if message_id > 0x80000000:
                        message_id -= 0x80000000
                        group["extended_id"] = True
                    else:
                        group["extended_id"] = False
                    group["message_name"] = message_name
                    group["message_id"] = message_id
                group["channel_group"].acq_source = cg_source
                group["data_group"].comment = 'From message {}="{}"'.format(
                    hex(message_id), message_name
                )

        self.can_logging_db = {}

        for i, group in enumerate(self.groups):
            if not group.get("CAN_logging", False):
                continue
            if not group["CAN_id"] in self.can_logging_db:
                self.can_logging_db[group["CAN_id"]] = {}
            if "message_id" in group:
                self.can_logging_db[group["CAN_id"]][group["message_id"]] = i

        # read events
        addr = self.header["first_event_addr"]
        ev_map = {}
        event_index = 0
        while addr:
            event = EventBlock(address=addr, stream=stream)
            event.update_references(self._ch_map, self._cg_map)
            self.events.append(event)
            ev_map[addr] = event_index
            event_index += 1

            addr = event["next_ev_addr"]

        for event in self.events:
            addr = event["parent_ev_addr"]
            if addr:
                event.parent = ev_map[addr]

            addr = event["range_start_ev_addr"]
            if addr:
                event.range_start = ev_map[addr]

        if self.memory == "full":
            self._file.close()

        self._si_map.clear()
        self._ch_map.clear()
        self._cc_map.clear()
        self._master_channel_cache.clear()

        self.progress = cg_count, cg_count

    def _read_channels(
        self,
        ch_addr,
        grp,
        stream,
        dg_cntr,
        ch_cntr,
        neg_ch_cntr,
        channel_composition=False,
    ):

        memory = self.memory
        channels = grp["channels"]
        if memory == "minimum" and not self._skip_record_preparation:
            temp_channels = grp["temp_channels"]

        dependencies = grp["channel_dependencies"]

        composition = []
        composition_dtype = []
        while ch_addr:
            # read channel block and create channel object
            if memory == "minimum":
                channel = Channel(
                    address=ch_addr,
                    stream=stream,
                    cc_map=self._cc_map,
                    si_map=self._si_map,
                    load_metadata=False,
                    at_map=self._attachments_map,
                )
                if not self._skip_record_preparation:
                    temp_channels.append(channel)
                value = ch_addr
                name = get_text_v4(address=channel["name_addr"], stream=stream)

                if self._use_display_names:
                    comment = get_text_v4(
                        address=channel["comment_addr"],
                        stream=stream,
                    )

                    if comment.startswith("<CNcomment"):
                        try:
                            display_name = ET.fromstring(sanitize_xml(comment)).find(
                                ".//names/display"
                            )
                            if display_name is not None:
                                display_name = display_name.text
                        except UnicodeEncodeError:
                            display_name = ""
                    else:
                        display_name = ""
                else:
                    display_name = ""

            else:
                channel = Channel(
                    address=ch_addr,
                    stream=stream,
                    cc_map=self._cc_map,
                    si_map=self._si_map,
                    at_map=self._attachments_map,
                    use_display_names=self._use_display_names,
                )
                value = channel
                display_name = channel.display_name
                name = channel.name

            entry = (dg_cntr, ch_cntr)
            self._ch_map[ch_addr] = entry

            channels.append(value)
            if channel_composition:
                composition.append(entry)

            self.channels_db.add(display_name, entry)
            self.channels_db.add(name, entry)

            # signal data
            address = channel["data_block_addr"]
            grp["signal_data"].append(address)

            if channel["channel_type"] in MASTER_CHANNELS:
                self.masters_db[dg_cntr] = ch_cntr

            ch_cntr += 1

            component_addr = channel["component_addr"]

            if component_addr:
                # check if it is a CABLOCK or CNBLOCK
                stream.seek(component_addr)
                blk_id = stream.read(4)
                if blk_id == b"##CN":
                    index = ch_cntr - 1
                    dependencies.append(None)
                    ch_cntr, neg_ch_cntr, ret_composition, ret_composition_dtype = self._read_channels(
                        component_addr,
                        grp,
                        stream,
                        dg_cntr,
                        ch_cntr,
                        neg_ch_cntr,
                        True,
                    )
                    dependencies[index] = ret_composition
                    channel.dtype_fmt = ret_composition_dtype
                    composition_dtype.append((channel.name, channel.dtype_fmt))
                    if (
                        grp.get("CAN_id", None) is not None
                        and grp.get("message_id", None) is not None
                    ):
                        addr = channel.get("attachment_0_addr", 0)
                        if addr:
                            attachment_addr = self._attachments_map[addr]
                            if attachment_addr not in self._dbc_cache:
                                attachment, at_name = self.extract_attachment(
                                    index=attachment_addr
                                )
                                if (
                                    not at_name.lower().endswith(("dbc", "arxml"))
                                    or not attachment
                                ):
                                    message = 'Expected .dbc or .arxml file as CAN channel attachment but got "{}"'.format(
                                        at_name
                                    )
                                    logger.warning(message)
                                    grp["CAN_database"] = False
                                else:
                                    import_type = (
                                        "dbc"
                                        if at_name.lower().endswith("dbc")
                                        else "arxml"
                                    )
                                    try:
                                        attachment_string = attachment.decode("utf-8")
                                        self._dbc_cache[attachment_addr] = loads(
                                            attachment_string,
                                            importType=import_type,
                                            key="db",
                                        )["db"]
                                        grp["CAN_database"] = True
                                    except UnicodeDecodeError:
                                        try:
                                            from cchardet import detect

                                            encoding = detect(attachment)["encoding"]
                                            attachment_string = attachment.decode(
                                                encoding
                                            )
                                            self._dbc_cache[attachment_addr] = loads(
                                                attachment_string,
                                                importType=import_type,
                                                key="db",
                                                encoding=encoding,
                                            )["db"]
                                            grp["CAN_database"] = True
                                        except ImportError:
                                            message = (
                                                "Unicode exception occured while processing the database "
                                                'attachment "{}" and "cChardet" package is '
                                                'not installed. Mdf version 4 expects "utf-8" '
                                                "strings and this package may detect if a different"
                                                " encoding was used"
                                            ).format(at_name)
                                            logger.warning(message)
                                            grp["CAN_database"] = False
                            else:
                                grp["CAN_database"] = True
                        else:
                            grp["CAN_database"] = False

                        if grp["CAN_database"]:

                            # here we make available multiple ways to refer to
                            # CAN signals by using fake negative indexes for
                            # the channel entries in the channels_db

                            grp["dbc_addr"] = attachment_addr

                            message_id = grp["message_id"]
                            message_name = grp["message_name"]
                            can_id = grp["CAN_id"]

                            can_msg = self._dbc_cache[attachment_addr].frameById(
                                message_id
                            )
                            can_msg_name = can_msg.name

                            for entry in self.channels_db["CAN_DataFrame.DataBytes"]:
                                if entry[0] == dg_cntr:
                                    index = entry[1]
                                    break

                            payload = channels[index]
                            if self.memory == "minimum":
                                payload = Channel(stream=stream, address=payload)

                            logging_channels = grp["logging_channels"]

                            for signal in can_msg.signals:
                                signal_name = signal.name

                                # 0 - name
                                # 1 - message_name.name
                                # 2 - can_id.message_name.name
                                # 3 - can_msg_name.name
                                # 4 - can_id.can_msg_name.name

                                name_ = signal_name
                                little_endian = (
                                    True if signal.is_little_endian else False
                                )
                                signed = signal.is_signed
                                s_type = info_to_datatype_v4(signed, little_endian)
                                bit_offset = signal.startBit % 8
                                byte_offset = signal.startBit // 8
                                bit_count = signal.size
                                comment = signal.comment or ""

                                if (signal.factor, signal.offset) != (1, 0):
                                    conversion = ChannelConversion(
                                        a=float(signal.factor),
                                        b=float(signal.offset),
                                        conversion_type=v4c.CONVERSION_TYPE_LIN,
                                    )
                                    conversion.unit = signal.unit or ""
                                else:
                                    conversion = None

                                kargs = {
                                    "channel_type": v4c.CHANNEL_TYPE_VALUE,
                                    "data_type": s_type,
                                    "sync_type": payload["sync_type"],
                                    "byte_offset": byte_offset + payload["byte_offset"],
                                    "bit_offset": bit_offset,
                                    "bit_count": bit_count,
                                    "min_raw_value": 0,
                                    "max_raw_value": 0,
                                    "lower_limit": 0,
                                    "upper_limit": 0,
                                    "flags": 0,
                                    "pos_invalidation_bit": payload[
                                        "pos_invalidation_bit"
                                    ],
                                }

                                log_channel = Channel(**kargs)
                                log_channel.name = name_
                                log_channel.comment = comment
                                log_channel.source = deepcopy(channel.source)
                                log_channel.conversion = conversion
                                log_channel.unit = signal.unit or ""

                                logging_channels.append(log_channel)

                                entry = dg_cntr, neg_ch_cntr
                                self.channels_db.add(name_, entry)

                                name_ = "{}.{}".format(message_name, signal_name)
                                self.channels_db.add(name_, entry)

                                name_ = "CAN{}.{}.{}".format(
                                    can_id, message_name, signal_name
                                )
                                self.channels_db.add(name_, entry)

                                name_ = "{}.{}".format(can_msg_name, signal_name)
                                self.channels_db.add(name_, entry)

                                name_ = "CAN{}.{}.{}".format(
                                    can_id, can_msg_name, signal_name
                                )
                                self.channels_db.add(name_, entry)

                                neg_ch_cntr -= 1

                            grp["channel_group"][
                                "flags"
                            ] &= ~v4c.FLAG_CG_PLAIN_BUS_EVENT

                else:
                    # only channel arrays with storage=CN_TEMPLATE are
                    # supported so far
                    ca_block = ChannelArrayBlock(
                        address=component_addr, stream=stream
                    )
                    if ca_block["storage"] != v4c.CA_STORAGE_TYPE_CN_TEMPLATE:
                        logger.warning("Only CN template arrays are supported")
                    ca_list = [ca_block]
                    while ca_block["composition_addr"]:
                        ca_block = ChannelArrayBlock(
                            address=ca_block["composition_addr"], stream=stream
                        )
                        ca_list.append(ca_block)
                    dependencies.append(ca_list)

            else:
                dependencies.append(None)
                if channel_composition:
                    channel.dtype_fmt = get_fmt_v4(channel["data_type"], channel["bit_count"], channel["channel_type"])
                    composition_dtype.append((channel.name, channel.dtype_fmt))

            # go to next channel of the current channel group
            ch_addr = channel["next_ch_addr"]

        return ch_cntr, neg_ch_cntr, composition, composition_dtype

    def _read_data_block(self, address, stream, size=-1):
        """read and aggregate data blocks for a given data group

        Returns
        -------
        data : bytes
            aggregated raw data
        """
        count = 0
        if address:
            stream.seek(address)
            id_string = stream.read(4)
            # can be a DataBlock
            if id_string in (b"##DT", b"##RD"):
                data = DataBlock(address=address, stream=stream)
                data = data["data"]
                count += 1
                yield data
            # or a DataZippedBlock
            elif id_string == b"##DZ":
                data = DataZippedBlock(address=address, stream=stream)
                data = data["data"]
                count += 1
                yield data
            # or a DataList
            elif id_string == b"##DL":
                if size >= 0:
                    data = bytearray(size)
                    view = memoryview(data)
                    position = 0
                    while address:
                        dl = DataList(address=address, stream=stream)

                        for i in range(dl["links_nr"] - 1):
                            addr = dl["data_block_addr{}".format(i)]
                            stream.seek(addr)
                            id_string = stream.read(4)
                            if id_string == b"##DT":
                                _, dim, __ = unpack("<4s2Q", stream.read(20))
                                dim -= 24
                                if hasattr(stream, "readinto"):
                                    position += stream.readinto(
                                        view[position : position + dim]
                                    )
                                else:  # Try to fall back to simple read
                                    view[position : position + dim] = stream.read(dim)
                                    position += dim
                            elif id_string == b"##DZ":
                                block = DataZippedBlock(stream=stream, address=addr)
                                uncompressed_size = block["original_size"]
                                view[position : position + uncompressed_size] = block[
                                    "data"
                                ]
                                position += uncompressed_size
                            else:
                                raise MdfException("Expected b'##DT' or b'##DZ' @0x{} but found {}".format(hex(addr), id_string))
                        address = dl["next_dl_addr"]
                    count += 1
                    yield data

                else:
                    while address:
                        dl = DataList(address=address, stream=stream)
                        for i in range(dl["links_nr"] - 1):
                            addr = dl["data_block_addr{}".format(i)]
                            stream.seek(addr)
                            id_string = stream.read(4)
                            if id_string == b"##DT":
                                block = DataBlock(stream=stream, address=addr)
                                count += 1
                                yield block["data"]
                            elif id_string == b"##DZ":
                                block = DataZippedBlock(stream=stream, address=addr)
                                count += 1
                                yield block["data"]
                            elif id_string == b"##DL":
                                for data in self._read_data_block(
                                    address=addr, stream=stream
                                ):
                                    count += 1
                                    yield data
                        address = dl["next_dl_addr"]

            # or a header list
            elif id_string == b"##HL":
                hl = HeaderList(address=address, stream=stream)
                for data in self._read_data_block(
                    address=hl["first_dl_addr"], stream=stream, size=size
                ):
                    count += 1
                    yield data
            if not count:
                yield b""
        else:
            yield b""

    def _load_signal_data(self, address=None, stream=None, group=None, index=None):
        """ this method is used to get the channel signal data, usually for
        VLSD channels

        Parameters
        ----------
        address : int
            address of refrerenced block
        stream : handle
            file IO stream handle

        Returns
        -------
        data : bytes
            signal data bytes

        """

        if address == 0:
            data = b""

        elif address is not None and stream is not None:
            stream.seek(address)
            blk_id = stream.read(4)
            if blk_id == b"##SD":
                data = DataBlock(address=address, stream=stream)
                data = data["data"]
            elif blk_id == b"##DZ":
                data = DataZippedBlock(address=address, stream=stream)
                data = data["data"]
            elif blk_id == b"##CG":
                group = self.groups[self._cg_map[address]]
                data = b"".join(fragment[0] for fragment in self._load_data(group))
            elif blk_id == b"##DL":
                data = []
                while address:
                    # the data list will contain only links to SDBLOCK's
                    data_list = DataList(address=address, stream=stream)
                    nr = data_list["links_nr"]
                    # aggregate data from all SDBLOCK
                    for i in range(nr - 1):
                        addr = data_list["data_block_addr{}".format(i)]
                        stream.seek(addr)
                        blk_id = stream.read(4)
                        if blk_id == b"##SD":
                            block = DataBlock(address=addr, stream=stream)
                            data.append(block["data"])
                        elif blk_id == b"##DZ":
                            block = DataZippedBlock(address=addr, stream=stream)
                            data.append(block["data"])
                        else:
                            message = (
                                "Expected SD, DZ or DL block at {} " 'but found id="{}"'
                            )
                            message = message.format(hex(address), blk_id)
                            logger.warning(message)
                            return b""
                    address = data_list["next_dl_addr"]
                data = b"".join(data)
            elif blk_id == b"##CN":
                data = b""
            elif blk_id == b"##HL":
                hl = HeaderList(address=address, stream=stream)

                data = self._load_signal_data(
                    address=hl["first_dl_addr"], stream=stream, group=group, index=index
                )
            elif blk_id == b"##AT":
                data = b""
            else:
                message = (
                    "Expected AT, CG, SD, DL, DZ or CN block at {} " 'but found id="{}"'
                )
                message = message.format(hex(address), blk_id)
                logger.warning(message)
                data = b""

        elif group is not None and index is not None:
            if group["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
                data = self._load_signal_data(
                    address=group["signal_data"][index], stream=self._file
                )
            elif group["data_location"] == v4c.LOCATION_MEMORY:
                data = group["signal_data"][index]
            else:
                data = []
                stream = self._tempfile
                if group["signal_data"][index]:
                    for addr, size in zip(
                        group["signal_data"][index], group["signal_data_size"][index]
                    ):
                        if not size:
                            continue
                        stream.seek(addr)
                        data.append(stream.read(size))
                data = b"".join(data)
        else:
            data = b""

        return data

    def _load_data(self, group, index=None, record_offset=0, record_count=None):
        """ get group's data block bytes """
        offset = 0
        has_yielded = False
        _count = record_count
        if self.memory == "full":
            if index is None:
                yield group["data_block"]["data"], offset, _count
            else:
                yield group["reduction_blocks"][index]["data"], offset, _count
        else:
            data_group = group["data_group"]
            channel_group = group["channel_group"]

            if group["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
                stream = self._file
            else:
                stream = self._tempfile

            read = stream.read
            seek = stream.seek

            if index is None:
                block_type = group["data_block_type"]
                param = group["param"]
            else:
                block_type = group["reduction_data_block"][index]["data_block_type"]
                param = group["reduction_data_block"][index]["param"]

            if index is None:
                samples_size = (
                    channel_group["samples_byte_nr"]
                    + channel_group["invalidation_bytes_nr"]
                )
            else:
                samples_size = (
                    channel_group["samples_byte_nr"] * 3
                    + channel_group["invalidation_bytes_nr"]
                )

            record_offset *= samples_size

            finished = False
            if record_count is not None:
                record_count *= samples_size

            if not samples_size:
                yield b"", offset, _count
            else:

                if not group["sorted"]:
                    cg_size = group["record_size"]
                    record_id = channel_group["record_id"]
                    if data_group["record_id_len"] <= 2:
                        record_id_nr = data_group["record_id_len"]
                    else:
                        record_id_nr = 0
                else:
                    if self._read_fragment_size:
                        split_size = self._read_fragment_size // samples_size
                        split_size *= samples_size
                    else:
                        channels_nr = len(group["channels"])

                        if self.memory == "minimum":
                            y_axis = CONVERT_MINIMUM
                        else:
                            y_axis = CONVERT_LOW

                        idx = searchsorted(CHANNEL_COUNT, channels_nr, side='right') - 1
                        if idx < 0:
                            idx = 0
                        split_size = y_axis[idx]

                        split_size = split_size // samples_size
                        split_size *= samples_size

                    if split_size == 0:
                        split_size = samples_size

                if index is None:
                    addr = group["data_block_addr"]
                    blocks = zip(
                        group["data_block_addr"],
                        group["data_size"],
                        group["data_block_size"],
                    )
                else:
                    addr = group["reduction_data_block"][index]["data_block_addr"]
                    blocks = zip(
                        group["reduction_data_block"][index]["data_block_addr"],
                        group["reduction_data_block"][index]["data_size"],
                        group["reduction_data_block"][index]["data_block_size"],
                    )

                if addr:
                    if PYVERSION == 2:
                        blocks = iter(blocks)

                    if group["sorted"]:

                        if block_type == v4c.DT_BLOCK:
                            cur_size = 0
                            data = []

                            while True:
                                try:
                                    address, size, block_size = next(blocks)
                                    current_address = address
                                except StopIteration:
                                    break

                                if offset + size < record_offset + 1:
                                    offset += size
                                    continue

                                if offset < record_offset:
                                    delta = record_offset - offset
                                    current_address += delta
                                    size -= delta
                                    offset = record_offset

                                while size >= split_size - cur_size:
                                    seek(current_address)
                                    if data:
                                        data.append(read(split_size - cur_size))
                                        data_ = b"".join(data)
                                        if record_count is not None:
                                            yield data_[:record_count], offset, _count
                                            has_yielded = True
                                            record_count -= len(data_)
                                            if record_count <= 0:
                                                finished = True
                                                break
                                        else:
                                            yield data_, offset, _count
                                            has_yielded = True
                                        current_address += split_size - cur_size
                                    else:
                                        data_ = read(split_size)
                                        if record_count is not None:
                                            yield data_[:record_count], offset, _count
                                            has_yielded = True
                                            record_count -= len(data_)
                                            if record_count <= 0:
                                                finished = True
                                                break
                                        else:
                                            yield data_, offset, _count
                                            has_yielded = True
                                        current_address += split_size
                                    offset += split_size

                                    size -= split_size - cur_size
                                    data = []
                                    cur_size = 0

                                if finished:
                                    data = []
                                    break

                                if size:
                                    seek(current_address)
                                    data.append(read(size))
                                    cur_size += size
                            if data:
                                data_ = b"".join(data)
                                if record_count is not None:
                                    yield data_[:record_count], offset, _count
                                    has_yielded = True
                                    record_count -= len(data_)
                                else:
                                    yield data_, offset, _count
                                    has_yielded = True
                        else:

                            extra_bytes = b""
                            for (address, size, block_size) in blocks:
                                if offset + size < record_offset + 1:
                                    offset += size
                                    continue

                                seek(address)
                                data = read(block_size)

                                if block_type == v4c.DZ_BLOCK_DEFLATE:
                                    data = decompress(data, 0, size)
                                else:
                                    data = decompress(data, 0, size)
                                    cols = param
                                    lines = size // cols

                                    nd = fromstring(data[: lines * cols], dtype=uint8)
                                    nd = nd.reshape((cols, lines))
                                    data = nd.T.tostring() + data[lines * cols:]

                                if offset < record_offset:
                                    delta = record_offset - offset
                                    offset = record_offset
                                    data = data[delta:]

                                if extra_bytes:
                                    data = extra_bytes + data

                                dim = len(data)
                                new_extra_bytes = dim % samples_size
                                if new_extra_bytes:
                                    extra_bytes = data[-new_extra_bytes:]
                                    data = data[:-new_extra_bytes]
                                    offset_increase = dim - new_extra_bytes
                                else:
                                    extra_bytes = b""
                                    offset_increase = dim

                                if record_count is not None:
                                    yield data[:record_count], offset, _count
                                    has_yielded = True
                                    record_count -= len(data)
                                    if record_count <= 0:
                                        finished = True
                                        break
                                else:
                                    yield data, offset, _count
                                    has_yielded = True
                                offset += offset_increase

                            if extra_bytes:
                                if record_count is not None:
                                    if not finished:
                                        yield extra_bytes[:record_count], offset, _count
                                        has_yielded = True
                                else:
                                    yield extra_bytes, offset, _count
                                    has_yielded = True
                    else:
                        for (address, size, block_size) in blocks:
                            seek(address)
                            data = read(block_size)

                            if block_type == v4c.DZ_BLOCK_DEFLATE:
                                data = decompress(data, 0, size)
                            elif block_type == v4c.DZ_BLOCK_TRANSPOSED:
                                data = decompress(data, 0, size)
                                cols = param
                                lines = size // cols

                                nd = fromstring(data[: lines * cols],
                                                dtype=uint8)
                                nd = nd.reshape((cols, lines))
                                data = nd.T.tostring() + data[lines * cols:]

                            rec_data = []

                            cg_size = group["record_size"]
                            record_id = channel_group["record_id"]
                            record_id_nr = data_group["record_id_len"]

                            if record_id_nr == 1:
                                _unpack_stuct = UINT8_u
                            elif record_id_nr == 2:
                                _unpack_stuct = UINT16_u
                            elif record_id_nr == 4:
                                _unpack_stuct = UINT32_u
                            elif record_id_nr == 8:
                                _unpack_stuct = UINT64_u
                            else:
                                message = "invalid record id size {}"
                                message = message.format(record_id_nr)
                                raise MdfException(message)

                            i = 0
                            size = len(data)
                            while i < size:
                                (rec_id, ) = _unpack_stuct(data[i : i + record_id_nr])
                                # skip record id
                                i += record_id_nr
                                rec_size = cg_size[rec_id]
                                if rec_size:
                                    if rec_id == record_id:
                                        rec_data.append(data[i : i + rec_size])
                                else:
                                    (rec_size, ) = UINT32_u(data[i : i + 4])
                                    if rec_id == record_id:
                                        rec_data.append(data[i : i + 4 + rec_size])
                                    i += 4
                                i += rec_size
                            rec_data = b"".join(rec_data)

                            size = len(rec_data)

                            if size:

                                if offset + size < record_offset + 1:
                                    offset += size
                                    continue

                                if offset < record_offset:
                                    delta = record_offset - offset
                                    size -= delta
                                    offset = record_offset

                                if record_count is not None:
                                    yield rec_data[:record_count], offset, _count
                                    has_yielded = True
                                    record_count -= len(rec_data)
                                    if record_count <= 0:
                                        finished = True
                                        break
                                else:
                                    yield rec_data, offset, _count
                                    has_yielded = True
                                offset += size

                    if not has_yielded:
                        yield b"", 0, _count
                else:
                    yield b"", offset, _count

    def _prepare_record(self, group):
        """ compute record dtype and parents dict fro this group

        Parameters
        ----------
        group : dict
            MDF group dict

        Returns
        -------
        parents, dtypes : dict, numpy.dtype
            mapping of channels to records fields, records fields dtype

        """
        try:
            parents, dtypes = group["parents"], group["types"]
        except KeyError:

            grp = group
            stream = self._file
            memory = self.memory
            channel_group = grp["channel_group"]
            if memory == "minimum":
                channels = grp["temp_channels"]
            else:
                channels = grp["channels"]

            record_size = channel_group["samples_byte_nr"]
            invalidation_bytes_nr = channel_group["invalidation_bytes_nr"]
            next_byte_aligned_position = 0
            types = []
            current_parent = ""
            parent_start_offset = 0
            parents = {}
            group_channels = UniqueDB()

            neg_index = -1

            sortedchannels = sorted(enumerate(channels), key=lambda i: i[1])
            for original_index, new_ch in sortedchannels:

                start_offset = new_ch["byte_offset"]
                bit_offset = new_ch["bit_offset"]
                data_type = new_ch["data_type"]
                bit_count = new_ch["bit_count"]
                ch_type = new_ch["channel_type"]
                dependency_list = grp["channel_dependencies"][original_index]
                if memory == "minimum":
                    name = get_text_v4(address=new_ch["name_addr"], stream=stream)
                else:
                    name = new_ch.name

                # handle multiple occurance of same channel name
                name = group_channels.get_unique_name(name)

                if start_offset >= next_byte_aligned_position:
                    if ch_type not in v4c.VIRTUAL_TYPES:
                        if not dependency_list:
                            parent_start_offset = start_offset

                            # check if there are byte gaps in the record
                            gap = parent_start_offset - next_byte_aligned_position
                            if gap:
                                types.append(("", "a{}".format(gap)))

                            # adjust size to 1, 2, 4 or 8 bytes
                            size = bit_offset + bit_count
                            if data_type not in v4c.NON_SCALAR_TYPES:
                                if size > 32:
                                    size = 8
                                elif size > 16:
                                    size = 4
                                elif size > 8:
                                    size = 2
                                else:
                                    size = 1
                            else:
                                size = size >> 3

                            next_byte_aligned_position = parent_start_offset + size
                            bit_count = size * 8
                            if next_byte_aligned_position <= record_size:
                                if not new_ch.dtype_fmt:
                                    new_ch.dtype_fmt = get_fmt_v4(data_type, bit_count, ch_type)
                                dtype_pair = (
                                    name,
                                    new_ch.dtype_fmt,
                                )
                                types.append(dtype_pair)
                                parents[original_index] = name, bit_offset
                            else:
                                next_byte_aligned_position = parent_start_offset

                            current_parent = name
                        else:
                            if isinstance(dependency_list[0], ChannelArrayBlock):
                                ca_block = dependency_list[0]

                                # check if there are byte gaps in the record
                                gap = start_offset - next_byte_aligned_position
                                if gap:
                                    dtype_pair = "", "a{}".format(gap)
                                    types.append(dtype_pair)

                                size = max(bit_count >> 3, 1)
                                shape = tuple(
                                    ca_block["dim_size_{}".format(i)]
                                    for i in range(ca_block["dims"])
                                )

                                if (
                                    ca_block["byte_offset_base"] // size > 1
                                    and len(shape) == 1
                                ):
                                    shape += (ca_block["byte_offset_base"] // size,)
                                dim = 1
                                for d in shape:
                                    dim *= d

                                if not new_ch.dtype_fmt:
                                    new_ch.dtype_fmt = get_fmt_v4(data_type, bit_count)
                                dtype_pair = (
                                    name,
                                    new_ch.dtype_fmt,
                                    shape,
                                )
                                types.append(dtype_pair)

                                current_parent = name
                                next_byte_aligned_position = start_offset + size * dim
                                parents[original_index] = name, 0

                            else:
                                parents[original_index] = None, None
                                if channel_group["flags"] & v4c.FLAG_CG_BUS_EVENT:
                                    for logging_channel in grp["logging_channels"]:
                                        parents[neg_index] = (
                                            "CAN_DataFrame.DataBytes",
                                            logging_channel["bit_offset"],
                                        )
                                        neg_index -= 1

                    # virtual channels do not have bytes in the record
                    else:
                        parents[original_index] = None, None

                else:
                    max_overlapping_size = (
                        next_byte_aligned_position - start_offset
                    ) * 8
                    needed_size = bit_offset + bit_count
                    if max_overlapping_size >= needed_size:
                        parents[original_index] = (
                            current_parent,
                            ((start_offset - parent_start_offset) << 3) + bit_offset,
                        )
                if next_byte_aligned_position > record_size:
                    break

            gap = record_size - next_byte_aligned_position
            if gap > 0:
                dtype_pair = "", "a{}".format(gap)
                types.append(dtype_pair)

            dtype_pair = "invalidation_bytes", "<u1", (invalidation_bytes_nr,)
            types.append(dtype_pair)
            if PYVERSION == 2:
                types = fix_dtype_fields(types, "utf-8")
                parents_ = {}
                for key, (name, offset) in parents.items():
                    if isinstance(name, unicode):
                        parents_[key] = name.encode("utf-8"), offset
                    else:
                        parents_[key] = name, offset
                parents = parents_

            dtypes = dtype(types)

        return parents, dtypes

    def _append_structure_composition(
        self,
        grp,
        signal,
        field_names,
        offset,
        dg_cntr,
        ch_cntr,
        parents,
        defined_texts,
        invalidation_bytes_nr,
        inval_bits,
        inval_cntr,
    ):

        si_map = self._si_map
        file_si_map = self._file_si_map
        cc_map = self._cc_map
        file_cc_map = self._file_cc_map

        fields = []
        types = []

        canopen_time_fields = ("ms", "days")
        canopen_date_fields = (
            "ms",
            "min",
            "hour",
            "day",
            "month",
            "year",
            "summer_time",
            "day_of_week",
        )

        memory = self.memory
        file = self._tempfile
        seek = file.seek
        seek(0, 2)

        gp = grp
        gp_sdata = gp["signal_data"]
        gp_sdata_size = gp["signal_data_size"]
        gp_channels = gp["channels"]
        gp_dep = gp["channel_dependencies"]

        name = signal.name
        names = signal.samples.dtype.names

        field_name = field_names.get_unique_name(name)

        # first we add the structure channel

        if signal.attachment:
            at_data, at_name = signal.attachment
            attachment_addr = self.attach(at_data, at_name, mime="application/x-dbc")
        else:
            attachment_addr = 0

        # add channel block
        kargs = {
            "channel_type": v4c.CHANNEL_TYPE_VALUE,
            "bit_count": signal.samples.dtype.itemsize * 8,
            "byte_offset": offset,
            "bit_offset": 0,
            "data_type": v4c.DATA_TYPE_BYTEARRAY,
            "precision": 255,
            "flags": 0,
        }
        if attachment_addr:
            kargs["attachment_0_addr"] = attachment_addr
            kargs["flags"] |= v4c.FLAG_CN_BUS_EVENT
        if invalidation_bytes_nr and signal.invalidation_bits is not None:
            inval_bits.append(signal.invalidation_bits)
            kargs["flags"] |= v4c.FLAG_CN_INVALIDATION_PRESENT
            kargs["pos_invalidation_bit"] = inval_cntr
            inval_cntr += 1

        ch = Channel(**kargs)
        ch.name = name
        ch.unit = signal.unit
        ch.comment = signal.comment
        ch.display_name = signal.display_name

        # source for channel
        source = signal.source
        if source:
            if source in si_map:
                ch.source = si_map[source]
            else:
                new_source = SourceInformation(
                    source_type=source.source_type,
                    bus_type=source.bus_type,
                )
                new_source.name = source.name
                new_source.path = source.path
                new_source.comment = source.comment

                si_map[source] = new_source

                ch.source = new_source

        entry = dg_cntr, ch_cntr
        if memory != "minimum":
            gp_channels.append(ch)
            struct_self = entry
        else:
            ch.to_stream(file, defined_texts, file_cc_map, file_si_map)
            gp_channels.append(ch.address)
            struct_self = entry

        gp_sdata.append(None)
        gp_sdata_size.append(0)
        self.channels_db.add(name, entry)
        self.channels_db.add(ch.display_name, entry)

        # update the parents as well
        parents[ch_cntr] = name, 0

        ch_cntr += 1

        dep_list = []
        gp_dep.append(dep_list)

        # then we add the fields

        for name in names:
            field_name = field_names.get_unique_name(name)

            samples = signal.samples[name]
            fld_names = samples.dtype.names

            if fld_names is None:
                sig_type = v4c.SIGNAL_TYPE_SCALAR
                if samples.dtype.kind in "SV":
                    sig_type = v4c.SIGNAL_TYPE_STRING
            else:
                if fld_names in (canopen_time_fields, canopen_date_fields):
                    sig_type = v4c.SIGNAL_TYPE_CANOPEN
                elif fld_names[0] != name:
                    sig_type = v4c.SIGNAL_TYPE_STRUCTURE_COMPOSITION
                else:
                    sig_type = v4c.SIGNAL_TYPE_ARRAY

            if sig_type == v4c.SIGNAL_TYPE_SCALAR:

                s_type, s_size = fmt_to_datatype_v4(samples.dtype, samples.shape)
                byte_size = s_size >> 3

                fields.append(samples)
                types.append((field_name, samples.dtype, samples.shape[1:]))

                # add channel block
                kargs = {
                    "channel_type": v4c.CHANNEL_TYPE_VALUE,
                    "bit_count": s_size,
                    "byte_offset": offset,
                    "bit_offset": 0,
                    "data_type": s_type,
                    "flags": 0,
                }

                if attachment_addr:
                    kargs["flags"] |= v4c.FLAG_CN_BUS_EVENT

                if invalidation_bytes_nr:
                    if signal.invalidation_bits is not None:
                        inval_bits.append(signal.invalidation_bits)
                        kargs["flags"] |= v4c.FLAG_CN_INVALIDATION_PRESENT
                        kargs["pos_invalidation_bit"] = inval_cntr
                        inval_cntr += 1

                ch = Channel(**kargs)
                ch.name = name

                entry = (dg_cntr, ch_cntr)
                if memory != "minimum":
                    gp_channels.append(ch)
                    dep_list.append(entry)
                else:
                    ch.to_stream(file, defined_texts, file_cc_map, file_si_map)
                    gp_channels.append(ch.address)
                    dep_list.append(entry)

                offset += byte_size

                gp_sdata.append(None)
                gp_sdata_size.append(0)
                self.channels_db.add(name, entry)
                self.channels_db.add(ch.display_name, entry)

                # update the parents as well
                parents[ch_cntr] = field_name, 0

                ch_cntr += 1
                gp_dep.append(None)

            elif sig_type == v4c.SIGNAL_TYPE_STRUCTURE_COMPOSITION:
                struct = Signal(
                    samples,
                    samples,
                    name=name,
                    invalidation_bits=signal.invalidation_bits,
                )
                offset, dg_cntr, ch_cntr, sub_structure, new_fields, new_types, inval_cntr = self._append_structure_composition(
                    grp,
                    struct,
                    field_names,
                    offset,
                    dg_cntr,
                    ch_cntr,
                    parents,
                    defined_texts,
                    invalidation_bytes_nr,
                    inval_bits,
                    inval_cntr,
                )
                dep_list.append(sub_structure)
                fields.extend(new_fields)
                types.extend(new_types)

        return offset, dg_cntr, ch_cntr, struct_self, fields, types, inval_cntr

    def _get_not_byte_aligned_data(self, data, group, ch_nr):
        big_endian_types = (
            v4c.DATA_TYPE_UNSIGNED_MOTOROLA,
            v4c.DATA_TYPE_REAL_MOTOROLA,
            v4c.DATA_TYPE_SIGNED_MOTOROLA,
        )

        record_size = group["channel_group"]["samples_byte_nr"] + group["channel_group"]["invalidation_bytes_nr"]

        if ch_nr >= 0:
            if self.memory == "minimum":
                if group["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
                    channel = Channel(
                        address=group["channels"][ch_nr],
                        stream=self._file,
                        load_metadata=False,
                    )
                else:
                    channel = Channel(
                        address=group["channels"][ch_nr],
                        stream=self._tempfile,
                        load_metadata=False,
                    )
            else:
                channel = group["channels"][ch_nr]
        else:
            channel = group["logging_channels"][-ch_nr - 1]

        bit_offset = channel["bit_offset"]
        byte_offset = channel["byte_offset"]
        bit_count = channel["bit_count"]

        dependencies = group["channel_dependencies"][ch_nr]
        if dependencies and isinstance(dependencies[0], ChannelArrayBlock):
            ca_block = dependencies[0]

            size = bit_count >> 3
            shape = tuple(
                ca_block["dim_size_{}".format(i)] for i in range(ca_block["dims"])
            )
            if ca_block["byte_offset_base"] // size > 1 and len(shape) == 1:
                shape += (ca_block["byte_offset_base"] // size,)
            dim = 1
            for d in shape:
                dim *= d
            size *= dim
            bit_count = size << 3

        byte_count = bit_offset + bit_count
        if byte_count % 8:
            byte_count = (byte_count >> 3) + 1
        else:
            byte_count >>= 3

        types = [
            ("", "a{}".format(byte_offset)),
            ("vals", "({},)u1".format(byte_count)),
            ("", "a{}".format(record_size - byte_count - byte_offset)),
        ]

        vals = fromstring(data, dtype=dtype(types))

        vals = vals["vals"]

        if channel["data_type"] not in big_endian_types:
            vals = flip(vals, 1)

        vals = unpackbits(vals)
        vals = roll(vals, bit_offset)
        vals = vals.reshape((len(vals) // 8, 8))
        vals = packbits(vals)
        vals = vals.reshape((len(vals) // byte_count, byte_count))

        if bit_count < 64:
            mask = 2 ** bit_count - 1
            masks = []
            while mask:
                masks.append(mask & 0xFF)
                mask >>= 8
            for i in range(byte_count - len(masks)):
                masks.append(0)

            masks = masks[::-1]
            for i, mask in enumerate(masks):
                vals[:, i] &= mask

        if channel["data_type"] not in big_endian_types:
            vals = flip(vals, 1)

        if bit_count <= 8:
            size = 1
        elif bit_count <= 16:
            size = 2
        elif bit_count <= 32:
            size = 4
        elif bit_count <= 64:
            size = 8
        else:
            size = bit_count // 8

        if size > byte_count:
            extra_bytes = size - byte_count
            extra = zeros((len(vals), extra_bytes), dtype=uint8)

            types = [
                ("vals", vals.dtype, vals.shape[1:]),
                ("", extra.dtype, extra.shape[1:]),
            ]
            vals = fromarrays([vals, extra], dtype=dtype(types))

        vals = vals.tostring()

        channel.dtype_fmt = get_fmt_v4(channel["data_type"], bit_count)

        fmt = channel.dtype_fmt
        if size <= byte_count:
            if channel["data_type"] in big_endian_types:
                types = [("", "a{}".format(byte_count - size)), ("vals", fmt)]
            else:
                types = [("vals", fmt), ("", "a{}".format(byte_count - size))]
        else:
            types = [("vals", fmt)]

        vals = fromstring(vals, dtype=dtype(types))["vals"]

        if channel["data_type"] in v4c.SIGNED_INT:
            return as_non_byte_sized_signed_int(vals, bit_count)
        else:
            return vals

    def _validate_channel_selection(
        self, name=None, group=None, index=None, source=None
    ):
        """Gets channel comment.
        Channel can be specified in two ways:

        * using the first positional argument *name*

            * if there are multiple occurrences for this channel then the
            *group* and *index* arguments can be used to select a specific
            group.
            * if there are multiple occurrences for this channel and either the
            *group* or *index* arguments is None then a warning is issued

        * using the group number (keyword argument *group*) and the channel
        number (keyword argument *index*). Use *info* method for group and
        channel numbers


        If the *raster* keyword argument is not *None* the output is
        interpolated accordingly.

        Parameters
        ----------
        name : string
            name of channel
        group : int
            0-based group index
        index : int
            0-based channel index

        Returns
        -------
        group_index, channel_index : (int, int)
            selected channel's group and channel index

        """
        suppress = True
        if name is None:
            if group is None or index is None:
                message = (
                    "Invalid arguments for channel selection: "
                    'must give "name" or, "group" and "index"'
                )
                raise MdfException(message)
            else:
                gp_nr, ch_nr = group, index
                if ch_nr >= 0:
                    try:
                        grp = self.groups[gp_nr]
                    except IndexError:
                        raise MdfException("Group index out of range")

                    try:
                        grp["channels"][ch_nr]
                    except IndexError:
                        raise MdfException("Channel index out of range")
        else:
            if name not in self.channels_db:
                raise MdfException('Channel "{}" not found'.format(name))
            else:
                if source is not None:
                    for gp_nr, ch_nr in self.channels_db[name]:
                        source_name = self._get_source_name(gp_nr, ch_nr)
                        if source_name == source:
                            break
                    else:
                        raise MdfException(
                            "{} with source {} not found".format(name, source)
                        )
                elif group is None:

                    gp_nr, ch_nr = self.channels_db[name][0]
                    if len(self.channels_db[name]) > 1 and not suppress:
                        message = (
                            'Multiple occurances for channel "{}". '
                            "Using first occurance from data group {}. "
                            'Provide both "group" and "index" arguments'
                            " to select another data group"
                        )
                        message = message.format(name, gp_nr)
                        logger.warning(message)

                else:
                    if index is not None and index < 0:
                        gp_nr = group
                        ch_nr = index
                    else:
                        for gp_nr, ch_nr in self.channels_db[name]:
                            if gp_nr == group:
                                if index is None:
                                    break
                                elif index == ch_nr:
                                    break
                        else:
                            if index is None:
                                message = 'Channel "{}" not found in group {}'
                                message = message.format(name, group)
                            else:
                                message = (
                                    'Channel "{}" not found in group {} ' "at index {}"
                                )
                                message = message.format(name, group, index)
                            raise MdfException(message)

        return gp_nr, ch_nr

    def _get_source_name(self, group, index):
        grp = self.groups[group]
        if self.memory == "minimum":
            if grp["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
                stream = self._file
            else:
                stream = self._tempfile

            if index >= 0:
                channel = Channel(address=grp["channels"][index], stream=stream)
                if channel.source:
                    name = channel.source.name
                else:
                    name = ""
            else:
                name = ""
        else:
            if grp["channels"][index].source:
                name = grp["channels"][index].source.name
            else:
                name = ""
        return name

    def _get_data_blocks_info(self, address, stream, block_type=b"##DT"):
        info = {
            "data_block_addr": [],
            "data_block_type": 0,
            "data_size": [],
            "data_block_size": [],
            "param": 0,
        }

        # for low and minimum options save each block's type,
        # address and size

        if address:
            stream.seek(address)
            id_string, _, block_len, __ = COMMON_u(stream.read(COMMON_SIZE))

            # can be a DataBlock
            if id_string == block_type:
                size = block_len - 24
                if size:
                    info["data_size"].append(size)
                    info["data_block_size"].append(size)
                    info["data_block_addr"].append(address + COMMON_SIZE)
                    info["data_block_type"] = v4c.DT_BLOCK
            # or a DataZippedBlock
            elif id_string == b"##DZ":
                stream.seek(address)

                temp = {}
                (
                    temp["id"],
                    temp["reserved0"],
                    temp["block_len"],
                    temp["links_nr"],
                    temp["original_type"],
                    temp["zip_type"],
                    temp["reserved1"],
                    temp["param"],
                    temp["original_size"],
                    temp["zip_size"],
                ) = unpack(v4c.FMT_DZ_COMMON, stream.read(v4c.DZ_COMMON_SIZE))

                if temp["original_size"]:
                    info["data_size"].append(temp["original_size"])
                    info["data_block_size"].append(temp["zip_size"])
                    info["data_block_addr"].append(address + v4c.DZ_COMMON_SIZE)
                    if temp["zip_type"] == v4c.FLAG_DZ_DEFLATE:
                        info["data_block_type"] = v4c.DZ_BLOCK_DEFLATE
                    else:
                        info["data_block_type"] = v4c.DZ_BLOCK_TRANSPOSED
                        info["param"] = temp["param"]

            # or a DataList
            elif id_string == b"##DL":
                info["data_block_type"] = v4c.DT_BLOCK
                while address:
                    dl = DataList(address=address, stream=stream)
                    for i in range(dl["data_block_nr"]):
                        addr = dl["data_block_addr{}".format(i)]
                        stream.seek(addr + 8)
                        (size, ) = UINT64_u(stream.read(8))
                        size -= COMMON_SIZE
                        if size:
                            info["data_block_addr"].append(addr + COMMON_SIZE)
                            info["data_size"].append(size)
                            info["data_block_size"].append(size)
                    address = dl["next_dl_addr"]
            # or a header list
            elif id_string == b"##HL":
                hl = HeaderList(address=address, stream=stream)
                if hl["zip_type"] == v4c.FLAG_DZ_DEFLATE:
                    info["data_block_type"] = v4c.DZ_BLOCK_DEFLATE
                else:
                    info["data_block_type"] = v4c.DZ_BLOCK_TRANSPOSED

                address = hl["first_dl_addr"]
                while address:
                    dl = DataList(address=address, stream=stream)
                    for i in range(dl["data_block_nr"]):
                        addr = dl["data_block_addr{}".format(i)]

                        stream.seek(addr + 28)
                        param, size, zip_size = unpack("<I2Q", stream.read(20))
                        if size:
                            info["data_block_addr"].append(addr + v4c.DZ_COMMON_SIZE)
                            info["data_size"].append(size)
                            info["data_block_size"].append(zip_size)
                            info["param"] = param

                    address = dl["next_dl_addr"]

        return info

    def get_invalidation_bits(self, group_index, channel, fragment):
        """ get invalidation indexes for the channel

        Parameters
        ----------
        group_index : int
            group index
        channel : Channel
            channel object
        fragment : (bytes, int)
            (fragment bytes, fragment offset)

        Returns
        -------
        invalidation_bits : iterable
            iterable of valid channel indexes; if all are valid `None` is
            returned

        """
        group = self.groups[group_index]
        dtypes = group["types"]
        invalidation_size = group["channel_group"]["invalidation_bytes_nr"]

        data_bytes, offset, _count = fragment
        try:
            invalidation = self._invalidation_cache[(group_index, offset, _count)]
        except KeyError:
            not_found = object()
            record = group.get("record", not_found)
            if record is not_found:
                if dtypes.itemsize:
                    record = fromstring(data_bytes, dtype=dtypes)
                else:
                    record = None

            invalidation = record["invalidation_bytes"].tostring()
            self._invalidation_cache[(group_index, offset, _count)] = invalidation

        ch_invalidation_pos = channel["pos_invalidation_bit"]
        pos_byte, pos_offset = divmod(ch_invalidation_pos, 8)

        rec = fromstring(
            invalidation,
            dtype=[
                ("", "V{}".format(pos_byte)),
                ("vals", "<u1"),
                ("", "V{}".format(invalidation_size - pos_byte - 1)),
            ],
        )

        mask = 1 << pos_offset

        invalidation_bits = rec["vals"] & mask
        invalidation_bits = invalidation_bits

        return invalidation_bits

    def configure(
        self,
        read_fragment_size=None,
        write_fragment_size=None,
        use_display_names=None,
        single_bit_uint_as_bool=None,
    ):
        """ configure read and write fragment size for chuncked
        data access

        Parameters
        ----------
        read_fragment_size : int
            size hint of split data blocks, default 8MB; if the initial size is
            smaller, then no data list is used. The actual split size depends on
            the data groups' records size
        write_fragment_size : int
            size hint of split data blocks, default 4MB; if the initial size is
            smaller, then no data list is used. The actual split size depends on
            the data groups' records size. Maximum size is 4MB to ensure
            compatibility with CANape

        """

        if read_fragment_size is not None:
            self._read_fragment_size = int(read_fragment_size)

        if write_fragment_size:
            self._write_fragment_size = min(int(write_fragment_size), 4 * 2 ** 20)

        if use_display_names is not None:
            self._use_display_names = bool(use_display_names)

        if single_bit_uint_as_bool is not None:
            self._single_bit_uint_as_bool = bool(single_bit_uint_as_bool)

    def append(self, signals, source_info="Python", common_timebase=False, units=None):
        """
        Appends a new data group.

        For channel dependencies type Signals, the *samples* attribute must be
        a numpy.recarray

        Parameters
        ----------
        signals : list | Signal | pandas.DataFrame
            list of *Signal* objects, or a single *Signal* object, or a pandas
            *DataFrame* object. All bytes columns in the pandas *DataFrame*
            must be *utf-8* encoded
        source_info : str
            source information; default 'Python'
        common_timebase : bool
            flag to hint that the signals have the same timebase. Only set this
            if you know for sure that all appended channels share the same
            time base
        units : dict
            will contain the signal units mapped to the singal names when
            appending a pandas DataFrame

        Examples
        --------
        >>> # case 1 conversion type None
        >>> s1 = np.array([1, 2, 3, 4, 5])
        >>> s2 = np.array([-1, -2, -3, -4, -5])
        >>> s3 = np.array([0.1, 0.04, 0.09, 0.16, 0.25])
        >>> t = np.array([0.001, 0.002, 0.003, 0.004, 0.005])
        >>> names = ['Positive', 'Negative', 'Float']
        >>> units = ['+', '-', '.f']
        >>> info = {}
        >>> s1 = Signal(samples=s1, timstamps=t, unit='+', name='Positive')
        >>> s2 = Signal(samples=s2, timstamps=t, unit='-', name='Negative')
        >>> s3 = Signal(samples=s3, timstamps=t, unit='flts', name='Floats')
        >>> mdf = MDF4('new.mdf')
        >>> mdf.append([s1, s2, s3], 'created by asammdf v4.0.0')
        >>> # case 2: VTAB conversions from channels inside another file
        >>> mdf1 = MDF4('in.mf4')
        >>> ch1 = mdf1.get("Channel1_VTAB")
        >>> ch2 = mdf1.get("Channel2_VTABR")
        >>> sigs = [ch1, ch2]
        >>> mdf2 = MDF4('out.mf4')
        >>> mdf2.append(sigs, 'created by asammdf v4.0.0')
        >>> mdf2.append(ch1, 'just a single channel')
        >>> df = pd.DataFrame.from_dict({'s1': np.array([1, 2, 3, 4, 5]), 's2': np.array([-1, -2, -3, -4, -5])})
        >>> units = {'s1': 'V', 's2': 'A'}
        >>> mdf2.append(df, units=units)

        """
        if isinstance(signals, Signal):
            signals = [signals]
        elif isinstance(signals, DataFrame):
            self._append_dataframe(signals, source_info, units=units)
            return

        # check if the signals have a common timebase
        # if not interpolate the signals using the union of all timbases
        if signals:
            t_ = signals[0].timestamps
            if not common_timebase:
                for s in signals[1:]:
                    if not array_equal(s.timestamps, t_):
                        different = True
                        break
                else:
                    different = False

                if different:
                    times = [s.timestamps for s in signals]
                    t = reduce(union1d, times).flatten().astype(float64)
                    signals = [s.interp(t) for s in signals]
                    times = None
                else:
                    t = t_
            else:
                t = t_
        else:
            t = []

        canopen_time_fields = ("ms", "days")
        canopen_date_fields = (
            "ms",
            "min",
            "hour",
            "day",
            "month",
            "year",
            "summer_time",
            "day_of_week",
        )

        dg_cntr = len(self.groups)

        gp = {}
        gp["signal_data"] = gp_sdata = []
        gp["signal_data_size"] = gp_sdata_size = []
        gp["channels"] = gp_channels = []
        gp["channel_dependencies"] = gp_dep = []
        gp["signal_types"] = gp_sig_types = []
        gp["logging_channels"] = []

        # channel group
        kargs = {"cycles_nr": 0, "samples_byte_nr": 0}
        gp["channel_group"] = ChannelGroup(**kargs)
        gp["channel_group"].name = source_info

        if any(sig.invalidation_bits is not None for sig in signals):
            invalidation_bytes_nr = 1
            gp["channel_group"]["invalidation_bytes_nr"] = invalidation_bytes_nr

            inval_bits = []

        else:
            invalidation_bytes_nr = 0
            inval_bits = []
        inval_cntr = 0

        self.groups.append(gp)

        cycles_nr = len(t)
        fields = []
        types = []
        parents = {}
        ch_cntr = 0
        offset = 0
        field_names = UniqueDB()

        defined_texts = {}
        si_map = self._si_map
        file_si_map = self._file_si_map
        cc_map = self._cc_map
        file_cc_map = self._file_cc_map

        # setup all blocks related to the time master channel

        memory = self.memory
        file = self._tempfile
        write = file.write
        tell = file.tell
        seek = file.seek

        seek(0, 2)

        if signals:
            master_metadata = signals[0].master_metadata
        else:
            master_metadata = None
        if master_metadata:
            time_name, sync_type = master_metadata
            if sync_type in (0, 1):
                time_unit = "s"
            elif sync_type == 2:
                time_unit = "deg"
            elif sync_type == 3:
                time_unit = "m"
            elif sync_type == 4:
                time_unit = "index"
        else:
            time_name, sync_type = "time", v4c.SYNC_TYPE_TIME
            time_unit = "s"

        source_block = SourceInformation()
        source_block.name = source_block.path = source_info

        if signals:
            # time channel
            t_type, t_size = fmt_to_datatype_v4(t.dtype, t.shape)
            kargs = {
                "channel_type": v4c.CHANNEL_TYPE_MASTER,
                "data_type": t_type,
                "sync_type": sync_type,
                "byte_offset": 0,
                "bit_offset": 0,
                "bit_count": t_size,
            }

            ch = Channel(**kargs)
            ch.unit = time_unit
            ch.name = time_name
            ch.source = source_block
            name = time_name

            if memory == "minimum":
                ch.to_stream(file, defined_texts, file_cc_map, file_si_map)
                gp_channels.append(ch.address)
            else:
                gp_channels.append(ch)

            gp_sdata.append(None)
            gp_sdata_size.append(0)
            self.channels_db.add(name, (dg_cntr, ch_cntr))
            self.masters_db[dg_cntr] = 0
            # data group record parents
            parents[ch_cntr] = name, 0

            # time channel doesn't have channel dependencies
            gp_dep.append(None)

            fields.append(t)
            types.append((name, t.dtype))
            field_names.get_unique_name(name)

            offset += t_size // 8
            ch_cntr += 1

            gp_sig_types.append(0)

        for signal in signals:
            sig = signal
            samples = sig.samples
            sig_dtype = samples.dtype
            sig_shape = samples.shape
            names = sig_dtype.names
            name = signal.name

            if names is None:
                sig_type = v4c.SIGNAL_TYPE_SCALAR
                if sig_dtype.kind in "SV":
                    sig_type = v4c.SIGNAL_TYPE_STRING
            else:
                if names in (canopen_time_fields, canopen_date_fields):
                    sig_type = v4c.SIGNAL_TYPE_CANOPEN
                elif names[0] != sig.name:
                    sig_type = v4c.SIGNAL_TYPE_STRUCTURE_COMPOSITION
                else:
                    sig_type = v4c.SIGNAL_TYPE_ARRAY

            gp_sig_types.append(sig_type)

            # first add the signals in the simple signal list
            if sig_type == v4c.SIGNAL_TYPE_SCALAR:

                # compute additional byte offset for large records size
                s_type, s_size = fmt_to_datatype_v4(
                    sig_dtype, sig_shape
                )

                byte_size = max(s_size // 8, 1)

                if sig_dtype.kind == "u" and signal.bit_count <= 4:
                    s_size = signal.bit_count

                if signal.stream_sync:
                    channel_type = v4c.CHANNEL_TYPE_SYNC
                    at_data, at_name = signal.attachment
                    attachment_addr = self.attach(at_data, at_name, mime="video/avi")
                    data_block_addr = attachment_addr
                    sync_type = v4c.SYNC_TYPE_TIME
                else:
                    channel_type = v4c.CHANNEL_TYPE_VALUE
                    data_block_addr = 0
                    sync_type = v4c.SYNC_TYPE_NONE

                kargs = {
                    "channel_type": channel_type,
                    "sync_type": sync_type,
                    "bit_count": s_size,
                    "byte_offset": offset,
                    "bit_offset": 0,
                    "data_type": s_type,
                    "data_block_addr": data_block_addr,
                    "flags": 0,
                }

                if invalidation_bytes_nr and signal.invalidation_bits is not None:
                    inval_bits.append(signal.invalidation_bits)
                    kargs["flags"] |= v4c.FLAG_CN_INVALIDATION_PRESENT
                    kargs["pos_invalidation_bit"] = inval_cntr
                    inval_cntr += 1

                ch = Channel(**kargs)
                ch.name = name
                ch.unit = signal.unit
                ch.comment = signal.comment
                ch.display_name = signal.display_name

                # conversions for channel
                conversion = conversion_transfer(signal.conversion, version=4)
                if signal.raw:
                    ch.conversion = conversion

                # source for channel
                source = signal.source
                if source:
                    if source in si_map:
                        ch.source = si_map[source]
                    else:
                        new_source = SourceInformation(
                            source_type=source.source_type,
                            bus_type=source.bus_type,
                        )
                        new_source.name = source.name
                        new_source.path = source.path
                        new_source.comment = source.comment

                        si_map[source] = new_source

                        ch.source = new_source

                if memory != "minimum":
                    gp_channels.append(ch)
                else:
                    ch.to_stream(file, defined_texts, file_cc_map, file_si_map)
                    gp_channels.append(ch.address)

                offset += byte_size

                gp_sdata.append(None)
                gp_sdata_size.append(0)
                self.channels_db.add(name, (dg_cntr, ch_cntr))

                # update the parents as well
                field_name = field_names.get_unique_name(name)
                parents[ch_cntr] = field_name, 0

                fields.append(samples)
                types.append((field_name, sig_dtype, sig_shape[1:]))

                ch_cntr += 1

                # simple channels don't have channel dependencies
                gp_dep.append(None)

            elif sig_type == v4c.SIGNAL_TYPE_CANOPEN:

                field_name = field_names.get_unique_name(name)

                if names == canopen_time_fields:

                    vals = signal.samples.tostring()

                    fields.append(frombuffer(vals, dtype="V6"))
                    types.append((field_name, "V6"))
                    byte_size = 6
                    s_type = v4c.DATA_TYPE_CANOPEN_TIME

                else:
                    vals = []
                    for field in ("ms", "min", "hour", "day", "month", "year"):
                        if field == "hour":
                            vals.append(
                                signal.samples[field]
                                + (signal.samples["summer_time"] << 7)
                            )
                        elif field == "day":
                            vals.append(
                                signal.samples[field]
                                + (signal.samples["day_of_week"] << 4)
                            )
                        else:
                            vals.append(signal.samples[field])
                    vals = fromarrays(vals).tostring()

                    fields.append(frombuffer(vals, dtype="V7"))
                    types.append((field_name, "V7"))
                    byte_size = 7
                    s_type = v4c.DATA_TYPE_CANOPEN_DATE

                s_size = byte_size << 3

                # there is no channel dependency
                gp_dep.append(None)

                # add channel block
                kargs = {
                    "channel_type": v4c.CHANNEL_TYPE_VALUE,
                    "bit_count": s_size,
                    "byte_offset": offset,
                    "bit_offset": 0,
                    "data_type": s_type,
                    "flags": 0,
                }
                if invalidation_bytes_nr and signal.invalidation_bits is not None:
                    inval_bits.append(signal.invalidation_bits)
                    kargs["flags"] |= v4c.FLAG_CN_INVALIDATION_PRESENT
                    kargs["pos_invalidation_bit"] = inval_cntr
                    inval_cntr += 1

                ch = Channel(**kargs)
                ch.name = name
                ch.unit = signal.unit
                ch.comment = signal.comment
                ch.display_name = signal.display_name

                # source for channel
                source = signal.source
                if source:
                    if source in si_map:
                        ch.source = si_map[source]
                    else:
                        new_source = SourceInformation(
                            source_type=source.source_type,
                            bus_type=source.bus_type,
                        )
                        new_source.name = source.name
                        new_source.path = source.path
                        new_source.comment = source.comment

                        si_map[source] = new_source

                        ch.source = new_source

                if memory != "minimum":
                    gp_channels.append(ch)
                else:
                    ch.to_stream(file, defined_texts, file_cc_map, file_si_map)
                    gp_channels.append(ch.address)

                offset += byte_size

                self.channels_db.add(name, (dg_cntr, ch_cntr))

                # update the parents as well
                parents[ch_cntr] = field_name, 0

                if memory == "full":
                    gp_sdata.append(None)
                    gp_sdata_size.append(0)
                else:
                    gp_sdata.append(0)
                    gp_sdata_size.append(0)

                ch_cntr += 1

            elif sig_type == v4c.SIGNAL_TYPE_STRUCTURE_COMPOSITION:
                offset, dg_cntr, ch_cntr, struct_self, new_fields, new_types, inval_cntr = self._append_structure_composition(
                    gp,
                    signal,
                    field_names,
                    offset,
                    dg_cntr,
                    ch_cntr,
                    parents,
                    defined_texts,
                    invalidation_bytes_nr,
                    inval_bits,
                    inval_cntr,
                )
                fields.extend(new_fields)
                types.extend(new_types)

            elif sig_type == v4c.SIGNAL_TYPE_ARRAY:
                # here we have channel arrays or mdf v3 channel dependencies
                samples = signal.samples[names[0]]
                shape = samples.shape[1:]

                if len(shape) > 1:
                    # add channel dependency block for composed parent channel
                    dims_nr = len(shape)
                    names_nr = len(names)

                    if names_nr == 0:
                        kargs = {
                            "dims": dims_nr,
                            "ca_type": v4c.CA_TYPE_LOOKUP,
                            "flags": v4c.FLAG_CA_FIXED_AXIS,
                            "byte_offset_base": samples.dtype.itemsize,
                        }
                        for i in range(dims_nr):
                            kargs["dim_size_{}".format(i)] = shape[i]

                    elif len(names) == 1:
                        kargs = {
                            "dims": dims_nr,
                            "ca_type": v4c.CA_TYPE_ARRAY,
                            "flags": 0,
                            "byte_offset_base": samples.dtype.itemsize,
                        }
                        for i in range(dims_nr):
                            kargs["dim_size_{}".format(i)] = shape[i]

                    else:
                        kargs = {
                            "dims": dims_nr,
                            "ca_type": v4c.CA_TYPE_LOOKUP,
                            "flags": v4c.FLAG_CA_AXIS,
                            "byte_offset_base": samples.dtype.itemsize,
                        }
                        for i in range(dims_nr):
                            kargs["dim_size_{}".format(i)] = shape[i]

                    parent_dep = ChannelArrayBlock(**kargs)
                    gp_dep.append([parent_dep])

                else:
                    # add channel dependency block for composed parent channel
                    kargs = {
                        "dims": 1,
                        "ca_type": v4c.CA_TYPE_SCALE_AXIS,
                        "flags": 0,
                        "byte_offset_base": samples.dtype.itemsize,
                        "dim_size_0": shape[0],
                    }
                    parent_dep = ChannelArrayBlock(**kargs)
                    gp_dep.append([parent_dep])

                field_name = field_names.get_unique_name(name)

                fields.append(samples)
                dtype_pair = field_name, samples.dtype, shape
                types.append(dtype_pair)

                # first we add the structure channel
                s_type, s_size = fmt_to_datatype_v4(samples.dtype, samples.shape, True)

                # add channel block
                kargs = {
                    "channel_type": v4c.CHANNEL_TYPE_VALUE,
                    "bit_count": s_size,
                    "byte_offset": offset,
                    "bit_offset": 0,
                    "data_type": s_type,
                    "flags": 0,
                }

                if invalidation_bytes_nr:
                    if signal.invalidation_bits is not None:
                        inval_bits.append(signal.invalidation_bits)
                        kargs["flags"] |= v4c.FLAG_CN_INVALIDATION_PRESENT
                        kargs["pos_invalidation_bit"] = inval_cntr
                        inval_cntr += 1

                ch = Channel(**kargs)
                ch.name = name
                ch.unit = signal.unit
                ch.comment = signal.comment
                ch.display_name = signal.display_name

                # source for channel
                source = signal.source
                if source:
                    if source in si_map:
                        ch.source = si_map[source]
                    else:
                        new_source = SourceInformation(
                            source_type=source.source_type,
                            bus_type=source.bus_type,
                        )
                        new_source.name = source.name
                        new_source.path = source.path
                        new_source.comment = source.comment

                        si_map[source] = new_source

                        ch.source = new_source

                if memory != "minimum":
                    gp_channels.append(ch)
                else:
                    ch.to_stream(file, defined_texts, file_cc_map, file_si_map)
                    gp_channels.append(ch.address)

                size = s_size >> 3
                for dim in shape:
                    size *= dim
                offset += size

                gp_sdata.append(None)
                gp_sdata_size.append(0)
                self.channels_db.add(name, (dg_cntr, ch_cntr))

                # update the parents as well
                parents[ch_cntr] = name, 0

                ch_cntr += 1

                for name in names[1:]:
                    field_name = field_names.get_unique_name(name)

                    samples = signal.samples[name]
                    shape = samples.shape[1:]
                    fields.append(samples)
                    types.append((field_name, samples.dtype, shape))

                    # add channel dependency block
                    kargs = {
                        "dims": 1,
                        "ca_type": v4c.CA_TYPE_SCALE_AXIS,
                        "flags": 0,
                        "byte_offset_base": samples.dtype.itemsize,
                        "dim_size_0": shape[0],
                    }
                    dep = ChannelArrayBlock(**kargs)
                    gp_dep.append([dep])

                    # add components channel
                    s_type, s_size = fmt_to_datatype_v4(samples.dtype, ())
                    byte_size = max(s_size // 8, 1)
                    kargs = {
                        "channel_type": v4c.CHANNEL_TYPE_VALUE,
                        "bit_count": s_size,
                        "byte_offset": offset,
                        "bit_offset": 0,
                        "data_type": s_type,
                        "flags": 0,
                    }

                    if invalidation_bytes_nr:
                        if signal.invalidation_bits is not None:
                            inval_bits.append(signal.invalidation_bits)
                            kargs["flags"] |= v4c.FLAG_CN_INVALIDATION_PRESENT
                            kargs["pos_invalidation_bit"] = inval_cntr
                            inval_cntr += 1

                    ch = Channel(**kargs)
                    ch.name = name
                    ch.unit = signal.unit
                    ch.comment = signal.comment
                    ch.display_name = signal.display_name

                    if memory != "minimum":
                        gp_channels.append(ch)
                    else:
                        ch.to_stream(file, defined_texts, file_cc_map, file_si_map)
                        gp_channels.append(ch.address)

                    entry = dg_cntr, ch_cntr
                    parent_dep.referenced_channels.append(entry)
                    for dim in shape:
                        byte_size *= dim
                    offset += byte_size

                    gp_sdata.append(None)
                    gp_sdata_size.append(0)
                    self.channels_db.add(name, entry)

                    # update the parents as well
                    parents[ch_cntr] = field_name, 0

                    ch_cntr += 1

            else:

                encoding = signal.encoding
                samples = signal.samples
                sig_dtype = samples.dtype

                if encoding == 'utf-8':
                    data_type = v4c.DATA_TYPE_STRING_UTF_8
                elif encoding == 'latin-1':
                    data_type = v4c.DATA_TYPE_STRING_LATIN_1
                elif encoding == 'utf-16-be':
                    data_type = v4c.DATA_TYPE_STRING_UTF_16_BE
                elif encoding == 'utf-16-le':
                    data_type = v4c.DATA_TYPE_STRING_UTF_16_LE
                else:
                    raise MdfException('wrong encoding "{}" for string signal'.format(encoding))

                offsets = arange(len(samples), dtype=uint64) * (
                    signal.samples.itemsize + 4
                )

                values = [
                    full(len(samples), samples.itemsize, dtype=uint32),
                    samples,
                ]

                types_ = [("o", uint32), ("s", sig_dtype)]

                data = fromarrays(values, dtype=types_)

                if memory == "full":
                    gp_sdata.append(data.tostring())
                    data_addr = 0
                else:
                    data_size = len(data) * data.itemsize
                    if data_size:
                        data_addr = tell()
                        gp_sdata.append([data_addr])
                        gp_sdata_size.append([data_size])
                        data.tofile(file)
                    else:
                        data_addr = 0
                        gp_sdata.append([])
                        gp_sdata_size.append([])

                # compute additional byte offset for large records size
                byte_size = 8
                kargs = {
                    "channel_type": v4c.CHANNEL_TYPE_VLSD,
                    "bit_count": 64,
                    "byte_offset": offset,
                    "bit_offset": 0,
                    "data_type": data_type,
                    "data_block_addr": data_addr,
                    "flags": 0,
                }

                if invalidation_bytes_nr:
                    if signal.invalidation_bits is not None:
                        inval_bits.append(signal.invalidation_bits)
                        kargs["flags"] |= v4c.FLAG_CN_INVALIDATION_PRESENT
                        kargs["pos_invalidation_bit"] = inval_cntr
                        inval_cntr += 1

                ch = Channel(**kargs)
                ch.name = name
                ch.unit = signal.unit
                ch.comment = signal.comment
                ch.display_name = signal.display_name

                # conversions for channel
                conversion = conversion_transfer(signal.conversion, version=4)
                if signal.raw:
                    ch.conversion = conversion

                # source for channel
                source = signal.source
                if source:
                    if source in si_map:
                        ch.source = si_map[source]
                    else:
                        new_source = SourceInformation(
                            source_type=source.source_type,
                            bus_type=source.bus_type,
                        )
                        new_source.name = source.name
                        new_source.path = source.path
                        new_source.comment = source.comment

                        si_map[source] = new_source

                        ch.source = new_source

                if memory != "minimum":
                    gp_channels.append(ch)
                else:
                    ch.to_stream(file, defined_texts, file_cc_map, file_si_map)
                    gp_channels.append(ch.address)

                offset += byte_size

                self.channels_db.add(name, (dg_cntr, ch_cntr))

                # update the parents as well
                field_name = field_names.get_unique_name(name)
                parents[ch_cntr] = field_name, 0

                fields.append(offsets)
                types.append((field_name, uint64))

                ch_cntr += 1

                # simple channels don't have channel dependencies
                gp_dep.append(None)


        if invalidation_bytes_nr:
            invalidation_bytes_nr = len(inval_bits)

            for _ in range(8 - invalidation_bytes_nr % 8):
                inval_bits.append(zeros(cycles_nr, dtype='<u1'))

            inval_bits.reverse()

            invalidation_bytes_nr = len(inval_bits) // 8

            gp["channel_group"]["invalidation_bytes_nr"] = invalidation_bytes_nr

            inval_bits = fliplr(
                packbits(array(inval_bits).T).reshape(
                    (cycles_nr, invalidation_bytes_nr)
                )
            )

            fields.append(inval_bits)
            types.append(("invalidation_bytes", inval_bits.dtype, inval_bits.shape[1:]))

        gp["channel_group"]["cycles_nr"] = cycles_nr
        gp["channel_group"]["samples_byte_nr"] = offset
        gp["size"] = cycles_nr * (offset + invalidation_bytes_nr)

        gp["reduction_blocks"] = []
        gp["reduction_data_block"] = []

        # data group
        gp["data_group"] = DataGroup()

        # data block
        if PYVERSION == 2:
            types = fix_dtype_fields(types, "utf-8")
        types = dtype(types)

        gp["sorted"] = True
        gp["types"] = types
        gp["parents"] = parents

        if signals:
            samples = fromarrays(fields, dtype=types)
        else:
            samples = array([])

        signals = None
        del signals

        if memory == "full":
            gp["data_location"] = v4c.LOCATION_MEMORY
            gp["data_block"] = DataBlock(data=samples.tostring())

            gp["data_block_type"] = v4c.DT_BLOCK
            gp["param"] = 0
            gp["data_size"] = []
            gp["data_block_size"] = []
            gp["data_block_addr"] = []

        else:
            size = len(samples) * samples.itemsize
            if size:
                data_address = self._tempfile.tell()
                gp["data_location"] = v4c.LOCATION_TEMPORARY_FILE
                samples.tofile(self._tempfile)
                dim = size
                block_type = v4c.DT_BLOCK
                gp["data_block_type"] = block_type
                gp["param"] = 0
                gp["data_size"] = [size]
                gp["data_block_size"] = [dim]
                gp["data_block_addr"] = [data_address]
                gp["data_block"] = [data_address]
            else:
                gp["data_location"] = v4c.LOCATION_TEMPORARY_FILE
                gp["data_block"] = []
                gp["data_block_type"] = v4c.DT_BLOCK
                gp["param"] = 0
                gp["data_size"] = []
                gp["data_block_size"] = []
                gp["data_block_addr"] = []


    def _append_dataframe(self, df, source_info="", units=None):
        """
        Appends a new data group from a Pandas data frame.

        """

        units = units or {}

        t = df.index
        index_name = df.index.name
        time_name = index_name or "time"
        sync_type = v4c.SYNC_TYPE_TIME
        time_unit = "s"

        dg_cntr = len(self.groups)

        gp = {}
        gp["signal_data"] = gp_sdata = []
        gp["signal_data_size"] = gp_sdata_size = []
        gp["channels"] = gp_channels = []
        gp["channel_dependencies"] = gp_dep = []
        gp["signal_types"] = gp_sig_types = []
        gp["logging_channels"] = []

        # channel group
        kargs = {"cycles_nr": 0, "samples_byte_nr": 0}
        gp["channel_group"] = ChannelGroup(**kargs)
        gp["channel_group"].acq_name = source_info

        invalidation_bytes_nr = 0
        inval_bits = []

        self.groups.append(gp)

        cycles_nr = len(t)
        fields = []
        types = []
        parents = {}
        ch_cntr = 0
        offset = 0
        field_names = UniqueDB()

        defined_texts = {}
        si_map = self._si_map
        file_si_map = self._file_si_map
        cc_map = self._cc_map
        file_cc_map = self._file_cc_map

        # setup all blocks related to the time master channel

        memory = self.memory
        file = self._tempfile
        write = file.write
        tell = file.tell
        seek = file.seek

        seek(0, 2)

        source_block = SourceInformation()
        source_block.name = source_block.path = source_info

        if df.shape[0]:
            # time channel
            t_type, t_size = fmt_to_datatype_v4(t.dtype, t.shape)
            kargs = {
                "channel_type": v4c.CHANNEL_TYPE_MASTER,
                "data_type": t_type,
                "sync_type": sync_type,
                "byte_offset": 0,
                "bit_offset": 0,
                "bit_count": t_size,
                "min_raw_value": t[0] if cycles_nr else 0,
                "max_raw_value": t[-1] if cycles_nr else 0,
                "lower_limit": t[0] if cycles_nr else 0,
                "upper_limit": t[-1] if cycles_nr else 0,
                "flags": v4c.FLAG_PHY_RANGE_OK | v4c.FLAG_VAL_RANGE_OK,
            }
            ch = Channel(**kargs)
            ch.unit = time_unit
            ch.name = time_name
            ch.source = source_block
            name = time_name
            if memory == "minimum":
                ch.to_stream(file, defined_texts, file_cc_map, file_si_map)
                gp_channels.append(ch.address)
            else:
                gp_channels.append(ch)

            gp_sdata.append(None)
            gp_sdata_size.append(0)
            self.channels_db.add(name, (dg_cntr, ch_cntr))
            self.masters_db[dg_cntr] = 0
            # data group record parents
            parents[ch_cntr] = name, 0

            # time channel doesn't have channel dependencies
            gp_dep.append(None)

            fields.append(t)
            types.append((name, t.dtype))
            field_names.get_unique_name(name)

            offset += t_size // 8
            ch_cntr += 1

            gp_sig_types.append(0)

        for signal in df:
            if index_name == signal:
                continue

            sig = df[signal]
            name = signal

            sig_type = v4c.SIGNAL_TYPE_SCALAR
            if sig.dtype.kind in {"S", "V"}:
                sig_type = v4c.SIGNAL_TYPE_STRING

            gp_sig_types.append(sig_type)

            # first add the signals in the simple signal list
            if sig_type == v4c.SIGNAL_TYPE_SCALAR:

                # compute additional byte offset for large records size
                s_type, s_size = fmt_to_datatype_v4(sig.dtype, sig.shape)

                byte_size = max(s_size // 8, 1)

                channel_type = v4c.CHANNEL_TYPE_VALUE
                data_block_addr = 0
                sync_type = v4c.SYNC_TYPE_NONE

                kargs = {
                    "channel_type": channel_type,
                    "sync_type": sync_type,
                    "bit_count": s_size,
                    "byte_offset": offset,
                    "bit_offset": 0,
                    "data_type": s_type,
                    "data_block_addr": data_block_addr,
                }

                ch = Channel(**kargs)
                ch.name = name
                ch.unit = units.get(name, "")

                if memory != "minimum":
                    gp_channels.append(ch)
                else:
                    ch.to_stream(file, defined_texts, file_cc_map, file_si_map)
                    gp_channels.append(ch.address)

                offset += byte_size

                gp_sdata.append(None)
                gp_sdata_size.append(0)
                self.channels_db.add(name, (dg_cntr, ch_cntr))

                # update the parents as well
                field_name = field_names.get_unique_name(name)
                parents[ch_cntr] = field_name, 0

                fields.append(sig)
                types.append((field_name, sig.dtype, sig.shape[1:]))

                ch_cntr += 1

                # simple channels don't have channel dependencies
                gp_dep.append(None)

            elif sig_type == v4c.SIGNAL_TYPE_STRING:
                offsets = arange(len(sig), dtype=uint64) * (sig.itemsize + 4)

                values = [full(len(signal), sig.itemsize, dtype=uint32), sig]

                types_ = [("", uint32), ("", sig.dtype)]

                data = fromarrays(values, dtype=types_)

                if memory == "full":
                    data = data.tostring()
                    gp_sdata.append(data)
                    data_addr = 0
                else:
                    data_size = len(data) * data.itemsize
                    if data_size:
                        data_addr = tell()
                        gp_sdata.append([data_addr])
                        gp_sdata_size.append([data_size])
                        data.tofile(file)
                    else:
                        data_addr = 0
                        gp_sdata.append([])
                        gp_sdata_size.append([])

                # compute additional byte offset for large records size
                byte_size = 8
                kargs = {
                    "channel_type": v4c.CHANNEL_TYPE_VLSD,
                    "bit_count": 64,
                    "byte_offset": offset,
                    "bit_offset": 0,
                    "data_type": v4c.DATA_TYPE_STRING_UTF_8,
                    "min_raw_value": 0,
                    "max_raw_value": 0,
                    "lower_limit": 0,
                    "upper_limit": 0,
                    "flags": 0,
                    "data_block_addr": data_addr,
                }

                ch = Channel(**kargs)
                ch.name = name
                ch.unit = units.get(name, "")

                if memory != "minimum":
                    gp_channels.append(ch)
                else:
                    ch.to_stream(file, defined_texts, file_cc_map, file_si_map)
                    gp_channels.append(ch.address)

                offset += byte_size

                self.channels_db.add(name, (dg_cntr, ch_cntr))

                # update the parents as well
                field_name = field_names.field_names.get_unique_name(name)
                parents[ch_cntr] = field_name, 0

                fields.append(offsets)
                types.append((field_name, uint64))

                ch_cntr += 1

                # simple channels don't have channel dependencies
                gp_dep.append(None)

        gp["channel_group"]["cycles_nr"] = cycles_nr
        gp["channel_group"]["samples_byte_nr"] = offset
        gp["size"] = cycles_nr * (offset + invalidation_bytes_nr)

        gp["reduction_blocks"] = []
        gp["reduction_data_block"] = []

        # data group
        gp["data_group"] = DataGroup()

        # data block
        if PYVERSION == 2:
            types = fix_dtype_fields(types, "utf-8")
        types = dtype(types)

        gp["sorted"] = True
        gp["types"] = types
        gp["parents"] = parents

        if df.shape[0]:
            samples = fromarrays(fields, dtype=types)
        else:
            samples = array([])

        if memory == "full":
            gp["data_location"] = v4c.LOCATION_MEMORY
            gp["data_block"] = DataBlock(data=samples.tostring())

            gp["data_block_type"] = v4c.DT_BLOCK
            gp["param"] = 0
            gp["data_size"] = []
            gp["data_block_size"] = []
            gp["data_block_addr"] = []

        else:
            size = len(samples) * samples.itemsize
            if size:
                data_address = self._tempfile.tell()
                gp["data_location"] = v4c.LOCATION_TEMPORARY_FILE
                samples.tofile(self._tempfile)
                dim = size
                block_type = v4c.DT_BLOCK
                gp["data_block_type"] = block_type
                gp["param"] = 0
                gp["data_size"] = [size]
                gp["data_block_size"] = [dim]
                gp["data_block_addr"] = [data_address]
                gp["data_block"] = [data_address]
            else:
                gp["data_location"] = v4c.LOCATION_TEMPORARY_FILE
                gp["data_block"] = []
                gp["data_block_type"] = v4c.DT_BLOCK
                gp["param"] = 0
                gp["data_size"] = []
                gp["data_block_size"] = []
                gp["data_block_addr"] = []

    def extend(self, index, signals):
        """
        Extend a group with new samples. *signals* contains (values, invalidation_bits)
        pairs for each extended signal. The first pair is the master channel's pair, and the
        next pairs must respect the same order in which the signals were appended. The samples must have raw
        or physical values according to the *Signals* used for the initial append.

        Parameters
        ----------
        index : int
            group index
        signals : list
            list on (numpy.ndarray, numpy.ndarray) objects

        Examples
        --------
        >>> # case 1 conversion type None
        >>> s1 = np.array([1, 2, 3, 4, 5])
        >>> s2 = np.array([-1, -2, -3, -4, -5])
        >>> s3 = np.array([0.1, 0.04, 0.09, 0.16, 0.25])
        >>> t = np.array([0.001, 0.002, 0.003, 0.004, 0.005])
        >>> names = ['Positive', 'Negative', 'Float']
        >>> units = ['+', '-', '.f']
        >>> s1 = Signal(samples=s1, timstamps=t, unit='+', name='Positive')
        >>> s2 = Signal(samples=s2, timstamps=t, unit='-', name='Negative')
        >>> s3 = Signal(samples=s3, timstamps=t, unit='flts', name='Floats')
        >>> mdf = MDF3('new.mdf')
        >>> mdf.append([s1, s2, s3], 'created by asammdf v1.1.0')
        >>> t = np.array([0.006, 0.007, 0.008, 0.009, 0.010])
        >>> # extend without invalidation bits
        >>> mdf2.extend(0, [(t, None), (s1, None), (s2, None), (s3, None)])
        >>> # some invaldiation btis
        >>> s1_inv = np.array([0,0,0,1,1], dtype=np.bool)
        >>> mdf2.extend(0, [(t, None), (s1.samples, None), (s2.samples, None), (s3.samples, None)])

        """
        gp = self.groups[index]
        if not signals:
            message = '"append" requires a non-empty list of Signal objects'
            raise MdfException(message)

        stream = self._tempfile

        canopen_time_fields = ("ms", "days")

        fields = []
        types = []
        inval_bits = []

        invalidation_bytes_nr = gp["channel_group"]["invalidation_bytes_nr"]

        for i, ((signal, invalidation_bits), sig_type) in enumerate(
            zip(signals, gp["signal_types"])
        ):

            # first add the signals in the simple signal list
            if sig_type == v4c.SIGNAL_TYPE_SCALAR:

                fields.append(signal)
                types.append(("", signal.dtype, signal.shape[1:]))

                if invalidation_bytes_nr and invalidation_bits is not None:
                    inval_bits.append(invalidation_bits)

            elif sig_type == v4c.SIGNAL_TYPE_CANOPEN:
                names = signal.dtype.names

                if names == canopen_time_fields:

                    vals = signal.tostring()

                    fields.append(frombuffer(vals, dtype="V6"))
                    types.append(("", "V6"))

                else:
                    vals = []
                    for field in ("ms", "min", "hour", "day", "month", "year"):
                        vals.append(signal[field])
                    vals = fromarrays(vals).tostring()

                    fields.append(frombuffer(vals, dtype="V7"))
                    types.append(("", "V7"))

                if invalidation_bytes_nr and invalidation_bits is not None:
                    inval_bits.append(invalidation_bits)

            elif sig_type == v4c.SIGNAL_TYPE_STRUCTURE_COMPOSITION:
                if invalidation_bytes_nr and invalidation_bits is not None:
                    inval_bits.append(invalidation_bits)

                fields.append(signal)
                types.append(("", signal.dtype))
                names = signal.dtype.names

            elif sig_type == v4c.SIGNAL_TYPE_ARRAY:
                names = signal.dtype.names

                samples = signal[names[0]]

                shape = samples.shape[1:]

                fields.append(samples)
                types.append(("", samples.dtype, shape))

                if invalidation_bytes_nr and invalidation_bits is not None:
                    inval_bits.append(invalidation_bits)

                for name in names[1:]:

                    samples = signal[name]
                    shape = samples.shape[1:]
                    fields.append(samples)
                    types.append(("", samples.dtype, shape))

                    if invalidation_bytes_nr and invalidation_bits is not None:
                        inval_bits.append(invalidation_bits)

            else:
                if self.memory == "full":
                    data = gp["signal_data"][i]
                    cur_offset = len(data)
                else:
                    cur_offset = sum(gp["signal_data_size"][i])

                offsets = (
                    arange(len(signal), dtype=uint64) * (signal.itemsize + 4)
                    + cur_offset
                )
                values = [full(len(signal), signal.itemsize, dtype=uint32), signal]

                types_ = [("", uint32), ("", signal.dtype)]

                values = fromarrays(values, dtype=types_)

                if self.memory == "full":
                    values = values.tostring()
                    gp["signal_data"][i] = data + values
                else:
                    stream.seek(0, 2)
                    addr = stream.tell()
                    block_size = len(values) * values.itemsize
                    if block_size:
                        values.tofile(stream)
                        gp["signal_data"][i].append(addr)
                        gp["signal_data_size"][i].append(block_size)

                fields.append(offsets)
                types.append(("", uint64))

                if invalidation_bytes_nr and invalidation_bits is not None:
                    inval_bits.append(invalidation_bits)

        if invalidation_bytes_nr:
            invalidation_bytes_nr = len(inval_bits)
            cycles_nr = len(inval_bits[0])

            for _ in range(8 - invalidation_bytes_nr % 8):
                inval_bits.append(zeros(cycles_nr, dtype='<u1'))

            inval_bits.reverse()

            invalidation_bytes_nr = len(inval_bits) // 8

            gp["channel_group"]["invalidation_bytes_nr"] = invalidation_bytes_nr

            inval_bits = fliplr(
                packbits(array(inval_bits).T).reshape(
                    (cycles_nr, invalidation_bytes_nr)
                )
            )

            fields.append(inval_bits)
            types.append(("invalidation_bytes", inval_bits.dtype, inval_bits.shape[1:]))

        # data block
        if PYVERSION == 2:
            types = fix_dtype_fields(types, "utf-8")
        types = dtype(types)

        samples = fromarrays(fields, dtype=types)

        del fields
        del types

        if self.memory == "full":
            samples = samples.tostring()
            samples = gp["data_block"]["data"] + samples
            gp["data_block"] = DataBlock(data=samples)

            size = gp["data_block"]["block_len"] - COMMON_SIZE

            record_size = gp["channel_group"]["samples_byte_nr"]
            record_size += gp["data_group"]["record_id_len"]
            record_size += gp["channel_group"]["invalidation_bytes_nr"]

            gp["channel_group"]["cycles_nr"] = size // record_size

            if "record" in gp:
                del gp["record"]
        else:
            stream.seek(0, 2)
            addr = stream.tell()
            size = len(samples) * samples.itemsize

            if size:
                gp["data_block"].append(addr)
                samples.tofile(stream)
                dim = size

                record_size = gp["channel_group"]["samples_byte_nr"]
                record_size += gp["data_group"]["record_id_len"]
                record_size += gp["channel_group"]["invalidation_bytes_nr"]
                added_cycles = size // record_size
                gp["channel_group"]["cycles_nr"] += added_cycles

                gp["data_block_addr"].append(addr)
                gp["data_size"].append(size)
                gp["data_block_size"].append(dim)

        del samples

    def attach(
        self,
        data,
        file_name=None,
        comment=None,
        compression=True,
        mime=r"application/octet-stream",
    ):
        """ attach embedded attachment as application/octet-stream

        Parameters
        ----------
        data : bytes
            data to be attached
        file_name : str
            string file name
        comment : str
            attachment comment
        compression : bool
            use compression for embedded attachment data
        mime : str
            mime type string

        Returns
        -------
        index : int
            new attachment index

        """
        if data in self._attachments_cache:
            return self._attachments_cache[data]
        else:
            creator_index = len(self.file_history)
            fh = FileHistory()
            fh.comment = """<FHcomment>
<TX>Added new embedded attachment from {}</TX>
<tool_id>asammdf</tool_id>
<tool_vendor>asammdf</tool_vendor>
<tool_version>{}</tool_version>
</FHcomment>""".format(
                file_name if file_name else "bin.bin", __version__
            )

            self.file_history.append(fh)

            at_block = AttachmentBlock(data=data, compression=compression)
            at_block["creator_index"] = creator_index
            index = v4c.MAX_UINT64 - 1
            while index in self._attachments_map:
                index -= 1
            self.attachments.append(at_block)

            at_block.file_name = file_name if file_name else "bin.bin"
            at_block.mime = mime
            at_block.comment = comment

            self._attachments_cache[data] = index
            self._attachments_map[index] = len(self.attachments) - 1

            return index

    def close(self):
        """ if the MDF was created with memory=False and new
        channels have been appended, then this must be called just before the
        object is not used anymore to clean-up the temporary file"""
        if self._tempfile is not None:
            self._tempfile.close()
        if self._file is not None and not self._from_filelike:
            self._file.close()

    def extract_attachment(self, address=None, index=None):
        """ extract attachment data by original address or by index. If it is an embedded attachment,
        then this method creates the new file according to the attachment file
        name information

        Parameters
        ----------
        address : int
            attachment index; default *None*
        index : int
            attachment index; default *None*

        Returns
        -------
        data : bytes | str
            attachment data

        """
        if address is None and index is None:
            return b"", ""

        if address is not None:
            index = self._attachments_map[address]
        attachment = self.attachments[index]

        current_path = os.getcwd()
        file_path = attachment.file_name or "embedded"
        try:
            os.chdir(os.path.dirname(os.path.abspath(self.name)))

            flags = attachment["flags"]

            # for embedded attachments extrat data and create new files
            if flags & v4c.FLAG_AT_EMBEDDED:
                data = attachment.extract()

                return data, file_path
            else:
                # for external attachments read the file and return the content
                if flags & v4c.FLAG_AT_MD5_VALID:
                    data = open(file_path, "rb").read()
                    md5_worker = md5()
                    md5_worker.update(data)
                    md5_sum = md5_worker.digest()
                    if attachment["md5_sum"] == md5_sum:
                        if attachment.mime.startswith("text"):
                            with open(file_path, "r") as f:
                                data = f.read()
                        return data, file_path
                    else:
                        message = (
                            'ATBLOCK md5sum="{}" '
                            "and external attachment data ({}) "
                            'md5sum="{}"'
                        )
                        message = message.format(
                            attachment["md5_sum"], file_path, md5_sum
                        )
                        logger.warning(message)
                else:
                    if attachment.mime.startswith("text"):
                        mode = "r"
                    else:
                        mode = "rb"
                    with open(file_path, mode) as f:
                        data = f.read()
                    return data, file_path
        except Exception as err:
            os.chdir(current_path)
            message = "Exception during attachment extraction: " + repr(err)
            logger.warning(message)
            return b"", file_path

    def get(
        self,
        name=None,
        group=None,
        index=None,
        raster=None,
        samples_only=False,
        data=None,
        raw=False,
        ignore_invalidation_bits=False,
        source=None,
        sample_reduction_index=None,
        record_offset=0,
        record_count=None,
        copy_master=True,
    ):
        """Gets channel samples.
        Channel can be specified in two ways:

        * using the first positional argument *name*

            * if *source* is given this will be first used to validate the
              channel selection
            * if there are multiple occurances for this channel then the
              *group* and *index* arguments can be used to select a specific
              group.
            * if there are multiple occurances for this channel and either the
              *group* or *index* arguments is None then a warning is issued

        * using the group number (keyword argument *group*) and the channel
          number (keyword argument *index*). Use *info* method for group and
          channel numbers

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
        data : bytes
            prevent redundant data read by providing the raw data group samples
        raw : bool
            return channel samples without appling the conversion rule; default
            `False`
        ignore_invalidation_bits : bool
            option to ignore invalidation bits
        source : str
            source name used to select the channel
        record_offset : int
            if *data=None* use this to select the record offset from which the
            group data should be loaded
        record_count : int
            number of records to read; default *None* and in this case all
            available records are used
        copy_master : bool
            make a copy of the timebase for this channel

        Returns
        -------
        res : (numpy.array, numpy.array) | Signal
            returns *Signal* if *samples_only*=*False* (default option),
            otherwise returns a (numpy.array, numpy.array) tuple of samples and
            invalidation bits. If invalidation bits are not used or if
            *ignore_invalidation_bits* if False, then the second item will be
            None.

            The *Signal* samples are:

                * numpy recarray for channels that have composition/channel
                  array address or for channel of type
                  CANOPENDATE, CANOPENTIME
                * numpy array for all the rest

        Raises
        ------
        MdfException :

        * if the channel name is not found
        * if the group index is out of range
        * if the channel index is out of range

        Examples
        --------
        >>> from asammdf import MDF, Signal
        >>> import numpy as np
        >>> t = np.arange(5)
        >>> s = np.ones(5)
        >>> mdf = MDF(version='4.10')
        >>> for i in range(4):
        ...     sigs = [Signal(s*(i*10+j), t, name='Sig') for j in range(1, 4)]
        ...     mdf.append(sigs)
        ...
        >>> # first group and channel index of the specified channel name
        ...
        >>> mdf.get('Sig')
        UserWarning: Multiple occurances for channel "Sig". Using first occurance from data group 4. Provide both "group" and "index" arguments to select another data group
        <Signal Sig:
                samples=[ 1.  1.  1.  1.  1.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        >>> # first channel index in the specified group
        ...
        >>> mdf.get('Sig', 1)
        <Signal Sig:
                samples=[ 11.  11.  11.  11.  11.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        >>> # channel named Sig from group 1 channel index 2
        ...
        >>> mdf.get('Sig', 1, 2)
        <Signal Sig:
                samples=[ 12.  12.  12.  12.  12.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        >>> # channel index 1 or group 2
        ...
        >>> mdf.get(None, 2, 1)
        <Signal Sig:
                samples=[ 21.  21.  21.  21.  21.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        >>> mdf.get(group=2, index=1)
        <Signal Sig:
                samples=[ 21.  21.  21.  21.  21.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">
        >>> # validation using source name
        ...
        >>> mdf.get('Sig', source='VN7060')
        <Signal Sig:
                samples=[ 12.  12.  12.  12.  12.]
                timestamps=[0 1 2 3 4]
                unit=""
                info=None
                comment="">

        """

        gp_nr, ch_nr = self._validate_channel_selection(
            name, group, index, source=source
        )

        memory = self.memory
        grp = self.groups[gp_nr]
        if grp["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
            stream = self._file
        else:
            stream = self._tempfile

        if ch_nr >= 0:

            # get the channel object
            if memory == "minimum":
                if samples_only and raw:
                    channel = Channel(
                        address=grp["channels"][ch_nr],
                        stream=stream,
                        load_metadata=False,
                        at_map=self._attachments_map,
                    )
                else:
                    channel = Channel(
                        address=grp["channels"][ch_nr],
                        stream=stream,
                        cc_map=self._cc_map,
                        si_map=self._si_map,
                        at_map=self._attachments_map,
                        use_display_names=self._use_display_names,
                    )
            else:
                channel = grp["channels"][ch_nr]

            dependency_list = grp["channel_dependencies"][ch_nr]

            # get data group record
            try:
                parents, dtypes = grp["parents"], grp["types"]
            except KeyError:
                grp["parents"], grp["types"] = self._prepare_record(grp)
                parents, dtypes = grp["parents"], grp["types"]

            # get group data
            if data is None:
                data = self._load_data(
                    grp,
                    record_offset=record_offset,
                    record_count=record_count,
                )
            else:
                data = (data,)

            channel_invalidation_present = (
                channel["flags"]
                & (v4c.FLAG_INVALIDATION_BIT_VALID | v4c.FLAG_ALL_SAMPLES_VALID)
                == v4c.FLAG_INVALIDATION_BIT_VALID
            )

            bit_count = channel["bit_count"]
        else:
            # get data group record
            try:
                parents, dtypes = grp["parents"], grp["types"]
            except KeyError:
                grp["parents"], grp["types"] = self._prepare_record(grp)
                parents, dtypes = grp["parents"], grp["types"]

            parent, bit_offset = parents[ch_nr]

            channel_invalidation_present = False
            dependency_list = None

            channel = grp["logging_channels"][-ch_nr - 1]

            # get group data
            if data is None:
                data = self._load_data(
                    grp,
                    record_offset=record_offset,
                    record_count=record_count,
                )
            else:
                data = (data,)

            bit_count = channel["bit_count"]

        data_type = channel["data_type"]
        channel_type = channel["channel_type"]
        stream_sync = channel_type == v4c.CHANNEL_TYPE_SYNC

        encoding = None

        # check if this is a channel array
        if dependency_list:
            arrays = []
            if name is None:
                name = channel.name

            if all(not isinstance(dep, ChannelArrayBlock) for dep in dependency_list):
                # structure channel composition
                if PYVERSION == 2 and channel.dtype_fmt is not None:
                    _dtype = dtype(fix_dtype_fields(channel.dtype_fmt, "utf-8"))
                else:
                    _dtype = dtype(channel.dtype_fmt)
                if _dtype.itemsize == bit_count >> 3:
                    fast_path = True
                    channel_values = []
                    timestamps = []
                    invalidation_bits = []

                    byte_offset = channel["byte_offset"]
                    record_size = grp["channel_group"]["samples_byte_nr"] + grp["channel_group"]["invalidation_bytes_nr"]

                    count = 0
                    for fragment in data:

                        bts = fragment[0]
                        types = [
                            ("", "V{}".format(byte_offset)),
                            ("vals", _dtype),
                            ("", "V{}".format(record_size - _dtype.itemsize - byte_offset)),
                        ]

                        channel_values.append(fromstring(bts, types)["vals"].copy())

                        if not samples_only or raster:
                            timestamps.append(self.get_master(gp_nr, fragment, copy_master=copy_master))
                        if channel_invalidation_present:
                            invalidation_bits.append(
                                self.get_invalidation_bits(gp_nr, channel, fragment)
                            )

                        count += 1
                else:
                    fast_path = False
                    if memory == "minimum":
                        names = []

                        for _, ch_nr in dependency_list:
                            address = grp["channels"][ch_nr]
                            channel_ = Channel(
                                address=address, stream=stream, load_metadata=False
                            )

                            name_ = get_text_v4(
                                address=channel_["name_addr"], stream=stream
                            )
                            names.append(name_)
                    else:
                        names = [
                            grp["channels"][ch_nr].name for _, ch_nr in dependency_list
                        ]

                    channel_values = [[] for _ in dependency_list]
                    timestamps = []
                    invalidation_bits = []

                    count = 0
                    for fragment in data:
                        for i, (dg_nr, ch_nr) in enumerate(dependency_list):
                            vals = self.get(
                                group=dg_nr,
                                index=ch_nr,
                                samples_only=True,
                                raw=raw,
                                data=fragment,
                                ignore_invalidation_bits=ignore_invalidation_bits,
                                record_offset=record_offset,
                                record_count=record_count,
                            )[0]
                            channel_values[i].append(vals)
                        if not samples_only or raster:
                            timestamps.append(self.get_master(gp_nr, fragment, copy_master=copy_master))
                        if channel_invalidation_present:
                            invalidation_bits.append(
                                self.get_invalidation_bits(gp_nr, channel, fragment)
                            )

                        count += 1

                if fast_path:
                    if count > 1:
                        vals = concatenate(channel_values)
                    else:
                        vals = channel_values[0]
                else:
                    if count > 1:
                        arrays = [concatenate(lst) for lst in channel_values]
                    else:
                        arrays = [lst[0] for lst in channel_values]
                    types = [
                        (name_, arr.dtype, arr.shape[1:])
                        for name_, arr in zip(names, arrays)
                    ]
                    if PYVERSION == 2:
                        types = fix_dtype_fields(types, "utf-8")
                    types = dtype(types)

                    vals = fromarrays(arrays, dtype=types)

                if not samples_only or raster:
                    if count > 1:
                        timestamps = concatenate(timestamps)
                    else:
                        timestamps = timestamps[0]

                if channel_invalidation_present:
                    if count > 1:
                        invalidation_bits = concatenate(invalidation_bits)
                    else:
                        invalidation_bits = invalidation_bits[0]
                    if not ignore_invalidation_bits:
                        vals = vals[nonzero(~invalidation_bits)[0]]
                        if not samples_only or raster:
                            timestamps = timestamps[nonzero(~invalidation_bits)[0]]

                if raster and len(timestamps) > 1:
                    t = arange(timestamps[0], timestamps[-1], raster)

                    vals = (
                        Signal(vals, timestamps, name="_")
                        .interp(t)
                    )

                    vals, timestamps, invalidation_bits = (
                        vals.samples,
                        vals.timestamps,
                        vals.invalidation_bits,
                    )

            else:
                # channel arrays
                channel_group = grp["channel_group"]
                samples_size = (
                    channel_group["samples_byte_nr"]
                    + channel_group["invalidation_bytes_nr"]
                )

                channel_values = []
                timestamps = []
                invalidation_bits = []
                count = 0
                for fragment in data:

                    data_bytes, offset, _count = fragment

                    cycles = len(data_bytes) // samples_size

                    arrays = []
                    types = []
                    try:
                        parent, bit_offset = parents[ch_nr]
                    except KeyError:
                        parent, bit_offset = None, None

                    if parent is not None:
                        if "record" not in grp:
                            if dtypes.itemsize:
                                record = fromstring(data_bytes, dtype=dtypes)
                            else:
                                record = None

                            if self.memory == "full":
                                record.setflags(write=False)
                                grp["record"] = record
                        else:
                            record = grp["record"]

                        vals = record[parent]
                    else:
                        vals = self._get_not_byte_aligned_data(data_bytes, grp, ch_nr)

                    vals = vals.copy()

                    dep = dependency_list[0]
                    if dep["flags"] & v4c.FLAG_CA_INVERSE_LAYOUT:
                        shape = vals.shape
                        shape = (shape[0],) + shape[1:][::-1]
                        vals = vals.reshape(shape)

                        axes = (0,) + tuple(range(len(shape) - 1, 0, -1))
                        vals = transpose(vals, axes=axes)

                    cycles_nr = len(vals)

                    for ca_block in dependency_list[:1]:
                        dims_nr = ca_block["dims"]

                        if ca_block["ca_type"] == v4c.CA_TYPE_SCALE_AXIS:
                            shape = (ca_block["dim_size_0"],)
                            arrays.append(vals)
                            dtype_pair = channel.name, vals.dtype, shape
                            types.append(dtype_pair)

                        elif ca_block["ca_type"] == v4c.CA_TYPE_LOOKUP:
                            shape = vals.shape[1:]
                            arrays.append(vals)
                            dtype_pair = channel.name, vals.dtype, shape
                            types.append(dtype_pair)

                            if ca_block["flags"] & v4c.FLAG_CA_FIXED_AXIS:
                                for i in range(dims_nr):
                                    shape = (ca_block["dim_size_{}".format(i)],)
                                    axis = []
                                    for j in range(shape[0]):
                                        key = "axis_{}_value_{}".format(i, j)
                                        axis.append(ca_block[key])
                                    axis = array([axis for _ in range(cycles_nr)])
                                    arrays.append(axis)
                                    dtype_pair = (
                                        "axis_{}".format(i),
                                        axis.dtype,
                                        shape,
                                    )
                                    types.append(dtype_pair)
                            else:
                                for i in range(dims_nr):
                                    try:
                                        ref_dg_nr, ref_ch_nr = ca_block.referenced_channels[
                                            i
                                        ]
                                    except:
                                        debug_channel(
                                            self, grp, channel, dependency_list
                                        )
                                        raise
                                    if memory == "minimum":
                                        address = self.groups[ref_dg_nr]["channels"][
                                            ref_ch_nr
                                        ]
                                        ref_channel = Channel(
                                            address=address,
                                            stream=stream,
                                            cc_map=self._cc_map,
                                            si_map=self._si_map,
                                            use_display_names=self._use_display_names,
                                        )
                                        axisname = ref_channel.name
                                    else:
                                        axisname = self.groups[ref_dg_nr]["channels"][
                                            ref_ch_nr
                                        ].name

                                    shape = (ca_block["dim_size_{}".format(i)],)
                                    if ref_dg_nr == gp_nr:
                                        axis_values = self.get(
                                            group=ref_dg_nr,
                                            index=ref_ch_nr,
                                            samples_only=True,
                                            data=fragment,
                                            ignore_invalidation_bits=ignore_invalidation_bits,
                                            record_offset=record_offset,
                                            record_count=cycles,
                                        )[0]
                                    else:
                                        channel_group = grp["channel_group"]
                                        record_size = channel_group["samples_byte_nr"]
                                        record_size += channel_group[
                                            "invalidation_bytes_nr"
                                        ]
                                        start = offset // record_size
                                        end = start + len(data_bytes) // record_size + 1
                                        ref = self.get(
                                            group=ref_dg_nr,
                                            index=ref_ch_nr,
                                            samples_only=True,
                                            ignore_invalidation_bits=ignore_invalidation_bits,
                                            record_offset=record_offset,
                                            record_count=cycles,
                                        )[0]
                                        axis_values = ref[start:end].copy()
                                    axis_values = axis_values[axisname]

                                    arrays.append(axis_values)
                                    dtype_pair = (axisname, axis_values.dtype, shape)
                                    types.append(dtype_pair)

                        elif ca_block["ca_type"] == v4c.CA_TYPE_ARRAY:
                            shape = vals.shape[1:]
                            arrays.append(vals)
                            dtype_pair = channel.name, vals.dtype, shape
                            types.append(dtype_pair)

                    for ca_block in dependency_list[1:]:
                        dims_nr = ca_block["dims"]

                        if ca_block["flags"] & v4c.FLAG_CA_FIXED_AXIS:
                            for i in range(dims_nr):
                                shape = (ca_block["dim_size_{}".format(i)],)
                                axis = []
                                for j in range(shape[0]):
                                    key = "axis_{}_value_{}".format(i, j)
                                    axis.append(ca_block[key])
                                axis = array([axis for _ in range(cycles_nr)])
                                arrays.append(axis)
                                types.append(("axis_{}".format(i), axis.dtype, shape))
                        else:
                            for i in range(dims_nr):
                                ref_dg_nr, ref_ch_nr = ca_block.referenced_channels[i]
                                if memory == "minimum":
                                    address = self.groups[ref_dg_nr]["channels"][
                                        ref_ch_nr
                                    ]
                                    ref_channel = Channel(
                                        address=address,
                                        stream=stream,
                                        cc_map=self._cc_map,
                                        si_map=self._si_map,
                                        use_display_names=self._use_display_names,
                                    )
                                    axisname = ref_channel.name
                                else:
                                    axisname = self.groups[ref_dg_nr]["channels"][
                                        ref_ch_nr
                                    ].name

                                shape = (ca_block["dim_size_{}".format(i)],)
                                if ref_dg_nr == gp_nr:
                                    axis_values = self.get(
                                        group=ref_dg_nr,
                                        index=ref_ch_nr,
                                        samples_only=True,
                                        data=fragment,
                                        ignore_invalidation_bits=ignore_invalidation_bits,
                                        record_offset=record_offset,
                                        record_count=cycles,
                                    )[0]
                                else:
                                    channel_group = grp["channel_group"]
                                    record_size = channel_group["samples_byte_nr"]
                                    record_size += channel_group[
                                        "invalidation_bytes_nr"
                                    ]
                                    start = offset // record_size
                                    end = start + len(data_bytes) // record_size + 1
                                    ref = self.get(
                                        group=ref_dg_nr,
                                        index=ref_ch_nr,
                                        samples_only=True,
                                        ignore_invalidation_bits=ignore_invalidation_bits,
                                        record_offset=record_offset,
                                        record_count=cycles,
                                    )[0]
                                    axis_values = ref[start:end].copy()
                                axis_values = axis_values[axisname]

                                arrays.append(axis_values)
                                dtype_pair = axisname, axis_values.dtype, shape
                                types.append(dtype_pair)

                    if PYVERSION == 2:
                        types = fix_dtype_fields(types, "utf-8")

                    vals = fromarrays(arrays, dtype(types))

                    if not samples_only or raster:
                        timestamps.append(self.get_master(gp_nr, fragment, copy_master=copy_master))
                    if channel_invalidation_present:
                        invalidation_bits.append(
                            self.get_invalidation_bits(gp_nr, channel, fragment)
                        )

                    channel_values.append(vals)
                    count += 1

                if count > 1:
                    vals = concatenate(channel_values)
                elif count == 1:
                    vals = channel_values[0]
                else:
                    vals = []

                if not samples_only or raster:
                    if count > 1:
                        timestamps = concatenate(timestamps)
                    else:
                        timestamps = timestamps[0]

                if channel_invalidation_present:
                    if count > 1:
                        invalidation_bits = concatenate(invalidation_bits)
                    else:
                        invalidation_bits = invalidation_bits[0]
                    if not ignore_invalidation_bits:
                        vals = vals[nonzero(~invalidation_bits)[0]]
                        if not samples_only or raster:
                            timestamps = timestamps[nonzero(~invalidation_bits)[0]]

                if raster and len(timestamps) > 1:
                    t = arange(timestamps[0], timestamps[-1], raster)

                    vals = (
                        Signal(vals, timestamps, name="_")
                        .interp(t)
                    )

                    vals, timestamps, invalidation_bits = (
                        vals.samples,
                        vals.timestamps,
                        vals.invalidation_bits,
                    )

            conversion = channel.conversion

        else:
            # get channel values
            if channel_type in {
                v4c.CHANNEL_TYPE_VIRTUAL,
                v4c.CHANNEL_TYPE_VIRTUAL_MASTER,
            }:
                if not channel.dtype_fmt:
                    channel.dtype_fmt = get_fmt_v4(data_type, 64)
                ch_dtype = dtype(channel.dtype_fmt)

                channel_values = []
                timestamps = []
                invalidation_bits = []

                channel_group = grp["channel_group"]
                record_size = channel_group["samples_byte_nr"]
                record_size += channel_group["invalidation_bytes_nr"]

                count = 0
                for fragment in data:
                    data_bytes, offset, _count = fragment
                    offset = offset // record_size

                    vals = arange(len(data_bytes) // record_size, dtype=ch_dtype)
                    vals += offset

                    if not samples_only or raster:
                        timestamps.append(self.get_master(gp_nr, fragment, copy_master=copy_master))
                    if channel_invalidation_present:
                        invalidation_bits.append(
                            self.get_invalidation_bits(gp_nr, channel, fragment)
                        )

                    channel_values.append(vals)
                    count += 1

                if count > 1:
                    vals = concatenate(channel_values)
                elif count == 1:
                    vals = channel_values[0]
                else:
                    vals = []

                if not samples_only or raster:
                    if count > 1:
                        timestamps = concatenate(timestamps)
                    else:
                        timestamps = timestamps[0]

                if channel_invalidation_present:
                    if count > 1:
                        invalidation_bits = concatenate(invalidation_bits)
                    else:
                        invalidation_bits = invalidation_bits[0]
                    if not ignore_invalidation_bits:
                        vals = vals[nonzero(~invalidation_bits)[0]]
                        if not samples_only or raster:
                            timestamps = timestamps[nonzero(~invalidation_bits)[0]]

                if raster and len(timestamps) > 1:
                    num = float(
                        float32((timestamps[-1] - timestamps[0]) / raster)
                    )
                    if num.is_integer():
                        t = linspace(
                            timestamps[0],
                            timestamps[-1],
                            int(num),
                        )
                    else:
                        t = arange(timestamps[0], timestamps[-1], raster)

                    vals = (
                        Signal(vals, timestamps, name="_")
                        .interp(t)
                    )

                    vals, timestamps, invalidation_bits = (
                        vals.samples,
                        vals.timestamps,
                        vals.invalidation_bits,
                    )

            else:
                channel_values = []
                timestamps = []
                invalidation_bits = []

                count = 0
                for fragment in data:

                    data_bytes, offset, _count = fragment
                    try:
                        parent, bit_offset = parents[ch_nr]
                    except KeyError:
                        parent, bit_offset = None, None

                    if parent is not None:
                        if "record" not in grp:
                            record = fromstring(data_bytes, dtype=dtypes)

                            if memory == "full":
                                record.setflags(write=False)
                                grp["record"] = record

                        else:
                            record = grp["record"]

                        vals = record[parent]

                        dtype_ = vals.dtype
                        shape_ = vals.shape
                        size = vals.dtype.itemsize
                        for dim in shape_[1:]:
                            size *= dim

                        kind_ = dtype_.kind

                        if kind_ == "b":
                            pass
                        elif (
                            kind_ not in {"u", "i"}
                            and (bit_offset or bit_count != size * 8)
                            or (
                                len(shape_) > 1
                                and data_type != v4c.DATA_TYPE_BYTEARRAY
                            )
                        ):
                            vals = self._get_not_byte_aligned_data(
                                data_bytes, grp, ch_nr
                            )
                        else:
                            if data_type in (v4c.DATA_TYPE_REAL_INTEL, v4c.DATA_TYPE_REAL_MOTOROLA):
                                if bit_count != size * 8:
                                    vals = self._get_not_byte_aligned_data(
                                        data_bytes, grp, ch_nr
                                    )
                                else:
                                    if kind_ in "ui":
                                        if not channel.dtype_fmt:
                                            channel.dtype_fmt = get_fmt_v4(data_type, bit_count, channel_type)
                                        channel_dtype = dtype(channel.dtype_fmt.split(')')[-1])
                                        vals = vals.view(channel_dtype)

                            else:
                                if kind_ == "f":
                                    if bit_count != size * 8:
                                        vals = self._get_not_byte_aligned_data(
                                            data_bytes, grp, ch_nr
                                        )
                                    else:
                                        if not channel.dtype_fmt:
                                            channel.dtype_fmt = get_fmt_v4(data_type, bit_count, channel_type)
                                        channel_dtype = dtype(channel.dtype_fmt.split(')')[-1])
                                        vals = vals.view(channel_dtype)
                                else:
                                    if dtype_.byteorder == '>':
                                        if bit_offset or bit_count != size << 3:
                                            vals = self._get_not_byte_aligned_data(data_bytes, grp, ch_nr)
                                    else:
                                        if bit_offset:
                                            if kind_ == "i":
                                                vals = vals.astype(dtype("{}u{}".format(dtype_.byteorder, size)))
                                                vals >>= bit_offset
                                            else:
                                                vals = vals >> bit_offset

                                        if bit_count != size << 3:
                                            if data_type in v4c.SIGNED_INT:
                                                vals = as_non_byte_sized_signed_int(vals, bit_count)
                                            else:
                                                mask = (1 << bit_count) - 1
                                                if vals.flags.writeable:
                                                    vals &= mask
                                                else:
                                                    vals = vals & mask

                    else:
                        vals = self._get_not_byte_aligned_data(data_bytes, grp, ch_nr)

                    if bit_count == 1 and self._single_bit_uint_as_bool:
                        vals = array(vals, dtype=bool)
                    else:
                        if not channel.dtype_fmt:
                            channel.dtype_fmt = get_fmt_v4(data_type, bit_count, channel_type)
                        channel_dtype = dtype(channel.dtype_fmt.split(')')[-1])
                        if vals.dtype != channel_dtype:
                            vals = vals.astype(channel_dtype)

                    if not samples_only or raster:
                        timestamps.append(self.get_master(gp_nr, fragment, copy_master=copy_master))
                    if channel_invalidation_present:
                        invalidation_bits.append(
                            self.get_invalidation_bits(gp_nr, channel, fragment)
                        )
                    if vals.flags.writeable:
                        channel_values.append(vals)
                    else:
                        channel_values.append(vals.copy())
                    count += 1

                if count > 1:
                    vals = concatenate(channel_values)
                elif count == 1:
                    vals = channel_values[0]
                else:
                    vals = []

                if not samples_only or raster:
                    if count > 1:
                        timestamps = concatenate(timestamps)
                    elif count == 1:
                        timestamps = timestamps[0]
                    else:
                        timestamps = []

                if channel_invalidation_present:
                    if count > 1:
                        invalidation_bits = concatenate(invalidation_bits)
                    elif count == 1:
                        invalidation_bits = invalidation_bits[0]
                    else:
                        invalidation_bits = []
                    if not ignore_invalidation_bits:
                        vals = vals[nonzero(~invalidation_bits)[0]]
                        if not samples_only or raster:
                            timestamps = timestamps[nonzero(~invalidation_bits)[0]]

                if raster and len(timestamps) > 1:

                    num = float(
                        float32((timestamps[-1] - timestamps[0]) / raster)
                    )
                    if num.is_integer():
                        t = linspace(
                            timestamps[0],
                            timestamps[-1],
                            int(num),
                        )
                    else:
                        t = arange(timestamps[0], timestamps[-1], raster)

                    vals = (
                        Signal(vals, timestamps, name="_")
                        .interp(t)
                    )

                    vals, timestamps, invalidation_bits = (
                        vals.samples,
                        vals.timestamps,
                        vals.invalidation_bits,
                    )

            # get the channel conversion
            conversion = channel.conversion

            if conversion is None:
                conversion_type = v4c.CONVERSION_TYPE_NON
            else:
                conversion_type = conversion["conversion_type"]

            if conversion_type in v4c.CONVERSION_GROUP_1:

                if channel_type == v4c.CHANNEL_TYPE_VLSD:
                    signal_data = self._load_signal_data(group=grp, index=ch_nr)
                    if signal_data:
                        values = []

                        vals = vals.tolist()

                        for offset in vals:
                            (str_size, ) = UINT32_uf(signal_data, offset)
                            offset += 4
                            values.append(
                                signal_data[offset: offset + str_size]
                            )

                        if data_type == v4c.DATA_TYPE_BYTEARRAY:

                            if PYVERSION >= 3:
                                values = [list(val) for val in values]
                            else:
                                values = [[ord(byte) for byte in val] for val in values]

                            dim = max(len(arr) for arr in values) if values else 0

                            for lst in values:
                                lst.extend([0] * (dim - len(lst)))

                            vals = array(values, dtype=uint8)

                        else:

                            vals = array(values)

                            if data_type == v4c.DATA_TYPE_STRING_UTF_16_BE:
                                encoding = "utf-16-be"

                            elif data_type == v4c.DATA_TYPE_STRING_UTF_16_LE:
                                encoding = "utf-16-le"

                            elif data_type == v4c.DATA_TYPE_STRING_UTF_8:
                                encoding = "utf-8"

                            elif data_type == v4c.DATA_TYPE_STRING_LATIN_1:
                                encoding = "latin-1"

                            else:
                                raise MdfException('wrong data type "{}" for vlsd channel'.format(data_type))

                    else:
                        # no VLSD signal data samples
                        vals = array([], dtype=dtype("S"))
                        if data_type != v4c.DATA_TYPE_BYTEARRAY:

                            if data_type == v4c.DATA_TYPE_STRING_UTF_16_BE:
                                encoding = "utf-16-be"

                            elif data_type == v4c.DATA_TYPE_STRING_UTF_16_LE:
                                encoding = "utf-16-le"

                            elif data_type == v4c.DATA_TYPE_STRING_UTF_8:
                                encoding = "utf-8"

                            elif data_type == v4c.DATA_TYPE_STRING_LATIN_1:
                                encoding = "latin-1"

                            else:
                                raise MdfException('wrong data type "{}" for vlsd channel'.format(data_type))

                elif channel_type in {
                    v4c.CHANNEL_TYPE_VALUE,
                    v4c.CHANNEL_TYPE_MLSD,
                } and (
                    v4c.DATA_TYPE_STRING_LATIN_1
                    <= data_type
                    <= v4c.DATA_TYPE_STRING_UTF_16_BE
                ):

                    if data_type == v4c.DATA_TYPE_STRING_UTF_16_BE:
                        encoding = "utf-16-be"

                    elif data_type == v4c.DATA_TYPE_STRING_UTF_16_LE:
                        encoding = "utf-16-le"

                    elif data_type == v4c.DATA_TYPE_STRING_UTF_8:
                        encoding = "utf-8"

                    elif data_type == v4c.DATA_TYPE_STRING_LATIN_1:
                        encoding = "latin-1"

                    else:
                        raise MdfException('wrong data type "{}" for string channel'.format(data_type))

                # CANopen date
                if data_type == v4c.DATA_TYPE_CANOPEN_DATE:

                    vals = vals.tostring()

                    types = dtype(
                        [
                            ("ms", "<u2"),
                            ("min", "<u1"),
                            ("hour", "<u1"),
                            ("day", "<u1"),
                            ("month", "<u1"),
                            ("year", "<u1"),
                        ]
                    )
                    dates = frombuffer(vals, types)

                    arrays = []
                    arrays.append(dates["ms"])
                    # bit 6 and 7 of minutes are reserved
                    arrays.append(dates["min"] & 0x3F)
                    # only firt 4 bits of hour are used
                    arrays.append(dates["hour"] & 0xF)
                    # the first 4 bits are the day number
                    arrays.append(dates["day"] & 0xF)
                    # bit 6 and 7 of month are reserved
                    arrays.append(dates["month"] & 0x3F)
                    # bit 7 of year is reserved
                    arrays.append(dates["year"] & 0x7F)
                    # add summer or standard time information for hour
                    arrays.append((dates["hour"] & 0x80) >> 7)
                    # add day of week information
                    arrays.append((dates["day"] & 0xF0) >> 4)

                    names = [
                        "ms",
                        "min",
                        "hour",
                        "day",
                        "month",
                        "year",
                        "summer_time",
                        "day_of_week",
                    ]
                    vals = fromarrays(arrays, names=names)

                # CANopen time
                elif data_type == v4c.DATA_TYPE_CANOPEN_TIME:
                    vals = vals.tostring()

                    types = dtype([("ms", "<u4"), ("days", "<u2")])
                    dates = fromstring(vals, types)

                    arrays = []
                    # bits 28 to 31 are reserverd for ms
                    arrays.append(dates["ms"] & 0xFFFFFFF)
                    arrays.append(dates["days"] & 0x3F)

                    names = ["ms", "days"]
                    vals = fromarrays(arrays, names=names)

                if conversion_type == v4c.CONVERSION_TYPE_TRANS:
                    if not raw:
                        vals = conversion.convert(vals)
                if conversion_type == v4c.CONVERSION_TYPE_TTAB:
                    raw = True

            elif conversion_type in v4c.CONVERSION_GROUP_2:
                if not raw:
                    vals = conversion.convert(vals)

            else:
                raw = True

        if samples_only:
            if not channel_invalidation_present or not ignore_invalidation_bits:
                invalidation_bits = None
            res = vals, invalidation_bits
        else:
            # search for unit in conversion texts

            if name is None:
                name = channel.name

            unit = conversion and conversion.unit or channel.unit

            comment = channel.comment

            source = channel.source
            cg_source = grp["channel_group"].acq_source
            if source:
                source = SignalSource(
                    source.name or (cg_source and cg_source.name) or "",
                    source.path,
                    source.comment,
                    source["source_type"],
                    source["bus_type"],
                )
            else:
                source = None

            if channel.attachments:
                attachment = self.extract_attachment(index=channel.attachments[0])
            elif channel_type == v4c.CHANNEL_TYPE_SYNC:
                index = self._attachments_map[channel["data_block_addr"]]
                attachment = self.extract_attachment(index=index)
            else:
                attachment = ()

            master_metadata = self._master_channel_metadata.get(gp_nr, None)

            if not channel_invalidation_present or not ignore_invalidation_bits:
                invalidation_bits = None

            try:
                res = Signal(
                    samples=vals,
                    timestamps=timestamps,
                    unit=unit,
                    name=name,
                    comment=comment,
                    conversion=conversion,
                    raw=raw,
                    master_metadata=master_metadata,
                    attachment=attachment,
                    source=source,
                    display_name=channel.display_name,
                    bit_count=bit_count,
                    stream_sync=stream_sync,
                    invalidation_bits=invalidation_bits,
                    encoding=encoding,
                )
            except:
                debug_channel(self, grp, channel, dependency_list)
                raise

        return res

    def get_master(self, index, data=None, raster=None, record_offset=0, record_count=None, copy_master=True):
        """ returns master channel samples for given group

        Parameters
        ----------
        index : int
            group index
        data : (bytes, int)
            (data block raw bytes, fragment offset); default None
        raster : float
            raster to be used for interpolation; default None
        record_offset : int
            if *data=None* use this to select the record offset from which the
            group data should be loaded
        record_count : int
            number of records to read; default *None* and in this case all
            available records are used
        copy_master : bool
            return a copy of the cached master

        Returns
        -------
        t : numpy.array
            master channel samples

        """
        fragment = data
        if fragment:
            data_bytes, offset, _count = fragment
            try:
                timestamps = self._master_channel_cache[(index, offset, _count)]
                if raster and len(timestamps):
                    timestamps = arange(timestamps[0], timestamps[-1], raster)
                    return timestamps
                else:
                    if copy_master:
                        return timestamps.copy()
                    else:
                        return timestamps
            except KeyError:
                pass
        else:
            try:
                timestamps = self._master_channel_cache[index]
                if raster and len(timestamps):
                    timestamps = arange(timestamps[0], timestamps[-1], raster)
                    return timestamps
                else:
                    if copy_master:
                        return timestamps.copy()
                    else:
                        return timestamps
            except KeyError:
                offset = 0

        group = self.groups[index]

        original_data = fragment

        if group["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
            stream = self._file
        else:
            stream = self._tempfile
        memory = self.memory

        time_ch_nr = self.masters_db.get(index, None)
        channel_group = group["channel_group"]
        record_size = channel_group["samples_byte_nr"]
        record_size += channel_group["invalidation_bytes_nr"]
        cycles_nr = group["channel_group"]["cycles_nr"]

        if original_data:
            cycles_nr = len(data_bytes) // record_size
        else:
            _count = record_count

        if time_ch_nr is None:
            if record_size:
                offset = offset // record_size
                t = arange(cycles_nr, dtype=float64)
                t += offset
            else:
                t = array([], dtype=float64)
            metadata = ("time", v4c.SYNC_TYPE_TIME)
        else:

            time_ch = group["channels"][time_ch_nr]
            if memory == "minimum":
                time_ch = Channel(
                    address=group["channels"][time_ch_nr],
                    stream=stream,
                    cc_map=self._cc_map,
                    si_map=self._si_map,
                    use_display_names=False,
                )
            time_conv = time_ch.conversion
            time_name = time_ch.name

            metadata = (time_name, time_ch["sync_type"])

            if time_ch["channel_type"] == v4c.CHANNEL_TYPE_VIRTUAL_MASTER:
                offset = offset // record_size
                time_a = time_conv["a"]
                time_b = time_conv["b"]
                t = arange(cycles_nr, dtype=float64)
                t += offset
                t *= time_a
                t += time_b

            else:
                # get data group parents and dtypes
                try:
                    parents, dtypes = group["parents"], group["types"]
                except KeyError:
                    parents, dtypes = self._prepare_record(group)
                    group["parents"], group["types"] = parents, dtypes

                # get data
                if fragment is None:
                    data = self._load_data(group, record_offset=record_offset, record_count=record_count)
                else:
                    data = (fragment,)
                time_values = []

                for fragment in data:
                    data_bytes, offset, _count = fragment
                    try:
                        parent, _ = parents[time_ch_nr]
                    except KeyError:
                        parent = None
                    if parent is not None:
                        not_found = object()
                        record = group.get("record", not_found)
                        if record is not_found:
                            if dtypes.itemsize:
                                record = fromstring(data_bytes, dtype=dtypes)
                            else:
                                record = None

                            if memory == "full":
                                group["record"] = record

                        t = record[parent]
                    else:
                        t = self._get_not_byte_aligned_data(
                            data_bytes, group, time_ch_nr
                        )

                    time_values.append(t.copy())

                if len(time_values) > 1:
                    t = concatenate(time_values)
                else:
                    t = time_values[0]

                # get timestamps
                if time_conv:
                    t = time_conv.convert(t)

        self._master_channel_metadata[index] = metadata

        if not t.dtype == float64:
            t = t.astype(float64)

        if original_data is None:
            self._master_channel_cache[index] = t
        else:
            data_bytes, offset, _ = original_data
            self._master_channel_cache[(index, offset, _count)] = t

        if raster and t.size:
            timestamps = t
            if len(t) > 1:
                num = float(
                    float32((timestamps[-1] - timestamps[0]) / raster)
                )
                if int(num) == num:
                    timestamps = linspace(
                        t[0],
                        t[-1],
                        int(num),
                    )
                else:
                    timestamps = arange(t[0], t[-1], raster)
            return timestamps
        else:
            timestamps = t
            if copy_master:
                return timestamps.copy()
            else:
                return timestamps

    def get_can_signal(
        self, name, database=None, db=None, ignore_invalidation_bits=False
    ):
        """ get CAN message signal. You can specify an external CAN database (
        *database* argument) or canmatrix databse object that has already been
        loaded from a file (*db* argument).

        The signal name can be specified in the following ways

        * ``CAN<ID>.<MESSAGE_NAME>.<SIGNAL_NAME>`` - the `ID` value starts from 1
          and must match the ID found in the measurement (the source CAN bus ID)
          Example: CAN1.Wheels.FL_WheelSpeed

        * ``CAN<ID>.CAN_DataFrame_<MESSAGE_ID>.<SIGNAL_NAME>`` - the `ID` value
          starts from 1 and the `MESSAGE_ID` is the decimal message ID as found
          in the database. Example: CAN1.CAN_DataFrame_218.FL_WheelSpeed

        * ``<MESSAGE_NAME>.SIGNAL_NAME`` - in this case the first occurence of
          the message name and signal are returned (the same message could be
          found on muplit CAN buses; for example on CAN1 and CAN3)
          Example: Wheels.FL_WheelSpeed

        * ``CAN_DataFrame_<MESSAGE_ID>.<SIGNAL_NAME>`` - in this case the first
          occurence of the message name and signal are returned (the same
          message could be found on muplit CAN buses; for example on CAN1 and
          CAN3). Example: CAN_DataFrame_218.FL_WheelSpeed

        * ``<SIGNAL_NAME>`` - in this case the first occurence of the signal
          name is returned ( the same signal anme coudl be found in multiple
          messages and on multiple CAN buses). Example: FL_WheelSpeed


        Parameters
        ----------
        name : str
            signal name
        database : str
            path of external CAN database file (.dbc or .arxml); default *None*
        db : canmatrix.database
            canmatrix CAN database object; default *None*
        ignore_invalidation_bits : bool
            option to ignore invalidation bits

        Returns
        -------
        sig : Signal
            Signal object with the physical values

        """

        if database is None and db is None:
            return self.get(name)

        if db is None:

            if not database.lower().endswith(("dbc", "arxml")):
                message = 'Expected .dbc or .arxml file as CAN channel attachment but got "{}"'.format(
                    database
                )
                logger.exception(message)
                raise MdfException(message)
            else:
                import_type = "dbc" if database.lower().endswith("dbc") else "arxml"
                with open(database, "rb") as db:
                    db_string = db.read()
                md5_sum = md5().update(db_string).digest()

                if md5_sum in self._external_dbc_cache:
                    db = self._external_dbc_cache[md5_sum]
                else:
                    try:
                        db_string = db_string.decode("utf-8")
                        db = self._external_dbc_cache[md5_sum] = loads(
                            db_string, importType=import_type, key="db"
                        )["db"]
                    except UnicodeDecodeError:
                        try:
                            from cchardet import detect

                            encoding = detect(db_string)["encoding"]
                            db_string = db_string.decode(encoding)
                            db = self._dbc_cache[md5_sum] = loads(
                                db_string,
                                importType=import_type,
                                key="db",
                                encoding=encoding,
                            )["db"]
                        except ImportError:
                            message = (
                                "Unicode exception occured while processing the database "
                                'attachment "{}" and "cChardet" package is '
                                'not installed. Mdf version 4 expects "utf-8" '
                                "strings and this package may detect if a different"
                                " encoding was used"
                            ).format(database)
                            logger.warning(message)

        name_ = name.split(".")

        if len(name_) == 3:
            can_id_str, message_id_str, signal = name_

            can_id = v4c.CAN_ID_PATTERN.search(can_id_str)
            if can_id is None:
                raise MdfException(
                    'CAN id "{}" of signal name "{}" is not recognised by this library'.format(
                        can_id_str, name
                    )
                )
            else:
                can_id = "CAN{}".format(can_id.group("id"))

            message_id = v4c.CAN_DATA_FRAME_PATTERN.search(message_id_str)
            if message_id is None:
                message_id = message_id_str
            else:
                message_id = int(message_id)

        elif len(name_) == 2:
            message_id_str, signal = name_

            can_id = None

            message_id = v4c.CAN_DATA_FRAME_PATTERN.search(message_id_str)
            if message_id is None:
                message_id = message_id_str
            else:
                message_id = int(message_id)

        else:
            can_id = message_id = None
            signal = name

        if isinstance(message_id, str):
            message = db.frameByName(message_id)
        else:
            message = db.frameById(message_id)

        for sig in message.signals:
            if sig.name == signal:
                signal = sig
                break
        else:
            raise MdfException(
                'Signal "{}" not found in message "{}" of "{}"'.format(
                    signal, message.name, database
                )
            )

        if can_id is None:
            for _can_id, messages in self.can_logging_db.items():
                if message.id in messages:
                    index = messages[message.id]
                    break
            else:
                raise MdfException(
                    'Message "{}" (ID={}) not found in the measurement'.format(
                        message.name, hex(message.id)
                    )
                )
        else:
            if can_id in self.can_logging_db:
                if message.id in self.can_logging_db[can_id]:
                    index = self.can_logging_db[can_id][message.id]
                else:
                    raise MdfException(
                        'Message "{}" (ID={}) not found in the measurement'.format(
                            message.name, hex(message.id)
                        )
                    )
            else:
                raise MdfException(
                    'No logging from "{}" was found in the measurement'.format(can_id)
                )

        can_ids = self.get(
            "CAN_DataFrame.ID",
            group=index,
            ignore_invalidation_bits=ignore_invalidation_bits,
        )
        payload = self.get(
            "CAN_DataFrame.DataBytes",
            group=index,
            samples_only=True,
            ignore_invalidation_bits=ignore_invalidation_bits,
        )[0]

        idx = nonzero(can_ids.samples == message.id)[0]
        data = payload[idx]
        t = can_ids.timestamps[idx].copy()
        if can_ids.invalidation_bits is not None:
            invalidation_bits = can_ids.invalidation_bits
        else:
            invalidation_bits = None

        record_size = data.shape[1]

        big_endian = False if signal.is_little_endian else True
        signed = signal.is_signed
        bit_offset = signal.startBit % 8
        byte_offset = signal.startBit // 8

        bit_count = signal.size

        byte_count = bit_offset + bit_count
        if byte_count % 8:
            byte_count = (byte_count >> 3) + 1
        else:
            byte_count //= 8

        types = [
            ("", "a{}".format(byte_offset)),
            ("vals", "({},)u1".format(byte_count)),
            ("", "a{}".format(record_size - byte_count - byte_offset)),
        ]

        vals = fromstring(data.tostring(), dtype=dtype(types))

        vals = vals["vals"]

        if not big_endian:
            vals = flip(vals, 1)

        vals = unpackbits(vals)
        vals = roll(vals, bit_offset)
        vals = vals.reshape((len(vals) // 8, 8))
        vals = packbits(vals)
        vals = vals.reshape((len(vals) // byte_count, byte_count))

        if bit_count < 64:
            mask = 2 ** bit_count - 1
            masks = []
            while mask:
                masks.append(mask & 0xFF)
                mask >>= 8
            for i in range(byte_count - len(masks)):
                masks.append(0)

            masks = masks[::-1]
            for i, mask in enumerate(masks):
                vals[:, i] &= mask

        if not big_endian:
            vals = flip(vals, 1)

        if bit_count <= 8:
            size = 1
        elif bit_count <= 16:
            size = 2
        elif bit_count <= 32:
            size = 4
        elif bit_count <= 64:
            size = 8
        else:
            size = bit_count // 8

        if size > byte_count:
            extra_bytes = size - byte_count
            extra = zeros((len(vals), extra_bytes), dtype=uint8)

            types = [
                ("vals", vals.dtype, vals.shape[1:]),
                ("", extra.dtype, extra.shape[1:]),
            ]
            vals = fromarrays([vals, extra], dtype=dtype(types))

        vals = vals.tostring()

        fmt = "{}u{}".format(">" if big_endian else "<", size)
        if size <= byte_count:
            if big_endian:
                types = [("", "a{}".format(byte_count - size)), ("vals", fmt)]
            else:
                types = [("vals", fmt), ("", "a{}".format(byte_count - size))]
        else:
            types = [("vals", fmt)]

        vals = fromstring(vals, dtype=dtype(types))

        if signed:
            vals = as_non_byte_sized_signed_int(vals["vals"], bit_count)
        else:
            vals = vals["vals"]

        comment = signal.comment or ""

        if (signal.factor, signal.offset) != (1, 0):
            vals = vals * float(signal.factor) + float(signal.offset)

        if ignore_invalidation_bits:

            return Signal(
                samples=vals,
                timestamps=t,
                name=name,
                unit=signal.unit or "",
                comment=comment,
                invalidation_bits=invalidation_bits,
            )

        else:

            if invalidation_bits is not None:
                vals = vals[nonzero(~invalidation_bits)[0]]
                t = t[nonzero(~invalidation_bits)[0]]

            return Signal(
                samples=vals,
                timestamps=t,
                name=name,
                unit=signal.unit or "",
                comment=comment,
            )

    def info(self):
        """get MDF information as a dict

        Examples
        --------
        >>> mdf = MDF4('test.mdf')
        >>> mdf.info()


        """
        info = {}
        info["version"] = (
            self.identification["version_str"].decode("utf-8").strip(" \n\t\0")
        )
        info["groups"] = len(self.groups)
        for i, gp in enumerate(self.groups):
            if gp["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
                stream = self._file
            elif gp["data_location"] == v4c.LOCATION_TEMPORARY_FILE:
                stream = self._tempfile
            inf = {}
            info["group {}".format(i)] = inf
            inf["cycles"] = gp["channel_group"]["cycles_nr"]
            inf["comment"] = gp["channel_group"].comment
            inf["channels count"] = len(gp["channels"])
            for j, channel in enumerate(gp["channels"]):
                if self.memory == "minimum":
                    channel = Channel(
                        address=channel,
                        stream=stream,
                        use_display_names=self._use_display_names,
                    )
                name = channel.name

                ch_type = v4c.CHANNEL_TYPE_TO_DESCRIPTION[channel["channel_type"]]
                inf["channel {}".format(j)] = 'name="{}" type={}'.format(name, ch_type)

        return info

    def save(self, dst="", overwrite=False, compression=0):
        """Save MDF to *dst*. If *dst* is not provided the the destination file
        name is the MDF name. If overwrite is *True* then the destination file
        is overwritten, otherwise the file name is appened with '_<cntr>', were
        '<cntr>' is the first conter that produces a new file name
        (that does not already exist in the filesystem)

        Parameters
        ----------
        dst : str
            destination file name, Default ''
        overwrite : bool
            overwrite flag, default *False*
        compression : int
            use compressed data blocks, default 0; valid since version 4.10

            * 0 - no compression
            * 1 - deflate (slower, but produces smaller files)
            * 2 - transposition + deflate (slowest, but produces
              the smallest files)

        Returns
        -------
        output_file : str
            output file name

        """

        if self.name is None and dst == "":
            message = (
                "Must specify a destination file name " "for MDF created from scratch"
            )
            raise MdfException(message)

        destination_dir = os.path.dirname(dst)
        if destination_dir and not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        if self.memory == "minimum":
            output_file = self._save_without_metadata(dst, overwrite, compression)
        else:
            output_file = self._save_with_metadata(dst, overwrite, compression)

        if self._callback:
            self._callback(100, 100)

        return output_file

    def _save_with_metadata(self, dst, overwrite, compression):
        """Save MDF to *dst*. If *dst* is not provided the the destination file
        name is the MDF name. If overwrite is *True* then the destination file
        is overwritten, otherwise the file name is appened with '_<cntr>', were
        '<cntr>' is the first conter that produces a new file name
        (that does not already exist in the filesystem)

        Parameters
        ----------
        dst : str
            destination file name, Default ''
        overwrite : bool
            overwrite flag, default *False*
        compression : int
            use compressed data blocks, default 0; valid since version 4.10

            * 0 - no compression
            * 1 - deflate (slower, but produces smaller files)
            * 2 - transposition + deflate (slowest, but produces
              the smallest files)

        """
        if self.name is None and dst == "":
            message = (
                "Must specify a destination file name " "for MDF created from scratch"
            )
            raise MdfException(message)

        dst = dst if dst else self.name
        if not dst.endswith(("mf4", "MF4")):
            dst = dst + ".mf4"
        if overwrite is False:
            if os.path.isfile(dst):
                cntr = 0
                while True:
                    name = os.path.splitext(dst)[0] + "_{}.mf4".format(cntr)
                    if not os.path.isfile(name):
                        break
                    else:
                        cntr += 1
                message = (
                    'Destination file "{}" already exists '
                    'and "overwrite" is False. Saving MDF file as "{}"'
                )
                message = message.format(dst, name)
                logger.warning(message)
                dst = name

        if not self.file_history:
            comment = "created"
        else:
            comment = "updated"

        fh = FileHistory()
        fh.comment = """<FHcomment>
<TX>{}</TX>
<tool_id>asammdf</tool_id>
<tool_vendor>asammdf</tool_vendor>
<tool_version>{}</tool_version>
</FHcomment>""".format(
            comment, __version__
        )

        self.file_history.append(fh)

        if self.memory == "low" and dst == self.name:
            destination = dst + ".temp"
        else:
            destination = dst

        with open(destination, "wb+") as dst_:
            defined_texts = {}
            cc_map = {}
            si_map = {}

            groups_nr = len(self.groups)

            write = dst_.write
            tell = dst_.tell
            seek = dst_.seek

            write(bytes(self.identification))
            self.header.to_stream(dst_)

            original_data_addresses = []

            if compression == 1:
                zip_type = v4c.FLAG_DZ_DEFLATE
            else:
                zip_type = v4c.FLAG_DZ_TRANPOSED_DEFLATE

            # write DataBlocks first
            for gp_nr, gp in enumerate(self.groups):
                original_data_addresses.append(gp["data_group"]["data_block_addr"])

                if gp["channel_group"]["flags"] & v4c.FLAG_CG_VLSD:
                    continue

                address = tell()

                data = self._load_data(gp)

                total_size = (
                    gp["channel_group"]["samples_byte_nr"]
                    + gp["channel_group"]["invalidation_bytes_nr"]
                ) * gp["channel_group"]["cycles_nr"]

                if self._write_fragment_size:

                    samples_size = (
                        gp["channel_group"]["samples_byte_nr"]
                        + gp["channel_group"]["invalidation_bytes_nr"]
                    )
                    if samples_size:
                        split_size = self._write_fragment_size // samples_size
                        split_size *= samples_size
                        if split_size == 0:
                            chunks = 1
                        else:
                            chunks = float(total_size) / split_size
                            chunks = int(ceil(chunks))
                    else:
                        chunks = 1
                else:
                    chunks = 1

                if chunks == 1:
                    if PYVERSION == 3:
                        data = b"".join(d[0] for d in data)
                    else:
                        data = b"".join(str(d[0]) for d in data)
                    if compression and self.version > "4.00":
                        if compression == 1:
                            param = 0
                        else:
                            param = (
                                gp["channel_group"]["samples_byte_nr"]
                                + gp["channel_group"]["invalidation_bytes_nr"]
                            )
                        kargs = {"data": data, "zip_type": zip_type, "param": param}
                        data_block = DataZippedBlock(**kargs)
                    else:
                        data_block = DataBlock(data=data)
                    write(bytes(data_block))

                    align = data_block["block_len"] % 8
                    if align:
                        write(b"\0" * (8 - align))

                    if gp["channel_group"]["cycles_nr"]:
                        gp["data_group"]["data_block_addr"] = address
                    else:
                        gp["data_group"]["data_block_addr"] = 0
                else:
                    kargs = {"flags": v4c.FLAG_DL_EQUAL_LENGHT, "zip_type": zip_type}
                    hl_block = HeaderList(**kargs)

                    kargs = {
                        "flags": v4c.FLAG_DL_EQUAL_LENGHT,
                        "links_nr": chunks + 1,
                        "data_block_nr": chunks,
                        "data_block_len": split_size,
                    }
                    dl_block = DataList(**kargs)

                    cur_data = b""

                    if self.memory == "low":
                        for i in range(chunks):
                            while len(cur_data) < split_size:
                                try:
                                    cur_data += next(data)[0]
                                except StopIteration:
                                    break

                            data_, cur_data = (
                                cur_data[:split_size],
                                cur_data[split_size:],
                            )
                            if compression and self.version > "4.00":
                                if compression == 1:
                                    zip_type = v4c.FLAG_DZ_DEFLATE
                                else:
                                    zip_type = v4c.FLAG_DZ_TRANPOSED_DEFLATE
                                if compression == 1:
                                    param = 0
                                else:
                                    param = (
                                        gp["channel_group"]["samples_byte_nr"]
                                        + gp["channel_group"]["invalidation_bytes_nr"]
                                    )
                                kargs = {
                                    "data": data_,
                                    "zip_type": zip_type,
                                    "param": param,
                                }
                                block = DataZippedBlock(**kargs)
                            else:
                                block = DataBlock(data=data_)
                            address = tell()
                            block.address = address

                            write(bytes(block))

                            align = block["block_len"] % 8
                            if align:
                                write(b"\0" * (8 - align))
                            dl_block["data_block_addr{}".format(i)] = address
                    else:
                        cur_data = next(data)[0]
                        for i in range(chunks):

                            data_ = cur_data[i * split_size : (i + 1) * split_size]
                            if compression and self.version > "4.00":
                                if compression == 1:
                                    zip_type = v4c.FLAG_DZ_DEFLATE
                                    param = 0
                                else:
                                    zip_type = v4c.FLAG_DZ_TRANPOSED_DEFLATE
                                    param = (
                                        gp["channel_group"]["samples_byte_nr"]
                                        + gp["channel_group"]["invalidation_bytes_nr"]
                                    )
                                kargs = {
                                    "data": data_,
                                    "zip_type": zip_type,
                                    "param": param,
                                }
                                block = DataZippedBlock(**kargs)
                            else:
                                block = DataBlock(data=data_)
                            address = tell()
                            block.address = address

                            write(bytes(block))

                            align = block["block_len"] % 8
                            if align:
                                write(b"\0" * (8 - align))
                            dl_block["data_block_addr{}".format(i)] = address

                    address = tell()
                    dl_block.address = address
                    write(bytes(dl_block))

                    if compression and self.version != "4.00":
                        hl_block["first_dl_addr"] = address
                        address = tell()
                        hl_block.address = address
                        write(bytes(hl_block))

                    gp["data_group"]["data_block_addr"] = address

                if self._callback:
                    self._callback(int(50 * (gp_nr + 1) / groups_nr), 100)
                if self._terminate:
                    dst_.close()
                    self.close()
                    return

            address = tell()

            blocks = []

            # attachments
            at_map = {}
            if self.attachments:
                for at_block in self.attachments:
                    address = at_block.to_blocks(address, blocks, defined_texts)

                for i in range(len(self.attachments) - 1):
                    at_block = self.attachments[i]
                    at_block["next_at_addr"] = self.attachments[i + 1].address
                self.attachments[-1]["next_at_addr"] = 0

            # file history blocks
            for fh in self.file_history:
                address = fh.to_blocks(address, blocks, defined_texts)

            for i, fh in enumerate(self.file_history[:-1]):
                fh["next_fh_addr"] = self.file_history[i + 1].address
            self.file_history[-1]["next_fh_addr"] = 0

            # data groups
            gp_rec_ids = []
            valid_data_groups = []
            for gp in self.groups:
                if gp["channel_group"]["flags"] & v4c.FLAG_CG_VLSD:
                    continue

                valid_data_groups.append(gp["data_group"])
                gp_rec_ids.append(gp["data_group"]["record_id_len"])

                address = gp["data_group"].to_blocks(address, blocks, defined_texts)

            if valid_data_groups:
                for i, dg in enumerate(valid_data_groups[:-1]):
                    addr_ = valid_data_groups[i + 1].address
                    dg["next_dg_addr"] = addr_
                valid_data_groups[-1]["next_dg_addr"] = 0

            # go through each data group and append the rest of the blocks
            for i, gp in enumerate(self.groups):

                for channel in gp["channels"]:
                    if channel["channel_type"] == v4c.CHANNEL_TYPE_SYNC:
                        idx = self._attachments_map[channel["data_block_addr"]]
                        channel["data_block_addr"] = self.attachments[idx].address

                    if channel.attachments:
                        for j, idx in enumerate(channel.attachments):
                            key = "attachment_{}_addr".format(j)
                            channel[key] = self.attachments[idx].address

                    address = channel.to_blocks(
                        address, blocks, defined_texts, cc_map, si_map
                    )

                # channel data
                gp_sd = []
                for j, sdata in enumerate(gp["signal_data"]):
                    sdata = self._load_signal_data(group=gp, index=j)
                    if sdata:
                        split_size = self._write_fragment_size
                        if self._write_fragment_size:
                            chunks = float(len(sdata)) / split_size
                            chunks = int(ceil(chunks))
                        else:
                            chunks = 1

                        if chunks == 1:
                            if compression and self.version > "4.00":
                                signal_data = DataZippedBlock(
                                    data=sdata,
                                    zip_type=v4c.FLAG_DZ_DEFLATE,
                                    original_type=b"SD",
                                )
                                signal_data.address = address
                                address += signal_data["block_len"]
                                blocks.append(signal_data)
                                align = signal_data["block_len"] % 8
                                if align:
                                    blocks.append(b"\0" * (8 - align))
                                    address += 8 - align
                            else:
                                signal_data = DataBlock(data=sdata, type="SD")
                                signal_data.address = address
                                address += signal_data["block_len"]
                                blocks.append(signal_data)
                                align = signal_data["block_len"] % 8
                                if align:
                                    blocks.append(b"\0" * (8 - align))
                                    address += 8 - align
                            gp_sd.append(signal_data)
                        else:
                            kargs = {
                                "flags": v4c.FLAG_DL_EQUAL_LENGHT,
                                "links_nr": chunks + 1,
                                "data_block_nr": chunks,
                                "data_block_len": self._write_fragment_size,
                            }
                            dl_block = DataList(**kargs)

                            for k in range(chunks):

                                data_ = sdata[k * split_size : (k + 1) * split_size]
                                if compression and self.version > "4.00":
                                    zip_type = v4c.FLAG_DZ_DEFLATE
                                    param = 0

                                    kargs = {
                                        "data": data_,
                                        "zip_type": zip_type,
                                        "param": param,
                                        "original_type": b"SD",
                                    }
                                    block = DataZippedBlock(**kargs)
                                else:
                                    block = DataBlock(data=data_, type="SD")
                                blocks.append(block)
                                block.address = address
                                address += block["block_len"]

                                align = block["block_len"] % 8
                                if align:
                                    blocks.append(b"\0" * (8 - align))
                                    address += 8 - align
                                dl_block["data_block_addr{}".format(k)] = block.address

                            dl_block.address = address
                            blocks.append(dl_block)

                            address += dl_block["block_len"]

                            if compression and self.version > "4.00":
                                kargs = {
                                    "flags": v4c.FLAG_DL_EQUAL_LENGHT,
                                    "zip_type": v4c.FLAG_DZ_DEFLATE,
                                    "first_dl_addr": dl_block.address,
                                }
                                hl_block = HeaderList(**kargs)
                                hl_block.address = address
                                address += hl_block["block_len"]

                                blocks.append(hl_block)

                                gp_sd.append(hl_block)
                            else:
                                gp_sd.append(dl_block)

                    else:
                        gp_sd.append(None)

                # channel dependecies
                for j, dep_list in enumerate(gp["channel_dependencies"]):
                    if dep_list:
                        if all(isinstance(dep, ChannelArrayBlock) for dep in dep_list):
                            for dep in dep_list:
                                dep.address = address
                                address += dep["block_len"]
                                blocks.append(dep)
                            for k, dep in enumerate(dep_list[:-1]):
                                dep["composition_addr"] = dep_list[k + 1].address
                            dep_list[-1]["composition_addr"] = 0

                # channels
                for j, (channel, signal_data) in enumerate(zip(gp["channels"], gp_sd)):

                    if signal_data:
                        channel["data_block_addr"] = signal_data.address
                    elif channel["channel_type"] == v4c.CHANNEL_TYPE_SYNC:
                        pass
                    else:
                        channel["data_block_addr"] = 0

                    if gp["channel_dependencies"][j]:
                        dep = gp["channel_dependencies"][j][0]
                        if isinstance(dep, tuple):
                            index = dep[1]
                            addr_ = gp["channels"][index].address
                        else:
                            addr_ = dep.address
                        channel["component_addr"] = addr_

                for channel in gp["logging_channels"]:
                    address = channel.to_blocks(
                        address, blocks, defined_texts, cc_map, si_map
                    )

                group_channels = list(chain(gp["channels"], gp["logging_channels"]))
                if group_channels:
                    for j, channel in enumerate(group_channels[:-1]):
                        channel["next_ch_addr"] = group_channels[j + 1].address
                    group_channels[-1]["next_ch_addr"] = 0

                # channel dependecies
                j = len(gp["channels"]) - 1
                while j >= 0:
                    dep_list = gp["channel_dependencies"][j]
                    if dep_list and all(isinstance(dep, tuple) for dep in dep_list):
                        index = dep_list[0][1]
                        gp["channels"][j]["component_addr"] = gp["channels"][
                            index
                        ].address
                        index = dep_list[-1][1]
                        gp["channels"][j]["next_ch_addr"] = gp["channels"][index][
                            "next_ch_addr"
                        ]
                        gp["channels"][index]["next_ch_addr"] = 0

                        for _, ch_nr in dep_list:
                            gp["channels"][ch_nr]["source_addr"] = 0
                    j -= 1

                # channel group
                if gp["channel_group"]["flags"] & v4c.FLAG_CG_VLSD:
                    continue

                # sample reduction blocks
                next_sr_addr = 0
                dim = len(gp["reduction_blocks"])
                for idx in range(dim - 1, -1, -1):
                    sr = gp["reduction_blocks"][idx]
                    data = gp["reduction_data_block"][idx]
                    if self.memory != "full":
                        bts = b"".join(e[0] for e in self._load_data(gp, idx))
                        data = DataBlock(data=bts, type="RD")

                    sr["data_block_addr"] = data.address = address
                    sr["next_sr_addr"] = next_sr_addr
                    address += data["block_len"]
                    blocks.append(data)
                    sr.adddress = next_sr_addr = address
                    address += sr["block_len"]
                    blocks.append(sr)

                gp["channel_group"]["first_sample_reduction_addr"] = next_sr_addr

                if gp["channels"]:
                    gp["channel_group"]["first_ch_addr"] = gp["channels"][0].address
                else:
                    gp["channel_group"]["first_ch_addr"] = 0
                gp["channel_group"]["next_cg_addr"] = 0

                address = gp["channel_group"].to_blocks(
                    address, blocks, defined_texts, si_map
                )
                gp["data_group"]["first_cg_addr"] = gp["channel_group"].address

                if self._callback:
                    self._callback(int(50 * (i + 1) / groups_nr) + 25, 100)
                if self._terminate:
                    dst_.close()
                    self.close()
                    return

            for gp in self.groups:
                for dep_list in gp["channel_dependencies"]:
                    if dep_list:
                        if all(isinstance(dep, ChannelArrayBlock) for dep in dep_list):
                            for dep in dep_list:
                                if dep["ca_type"] != v4c.CA_TYPE_LOOKUP:
                                    dep.referenced_channels = []
                                    continue
                                for i, (gp_nr, ch_nr) in enumerate(
                                    dep.referenced_channels
                                ):
                                    grp = self.groups[gp_nr]
                                    ch = grp["channels"][ch_nr]
                                    dep["scale_axis_{}_dg_addr".format(i)] = grp[
                                        "data_group"
                                    ].address
                                    dep["scale_axis_{}_cg_addr".format(i)] = grp[
                                        "channel_group"
                                    ].address
                                    dep["scale_axis_{}_ch_addr".format(i)] = ch.address

            for gp in self.groups:
                gp["data_group"]["record_id_len"] = 0

            ev_map = []

            if self.events:
                for event in self.events:
                    for i, ref in enumerate(event.scopes):
                        try:
                            dg_cntr, ch_cntr = ref
                            event["scope_{}_addr".format(i)] = self.groups[dg_cntr][
                                "channels"
                            ][ch_cntr].address
                        except TypeError:
                            dg_cntr = ref
                            event["scope_{}_addr".format(i)] = self.groups[dg_cntr][
                                "channel_group"
                            ].address
                    for i in range(event["attachment_nr"]):
                        key = "attachment_{}_addr".format(i)
                        addr = event[key]
                        event[key] = at_map[addr]

                    blocks.append(event)
                    ev_map.append(address)
                    event.address = address
                    address += event["block_len"]

                    if event.name:
                        tx_block = TextBlock(text=event.name)
                        tx_block.address = address
                        blocks.append(tx_block)
                        address += tx_block["block_len"]
                        event["name_addr"] = tx_block.address
                    else:
                        event["name_addr"] = 0

                    if event.comment:
                        meta = event.comment.startswith("<EVcomment")
                        tx_block = TextBlock(text=event.comment, meta=meta)
                        tx_block.address = address
                        blocks.append(tx_block)
                        address += tx_block["block_len"]
                        event["comment_addr"] = tx_block.address
                    else:
                        event["comment_addr"] = 0

                    if event.parent is not None:
                        event["parent_ev_addr"] = ev_map[event.parent]
                    if event.range_start is not None:
                        event["range_start_ev_addr"] = ev_map[event.range_start]

                for i in range(len(self.events) - 1):
                    self.events[i]["next_ev_addr"] = self.events[i + 1].address
                self.events[-1]["next_ev_addr"] = 0

                self.header["first_event_addr"] = self.events[0].address

            if self._terminate:
                dst_.close()
                self.close()
                return

            if self._callback:
                blocks_nr = len(blocks)
                threshold = blocks_nr / 25
                count = 1
                for i, block in enumerate(blocks):
                    write(bytes(block))
                    if i >= threshold:
                        self._callback(75 + count, 100)
                        count += 1
                        threshold += blocks_nr / 25
            else:
                for block in blocks:
                    write(bytes(block))

            for gp, rec_id in zip(self.groups, gp_rec_ids):
                gp["data_group"]["record_id_len"] = rec_id

            if valid_data_groups:
                addr_ = valid_data_groups[0].address
                self.header["first_dg_addr"] = addr_
            else:
                self.header["first_dg_addr"] = 0
            self.header["file_history_addr"] = self.file_history[0].address
            if self.attachments:
                first_attachment = self.attachments[0]
                addr_ = first_attachment.address
                self.header["first_attachment_addr"] = addr_
            else:
                self.header["first_attachment_addr"] = 0

            seek(v4c.IDENTIFICATION_BLOCK_SIZE)
            write(bytes(self.header))

            for orig_addr, gp in zip(original_data_addresses, self.groups):
                gp["data_group"]["data_block_addr"] = orig_addr

            at_map = {value: key for key, value in at_map.items()}

            for event in self.events:
                for i in range(event["attachment_nr"]):
                    key = "attachment_{}_addr".format(i)
                    addr = event[key]
                    event[key] = at_map[addr]

        if self.memory == "low" and dst == self.name:
            self.close()
            os.remove(self.name)
            os.rename(destination, self.name)

            self.groups.clear()
            self.header = None
            self.identification = None
            self.file_history.clear()
            self.channels_db.clear()
            self.masters_db.clear()
            self.attachments.clear()
            self.file_comment = None

            self._ch_map.clear()
            self._master_channel_cache.clear()

            self._tempfile = TemporaryFile()
            self._file = open(self.name, "rb")
            self._read()

        return dst

    def _save_without_metadata(self, dst, overwrite, compression):
        """Save MDF to *dst*. If *dst* is not provided the the destination file
        name is the MDF name. If overwrite is *True* then the destination file
        is overwritten, otherwise the file name is appened with '_<cntr>', were
        '<cntr>' is the first conter that produces a new file name
        (that does not already exist in the filesystem)

        Parameters
        ----------
        dst : str
            destination file name, Default ''
        overwrite : bool
            overwrite flag, default *False*
        compression : int
            use compressed data blocks, default 0; valid since version 4.10

            * 0 - no compression
            * 1 - deflate (slower, but produces smaller files)
            * 2 - transposition + deflate (slowest, but produces
              the smallest files)

        """
        if self.name is None and dst == "":
            message = (
                "Must specify a destination file name " "for MDF created from scratch"
            )
            raise MdfException(message)

        dst = dst if dst else self.name
        if not dst.endswith(("mf4", "MF4")):
            dst = dst + ".mf4"
        if overwrite is False:
            if os.path.isfile(dst):
                cntr = 0
                while True:
                    name = os.path.splitext(dst)[0] + "_{}.mf4".format(cntr)
                    if not os.path.isfile(name):
                        break
                    else:
                        cntr += 1
                message = (
                    'Destination file "{}" already exists '
                    'and "overwrite" is False. Saving MDF file as "{}"'
                )
                message = message.format(dst, name)
                logger.warning(message)
                dst = name

        if not self.file_history:
            comment = "created"
        else:
            comment = "updated"

        fh = FileHistory()
        fh.comment = """<FHcomment>
<TX>{}</TX>
<tool_id>asammdf</tool_id>
<tool_vendor>asammdf</tool_vendor>
<tool_version>{}</tool_version>
</FHcomment>""".format(
            comment, __version__
        )

        self.file_history.append(fh)

        if dst == self.name:
            destination = dst + ".temp"
        else:
            destination = dst

        with open(destination, "wb+") as dst_:
            defined_texts = {}
            file_cc_map = {}
            file_si_map = {}

            groups_nr = len(self.groups)

            write = dst_.write
            tell = dst_.tell
            seek = dst_.seek

            write(bytes(self.identification))
            self.header.to_stream(dst_)

            original_data_addresses = []

            if compression == 1:
                zip_type = v4c.FLAG_DZ_DEFLATE
            else:
                zip_type = v4c.FLAG_DZ_TRANPOSED_DEFLATE

            # write DataBlocks first
            for group_index, gp in enumerate(self.groups):
                original_data_addresses.append(gp["data_group"]["data_block_addr"])

                if gp["channel_group"]["flags"] & v4c.FLAG_CG_VLSD:
                    continue

                address = tell()

                data = self._load_data(gp)

                if self._write_fragment_size:
                    total_size = (
                        gp["channel_group"]["samples_byte_nr"]
                        + gp["channel_group"]["invalidation_bytes_nr"]
                    ) * gp["channel_group"]["cycles_nr"]
                    samples_size = (
                        gp["channel_group"]["samples_byte_nr"]
                        + gp["channel_group"]["invalidation_bytes_nr"]
                    )
                    if samples_size:
                        split_size = self._write_fragment_size // samples_size
                        split_size *= samples_size
                        if split_size == 0:
                            chunks = 1
                        else:
                            chunks = total_size / split_size
                            chunks = int(ceil(chunks))
                    else:
                        chunks = 1
                else:
                    chunks = 1

                if chunks == 1:
                    data = b"".join(d[0] for d in data)
                    if compression and self.version != "4.00":
                        if compression == 1:
                            param = 0
                        else:
                            param = (
                                gp["channel_group"]["samples_byte_nr"]
                                + gp["channel_group"]["invalidation_bytes_nr"]
                            )
                        kargs = {"data": data, "zip_type": zip_type, "param": param}
                        data_block = DataZippedBlock(**kargs)
                    else:
                        data_block = DataBlock(data=data)
                    write(bytes(data_block))

                    align = data_block["block_len"] % 8
                    if align:
                        write(b"\0" * (8 - align))

                    if gp["channel_group"]["cycles_nr"]:
                        gp["data_group"]["data_block_addr"] = address
                    else:
                        gp["data_group"]["data_block_addr"] = 0
                else:
                    kargs = {"flags": v4c.FLAG_DL_EQUAL_LENGHT, "zip_type": zip_type}
                    hl_block = HeaderList(**kargs)

                    kargs = {
                        "flags": v4c.FLAG_DL_EQUAL_LENGHT,
                        "links_nr": chunks + 1,
                        "data_block_nr": chunks,
                        "data_block_len": split_size,
                    }
                    dl_block = DataList(**kargs)

                    cur_data = b""

                    for i in range(chunks):
                        while len(cur_data) < split_size:
                            try:
                                cur_data += next(data)[0]
                            except StopIteration:
                                break

                        data_, cur_data = cur_data[:split_size], cur_data[split_size:]
                        if compression and self.version > "4.00":
                            if compression == 1:
                                zip_type = v4c.FLAG_DZ_DEFLATE
                                param = 0
                            else:
                                zip_type = v4c.FLAG_DZ_TRANPOSED_DEFLATE
                                param = (
                                    gp["channel_group"]["samples_byte_nr"]
                                    + gp["channel_group"]["invalidation_bytes_nr"]
                                )

                            kargs = {
                                "data": data_,
                                "zip_type": zip_type,
                                "param": param,
                            }
                            block = DataZippedBlock(**kargs)
                        else:
                            block = DataBlock(data=data_)
                        address = tell()
                        block.address = address

                        write(bytes(block))

                        align = block["block_len"] % 8
                        if align:
                            write(b"\0" * (8 - align))
                        dl_block["data_block_addr{}".format(i)] = address

                    address = tell()
                    dl_block.address = address
                    write(bytes(dl_block))

                    if compression and self.version != "4.00":
                        hl_block["first_dl_addr"] = address
                        address = tell()
                        hl_block.address = address
                        write(bytes(hl_block))

                    gp["data_group"]["data_block_addr"] = address

                if self._callback:
                    self._callback(int(50 * (group_index + 1) / groups_nr), 100)
                if self._terminate:
                    dst_.close()
                    self.close()
                    return

            address = tell()

            # attachments
            address = tell()
            blocks = []
            at_map = {}

            if self.attachments:
                for at_block in self.attachments:
                    address = at_block.to_blocks(address, blocks, defined_texts)

                for i in range(len(self.attachments) - 1):
                    at_block = self.attachments[i]
                    at_block["next_at_addr"] = self.attachments[i + 1].address
                self.attachments[-1]["next_at_addr"] = 0

            # file history blocks
            for fh in self.file_history:
                address = fh.to_blocks(address, blocks, defined_texts)

            for i, fh in enumerate(self.file_history[:-1]):
                fh["next_fh_addr"] = self.file_history[i + 1].address
            self.file_history[-1]["next_fh_addr"] = 0

            for blk in blocks:
                write(bytes(blk))

            del blocks

            address = tell()

            # go through each data group and append the rest of the blocks
            for i, gp in enumerate(self.groups):
                read_cc_map = {}
                read_si_map = {}

                gp["temp_channels"] = ch_addrs = []

                if gp["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
                    stream = self._file
                else:
                    stream = self._tempfile

                chans = gp["channels"] + gp["logging_channels"]

                # channel dependecies
                structs = [0 for _ in chans]

                temp_deps = []

                for j, dep_list in enumerate(
                    gp["channel_dependencies"] + [None for _ in gp["logging_channels"]]
                ):
                    if dep_list:
                        if all(isinstance(dep, ChannelArrayBlock) for dep in dep_list):
                            temp_deps.append([])

                            for dep in dep_list:
                                address = tell()
                                dep.address = address
                                temp_deps[-1].append(address)
                                write(bytes(dep))
                            for k, dep in enumerate(dep_list[:-1]):
                                dep["composition_addr"] = dep_list[k + 1].address
                            dep_list[-1]["composition_addr"] = 0
                        else:

                            temp_deps.append([])
                            level = structs[j]
                            for (_, ch_c) in dep_list:
                                structs[ch_c] = level + 1

                                temp_deps[-1].append(0)
                    else:
                        temp_deps.append(0)

                if structs:
                    next_ch_addr = [0 for _ in range(max(structs) + 1)]
                else:
                    next_ch_addr = []

                # channels
                address = blocks_start_addr = tell()

                size = len(chans)
                previous_level = structs[-1] if structs else 0
                for j in range(size - 1, -1, -1):
                    channel = chans[j]
                    level = structs[j]

                    if not isinstance(channel, Channel):
                        channel = Channel(
                            address=channel,
                            stream=stream,
                            use_display_names=False,
                            cc_map=read_cc_map,
                            si_map=read_si_map,
                        )

                    channel["next_ch_addr"] = next_ch_addr[level]
                    if level:
                        channel.source = None
                    elif temp_deps[j]:
                        channel["component_addr"] = temp_deps[j][0]
                    if level < previous_level:
                        channel["component_addr"] = next_ch_addr[previous_level]
                        next_ch_addr[previous_level] = 0

                    previous_level = level

                    try:
                        signal_data = self._load_signal_data(group=gp, index=j)
                    except IndexError:
                        signal_data = b""
                    if signal_data:
                        split_size = self._write_fragment_size
                        if self._write_fragment_size:
                            chunks = float(len(signal_data)) / split_size
                            chunks = int(ceil(chunks))
                        else:
                            chunks = 1

                        if chunks == 1:
                            if compression and self.version > "4.00":
                                signal_data = DataZippedBlock(
                                    data=signal_data,
                                    zip_type=v4c.FLAG_DZ_DEFLATE,
                                    original_type=b"SD",
                                )
                                channel["data_block_addr"] = address
                                address += signal_data["block_len"]
                                write(bytes(signal_data))
                                align = signal_data["block_len"] % 8
                                if align % 8:
                                    write(b"\0" * (8 - align))
                                    address += 8 - align
                            else:
                                signal_data = DataBlock(data=signal_data, type="SD")
                                channel["data_block_addr"] = address
                                write(bytes(signal_data))
                                address += signal_data["block_len"]
                                align = signal_data["block_len"] % 8
                                if align % 8:
                                    write(b"\0" * (8 - align))
                                    address += 8 - align
                        else:

                            kargs = {
                                "flags": v4c.FLAG_DL_EQUAL_LENGHT,
                                "links_nr": chunks + 1,
                                "data_block_nr": chunks,
                                "data_block_len": split_size,
                            }
                            dl_block = DataList(**kargs)

                            for k in range(chunks):

                                data_ = signal_data[
                                    k * split_size : (k + 1) * split_size
                                ]
                                if compression and self.version > "4.00":
                                    zip_type = v4c.FLAG_DZ_DEFLATE
                                    param = 0

                                    kargs = {
                                        "data": data_,
                                        "zip_type": zip_type,
                                        "param": param,
                                        "original_type": b"SD",
                                    }
                                    block = DataZippedBlock(**kargs)
                                else:
                                    block = DataBlock(data=data_, type="SD")

                                address = tell()
                                dl_block["data_block_addr{}".format(k)] = address
                                write(bytes(block))

                                align = block["block_len"] % 8
                                if align:
                                    write(b"\0" * (8 - align))

                            address = tell()
                            write(bytes(dl_block))

                            if compression and self.version != "4.00":
                                kargs = {
                                    "flags": v4c.FLAG_DL_EQUAL_LENGHT,
                                    "zip_type": zip_type,
                                    "first_dl_addr": address,
                                }
                                hl_block = HeaderList(**kargs)

                                address = tell()
                                write(bytes(hl_block))
                            channel["data_block_addr"] = address

                    elif channel["channel_type"] == v4c.CHANNEL_TYPE_SYNC:
                        idx = self._attachments_map[channel["data_block_addr"]]
                        channel["data_block_addr"] = self.attachments[idx].address
                    else:
                        channel["data_block_addr"] = 0

                    del signal_data

                    if channel.attachments:
                        for att_idx, idx in enumerate(channel.attachments):
                            key = "attachment_{}_addr".format(att_idx)
                            channel[key] = self.attachments[idx].address

                    address = channel.to_stream(dst_, defined_texts, file_cc_map, file_si_map)
                    ch_addrs.append(channel.address)
                    next_ch_addr[level] = channel.address

                ch_addrs.reverse()

                if next_ch_addr:
                    gp["channel_group"]["first_ch_addr"] = next_ch_addr[0]
                else:
                    gp["channel_group"]["first_ch_addr"] = 0

                if gp["channel_group"]["flags"] & v4c.FLAG_CG_VLSD:
                    continue

                # channel group
                gp["channel_group"]["next_cg_addr"] = 0

                # sample reduction blocks
                address = tell()
                next_sr_addr = 0
                dim = len(gp["reduction_blocks"])
                blocks = []
                for idx in range(dim - 1, -1, -1):
                    sr = gp["reduction_blocks"][idx]
                    bts = b"".join(e[0] for e in self._load_data(gp, idx))
                    data = DataBlock(data=bts, type="RD")

                    sr["data_block_addr"] = data.address = address
                    sr["next_sr_addr"] = next_sr_addr
                    address += data["block_len"]
                    blocks.append(data)
                    sr.adddress = next_sr_addr = address
                    address += sr["block_len"]
                    blocks.append(sr)
                gp["channel_group"]["first_sample_reduction_addr"] = next_sr_addr
                for block in blocks:
                    write(bytes(block))

                gp["channel_group"].to_stream(dst_, defined_texts, file_si_map)
                gp["data_group"]["first_cg_addr"] = gp["channel_group"].address

                if self._callback:
                    self._callback(int(50 * (i + 1) / groups_nr) + 50, 100)
                if self._terminate:
                    dst_.close()
                    self.close()
                    return

            blocks = []
            address = tell()
            gp_rec_ids = []
            valid_data_groups = []
            # data groups
            for gp in self.groups:

                gp_rec_ids.append(gp["data_group"]["record_id_len"])
                if gp["channel_group"]["flags"] & v4c.FLAG_CG_VLSD:
                    continue
                else:
                    valid_data_groups.append(gp["data_group"])

                    address = gp["data_group"].to_blocks(address, blocks, defined_texts)

            if valid_data_groups:
                for i, dg in enumerate(valid_data_groups[:-1]):
                    addr_ = valid_data_groups[i + 1].address
                    dg["next_dg_addr"] = addr_
                valid_data_groups[-1]["next_dg_addr"] = 0

            for gp in self.groups:
                gp["data_group"]["record_id_len"] = 0

            ev_map = {}
            if self.events:
                for event in self.events:
                    for i, ref in enumerate(event.scopes):
                        try:
                            dg_cntr, ch_cntr = ref
                            event["scope_{}_addr".format(i)] = self.groups[dg_cntr][
                                "channels"
                            ][ch_cntr].address
                        except TypeError:
                            dg_cntr = ref
                            event["scope_{}_addr".format(i)] = self.groups[dg_cntr][
                                "channel_group"
                            ].address
                    for i in range(event["attachment_nr"]):
                        key = "attachment_{}_addr".format(i)
                        addr = event[key]
                        event[key] = at_map[addr]

                    blocks.append(event)
                    ev_map[event.address] = address
                    event.address = address
                    address += event["block_len"]

                    if event.name:
                        tx_block = TextBlock(text=event.name)
                        tx_block.address = address
                        blocks.append(tx_block)
                        address += tx_block["block_len"]
                        event["name_addr"] = tx_block.address
                    else:
                        event["name_addr"] = 0

                    if event.comment:
                        meta = event.comment.startswith("<EVcomment")
                        tx_block = TextBlock(text=event.comment, meta=meta)
                        tx_block.address = address
                        blocks.append(tx_block)
                        address += tx_block["block_len"]
                        event["comment_addr"] = tx_block.address
                    else:
                        event["comment_addr"] = 0

                for event in self.events:
                    if event["parent_ev_addr"]:
                        event["parent_ev_addr"] = ev_map[event["parent_ev_addr"]]
                    if event["range_start_ev_addr"]:
                        event["range_start_ev_addr"] = ev_map[
                            event["range_start_ev_addr"]
                        ]

                for i in range(len(self.events) - 1):
                    self.events[i]["next_ev_addr"] = self.events[i + 1].address
                self.events[-1]["next_ev_addr"] = 0

                self.header["first_event_addr"] = self.events[0].address

            for block in blocks:
                write(bytes(block))

            del blocks

            for gp, rec_id in zip(self.groups, gp_rec_ids):
                gp["data_group"]["record_id_len"] = rec_id

            if valid_data_groups:
                addr_ = valid_data_groups[0].address
                self.header["first_dg_addr"] = addr_
            else:
                self.header["first_dg_addr"] = 0
            self.header["file_history_addr"] = self.file_history[0].address

            if self.attachments:
                first_attachment = self.attachments[0]
                addr_ = first_attachment.address
                self.header["first_attachment_addr"] = addr_
            else:
                self.header["first_attachment_addr"] = 0

            seek(v4c.IDENTIFICATION_BLOCK_SIZE)
            write(bytes(self.header))

            for orig_addr, gp in zip(original_data_addresses, self.groups):
                gp["data_group"]["data_block_addr"] = orig_addr

            ev_map = {value: key for key, value in ev_map.items()}

            for event in self.events:
                if event["parent_ev_addr"]:
                    event["parent_ev_addr"] = ev_map[event["parent_ev_addr"]]
                if event["range_start_ev_addr"]:
                    event["range_start_ev_addr"] = ev_map[event["range_start_ev_addr"]]
                for i in range(event["attachment_nr"]):
                    key = "attachment_{}_addr".format(i)
                    addr = event[key]
                    event[key] = at_map[addr]

            for gp in self.groups:
                for dep_list in gp["channel_dependencies"]:
                    if dep_list:
                        if all(isinstance(dep, ChannelArrayBlock) for dep in dep_list):
                            for dep in dep_list:
                                if dep["ca_type"] != v4c.CA_TYPE_LOOKUP:
                                    dep.referenced_channels = []
                                    continue
                                for i, (gp_nr, ch_nr) in enumerate(
                                    dep.referenced_channels
                                ):
                                    grp = self.groups[gp_nr]
                                    stream.seek(0, v4c.SEEK_END)

                                    dep["scale_axis_{}_dg_addr".format(i)] = grp[
                                        "data_group"
                                    ].address
                                    dep["scale_axis_{}_cg_addr".format(i)] = grp[
                                        "channel_group"
                                    ].address
                                    dep["scale_axis_{}_ch_addr".format(i)] = grp[
                                        "temp_channels"
                                    ][ch_nr]
                                seek(dep.address)
                                write(bytes(dep))

            for gp in self.groups:
                del gp["temp_channels"]

        if dst == self.name:
            self.close()
            os.remove(self.name)
            os.rename(destination, self.name)

            self.groups.clear()
            self.header = None
            self.identification = None
            self.file_history.clear()
            self.channels_db.clear()
            self.masters_db.clear()
            self.attachments.clear()
            self.file_comment = None

            self._ch_map.clear()
            self._master_channel_cache.clear()

            self._tempfile = TemporaryFile()
            self._file = open(self.name, "rb")
            self._read()
        return dst

    def get_channel_name(self, group, index):
        """Gets channel name.

        Parameters
        ----------
        group : int
            0-based group index
        index : int
            0-based channel index

        Returns
        -------
        name : str
            found channel name

        """
        gp_nr, ch_nr = self._validate_channel_selection(None, group, index)

        grp = self.groups[gp_nr]

        channel = grp["channels"][ch_nr]

        if self.memory == "minimum":
            if grp["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
                stream = self._file
            else:
                stream = self._tempfile
            stream.seek(channel + 40)
            (addr,) = UINT64_u(stream.read(8))
            name = get_text_v4(addr, stream)
        else:
            name = channel.name

        return name

    def get_channel_metadata(self, name=None, group=None, index=None):
        gp_nr, ch_nr = self._validate_channel_selection(name, group, index)

        grp = self.groups[gp_nr]

        if grp["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
            stream = self._file
        else:
            stream = self._tempfile

        if ch_nr >= 0:
            channel = grp["channels"][ch_nr]

            if self.memory == "minimum":
                channel = Channel(address=channel, stream=stream)
        else:
            channel = grp["logging_channels"][-ch_nr - 1]

        return channel

    def get_channel_unit(self, name=None, group=None, index=None):
        """Gets channel unit.

        Channel can be specified in two ways:

        * using the first positional argument *name*

            * if there are multiple occurrences for this channel then the
              *group* and *index* arguments can be used to select a specific
              group.
            * if there are multiple occurrences for this channel and either the
              *group* or *index* arguments is None then a warning is issued

        * using the group number (keyword argument *group*) and the channel
          number (keyword argument *index*). Use *info* method for group and
          channel numbers


        If the *raster* keyword argument is not *None* the output is
        interpolated accordingly.

        Parameters
        ----------
        name : string
            name of channel
        group : int
            0-based group index
        index : int
            0-based channel index

        Returns
        -------
        unit : str
            found channel unit

        """
        gp_nr, ch_nr = self._validate_channel_selection(name, group, index)

        grp = self.groups[gp_nr]

        if grp["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
            stream = self._file
        else:
            stream = self._tempfile

        channel = grp["channels"][ch_nr]

        if self.memory == "minimum":

            channel = Channel(address=channel, stream=stream)

        conversion = channel.conversion

        unit = conversion and conversion.unit or channel.unit or ""

        return unit

    def get_channel_comment(self, name=None, group=None, index=None):
        """Gets channel comment.

        Channel can be specified in two ways:

        * using the first positional argument *name*

            * if there are multiple occurrences for this channel then the
              *group* and *index* arguments can be used to select a specific
              group.
            * if there are multiple occurrences for this channel and either the
              *group* or *index* arguments is None then a warning is issued

        * using the group number (keyword argument *group*) and the channel
          number (keyword argument *index*). Use *info* method for group and
          channel numbers


        If the *raster* keyword argument is not *None* the output is
        interpolated accordingly.

        Parameters
        ----------
        name : string
            name of channel
        group : int
            0-based group index
        index : int
            0-based channel index

        Returns
        -------
        comment : str
            found channel comment

        """
        gp_nr, ch_nr = self._validate_channel_selection(name, group, index)

        grp = self.groups[gp_nr]

        if grp["data_location"] == v4c.LOCATION_ORIGINAL_FILE:
            stream = self._file
        else:
            stream = self._tempfile

        channel = grp["channels"][ch_nr]

        if self.memory == "minimum":
            channel = Channel(address=channel, stream=stream)

        return extract_cncomment_xml(channel.comment)
