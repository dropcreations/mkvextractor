# **MKVExtractor**

This ***mkvextractor python script*** is to use ***MKVToolNix's mkvextract***.

To use this python script you have to install MKVToolNix and add mkvextract path in environment variables and you have to be installed python.

## **Install MKVToolNix**

You can download and install MKVToolNix from [this](https://www.fosshub.com/MKVToolNix.html) link.

## **Set path to mkvextract**

- Right click on **"This PC"** and select **"Properties"**
- Now click on **"Advanced system settings"**
- Now select **"Environment Variables..."**
- Then select **"Path"** row in **'System variables'** section and hit **"Edit"**
- Click on **"New"** button and add your **installed MKVToolNix path** to it. (Usually it is **"C:\Program Files\MKVToolNix"**)


## **Usage**

- First of all add **`mkvextractor.py`** file to MKVToolNix folder.
- Open **Terminal** and type below command.
- You can add one mkv file or more mkv files at once.

`python mkvextractor.py [mkv_file_1] [mkv_file_2].......`

- You can also add a folder that includes mkv files.
- Don't add more than one folder.

`python mkvextractor.py [folder_path]`

### **NOTE**
- This is completely tested on **Windows**.