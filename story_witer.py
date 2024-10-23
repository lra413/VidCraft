import moviepy
import script_writer as sw
import edge_tts
import random
import asyncio
import threading as th
import os
import string
from englisttohindi.englisttohindi import EngtoHindi
def full_video(file_adress):
    print(os.path.dirname(file_adress)+"\story.docx")
    script = open(file_adress,'r', errors="ignore",encoding="utf-8")
    main_location_of_script=os.path.dirname(file_adress)
    lines = script.readlines()
    Text="".join(lines)
    print(Text)
    tmp_converted_holder=[]
    sgc=sw.script_given_checker(Text)
    script_satisfied=False
    context=[{'role':'user','content':Text}]
    if sgc==1:   
        print("generating script")
        while script_satisfied==False:
            response= sw.generate_script(context) 
            print(response['message']['content'])
            context.append({'role' : (response['message']['role']), 'content' :(response['message']['content'])})
            Text=response['message']['content']
            script_feedback=input("")
            context.append({'role': 'user', 'content': script_feedback})
            if script_feedback=="exit" or "satisfied":
                script_satisfied=True
                break
            if Text==0:
                exit  
 
        print(Text)
    Text=Text.replace("\n","")
    Text=Text.replace("  ","")
    prand=""
    count=0
    skip_error_msg=0
    for i in Text:
        if len(i)==1:
            if i=="(" or i=="[" or i=="{":
                skip_error_msg+=1
            elif skip_error_msg>=0  and (i==")" or i=="]" or i=="}"):
                skip_error_msg-=1
            prand+=i
            if i ==" ":
                if prand.find("Failed to Make Response"):
                    skip_error_msg+=1
                    prand=prand.replace("Failed to Make Response" ,"")
                if count==10:
                    specail_char_remover= str.maketrans("","",string.punctuation)
                    specail_remover=prand.translate(specail_char_remover)
                    translator=EngtoHindi(specail_remover)
                    tmp_converted_holder.append(translator.convert)
                    print(tmp_converted_holder)
                    prand=""
                    count=0
                else:
                    count+=1
            else:
                if skip_error_msg==0:
                    prand+=i
        else:
            for j in i:
                if j ==" ":
                    prand+=j
                    if count==10:
                        specail_char_remover= str.maketrans("","",string.punctuation)
                        specail_remover=prand.translate(specail_char_remover)
                        translator=EngtoHindi(specail_remover)
                        tmp_converted_holder.append(translator.convert)
                        print(tmp_converted_holder)
                        prand=""
                        count=0
                    else:
                        count+=1
                else:
                    prand+=j
            specail_char_remover= str.maketrans("","",string.punctuation)
            specail_remover=prand.translate(specail_char_remover)
            translator=EngtoHindi(specail_remover)
            tmp_converted_holder.append(translator.convert)
            print(tmp_converted_holder)
    try:
        hindi_Text="".join(tmp_converted_holder)
        print(tmp_converted_holder)
        print(hindi_Text)
    except: 
        print("script_not transfered")
        hindi_Text="genif"

    Voices =['en-US-GuyNeural','hi-IN-MadhurNeural']
    Voice=Voices[0]
    hindi_Voice=Voices[1]
    output_file=main_location_of_script+"/output.mp3"
    output_file_hindi=main_location_of_script+"/output_hindi.mp3"
    async def amain() -> None:
        communicate=edge_tts.Communicate(Text,Voice,rate='+5%',pitch="-18Hz")
        await communicate.save(output_file)
        communicate=edge_tts.Communicate(hindi_Text,hindi_Voice,rate='+20%',pitch="-17Hz")
        await communicate.save(output_file_hindi)
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(amain())
    except:
        print("tts is not working")
        loop.close()
    available_base_video=os.listdir("base video")
    random_selector=random.choice(available_base_video)
    clip =moviepy.VideoFileClip("base video/"+str(random_selector))
    duration_video = clip.duration 
    print("taken video")
    audio_c=moviepy.AudioFileClip(output_file)
    audio_c_hindi=moviepy.AudioFileClip(output_file_hindi)
    print("taken audio")
    duration_audio= audio_c.duration
    duration_audio_hindi= audio_c_hindi.duration
    final_durational=int(duration_video-duration_audio)
    final_durational_hindi=int(duration_video-duration_audio_hindi)
    timespan_selectore=random.randint(0,final_durational)
    timespan_selectore_hindi=random.randint(0,final_durational_hindi)
    print("random split happend")
    intro=clip.subclip(timespan_selectore,(timespan_selectore+2.5))
    intro_hindi=clip.subclip(timespan_selectore_hindi,(timespan_selectore_hindi+2.5))

    print("into made")
    outro=clip.subclip((timespan_selectore-2.5),timespan_selectore)
    outro_hindi=clip.subclip((timespan_selectore_hindi-2.5),timespan_selectore_hindi)
    
    print("outro made")
    clip_eng=clip.subclip((timespan_selectore+2.5),(timespan_selectore-2.5+duration_audio))
    clip_hindi=clip.subclip((timespan_selectore_hindi+2.5),(timespan_selectore_hindi-2.5+duration_audio_hindi))

    print("subcliping")

    finalclip=moviepy.concatenate_videoclips([intro,clip_eng,outro])
    finalclip_hindi=moviepy.concatenate_videoclips([intro_hindi,clip_hindi,outro_hindi])

    print("concated")
    bacground_noise=finalclip.audio
    finalaudio= moviepy.CompositeAudioClip([bacground_noise,audio_c])
    finalclip.audio = finalaudio
    finalclip.write_videofile(main_location_of_script+"/final.mp4")
    finalclip.close()
    finalaudio_hindi= moviepy.CompositeAudioClip([bacground_noise,audio_c_hindi])
    finalclip_hindi.audio = finalaudio_hindi
    finalclip_hindi.write_videofile(main_location_of_script+"/final_hindi.mp4")
    finalclip_hindi.close()
    print("video backgound and audio added and sending to edit")

def part_maker(video_path,sufix):
    parttable=moviepy.VideoFileClip(video_path)
    total_duration=parttable.duration
    if total_duration >= 58.5:
        partition_complete=0
        current_duration=0
        parts=0
        while partition_complete!=1:
            parts+=1
            if total_duration>(current_duration+40):
                print("creating part"+str(parts))
                Text="subscribe for part"+str(parts+1)
                Voices =['en-US-GuyNeural']
                Voice=Voices[0]
                output_file=(os.path.dirname(video_path)+"/output_part"+sufix+".mp3")
                async def amain() -> None:
                    communicate=edge_tts.Communicate(Text,Voice,rate='+20%')
                    await communicate.save(output_file)

                loop = asyncio.get_event_loop_policy().get_event_loop()
                try:
                    loop.run_until_complete(amain())
                except:
                    print("failed")
                
                audio_part_annoucement=moviepy.AudioFileClip(os.path.dirname(video_path)+"/output_part.mp3")
                parter=parttable.subclip((current_duration),(current_duration+40))
                outro=parttable.subclip((current_duration+40),(current_duration+45))
                outro.audio=audio_part_annoucement
                current_duration+=39
                print("part"+str(parts))
            else:
                print("creating final part")
                parter=parttable.subclip(current_duration,(total_duration-1))
                outro=parttable.subclip((total_duration-1),(total_duration))
                partition_complete=1
                loop.close() 
            try:
                final_output=moviepy.concatenate_videoclips([parter,outro])
                final_output.write_videofile(os.path.dirname(video_path)+"/output_part"+sufix+str(parts)+".mp4")
                final_output.close()
            except:
                final_output=moviepy.concatenate_videoclips([parter])
                final_output.write_videofile(os.path.dirname(video_path)+"/output_part"+sufix+str(parts)+".mp4")
                final_output.close()
