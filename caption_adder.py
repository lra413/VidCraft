import main
def add_caption (video_path,language): 
    main.video_path = video_path
    if (main.video_path != ""):

        main.transcriber = main.VideoTranscriber(main.model_path, main.video_path,language)

        main.transcriber.extract_audio()

        main.transcriber.transcribe_video()
        
        main.transcriber.create_video(main.output_video_path)

        processing = False
    else:
        print("caption not genrated")

