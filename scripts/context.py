#!/usr/bin/env python3
"""Calculate local slate date windows and approximate great-circle miles.

No network, file writes, third-party packages, or betting predictions.
"""

import argparse
from datetime import date, datetime, time, timedelta, timezone
import json
import math
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def slate_window(day, timezone_name="Asia/Manila"):
    local_zone = ZoneInfo(timezone_name)
    selected_date = date.fromisoformat(day) if day else datetime.now(local_zone).date()
    local_start = datetime.combine(selected_date, time.min, tzinfo=local_zone)
    local_end = datetime.combine(
        selected_date + timedelta(days=1), time.min, tzinfo=local_zone
    )
    start_utc = local_start.astimezone(timezone.utc)
    end_utc = local_end.astimezone(timezone.utc)
    nba_zone = ZoneInfo("America/New_York")
    first_et_date = start_utc.astimezone(nba_zone).date()
    last_et_date = (end_utc - timedelta(microseconds=1)).astimezone(nba_zone).date()
    et_dates = []
    current_date = first_et_date
    while current_date <= last_et_date:
        et_dates.append(current_date.isoformat())
        current_date += timedelta(days=1)
    return {
        "local_date": selected_date.isoformat(),
        "timezone": timezone_name,
        "start_local": local_start.isoformat(),
        "end_local_exclusive": local_end.isoformat(),
        "start_utc": start_utc.isoformat(),
        "end_utc_exclusive": end_utc.isoformat(),
        "nba_dates_et": et_dates,
    }


def great_circle_miles(origin, destination):
    for latitude, longitude in (origin, destination):
        if not (
            math.isfinite(latitude)
            and math.isfinite(longitude)
            and -90 <= latitude <= 90
            and -180 <= longitude <= 180
        ):
            raise ValueError("latitude must be in [-90, 90] and longitude in [-180, 180]")
    lat1, lon1 = map(math.radians, origin)
    lat2, lon2 = map(math.radians, destination)
    haversine = (
        math.sin((lat2 - lat1) / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    )
    angle = 2 * math.asin(math.sqrt(min(1.0, max(0.0, haversine))))
    # IUGG mean Earth radius in km, converted to statute miles.
    return 6371.0088 / 1.609344 * angle


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    window_parser = subparsers.add_parser("window", help="Get an inclusive/exclusive slate window")
    window_parser.add_argument("--date", help="YYYY-MM-DD; default: today in --timezone")
    window_parser.add_argument("--timezone", default="Asia/Manila", help="IANA timezone name")
    miles_parser = subparsers.add_parser("miles", help="Calculate approximate venue-to-venue miles")
    miles_parser.add_argument("--origin", type=float, nargs=2, required=True, metavar=("LAT", "LON"))
    miles_parser.add_argument("--destination", type=float, nargs=2, required=True, metavar=("LAT", "LON"))
    args = parser.parse_args()
    try:
        if args.command == "window":
            result = slate_window(args.date, args.timezone)
        else:
            result = {
                "origin_lat_lon": args.origin,
                "destination_lat_lon": args.destination,
                "approximate_miles": round(great_circle_miles(args.origin, args.destination), 1),
                "method": "great-circle; mean Earth radius; not actual itinerary",
            }
    except (ValueError, OverflowError, ZoneInfoNotFoundError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
