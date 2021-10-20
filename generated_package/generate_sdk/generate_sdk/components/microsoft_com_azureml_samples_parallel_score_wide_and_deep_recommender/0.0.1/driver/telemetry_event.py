# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Event object for telemetry."""
from typing import Any, Dict, Optional
from required_fields import RequiredFields
from standard_fields import StandardFields


class TelemetryEvent(dict):
    """Define an event which can be sent to telemetry.

    Comman Schema: https://msdata.visualstudio.com/Vienna/_wiki/wikis/Vienna.wiki/4672/Common-Schema
    """

    def __init__(
        self,
        requiredFields: RequiredFields,
        standardFields: Optional[StandardFields] = None,
        extensionFields: Optional[Dict[str, Any]] = None,
    ):
        """Merge all fields into one dict."""
        super().__init__()

        self["RequiredFields"] = requiredFields.__dict__

        if standardFields:
            self["StandardFields"] = standardFields.__dict__

        if extensionFields:
            self["ExtensionFields"] = extensionFields
