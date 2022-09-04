# Ciri


![Ciri Logo](images/readme_header.png)

Ciri is a steganography tool which uses AES-256 in GCM mode to encrypt the given input (txt file) and uses LSB (Least Significant Bit) to hide the data inside an image.

## Usage

To run this browser on your machine, simply run executable file or launch a terminal and run this command:

```
python ciri.py
```

[intro.webm](https://user-images.githubusercontent.com/71812212/188296064-95ff7f30-b023-4448-8181-a5c62aec735a.webm)


### Hiding Data
This tool is very straightforward and everything is clear. If you want to hide a message inside an image click on "Embed". Choose a text file and enter a strong password to encrypt it. Select a carrier which holds your message. When you are ready click on "Embed". If the operation was successful, you'll see a check mark. Do not try to store long texts inside the image.

[embed.webm](https://user-images.githubusercontent.com/71812212/188296106-83172d26-949a-4a7c-a6c9-02c62e16a6d3.webm)
  
### Extracting Data
If you have a carrier and you want to extract the hidden message, you must have the password to decrypt the text file. Open carrier and enter password and choose a directory where you want to save your message. When you're ready click on "Extract" button. If the operation was successful, you'll see a check mark.

[extract.webm](https://user-images.githubusercontent.com/71812212/188296125-897e67f6-5644-4740-9cd3-56dee5325e63.webm)


## Requirements

To install requirements for this project, open up a terminal window and run this command:

```
pip install -r requirements.txt	
```

## Disclaimer

Please do not use this tool for any nefarious purposes. I am not responsible for any kind of harm or damage. Use this tool at your own risk.
