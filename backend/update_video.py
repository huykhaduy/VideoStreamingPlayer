import time
import m3u8

CLOUD_FRONT_URL = "https://d3l1s92l55csfd.cloudfront.net/stream/"
segment_size = 17

while True:
    video = m3u8.load("storage/stream/test2.m3u8")
    video.target_duration = 14
    print("Update video status ...")
    print(f"Size: {len(video.segments)}")
    if len(video.segments) >= 4 and video.media_sequence + 4 <= segment_size:
        video.segments.pop(0)
        video.add_segment(m3u8.Segment(uri=f"{CLOUD_FRONT_URL}music_video{video.media_sequence+4}.ts", duration=10))
        video.media_sequence += 1
        print("Type 1")
    elif len(video.segments) == 0:
        # Lấy 4 cái segment đầu tiên
        [video.add_segment(m3u8.Segment(uri=f"{CLOUD_FRONT_URL}music_video{i}.ts", duration=10)) for i in range(4)]
        video.media_sequence = 0
        print("Type 2")
    elif video.media_sequence + 4 > segment_size:
        print("Type 3")
        video.is_endlist = True

    with open("storage/stream/test2.m3u8", "wb") as f:
        f.write(video.dumps().encode())

    time.sleep(10)