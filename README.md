# ByteSweep
### A simple python CLI tool for removing corrupted duplicates of files.

#### Package Requirements:
- Pillow (pip)
- [ffmpeg](https://www.ffmpeg.org/download.html) must be added to `PATH`

### Usage:
> `python ByteSweep.py "Path\To\Folder"`
### Supported Filetypes:
- All utf-8 endcoded files: `.html` `.css` `.js` `.txt` `.xml` `.json` `.ini` `.bat` `.log` `.cs` Unity project files, and more.
- Images: `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.tiff` `.webp` `.gif`
- Audio files: `.mp3` `.wav` `.flac` `.aac` `.ogg` `.m4a` `.wma` `.alac` `.opus`
- Video files: `.mp4` `.m4v` `.avi` `.mov` `.mkv` `.webm` `.flv` `.wmv` `.mpeg` `.mpg`
- Adobe: `.psd`
- Microsoft Office: `.docx` `.xlsx` `.pptx`
- OpenDocument files: `.odp` `.ods` `.odt`
- Blender Files: `.blend` `.blend1`
- Fonts: `.ttf` `.otf`
- Other files: `.pdf` `.jar` `.dll` `.exe` `.zip` `.ess` `.pyz` `.manifest` `.fbx`
- Experimental but work so far: `.obj` 

### Contribution
- This tool can be made to work with even more filetypes relatively easily.
- The code works for non-media files if you can *mostly* decode the file in `utf-8` (first 2KiB) or there is a constant file signature in the header
- Feel free to add extension types to see if it just works
> **Note**: Media files like images, video and audio files rely on `Pillow` and `ffmpeg`, so if these libraries support some file extension I've not included here, it should just work by adding it in.
- If you want to make a pull request, go ahead, I'll review changes and merge.