"""
IGG Conquerors Bot - Error Code Reference
==========================================
Complete mapping of game error codes to human-readable messages and bot actions.
Source: Binary analysis + PCAP observation + bot runtime logs.
"""

# ══════════════════════════════════════════════════════════════
#  ERROR CODES (from 0x0037 ERROR_STATUS packets)
# ══════════════════════════════════════════════════════════════

ERROR_CODES = {
    0:  "OK",
    1:  "FAILED",
    2:  "INVALID_PARAM",
    3:  "NOT_ENOUGH_RESOURCES",
    5:  "NOT_ENOUGH_TROOPS",
    7:  "COOLDOWN_ACTIVE",
    10: "QUEUE_FULL",
    13: "INVALID_TARGET",
    22: "TIMESTAMP_ERROR",
    38: "MARCH_SLOT_BUSY",
    43: "ACCOUNT_ERROR",
    100: "UNKNOWN_100",
}

# Map error codes to recommended bot actions
ERROR_ACTIONS = {
    0:  "continue",          # Success - proceed normally
    1:  "retry_once",        # Generic failure - retry after delay
    2:  "fix_params",        # Bad parameter - check packet format
    3:  "wait_resources",    # Insufficient resources - wait to accumulate
    5:  "reduce_troops",     # Not enough troops - reduce count or wait
    7:  "wait_cooldown",     # Cooldown active - wait and retry
    10: "wait_queue",        # Queue full - wait for slot to free up
    13: "find_new_target",   # Invalid target - pick different tile/coords
    22: "sync_time",         # Server time mismatch - resync
    38: "wait_march_slot",   # March slot in use - wait for return
    43: "reconnect",         # Account/session error - full reconnect
}

# Recommended delays per error type (seconds)
ERROR_DELAYS = {
    0:  0,     # No delay needed
    1:  5,     # Short retry
    2:  0,     # Immediate (fix params first)
    3:  60,    # Wait for resources (1 min)
    5:  30,    # Wait for troops (30s)
    7:  120,   # Cooldown (2 min)
    10: 60,    # Queue slot (1 min)
    13: 0,     # Find new target immediately
    22: 5,     # Resync (5s)
    38: 180,   # March return (3 min typical)
    43: 10,    # Reconnect delay
}


# ══════════════════════════════════════════════════════════════
#  MARCH ACK STATUS CODES (from 0x00B8)
# ══════════════════════════════════════════════════════════════

MARCH_ACK_STATUS = {
    0x00: "MARCH_OK",
    0x01: "MARCH_FAILED_GENERIC",
    0x02: "MARCH_INVALID_COORDS",
    0x03: "MARCH_NO_TROOPS",
    0x05: "MARCH_ALL_SLOTS_FULL",
}


def get_error_info(error_code):
    """Get full error info dict for a given error code."""
    return {
        'code': error_code,
        'message': ERROR_CODES.get(error_code, f"UNKNOWN_{error_code}"),
        'action': ERROR_ACTIONS.get(error_code, "log_and_continue"),
        'delay': ERROR_DELAYS.get(error_code, 10),
    }


def should_retry(error_code):
    """Whether the bot should retry after this error."""
    action = ERROR_ACTIONS.get(error_code, "log_and_continue")
    return action in ("retry_once", "wait_resources", "wait_cooldown",
                       "wait_queue", "wait_march_slot")


def should_reconnect(error_code):
    """Whether this error requires a full reconnection."""
    return ERROR_ACTIONS.get(error_code) == "reconnect"
