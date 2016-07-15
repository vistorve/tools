"""
Small library to make histograms from an array of values. Also a way
to pretty print the resulting value along with a basic graph.

CLI:
histogram.py [max_boxes] [max_x_width]

Values to histogram are streamed in as a single column.

max_boxes : The number of buckets to use in the histogram
max_x_width : The largest value in the histogram will be this many x's

Buckets are printed out as the max value in that bucket.
"""

import math
import collections

def make_histo(arr_to_histo, n_histo_boxes):
    """
    Create a histogram from the arr_to_histo array of values.

    arr_to_histo : array of floats
    n_histo_boxes : The number of buckets to use in the histogram
    
    Return: array with count of values in each bucket
    """
    histo = [0] * n_histo_boxes

    min_v = min(arr_to_histo)
    max_v = max(arr_to_histo)

    size = (max_v - min_v)/(n_histo_boxes - 1)

    for dv in arr_to_histo:
        v = dv - min_v
        bucket = int(v / size)
        histo[bucket] += 1

    return histo, size, min_v

def string_histo(histo, bucket_size, min_v, max_xs):
    """
    Convert a histogram into a nicely formated array of strings
    suitable for printing or text display.

    histo : array of bucket counts
    bucket_size : the wdith or size of each bucket
    min_v : The minimum value of the array that was histogramed
    max_xs : The max bucket count will have this many x's in the output

    bucket width is: i * (max - min)/n_boxes) + min_v
                     to
                     (i + 1) * (max - min)/n_boxes) + min_v

    The displayed bucket width is the max value in the bucket.

    Return: Array of formatted strings ready to print. Format is
    [max bucket value]:[number of items in bucket] [a bar graph of items]

    Example output piece:
    78.4   : 82705    xxxxxxxxxxxxxxxxx
    116.8  : 93507    xxxxxxxxxxxxxxxxxxx
    155.3  : 61109    xxxxxxxxxxxx
    """
    largest_value = float(max(histo))

    per_x = max_xs/largest_value

    output_strings = []

    max_bucket_size = 0
    for i, n in enumerate(histo):
        min_bucket = i * bucket_size + min_v
        max_bucket = (i + 1) * bucket_size + min_v
        bucket_string_length = len("{:.1f}-{:.1f}".format(min_bucket,
                                                          max_bucket))
        max_bucket_size = max(bucket_string_length, max_bucket_size)

    for i, n in enumerate(histo):
        min_bucket = i * bucket_size + min_v
        max_bucket = (i + 1) * bucket_size + min_v
        bucket_pad = int(max_bucket_size - len("{:.1f}-{:.1f}".format(
            min_bucket, max_bucket)))
        n_pad = len(str(largest_value)) - len(str(n))
        output_strings.append(
            "{:.1f}-{:.1f}{} : {}{} {}".format(
                min_bucket,
                max_bucket,
                " " * bucket_pad,
                n,
                " " * n_pad,
                "x" * int(per_x * n)))

    return output_strings

if __name__ == "__main__":
    import sys

    num_boxes, max_x_width = map(int, sys.argv[1:])

    arr = [float(l.rstrip("\n")) for l in sys.stdin]

    histo, bucket_size, min_value = make_histo(arr, num_boxes)
    for l in string_histo(histo, bucket_size, min_value, max_x_width):
        print l
