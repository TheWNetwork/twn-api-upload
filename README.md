# twn-api-upload
TheWNetwork bot to upload massively to a Telebox & Terabox folder.
- Allow Pictures and Videos

## Preparation
1.  ``pip install -Ur requirements.txt``

2. Copy base.env to .env and fill all the gaps

3. How to get the values for the .env file:

| Variable | Description |
| --- | --- |
| TELEBOX_TOKEN | Access to https://www.linkbox.to/admin/account and copy "Token" |
| TELEBOX_BASEFOLDER | Access to https://www.linkbox.to/admin/my-files, search the folder you wanna use and copy the ID. <br/>Do it copying from the url bar. <br/>Will have a format-like: https://www.linkbox.to/admin/share-folder/12345678 (12345678 is the ID) |

- ``python -m app --dir <path_to_folder> --filename <filename>``

> ``--telebox`` upload to telebox (you need to configrue the .env) [Working]
>
> ``--terabox`` upload to terabox (you need to configrue the .env) [MayNotWork]
>
> ``--dir`` is the path to the folder where the files are located
> 
> ``--filename`` is the name of the folder to be uploaded. will be created if not exists on Telebox

Imagine you have a folder named "FolderToUpload" that have a list of subfolders with names (can be recursive also). 
You must put on "filename" the folder you wanna upload. This folder WONT be created. (as you already created it on Linkbox)  

- Example: ``python -m app --telebox --dir /home/user/Downloads --filename FolderToUpload``

### Notes
Telebox speed is stupidly low, it may take a long time to upload large files. 
Also, the Telebox API does not give any information about how its working so, sorry

## Termux pre requisites
- ``pkg update``
- ``pkg in python-numpy -y``
- ``pkg in opencv-python -y``

# DISCLAIMER OF SOFTWARE WARRANTY

THEWNETWORK PROVIDES THE SOFTWARE TO YOU "AS IS" AND WITHOUT WARRANTY OF ANY KIND, EXPRESS, IMPLIED OR OTHERWISE, INCLUDING WITHOUT LIMITATION ANY WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.

THE USER IS SOLELY RESPONSIBLE FOR THE ACTIONS CARRIED OUT WITH THIS CODE AND THE COMPANY IS NOT RESPONSIBLE FOR ANY MANIPULATION, INVONVENIENCE, ERROR OR PROBLEM, BOTH LEGAL AND OF ANY OTHER TYPE THAT THE USER MAY SUFFER USING THE CODE.

