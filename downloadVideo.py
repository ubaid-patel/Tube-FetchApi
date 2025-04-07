import os,threading,cleanup,subprocess,re,app

def download(file, fname,itag):
    fname = app.formatFilename(fname=fname)
    # Define the paths 
    current_dir = os.getcwd()
    input_video_path = os.path.join(current_dir, "1" + fname)
    input_audio_path = os.path.join(current_dir, fname.replace(".mp4",".mp3"))
    output_video_path = os.path.join(current_dir, fname.replace(".mp4",str(itag)+".mp4"))
    if os.path.exists(output_video_path):
                print("File already exist")
                return
    file.download(filename = "1" + fname)

    try:
        cmd = [
            app.ffmpeg,
            "-i", input_video_path,
            "-i", input_audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            output_video_path
        ]
        subprocess.run(cmd, check=True)
        # Clean up: remove the temporary audio and video files
        os.remove(input_video_path)
        threading.Thread(target=cleanup.performCleanup,args=[output_video_path]).start()
        threading.Thread(target=cleanup.performCleanup,args=[input_audio_path]).start()
        print("Audio and video merging completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error merging audio and video:", e)
