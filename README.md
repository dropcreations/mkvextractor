<!-- PROJECT INTRO -->

__mkvExtractor__
=========

This python script is to use __MKVToolNix's mkvextract__ CLI tool.
You can extract content from both __MKV__ and __WebM__ containers.

## __Usage__

- Open __Terminal__ and type below command.
- You can add one or more files at once.
```shell
python mkvextractor.py [file_01] [file_02] [file_03]...
```
- You can also add a folder that includes MKV and WebM files.
- Don't add more than one folder.
```shell
python mkvextractor.py [folder_path]
```
- You can extract,
    - [__All tracks__](#extract-mode--all-tracks)
    - [__Single tracks__](#extract-mode--single-tracks)
    - [__Chapters__](#extract-mode--chapters)
    - [__Attachments__](#extract-mode--attachments)
    - [__Timestamps__](#extract-mode--timestamps)
    - [__Cues__](#extract-mode--cues)
    - [__Cue Sheets__](#extract-mode--cue-sheets)
    - [__Tags__](#extract-mode--tags)

### __Extract Mode : All tracks__

You can extract all video, audio and subtitle tracks available in all inputs.

### __Extract Mode : Single tracks__

In this mode, analyze every input and show a list of tracks that available, then you can enter track IDs that you want to extract.
Please seperate track numbers by a comma and a space<br>
- eg: `trackID: 0, 1, 2,...`

### __Extract Mode : Chapters__

You can extract chapters in both XML and OGM formats. Provide your choice when it asked.

### __Extract Mode : Attachments__

In this mode, also analyze every input and show a list of attachments that available, then you can enter attachment IDs that you want to extract.
Please seperate attachment IDs by a comma and a space<br>
- eg: `attachmentID: 1, 2, 3,...`

### __Extract Mode : Timestamps__

You can extract timestamps for all tracks at once.

### __Extract Mode : Cues__

You can extract cues for all tracks that available at once.

### __Extract Mode : Cue Sheets__

You can extract cue sheet in all inputs if available.

### __Extract Mode : Tags__

You can extract tags in all inputs if available.
