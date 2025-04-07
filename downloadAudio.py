import subprocess,os,cleanup,threading,re,app

def download(file, filename):
    filename = app.formatFilename(filename)
    # Define the paths    
    current_dir = os.getcwd()
    input_audio_path = os.path.join(current_dir,filename)
   
    output_audio_path = os.path.join(current_dir, filename.replace(".m4a", ".mp3"))
    print(output_audio_path)
    if os.path.exists(output_audio_path):
        print("file already exist")
        return
    
    file.download(filename=filename)

    try:
        cmd = [
            app.ffmpeg,
            "-i", input_audio_path,
            "-acodec", "libmp3lame",
            "-q:a", "2",
            output_audio_path
        ]
        subprocess.run(cmd, check=True)
        print("M4A to MP3 conversion completed successfully.")
        os.remove(input_audio_path)  # Clean up: remove the temporary M4A file
        threading.Thread(target=cleanup.performCleanup,args=[output_audio_path]).start()
    except subprocess.CalledProcessError as e:
        print("Error converting M4A to MP3:", e)
