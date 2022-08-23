import os
import sys
import json
import subprocess

inputCount = len(sys.argv)

mkvList = []
webmList = []

#process all inputs and get 'mkv' and 'webm' files.

def inputProcess():
    if inputCount == 2:
        if os.path.isfile(sys.argv[1]) is False:
            for inputFile in os.listdir(sys.argv[1]):
                if os.path.splitext(inputFile)[1] == '.mkv':
                    mkvList.append(inputFile)
                elif os.path.splitext(inputFile)[1] == '.webm':
                    webmList.append(inputFile)
        else:
            mkvList.append(sys.argv[1])
    elif inputCount > 2:
        for inputID in range(1, inputCount):
            if os.path.splitext(sys.argv[inputID])[1] == '.mkv':
                mkvList.append(sys.argv[inputID])
            elif os.path.splitext(sys.argv[inputID])[1] == '.webm':
                webmList.append(sys.argv[inputID])
    else:
        print(f'Please provide inputs...')

#get stream information in json format.

def get_output(mediaFile):
    global jsonData
    mkvmerge_JSON = subprocess.check_output(
        [
            'mkvmerge',
            '--identify',
            '--identification-format',
            'json',
            os.path.abspath(mediaFile),
        ],
        stderr=subprocess.DEVNULL
    )
    jsonData = json.loads(mkvmerge_JSON)

#parse data from json output

def get_tracks(mediaFile):
    get_output(mediaFile)
    global id; id = jsonData.get('tracks')[int(i)].get('id')
    global language; language = jsonData.get('tracks')[int(i)].get('properties').get('language')
    global language_ietf; language_ietf = jsonData.get('tracks')[int(i)].get('properties').get('language_ietf')
    global title; title = jsonData.get('tracks')[int(i)].get('properties').get('track_name')
    global codec_id; codec_id = jsonData.get('tracks')[int(i)].get('properties').get('codec_id')
    global codec; codec = jsonData.get('tracks')[int(i)].get('codec')
    global track_type; track_type = jsonData.get('tracks')[int(i)].get('type')

def get_attachments(mediaFile):
    get_output(mediaFile)
    global attach_id; attach_id = jsonData.get('attachments')[int(i)].get('id')
    global attach_type; attach_type = jsonData.get('attachments')[int(i)].get('content_type')
    global attach_desc; attach_desc = jsonData.get('attachments')[int(i)].get('description')
    global attach_name; attach_name = jsonData.get('attachments')[int(i)].get('file_name')
    global attach_uid; attach_uid = jsonData.get('attachments')[int(i)].get('properties').get('uid')

#List available tracks

def viewTracks(mediaFile):
    global i
    get_output(mediaFile)
    trackCount = len(jsonData['tracks'])
    print(os.path.basename(mediaFile))
    for i in range(trackCount):
        get_tracks(mediaFile)
        print(f'\nTrack ID : {id}')
        print(f'  |')
        print(f'  |--Type           : {track_type}')
        print(f'  |--Codec          : {codec}')
        print(f'  |--Language       : {language}')
        print(f'  |--Language_ietf  : {language_ietf}')
        print(f'  |--Title          : {title}')

#List available attachments

def viewAttachments(mediaFile):
    global i
    get_output(mediaFile)
    attachmentCount = len(jsonData['attachments'])
    print(os.path.basename(mediaFile))
    for i in range(attachmentCount):
        get_attachments(mediaFile)
        print(f'\nAttachment ID : {attach_id}')
        print(f'  |')
        print(f'  |--ContentType    : {attach_type}')
        print(f'  |--Filename       : {attach_name}')
        print(f'  |--Description    : {attach_desc}')
        print(f'  |--UID            : {attach_uid}')

#process the input file

def processFile(mediaFile):
    global extractName

    if track_type == 'video':
        get_output(mediaFile)
        pixel_dimensions = jsonData.get('tracks')[int(i)].get('properties').get('pixel_dimensions')
        extractName = f'TrackID_{id}_[{track_type}]_[{pixel_dimensions}]_[{language}]'
    elif track_type == 'audio':
        get_output(mediaFile)
        audio_channels = jsonData.get('tracks')[int(i)].get('properties').get('audio_channels')
        audio_sampling_frequency = jsonData.get('tracks')[int(i)].get('properties').get('audio_sampling_frequency')
        extractName = f'TrackID_{id}_[{track_type}]_[{audio_channels}CH]_[{audio_sampling_frequency / 1000}kHz]_[{language}]'
    elif track_type == "subtitles":
        extractName = f'TrackID_{id}_[{track_type}]_[{language}]'
    
    if "AVC" in codec_id:
        extractName = extractName + ".264"
    elif "HEVC" in codec_id:
        extractName = extractName + ".hevc"
    elif "V_VP8" in codec_id:
        extractName = extractName + ".ivf"
    elif "V_VP9" in codec_id:
        extractName = extractName + ".ivf"
    elif "V_AV1" in codec_id:
        extractName = extractName + ".ivf"
    elif "V_MPEG1" in codec_id:
        extractName = extractName + ".mpg"
    elif "V_MPEG2" in codec_id:
        extractName = extractName + ".mpg"
    elif "V_REAL" in codec_id:
        extractName = extractName + ".rm"
    elif "V_THEORA" in codec_id:
        extractName = extractName + ".ogg"
    elif "V_MS/VFW/FOURCC" in codec_id:
        extractName = extractName + ".avi"
    elif "AAC" in codec_id:
        extractName = extractName + ".aac"
    elif "A_AC3" in codec_id:
        extractName = extractName + ".ac3"
    elif "A_EAC3" in codec_id:
        extractName = extractName + ".eac3"
    elif "ALAC" in codec_id:
        extractName = extractName + ".caf"
    elif "DTS" in codec_id:
        extractName = extractName + ".dts"
    elif "FLAC" in codec_id:
        extractName = extractName + ".flac"
    elif "MPEG/L2" in codec_id:
        extractName = extractName + ".mp2"
    elif "MPEG/L3" in codec_id:
        extractName = extractName + ".mp3"
    elif "OPUS" in codec_id:
        extractName = extractName + ".ogg"
    elif "PCM" in codec_id:
        extractName = extractName + ".wav"
    elif "REAL" in codec_id:
        extractName = extractName + ".ra"
    elif "TRUEHD" in codec_id:
        extractName = extractName + ".thd"
    elif "MLP" in codec_id:
        extractName = extractName + ".mlp"
    elif "TTA1" in codec_id:
        extractName = extractName + ".tta"
    elif "VORBIS" in codec_id:
        extractName = extractName + ".ogg"
    elif "WAVPACK4" in codec_id:
        extractName = extractName + ".wv"
    elif "PGS" in codec_id:
        extractName = extractName + ".sup"
    elif "ASS" in codec_id:
        extractName = extractName + ".ass"
    elif "SSA" in codec_id:
        extractName = extractName + ".ssa"
    elif "UTF8" in codec_id:
        extractName = extractName + ".srt"
    elif "ASCII" in codec_id:
        extractName = extractName + ".srt"
    elif "VOBSUB" in codec_id:
        extractName = extractName + ".sub"
    elif "S_KATE" in codec_id:
        extractName = extractName + ".ogg"
    elif "USF" in codec_id:
        extractName = extractName + ".usf"
    elif "WEBVTT" in codec_id:
        extractName = extractName + ".vtt"

#make the items extract folder

def makeFolder(mediaFile):
    mediaFolder = os.path.dirname(mediaFile)
    mediaName = os.path.splitext(os.path.basename(mediaFile))[0]
    global extractFolder; extractFolder = os.path.join(mediaFolder, mediaName)
    os.makedirs(extractFolder, exist_ok=True)

#run commands for extract all tracks available

def runTracks(mediaFile):
    global i
    commandList = []
    makeFolder(mediaFile)
    get_output(mediaFile)
    trackCount = len(jsonData['tracks'])
    for i in range(trackCount):
        get_tracks(mediaFile)
        processFile(mediaFile)
        extractPath = os.path.join(extractFolder, extractName)
        extractParam = f'{id}:"{extractPath}"'
        commandList.append(extractParam)
    extractParam = ' '.join(commandList)
    command = f'mkvextract "{mediaFile}" tracks {extractParam}'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(process.stdout.decode())

#run commands for extract a specific track(s)

def runTrack(mediaFile):
    global i
    commandList = []
    makeFolder(mediaFile)
    viewTracks(mediaFile)
    trackID = input(f'\ntrackID: ')
    trackID = trackID.split(', ')
    for i in trackID:
        get_tracks(mediaFile)
        processFile(mediaFile)
        extractPath = os.path.join(extractFolder, extractName)
        extractParam = f'{id}:"{extractPath}"'
        commandList.append(extractParam)
    extractParam = ' '.join(commandList)
    command = f'mkvextract "{mediaFile}" tracks {extractParam}'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('\n' + process.stdout.decode())

#run commands for extract chapters

def runChapters(mediaFile):
    get_output(mediaFile)
    if len(jsonData.get('chapters')) > 0:
        makeFolder(mediaFile)
        if chaptersMode == 1:
            extractPath = os.path.join(extractFolder, 'Chapters_XML.xml')
            command = f'mkvextract "{mediaFile}" chapters "{extractPath}"'
        if chaptersMode == 2:
            extractPath = os.path.join(extractFolder, 'Chapters_OGM.txt')
            command = f'mkvextract "{mediaFile}" chapters --simple "{extractPath}"'
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(f'Extracting chapters to the file "{extractPath}".\nProgress: 100%')
    elif len(jsonData.get('chapters')) == 0:
        print(f'No chapters available in "{os.path.basename(mediaFile)}"')

#run commands for extract attachments

def runAttachments(mediaFile):
    global i
    commandList = []
    get_output(mediaFile)
    if len(jsonData.get('attachments')) > 0:
        makeFolder(mediaFile)
        viewAttachments(mediaFile)
        attachmentID = input(f'\nattachmentID: ')
        attachmentID = attachmentID.split(', ')
        for i in attachmentID:
            i = int(i) - 1
            get_attachments(mediaFile)
            extractPath = os.path.join(extractFolder, attach_name)
            extractParam = f'{attach_id}:"{extractPath}"'
            commandList.append(extractParam)
        extractParam = ' '.join(commandList)
        command = f'mkvextract "{mediaFile}" attachments {extractParam}'
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('\n' + process.stdout.decode())
    elif len(jsonData.get('attachments')) == 0:
        print(f'No attachments available in "{os.path.basename(mediaFile)}"')

#run commands for extract timestamps for all tracks

def runTimestamps(mediaFile):
    global i
    commandList = []
    makeFolder(mediaFile)
    get_output(mediaFile)
    trackCount = len(jsonData['tracks'])
    for i in range(trackCount):
        get_tracks(mediaFile)
        extractName = f'TrackID_{id}_[{track_type}]_[tc].txt'
        extractPath = os.path.join(extractFolder, extractName)
        extractParam = f'{id}:"{extractPath}"'
        commandList.append(extractParam)
    extractParam = ' '.join(commandList)
    command = f'mkvextract "{mediaFile}" timecodes_v2 {extractParam}'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(process.stdout.decode())

#run commands for extract cues for all tracks

def runCues(mediaFile):
    global i
    commandList = []
    makeFolder(mediaFile)
    get_output(mediaFile)
    trackCount = len(jsonData['tracks'])
    for i in range(trackCount):
        get_tracks(mediaFile)
        extractName = f'TrackID_{id}_[{track_type}]_[cues].txt'
        extractPath = os.path.join(extractFolder, extractName)
        extractParam = f'{id}:"{extractPath}"'
        commandList.append(extractParam)
    extractParam = ' '.join(commandList)
    command = f'mkvextract "{mediaFile}" cues {extractParam}'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(process.stdout.decode())

#run commands for extract cue sheet

def runCueSheet(mediaFile):
    makeFolder(mediaFile)
    extractPath = os.path.join(extractFolder, 'Cue_Sheet.cue')
    command = f'mkvextract "{mediaFile}" cuesheet "{extractPath}"'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(process.stdout.decode())

#run commands for extract tags

def runTags(mediaFile):
    makeFolder(mediaFile)
    get_output(mediaFile)
    if (len(jsonData.get('global_tags')) > 0) or (len(jsonData.get('track_tags')) > 0):
        extractPath = os.path.join(extractFolder, 'Tags.xml')
        command = f'mkvextract "{mediaFile}" tags "{extractPath}"'
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(f'Extracting tags to the file "{extractPath}".\nProgress: 100%')
    elif (len(jsonData.get('global_tags')) == 0) and (len(jsonData.get('track_tags')) == 0):
        print(f'No tags available in "{os.path.basename(mediaFile)}"')

#main screen for running the script

def main():
    inputProcess()
    mediaList = mkvList + webmList
    mediaList = sorted(mediaList)

    extractMode = int(input(
        f'\nmkvextractor (MKVToolNix : mkvextract)\
        \n|\
        \n|-- 1 : Extract All Tracks\
        \n|-- 2 : Extract Single Tracks\
        \n|-- 3 : Extract Chapters\
        \n|-- 4 : Extract Attachments\
        \n|-- 5 : Extract Timestamps\
        \n|-- 6 : Extract Cues\
        \n|-- 7 : Extract Cue Sheet\
        \n|-- 8 : Extract Tags\
        \n\
        \nextractMode: '
    ))
    
    print(' ')

    if extractMode == 1:
        for file in mediaList: runTracks(file)
    elif extractMode == 2:
        for file in mediaList: runTrack(file)
    elif extractMode == 3:
        global chaptersMode
        chaptersMode = int(input(
            f'1 : XML Chapters\
            \n2 : OGM Chapters\
            \n\nchaptersMode: '))
        print(' ')
        for file in mediaList: runChapters(file)
    elif extractMode == 4:
        for file in mediaList: runAttachments(file)
    elif extractMode == 5:
        for file in mediaList: runTimestamps(file)
    elif extractMode == 6:
        for file in mediaList: runCues(file)
    elif extractMode == 7:
        for file in mediaList: runCueSheet(file)
    elif extractMode == 8:
        for file in mediaList: runTags(file)

#run script

if __name__ == "__main__":
    main()
