    @staticmethod
    def init_stream_video(title, max_duration, thumbnail_path):
        # Ensure thumbnail_path is a valid path
        if thumbnail_path and QFile.exists(thumbnail_path):
            api = APIInterceptor()
            data = {'title': title, 'max_duration': max_duration}

            # Construct the files dictionary with the thumbnail file
            files = {'thumbnail': open(thumbnail_path, 'rb')}

            print(files)
            
            res = api.post("stream/init",  data=data, files=files)
            
            if res.status_code == 200:
                return Video.from_json(res.text)
            else:
                print(f"API returned status code {res.status_code}. Error message: {res.text}")
                return None
        else:
            print("Invalid thumbnail path or file does not exist")
            return None