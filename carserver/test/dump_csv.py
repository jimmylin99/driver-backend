from os import write


if __name__ == "__main__":
    import sys
    sys.path.append('../..')
    from carserver.utils.getlnglat import get_track_longitude_latitude
    from carserver import client
    status, longitude_list, latitude_list, \
        acc_list, gyr_list, speed_list, \
        time_list, unique_tag_info = get_track_longitude_latitude(
            client, 'chendy', 0
    )
    import csv
    with open("list.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(acc_list)
        writer.writerow(gyr_list)
        writer.writerow(speed_list)
