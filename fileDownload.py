import downloadVideo,os
from flask import jsonify
def performDownload(id,itag,users):
        if id in users:
            try:
                yt = users[id][0]
                file = yt.streams.get_by_itag(itag)
                if file.mime_type == "video/mp4":
                    fname = file.default_filename.encode("ascii", "ignore").decode("ascii")
                    downloadVideo.download(file, fname,itag)
                    output =  fname.replace(".mp4",str(itag)+".mp4")
                    return jsonify({"file":output}),200
                else:
                    fname = file.default_filename.encode("ascii", "ignore").decode("ascii").replace(".mp4",".m4a")
                    thread = users[id][1]
                    if thread.is_alive():
                        thread.join()
                        return jsonify({"file":fname}),200
                    else:
                        return jsonify({"file":fname}),200
            except Exception as e:
                print(e.with_traceback())
                return jsonify({"message":str(e.with_traceback())}),500
            
        else:
            return jsonify({"message":"Id not found"}),406