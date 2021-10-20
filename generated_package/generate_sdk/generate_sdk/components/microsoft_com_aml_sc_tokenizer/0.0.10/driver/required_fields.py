# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Defines Part A of the logging schema, keys that have a common meaning across telemetry data."""
from datetime import datetime, timezone
import uuid

class RequiredFields:
    """Defines Part A of the logging schema, keys that have a common meaning across telemetry data."""

    def __init__(self, subscriptionId,
                 workspaceId, correlationId, componentName, eventName) -> None:
        """Initialize a new instance of the RequiredFields."""
        self.EventId = str(uuid.uuid4())
        self.SubscriptionId = subscriptionId
        self.WorkspaceId = workspaceId
        self.CorrelationId = correlationId
        self.ComponentName = componentName
        self.EventName = eventName
        self.EventTime = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=None).isoformat()
        