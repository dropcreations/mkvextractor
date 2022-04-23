import os
import sys
import subprocess
import json

input_count = len(sys.argv)
mkv_file_list = []

def load_json_out():
    global json_data
    mkvmerge_json_out = subprocess.check_output([
        'mkvmerge',
        '--identify',
        '--identification-format',
        'json',
        os.path.abspath(mkv_file),
        ], stderr=subprocess.DEVNULL)
    json_data = json.loads(mkvmerge_json_out)

def load_json_data():
    global id
    global codec_id
    global language
    global language_ietf
    global title
    global codec
    global track_type
    global json_data

    load_json_out()
    id = json_data.get('tracks')[int(i)].get('id')
    language = json_data.get('tracks')[int(i)].get('properties').get('language')
    language_ietf = json_data.get('tracks')[int(i)].get('properties').get('language_ietf')
    title = json_data.get('tracks')[int(i)].get('properties').get('track_name')
    codec_id = json_data.get('tracks')[int(i)].get('properties').get('codec_id')
    codec = json_data.get('tracks')[int(i)].get('codec')
    track_type = json_data.get('tracks')[int(i)].get('type')

def load_json_data_attachments():
    global attachments_id
    global attachments_content_type
    global attachments_description
    global attachments_file_name
    global attachments_uid

    load_json_out()
    attachments_id = json_data.get('attachments')[int(i)].get('id')
    attachments_content_type = json_data.get('attachments')[int(i)].get('content_type')
    attachments_description = json_data.get('attachments')[int(i)].get('description')
    attachments_file_name = json_data.get('attachments')[int(i)].get('file_name')
    attachments_uid = json_data.get('attachments')[int(i)].get('properties').get('uid')

def list_tracks():
    global i
    load_json_out()
    track_count = len(json_data['tracks'])
    for i in range(track_count):
        load_json_data()
        print("|")
        print("|--Track ID : " + str(id))
        print("|")
        print("|--Type : " + str(track_type))
        print("|--Codec : " + str(codec))
        print("|--Language : " + str(language))
        print("|--Language_ietf : " + str(language_ietf))
        print("|--Title : " + str(title))
    print("|")

def list_attachments():
    global i
    load_json_out()
    attachment_count = len(json_data['attachments'])
    print("|")
    for i in range(attachment_count):
        load_json_data_attachments()
        print("|--Attachment ID : " + str(attachments_id))
        print("|")
        print("|--ContentType : " + str(attachments_content_type))
        print("|--Filename : " + str(attachments_file_name))
        print("|--Description : " + str(attachments_description))
        print("|--UID : " + str(attachments_uid))
        print("|")

def process_mkv_file():
    global extract_track_name
    global track_type

    if track_type == "video":
        load_json_out()
        pixel_dimensions = json_data.get('tracks')[int(i)].get('properties').get('pixel_dimensions')
        extract_track_name = "Track_" + str(id) + "_[" + str(track_type) + "]_[" + str(pixel_dimensions) + "]_[" + str(language) + "]"
    elif track_type == "audio":
        load_json_out()
        audio_channels = json_data.get('tracks')[int(i)].get('properties').get('audio_channels')
        audio_sampling_frequency = json_data.get('tracks')[int(i)].get('properties').get('audio_sampling_frequency')
        extract_track_name = "Track_" + str(id) + "_[" + str(track_type) + "]_[" + str(audio_channels) + "CH]_[" + str(audio_sampling_frequency / 1000) + "kHz]_[" + str(language) + "]"
    elif track_type == "subtitles":
        extract_track_name = "Track_" + str(id) + "_[" + str(track_type) + "]_[" + str(language) + "]"

    if "AVC" in codec_id:
        extract_track_name = extract_track_name + ".h264"
    elif "HEVC" in codec_id:
        extract_track_name = extract_track_name + ".h265"
    elif "V_VP8" in codec_id or "V_VP9" in codec_id:
        extract_track_name = extract_track_name + ".ivf"
    elif "V_AV1" in codec_id:
        extract_track_name = extract_track_name + ".ivf"
    elif "V_MPEG1" in codec_id or "V_MPEG2" in codec_id:
        extract_track_name = extract_track_name + ".mpg"
    elif "V_REAL" in codec_id:
        extract_track_name = extract_track_name + ".rm"
    elif "V_THEORA" in codec_id:
        extract_track_name = extract_track_name + ".ogg"
    elif "V_MS/VFW/FOURCC" in codec_id:
        extract_track_name = extract_track_name + ".avi"
    elif "AAC" in codec_id:
        extract_track_name = extract_track_name + ".aac"
    elif "A_AC3" in codec_id:
        extract_track_name = extract_track_name + ".ac3"
    elif "A_EAC3" in codec_id:
        extract_track_name = extract_track_name + ".eac3"
    elif "ALAC" in codec_id:
        extract_track_name = extract_track_name + ".caf"
    elif "DTS" in codec_id:
        extract_track_name = extract_track_name + ".dts"
    elif "FLAC" in codec_id:
        extract_track_name = extract_track_name + ".flac"
    elif "MPEG/L2" in codec_id:
        extract_track_name = extract_track_name + ".mp2"
    elif "MPEG/L3" in codec_id:
        extract_track_name = extract_track_name + ".mp3"
    elif "OPUS" in codec_id:
        extract_track_name = extract_track_name + ".ogg"
    elif "PCM" in codec_id:
        extract_track_name = extract_track_name + ".wav"
    elif "REAL" in codec_id:
        extract_track_name = extract_track_name + ".ra"
    elif "TRUEHD" in codec_id:
        extract_track_name = extract_track_name + ".thd"
    elif "MLP" in codec_id:
        extract_track_name = extract_track_name + ".mlp"
    elif "TTA1" in codec_id:
        extract_track_name = extract_track_name + ".tta"
    elif "VORBIS" in codec_id:
        extract_track_name = extract_track_name + ".ogg"
    elif "WAVPACK4" in codec_id:
        extract_track_name = extract_track_name + ".wv"
    elif "PGS" in codec_id:
        extract_track_name = extract_track_name + ".sup"
    elif "ASS" in codec_id:
        extract_track_name = extract_track_name + ".ass"
    elif "SSA" in codec_id:
        extract_track_name = extract_track_name + ".ssa"
    elif "UTF8" in codec_id or "ASCII" in codec_id:
        extract_track_name = extract_track_name + ".srt"
    elif "VOBSUB" in codec_id:
        extract_track_name = extract_track_name + ".sub"
    elif "S_KATE" in codec_id:
        extract_track_name = extract_track_name + ".ogg"
    elif "USF" in codec_id:
        extract_track_name = extract_track_name + ".usf"
    elif "WEBVTT" in codec_id:
        extract_track_name = extract_track_name + ".vtt"

def process_dir_all_tracks():
    global i
    global mkv_file
    for mkv_file_in in os.listdir(sys.argv[1]):
        if str(mkv_file_in[-3:]).lower() == "mkv":
            mkv_file_list.append(mkv_file_in)
    os.chdir(sys.argv[1])
    for mkv_file in mkv_file_list:
        folder_name = os.path.dirname(os.path.abspath(mkv_file))
        file_name = mkv_file[0:len(mkv_file) - 4]
        extract_folder = os.path.join(folder_name + "\\" + file_name)
        os.makedirs(extract_folder, exist_ok=True)
        load_json_out()            
        track_count = len(json_data['tracks'])
        extract_track_command = []
        for i in range(track_count):
            load_json_data()                
            process_mkv_file()
            extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
            extract_track_command.append(extract_track_param)
            extract_param_option = ' '.join(extract_track_command)
        command = (f'mkvextract "{os.path.abspath(mkv_file)}" tracks {extract_param_option}')
        os.system('cmd /c "'+ str(command) +'"')
        print(" ")

def extract_all_tracks():
    global i
    global mkv_file
    if input_count >= 2:
        if os.path.isfile(sys.argv[1]) is False:
            process_dir_all_tracks()
        else:
            for mkv_file_id in range(1, input_count):
                folder_name = os.path.dirname(os.path.abspath(sys.argv[int(mkv_file_id)]))
                mkv_file = sys.argv[int(mkv_file_id)]
                folder, file = os.path.split(mkv_file)
                file_name = file[0:len(file) - 4]
                extract_folder = os.path.join(folder_name + "\\" + file_name)
                mkv_file_list.append(mkv_file)
                os.makedirs(extract_folder, exist_ok=True)
                load_json_out()            
                track_count = len(json_data['tracks'])
                extract_track_command = []
                for i in range(track_count):
                    load_json_data()
                    process_mkv_file()
                    extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
                    extract_track_command.append(extract_track_param)
                    extract_param_option = ' '.join(extract_track_command)
                command = (f'mkvextract "{os.path.abspath(mkv_file)}" tracks {extract_param_option}')
                os.system('cmd /c "'+ str(command) +'"')
                print(" ")
    else:
        print("Add mkv file path or folder path")

def process_dir_single_tracks():
    global i
    global mkv_file
    for mkv_file_in in os.listdir(sys.argv[1]):
        if str(mkv_file_in[-3:]).lower() == "mkv":
            mkv_file_list.append(mkv_file_in)
    os.chdir(sys.argv[1])
    for mkv_file in mkv_file_list:
        folder_name = os.path.dirname(os.path.abspath(mkv_file))
        file_name = mkv_file[0:len(mkv_file) - 4]
        extract_folder = os.path.join(folder_name + "\\" + file_name)
        os.makedirs(extract_folder, exist_ok=True)
        list_tracks()
        track_in = input("|--Enter Track ID: ")
        print(" ")
        track_in_list = track_in.split(", ")
        extract_track_command = []
        for i in track_in_list:
            load_json_data()                
            process_mkv_file()
            extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
            extract_track_command.append(extract_track_param)
            extract_param_option = ' '.join(extract_track_command)
        command = (f'mkvextract "{os.path.abspath(mkv_file)}" tracks {extract_param_option}')
        os.system('cmd /c "'+ str(command) +'"')
        print(" ")

def extract_single_track():
    global i
    global mkv_file
    if input_count >= 2:
        if os.path.isfile(sys.argv[1]) is False:
            process_dir_single_tracks()
        else:
            for mkv_file_id in range(1, input_count):
                folder_name = os.path.dirname(os.path.abspath(sys.argv[int(mkv_file_id)]))
                mkv_file = sys.argv[int(mkv_file_id)]
                folder, file = os.path.split(mkv_file)
                file_name = file[0:len(file) - 4]
                extract_folder = os.path.join(folder_name + "\\" + file_name)
                mkv_file_list.append(mkv_file)
                os.makedirs(extract_folder, exist_ok=True)
                extract_track_command = []
                list_tracks()
                track_in = input("|--Enter Track ID: ")
                print(" ")
                track_in_list = track_in.split(", ")
                for i in track_in_list:
                    load_json_data()
                    process_mkv_file()
                    extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
                    extract_track_command.append(extract_track_param)
                    extract_param_option = ' '.join(extract_track_command)
                command = (f'mkvextract "{os.path.abspath(mkv_file)}" tracks {extract_param_option}')
                os.system('cmd /c "'+ str(command) +'"')
                print(" ")
    else:
        print("Add mkv file path or folder path")

def process_dir_chapters():
    global i
    global mkv_file
    global chapters_mode
    for mkv_file_in in os.listdir(sys.argv[1]):
        if str(mkv_file_in[-3:]).lower() == "mkv":
            mkv_file_list.append(mkv_file_in)
    os.chdir(sys.argv[1])
    for mkv_file in mkv_file_list:
        load_json_out()
        if len(json_data.get("chapters")) > 0:
            folder_name = os.path.dirname(os.path.abspath(mkv_file))
            file_name = mkv_file[0:len(mkv_file) - 4]
            extract_folder = os.path.join(folder_name + "\\" + file_name)
            os.makedirs(extract_folder, exist_ok=True)
            if chapters_mode == 1:
                extract_track_param = (f'"{str(extract_folder)}\Chapters.xml"')
                command = (f'mkvextract "{os.path.abspath(mkv_file)}" chapters {extract_track_param}')
            elif chapters_mode == 2:
                extract_track_param = (f'"{str(extract_folder)}\Chapters_OGM.txt"')
                command = (f'mkvextract "{os.path.abspath(mkv_file)}" chapters --simple {extract_track_param}')
            os.system('cmd /c "'+ str(command) +'"')
            print("Chapters Saved.")
            print(" ")
        elif len(json_data.get("chapters")) == 0:
            print("No Chapters.")
            print(" ")

def extract_chapters():
    global i
    global mkv_file
    if input_count >= 2:
        if os.path.isfile(sys.argv[1]) is False:
            process_dir_chapters()
        else:
            for mkv_file_id in range(1, input_count):
                folder_name = os.path.dirname(os.path.abspath(sys.argv[int(mkv_file_id)]))
                mkv_file = sys.argv[int(mkv_file_id)]
                folder, file = os.path.split(mkv_file)
                file_name = file[0:len(file) - 4]
                load_json_out()
                if len(json_data.get("chapters")) > 0:
                    extract_folder = os.path.join(folder_name + "\\" + file_name)
                    mkv_file_list.append(mkv_file)
                    os.makedirs(extract_folder, exist_ok=True)
                    if chapters_mode == 1:
                        extract_track_param = (f'"{str(extract_folder)}\Chapters.xml"')
                        command = (f'mkvextract "{os.path.abspath(mkv_file)}" chapters {extract_track_param}')
                    elif chapters_mode == 2:
                        extract_track_param = (f'"{str(extract_folder)}\Chapters_OGM.txt"')
                        command = (f'mkvextract "{os.path.abspath(mkv_file)}" chapters --simple {extract_track_param}')
                    os.system('cmd /c "'+ str(command) +'"')
                    print("Chapters Saved.")
                    print(" ")
                elif len(json_data.get("chapters")) == 0:
                    print("No Chapters.")
                    print(" ")
    else:
        print("Add mkv file path or folder path")

def process_dir_attachments():
    global i
    global mkv_file
    global attachments_mode
    global attachments_file_name
    for mkv_file_in in os.listdir(sys.argv[1]):
        if str(mkv_file_in[-3:]).lower() == "mkv":
            mkv_file_list.append(mkv_file_in)
    os.chdir(sys.argv[1])
    for mkv_file in mkv_file_list:
        load_json_out()
        if len(json_data.get("attachments")) > 0:
            folder_name = os.path.dirname(os.path.abspath(mkv_file))
            file_name = mkv_file[0:len(mkv_file) - 4]
            extract_folder = os.path.join(folder_name + "\\" + file_name)
            os.makedirs(extract_folder, exist_ok=True)
            if attachments_mode == 1:
                print(" ")
                attachment_count = len(json_data['attachments'])
                extract_track_command = []
                for i in range(attachment_count):
                    load_json_data_attachments()
                    extract_track_param = (f'{str(attachments_id)}:"{str(extract_folder)}\{str(attachments_file_name)}"')
                    extract_track_command.append(extract_track_param)
                    extract_param_option = ' '.join(extract_track_command)
                    command = (f'mkvextract "{os.path.abspath(mkv_file)}" attachments {extract_param_option}')
                os.system('cmd /c "'+ str(command) +'"')
                print("Attachments Saved.")
            elif attachments_mode == 2:
                list_attachments()
                choose_attach_id = input("|--Enter Attachment ID: ")
                print(" ")
                i = int(choose_attach_id) - 1
                attachments_file_name = json_data.get('attachments')[int(i)].get('file_name')
                extract_track_param = (f'{str(choose_attach_id)}:"{str(extract_folder)}\{str(attachments_file_name)}"')
                command = (f'mkvextract "{os.path.abspath(mkv_file)}" attachments {extract_track_param}')
                os.system('cmd /c "'+ str(command) +'"')
                print("Attachments Saved.")
                print(" ")
        elif len(json_data.get("attachments")) == 0:
            print("No Attachments.")
            print(" ")

def extract_attachments():
    global i
    global mkv_file
    global attachments_id
    global attachments_file_name
    if input_count >= 2:
        if os.path.isfile(sys.argv[1]) is False:
            process_dir_attachments()
        else:
            for mkv_file_id in range(1, input_count):
                folder_name = os.path.dirname(os.path.abspath(sys.argv[int(mkv_file_id)]))
                mkv_file = sys.argv[int(mkv_file_id)]
                folder, file = os.path.split(mkv_file)
                file_name = file[0:len(file) - 4]
                load_json_out()
                if len(json_data.get("attachments")) > 0:
                    extract_folder = os.path.join(folder_name + "\\" + file_name)
                    mkv_file_list.append(mkv_file)
                    os.makedirs(extract_folder, exist_ok=True)
                    if attachments_mode == 1:
                        print(" ")
                        attachment_count = len(json_data['attachments'])
                        extract_track_command = []
                        for i in range(attachment_count):
                            load_json_data_attachments()
                            extract_track_param = (f'{str(attachments_id)}:"{str(extract_folder)}\{str(attachments_file_name)}"')
                            extract_track_command.append(extract_track_param)
                            extract_param_option = ' '.join(extract_track_command)
                            command = (f'mkvextract "{os.path.abspath(mkv_file)}" attachments {extract_param_option}')
                        os.system('cmd /c "'+ str(command) +'"')
                        print("Attachments Saved.")
                    elif attachments_mode == 2:
                        list_attachments()
                        choose_attach_id = input("|--Enter Attachment ID: ")
                        print(" ")
                        i = int(choose_attach_id) - 1
                        attachments_file_name = json_data.get('attachments')[int(i)].get('file_name')
                        extract_track_param = (f'{str(choose_attach_id)}:"{str(extract_folder)}\{str(attachments_file_name)}"')
                        command = (f'mkvextract "{os.path.abspath(mkv_file)}" attachments {extract_track_param}')
                        os.system('cmd /c "'+ str(command) +'"')
                        print("Attachments Saved.")
                        print(" ")
                elif len(json_data.get("attachments")) == 0:
                    print("No Attachments.")
                    print(" ")
    else:
        print("Add mkv file path or folder path")

def process_dir_all_tracks_timestamps():
    global i
    global id
    global mkv_file
    global track_type
    for mkv_file_in in os.listdir(sys.argv[1]):
        if str(mkv_file_in[-3:]).lower() == "mkv":
            mkv_file_list.append(mkv_file_in)
    os.chdir(sys.argv[1])
    for mkv_file in mkv_file_list:
        folder_name = os.path.dirname(os.path.abspath(mkv_file))
        file_name = mkv_file[0:len(mkv_file) - 4]
        extract_folder = os.path.join(folder_name + "\\" + file_name)
        os.makedirs(extract_folder, exist_ok=True)
        load_json_out()            
        track_count = len(json_data['tracks'])
        extract_track_command = []
        for i in range(track_count):
            load_json_data()
            extract_track_name = "Track_" + str(id) + "_[" + str(track_type) + "]_tc.txt"
            extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
            extract_track_command.append(extract_track_param)
            extract_param_option = ' '.join(extract_track_command)
        command = (f'mkvextract "{os.path.abspath(mkv_file)}" timecodes_v2 {extract_param_option}')
        print(" ")
        os.system('cmd /c "'+ str(command) +'"')

def extract_all_tracks_timestamps():
    global i
    global mkv_file
    if input_count >= 2:
        if os.path.isfile(sys.argv[1]) is False:
            process_dir_all_tracks_timestamps()
        else:
            for mkv_file_id in range(1, input_count):
                folder_name = os.path.dirname(os.path.abspath(sys.argv[int(mkv_file_id)]))
                mkv_file = sys.argv[int(mkv_file_id)]
                folder, file = os.path.split(mkv_file)
                file_name = file[0:len(file) - 4]
                extract_folder = os.path.join(folder_name + "\\" + file_name)
                mkv_file_list.append(mkv_file)
                os.makedirs(extract_folder, exist_ok=True)
                load_json_out()            
                track_count = len(json_data['tracks'])
                extract_track_command = []
                for i in range(track_count):
                    load_json_data()
                    extract_track_name = "Track_" + str(id) + "_[" + str(track_type) + "]_tc.txt"
                    extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
                    extract_track_command.append(extract_track_param)
                    extract_param_option = ' '.join(extract_track_command)
                command = (f'mkvextract "{os.path.abspath(mkv_file)}" timecodes_v2 {extract_param_option}')
                print(" ")
                os.system('cmd /c "'+ str(command) +'"')
    else:
        print("Add mkv file path or folder path")

def process_dir_single_tracks_timestamps():
    global i
    global mkv_file
    for mkv_file_in in os.listdir(sys.argv[1]):
        if str(mkv_file_in[-3:]).lower() == "mkv":
            mkv_file_list.append(mkv_file_in)
    os.chdir(sys.argv[1])
    for mkv_file in mkv_file_list:
        folder_name = os.path.dirname(os.path.abspath(mkv_file))
        file_name = mkv_file[0:len(mkv_file) - 4]
        extract_folder = os.path.join(folder_name + "\\" + file_name)
        os.makedirs(extract_folder, exist_ok=True)
        list_tracks()
        track_in = input("|--Enter Track ID: ")
        track_in_list = track_in.split(", ")
        extract_track_command = []
        for i in track_in_list:
            load_json_data()                
            extract_track_name = "Track_" + str(id) + "_[" + str(track_type) + "]_tc.txt"
            extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
            extract_track_command.append(extract_track_param)
            extract_param_option = ' '.join(extract_track_command)
        command = (f'mkvextract "{os.path.abspath(mkv_file)}" timecodes_v2 {extract_param_option}')
        print(" ")
        os.system('cmd /c "'+ str(command) +'"')

def extract_single_track_timestamps():
    global i
    global mkv_file
    if input_count >= 2:
        if os.path.isfile(sys.argv[1]) is False:
            process_dir_single_tracks_timestamps()
        else:
            for mkv_file_id in range(1, input_count):
                folder_name = os.path.dirname(os.path.abspath(sys.argv[int(mkv_file_id)]))
                mkv_file = sys.argv[int(mkv_file_id)]
                folder, file = os.path.split(mkv_file)
                file_name = file[0:len(file) - 4]
                extract_folder = os.path.join(folder_name + "\\" + file_name)
                mkv_file_list.append(mkv_file)
                os.makedirs(extract_folder, exist_ok=True)
                extract_track_command = []
                list_tracks()
                track_in = input("|--Enter Track ID: ")
                track_in_list = track_in.split(", ")
                for i in track_in_list:
                    load_json_data()
                    extract_track_name = "Track_" + str(id) + "_[" + str(track_type) + "]_tc.txt"
                    extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
                    extract_track_command.append(extract_track_param)
                    extract_param_option = ' '.join(extract_track_command)
                command = (f'mkvextract "{os.path.abspath(mkv_file)}" timecodes_v2 {extract_param_option}')
                print(" ")
                os.system('cmd /c "'+ str(command) +'"')

def process_dir_all_tracks_cue():
    global i
    global id
    global mkv_file
    global track_type
    for mkv_file_in in os.listdir(sys.argv[1]):
        if str(mkv_file_in[-3:]).lower() == "mkv":
            mkv_file_list.append(mkv_file_in)
    os.chdir(sys.argv[1])
    for mkv_file in mkv_file_list:
        folder_name = os.path.dirname(os.path.abspath(mkv_file))
        file_name = mkv_file[0:len(mkv_file) - 4]
        extract_folder = os.path.join(folder_name + "\\" + file_name)
        os.makedirs(extract_folder, exist_ok=True)
        load_json_out()            
        track_count = len(json_data['tracks'])
        extract_track_command = []
        for i in range(track_count):
            load_json_data()
            extract_track_name = "Track_" + str(id) + "_[" + str(track_type) + "]_cues.txt"
            extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
            extract_track_command.append(extract_track_param)
            extract_param_option = ' '.join(extract_track_command)
        command = (f'mkvextract "{os.path.abspath(mkv_file)}" cues {extract_param_option}')
        print(" ")
        os.system('cmd /c "'+ str(command) +'"')

def extract_all_tracks_cue():
    global i
    global mkv_file
    if input_count >= 2:
        if os.path.isfile(sys.argv[1]) is False:
            process_dir_all_tracks_cue()
        else:
            for mkv_file_id in range(1, input_count):
                folder_name = os.path.dirname(os.path.abspath(sys.argv[int(mkv_file_id)]))
                mkv_file = sys.argv[int(mkv_file_id)]
                folder, file = os.path.split(mkv_file)
                file_name = file[0:len(file) - 4]
                extract_folder = os.path.join(folder_name + "\\" + file_name)
                mkv_file_list.append(mkv_file)
                os.makedirs(extract_folder, exist_ok=True)
                load_json_out()            
                track_count = len(json_data['tracks'])
                extract_track_command = []
                for i in range(track_count):
                    load_json_data()
                    extract_track_name = "Track_" + str(id) + "_[" + str(track_type) + "]_cues.txt"
                    extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
                    extract_track_command.append(extract_track_param)
                    extract_param_option = ' '.join(extract_track_command)
                command = (f'mkvextract "{os.path.abspath(mkv_file)}" cues {extract_param_option}')
                print(" ")
                os.system('cmd /c "'+ str(command) +'"')
    else:
        print("Add mkv file path or folder path")

def process_dir_single_tracks_cue():
    global i
    global mkv_file
    for mkv_file_in in os.listdir(sys.argv[1]):
        if str(mkv_file_in[-3:]).lower() == "mkv":
            mkv_file_list.append(mkv_file_in)
    os.chdir(sys.argv[1])
    for mkv_file in mkv_file_list:
        folder_name = os.path.dirname(os.path.abspath(mkv_file))
        file_name = mkv_file[0:len(mkv_file) - 4]
        extract_folder = os.path.join(folder_name + "\\" + file_name)
        os.makedirs(extract_folder, exist_ok=True)
        list_tracks()
        track_in = input("|--Enter Track ID: ")
        track_in_list = track_in.split(", ")
        extract_track_command = []
        for i in track_in_list:
            load_json_data()                
            extract_track_name = "Track_" + str(id) + "_[" + str(track_type) + "]_cues.txt"
            extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
            extract_track_command.append(extract_track_param)
            extract_param_option = ' '.join(extract_track_command)
        command = (f'mkvextract "{os.path.abspath(mkv_file)}" cues {extract_param_option}')
        print(" ")
        os.system('cmd /c "'+ str(command) +'"')
        print(" ")

def extract_single_track_cue():
    global i
    global mkv_file
    if input_count >= 2:
        if os.path.isfile(sys.argv[1]) is False:
            process_dir_single_tracks_cue()
        else:
            for mkv_file_id in range(1, input_count):
                folder_name = os.path.dirname(os.path.abspath(sys.argv[int(mkv_file_id)]))
                mkv_file = sys.argv[int(mkv_file_id)]
                folder, file = os.path.split(mkv_file)
                file_name = file[0:len(file) - 4]
                extract_folder = os.path.join(folder_name + "\\" + file_name)
                mkv_file_list.append(mkv_file)
                os.makedirs(extract_folder, exist_ok=True)
                extract_track_command = []
                list_tracks()
                track_in = input("|--Enter Track ID: ")
                track_in_list = track_in.split(", ")
                for i in track_in_list:
                    load_json_data()
                    extract_track_name = "Track_" + str(id) + "_[" + str(track_type) + "]_cues.txt"
                    extract_track_param = (f'{str(id)}:"{str(extract_folder)}\{str(extract_track_name)}"')
                    extract_track_command.append(extract_track_param)
                    extract_param_option = ' '.join(extract_track_command)
                command = (f'mkvextract "{os.path.abspath(mkv_file)}" cues {extract_param_option}')
                print(" ")
                os.system('cmd /c "'+ str(command) +'"')
                print(" ")

def process_dir_cue_sheet():
    global i
    global mkv_file
    global chapters_mode
    for mkv_file_in in os.listdir(sys.argv[1]):
        if str(mkv_file_in[-3:]).lower() == "mkv":
            mkv_file_list.append(mkv_file_in)
    os.chdir(sys.argv[1])
    for mkv_file in mkv_file_list:
        folder_name = os.path.dirname(os.path.abspath(mkv_file))
        file_name = mkv_file[0:len(mkv_file) - 4]
        extract_folder = os.path.join(folder_name + "\\" + file_name)
        os.makedirs(extract_folder, exist_ok=True)
        extract_track_param = (f'"{str(extract_folder)}\cue_sheet.cue"')
        command = (f'mkvextract "{os.path.abspath(mkv_file)}" cuesheet {extract_track_param}')
        os.system('cmd /c "'+ str(command) +'"')

def extract_cue_sheet():
    global i
    global mkv_file
    if input_count >= 2:
        if os.path.isfile(sys.argv[1]) is False:
            process_dir_cue_sheet()
        else:
            for mkv_file_id in range(1, input_count):
                folder_name = os.path.dirname(os.path.abspath(sys.argv[int(mkv_file_id)]))
                mkv_file = sys.argv[int(mkv_file_id)]
                folder, file = os.path.split(mkv_file)
                file_name = file[0:len(file) - 4]
                extract_folder = os.path.join(folder_name + "\\" + file_name)
                mkv_file_list.append(mkv_file)
                os.makedirs(extract_folder, exist_ok=True)
                extract_track_param = (f'"{str(extract_folder)}\cue_sheet.cue"')
                command = (f'mkvextract "{os.path.abspath(mkv_file)}" cuesheet {extract_track_param}')
                os.system('cmd /c "'+ str(command) +'"')
    else:
        print("Add mkv file path or folder path")

def process_dir_tags():
    global i
    global mkv_file
    for mkv_file_in in os.listdir(sys.argv[1]):
        if str(mkv_file_in[-3:]).lower() == "mkv":
            mkv_file_list.append(mkv_file_in)
    os.chdir(sys.argv[1])
    for mkv_file in mkv_file_list:
        load_json_out()
        if len(json_data.get("global_tags")) or len(json_data.get("track_tags")) > 0:
            folder_name = os.path.dirname(os.path.abspath(mkv_file))
            file_name = mkv_file[0:len(mkv_file) - 4]
            extract_folder = os.path.join(folder_name + "\\" + file_name)
            os.makedirs(extract_folder, exist_ok=True)
            extract_track_param = (f'"{str(extract_folder)}\Tags.xml"')
            command = (f'mkvextract "{os.path.abspath(mkv_file)}" tags {extract_track_param}')
            os.system('cmd /c "'+ str(command) +'"')
            print(" ")
            print("Tags Saved.")
        elif len(json_data.get("global_tags")) == 0:
            if len(json_data.get("track_tags")) == 0:
                print(" ")
                print("No Tags.")

def extract_tags():
    global i
    global mkv_file
    if input_count >= 2:
        if os.path.isfile(sys.argv[1]) is False:
            process_dir_tags()
        else:
            for mkv_file_id in range(1, input_count):
                folder_name = os.path.dirname(os.path.abspath(sys.argv[int(mkv_file_id)]))
                mkv_file = sys.argv[int(mkv_file_id)]
                folder, file = os.path.split(mkv_file)
                file_name = file[0:len(file) - 4]
                load_json_out()
                if len(json_data.get("global_tags")) or len(json_data.get("track_tags")) > 0:
                    extract_folder = os.path.join(folder_name + "\\" + file_name)
                    mkv_file_list.append(mkv_file)
                    os.makedirs(extract_folder, exist_ok=True)
                    extract_track_param = (f'"{str(extract_folder)}\Tags.xml"')
                    command = (f'mkvextract "{os.path.abspath(mkv_file)}" tags {extract_track_param}')
                    os.system('cmd /c "'+ str(command) +'"')
                    print(" ")
                    print("Tags Saved.")
                elif len(json_data.get("global_tags")) == 0:
                    if len(json_data.get("track_tags")) == 0:
                        print(" ")
                        print("No Tags.")
    else:
        print("Add mkv file path or folder path")

print("mkvextractor (MKVToolNix : mkvextract)")
print("|")
print("|-- 1 : Extract All Traks")
print("|-- 2 : Extract Single Tracks")
print("|-- 3 : Extract Chapters")
print("|-- 4 : Extract Attachments")
print("|-- 5 : Extract Timestamps")
print("|-- 6 : Extract Cues")
print("|-- 7 : Extract Cue Sheet")
print("|-- 8 : Extract Tags")
extract_mode = int(input("|--Extract Mode: "))

if extract_mode == 1:
    print(" ")
    extract_all_tracks()
elif extract_mode == 2:
    extract_single_track()
elif extract_mode == 3:
    print("|")
    print("|-- 1 : XML")
    print("|-- 2 : OGM")
    chapters_mode = int(input("|--Chapters Mode: "))
    print(" ")
    extract_chapters()
elif extract_mode == 4:
    print("|")
    print("|-- 1 : All Attachments")
    print("|-- 2 : Select Attachment")
    attachments_mode = int(input("|--Attachments Mode: "))
    extract_attachments()
elif extract_mode == 5:
    print("|")
    print("|-- 1 : Timestamps from all Tracks")
    print("|-- 2 : Timestamps from a Single Track")
    timestamps_mode = int(input("|--Timestamps Mode: "))
    if timestamps_mode == 1:
        extract_all_tracks_timestamps()
    elif timestamps_mode == 2:
        extract_single_track_timestamps()
elif extract_mode == 6:
    print("|")
    print("|-- 1 : Cues from all Tracks")
    print("|-- 2 : Cues from a Single Track")
    cues_mode = int(input("|--Cues Mode: "))
    if cues_mode == 1:
        extract_all_tracks_cue()
    elif cues_mode == 2:
        extract_single_track_cue()
elif extract_mode == 7:
    print(" ")
    extract_cue_sheet()
elif extract_mode == 8:
    extract_tags()
