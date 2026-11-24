"""Courier & parcel tracking system.

Books parcels with tracking ids, moves them through the delivery stages,
tracks a parcel by id, checks whether it is still with the courier,
generates a delivery OTP and works out the shipping cost by weight.
"""
import os
import re
import secrets
import shutil
import subprocess  # nosec B404 - fixed argv list only, never a shell
import tempfile
from datetime import date

STATUS_FLOW = ["Booked", "Picked Up", "In Transit",
               "Out for Delivery", "Delivered"]
# a parcel that is out for delivery is still with the courier
COURIER_STATUSES = {"Picked Up", "In Transit", "Out for Delivery"}
HOST_PATTERN = re.compile(r"^[A-Za-z0-9.-]{1,253}$")
parcels = {}


def book_parcel(sender, receiver, weight_kg, history=None):
    """Register a new parcel and return its tracking id."""
    if history is None:
        history = []
    tracking_id = "TRK" + str(10001 + len(parcels))
    parcels[tracking_id] = {"sender": sender, "receiver": receiver,
                            "weight": weight_kg, "status": 0,
                            "booked": str(date.today())}
    history.append(tracking_id)
    return tracking_id


def advance_status(tracking_id):
    """Move a parcel to its next delivery stage and return the new stage."""
    parcel = parcels[tracking_id]
    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1
    return STATUS_FLOW[parcel["status"]]


def shipping_cost(weight_kg):
    """Return the shipping cost: 50 for the first kg, 30 per extra kg."""
    if weight_kg <= 0:
        raise ValueError("weight must be positive")
    cost = 50
    if weight_kg > 1:
        cost += (weight_kg - 1) * 30
    return round(cost, 2)


def track_parcel(tracking_id):
    """Return 'sender -> receiver: status' for a tracking id."""
    try:
        parcel = parcels[tracking_id]
    except KeyError:
        return "Unknown tracking id " + tracking_id
    route = parcel["sender"] + " -> " + parcel["receiver"]
    return route + ": " + STATUS_FLOW[parcel["status"]]


def is_with_courier(tracking_id):
    """Return True while the courier physically has the parcel."""
    status = STATUS_FLOW[parcels[tracking_id]["status"]]
    return status in COURIER_STATUSES


def label_path():
    """Create an empty temporary label file and return its path."""
    # Helper kept for the lab: not called by the demo.
    # mkstemp creates the file atomically, so nobody else can take the name.
    fd, path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    return path


def ping_hub(hub_address):
    """Ping a courier hub once and return the command output."""
    # Helper kept for the lab: not called by the demo.
    # No shell, and the address must look like a hostname/IP (no injection).
    if not HOST_PATTERN.match(hub_address):
        raise ValueError("invalid hub address: " + repr(hub_address))
    ping = shutil.which("ping")
    if ping is None:
        raise FileNotFoundError("ping command not found")
    # nosec B603 - validated argv list, no shell
    return subprocess.check_output([ping, "-c", "1", hub_address])  # nosec


def main():
    """Run the parcel tracker demonstration."""
    first = book_parcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = book_parcel("Gadget Hub", "Sneha Rao", 0.8)
    third = book_parcel("Spice Store", "Imran Khan", 4)
    advance_status(first)
    advance_status(first)
    advance_status(second)
    for _ in range(6):
        advance_status(third)
    for tracking_id in (first, second, third):
        print(track_parcel(tracking_id))
        print("  with courier:", is_with_courier(tracking_id))
        print("  cost:", shipping_cost(parcels[tracking_id]["weight"]))
    print(track_parcel("TRK00000"))  # unknown id
    delivery_otp = 1000 + secrets.randbelow(9000)  # secure OTP
    print("Delivery OTP for", third, "is", delivery_otp)
    print("Parcels booked today:", len(parcels))


if __name__ == "__main__":
    main()
