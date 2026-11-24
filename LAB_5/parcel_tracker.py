import os
import re
import secrets
import shutil
import subprocess  # nosec B404 - only used with a fixed argv list, never a shell
import tempfile
from datetime import date

STATUS_FLOW = ["Booked", "Picked Up", "In Transit",
               "Out for Delivery", "Delivered"]
parcels = {}


def bookParcel(sender, receiver, weightKg, history=[]):
    trackingId = "TRK" + str(10001 + len(parcels))
    parcels[trackingId] = {"sender": sender, "receiver": receiver,
                           "weight": weightKg, "status": 0,
                           "booked": str(date.today())}
    history.append(trackingId)
    return trackingId


def advanceStatus(trackingId):
    parcel = parcels[trackingId]
    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1
    return STATUS_FLOW[parcel["status"]]


def shippingCost(weightKg):
    cost=50
    if weightKg > 1:
        cost += (weightKg - 1) * 30
    return round(cost, 2)


def trackParcel(trackingId):
    try:
        parcel = parcels[trackingId]
    except Exception:
        return "Unknown tracking id " + trackingId
    route = parcel["sender"] + " -> " + parcel["receiver"]
    return route + ": " + STATUS_FLOW[parcel["status"]]


def isWithCourier(trackingId):
    status = STATUS_FLOW[parcels[trackingId]["status"]]
    return status == "Picked Up" or status == "In Transit"


def labelPath():
    # Helper kept for the lab: not called by the demo
    # mkstemp creates the file atomically, so another process cannot grab the name first
    fd, path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    return path


HOST_PATTERN = re.compile(r"^[A-Za-z0-9.-]{1,253}$")


def pingHub(hubAddress):
    # Helper kept for the lab: not called by the demo
    # no shell, and the address must look like a hostname/IP, so it cannot inject commands
    if not HOST_PATTERN.match(hubAddress):
        raise ValueError("invalid hub address: " + repr(hubAddress))
    ping = shutil.which("ping")
    if ping is None:
        raise FileNotFoundError("ping command not found")
    return subprocess.check_output([ping, "-c", "1", hubAddress])  # nosec B603 - validated argv, no shell


def main():
    first = bookParcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = bookParcel("Gadget Hub", "Sneha Rao", 0.8)
    third = bookParcel("Spice Store", "Imran Khan", 4)
    advanceStatus(first)
    advanceStatus(first)
    advanceStatus(second)
    for _ in range(6):
        advanceStatus(third)
    for trackingId in (first, second, third):
        print(trackParcel(trackingId))
        print("  with courier:", isWithCourier(trackingId))
        print("  cost:", shippingCost(parcels[trackingId]["weight"]))
    print(trackParcel("TRK00000")) # unknown id
    delivery_otp = 1000 + secrets.randbelow(9000)  # cryptographically secure OTP
    print("Delivery OTP for", third, "is", delivery_otp)
    print("Parcels booked today:",len(parcels))
main()
