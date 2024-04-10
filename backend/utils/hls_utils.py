import subprocess


def convertMP4ToHLS(input_file_path: str, output_file_path: str, hls_time: int = 5):
    # Define the ffmpeg command
    ffmpeg_command = [
        'ffmpeg',  # Command
        '-i', f'{input_file_path}',  # Input file
        '-codec:', 'copy',  # Copy the codec
        '-start_number', '0',  # Start number
        '-hls_time', f'{hls_time}',  # HLS time
        '-hls_list_size', '0',  # HLS list size
        '-f', 'hls',  # Output format
        f'{output_file_path}'  # Output file name
    ]
    # Execute the ffmpeg command
    subprocess.run(ffmpeg_command)