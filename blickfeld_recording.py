try:
    import blickfeld_scanner
except ImportError:
    print("""Could not find library blickfeld_scanner! \nSee https://docs.blickfeld.com/cube/v1.0.1/external/blickfeld-scanner-lib/install.html""")
           
import argparse
from time import time
import numpy as np


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", type=str, default = "192.168.26.26", help = "IP or hostname of the device.")
    parser.add_argument("--outpath", type=str, default = "out/", help = "Output Path.")
    parser.add_argument("--length", type=int, default = 10, help = "Length of recordings.")
    opt = parser.parse_args()
    
    device_ip_or_hostname = opt.hostname  

    scanner = blickfeld_scanner.scanner(device_ip_or_hostname)

    print(scanner)

    stream = scanner.get_point_cloud_stream()
    try:
        start_time = time()
        point_clouds = []

        while time() - start_time < opt.length:
            frame = stream.recv_frame()
            points = []
            for s_ind in range(len(frame.scanlines)):
                # Iterate through all the points in a scanline
                for p_ind in range(len(frame.scanlines[s_ind].points)):
                    point = frame.scanlines[s_ind].points[p_ind]

                    # Iterate through all the returns for each points
                    for r_ind in range(len(point.returns)):
                        ret = point.returns[r_ind]
                        points.append([ret.cartesian[0], ret.cartesian[1], ret.cartesian[2]])
            point_clouds.append(points)
        for i in range(len(point_clouds)):
            np.save(f"{opt.outpath}/{i:06d}" % i, point_clouds[i])
    finally:
        del stream  # Close the stream
