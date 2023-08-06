# imgextract 

[imgextract v0.0.2](https://pypi.org/project/imgextract/)

This python package can be used for extracting pages from PDF and TIF/TIFF files.


This packages uses poppler for reading pdf files and tkinter for gui, for windows platform poppler has been included in package and tkinter can be installed with python but for linux we have to install them manually.

## How to install poppler and tkinter

We can download poppler from [poppler](https://poppler.freedesktop.org/) 

OR

We can install poppler using below command 

```

sudo apt-get install python-poppler

```

Install tkinter in linux using below command

```

sudo apt-get update
sudo apt-get install python3-tk


```

## How to use

### pdf page extraction

```python

from imgextract.imgext import ImgExtractor

if __name__ == "__main__":
    ss = ImgExtractor()
    # input files path, out put files path and file type
    ss.extract("/home/user/pdf_files", "/home/user/image_files", "pdf")


```

### tif/tiff image extraction

```python

from imgextract.imgext import ImgExtractor

if __name__ == "__main__":
    ss = ImgExtractor()
    # input files path, out put files path and file type
    ss.extract("/home/user/tif_files", "/home/user/image_files", "tif")


```

### GUI for Image extraction


[![GUI for Image extraction](screenshot.png)](https://pypi.org/project/imgextract/)


```python

from imgextract.imggui import GuiExtractor

if __name__ == "__main__":
    ss = GuiExtractor()
    ss.openwindow()


```

### Installation

```shell
$ pip install imgextract
```

### License

  [MIT](LICENSE)