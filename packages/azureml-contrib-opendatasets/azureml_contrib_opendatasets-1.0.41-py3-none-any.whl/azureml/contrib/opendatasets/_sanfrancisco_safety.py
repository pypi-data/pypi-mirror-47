# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""San Francisco safety."""

from ._sanfrancisco_safety_blob_info import SanFranciscoSafetyBlobInfo
from .dataaccess.blob_parquet_descriptor import BlobParquetDescriptor
from .city_safety import CitySafety
from datetime import datetime
from dateutil import parser


class SanFranciscoSafety(CitySafety):
    """San Francisco city safety class."""

    _default_start_date = parser.parse('2000-01-01')
    _default_end_date = datetime.today()

    """const instance of blobInfo."""
    _blobInfo = SanFranciscoSafetyBlobInfo()

    data = BlobParquetDescriptor(_blobInfo)
