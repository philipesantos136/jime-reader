# jime-reader
Reader for the boardgame Journeys in Middle Earth. Project built using computer vision (OpenCV), intense image pre-processing, text extraction from images (Tesseract OCR) and cloud computing (Azure TTS - free)
This project is an improved and PT-BR version of the user's project https://github.com/rpiotrow96/LOTR-Lector/tree/master

#  Installation

* download and install tesseract https://github.com/UB-Mannheim/tesseract/wiki
* Configure path to tesseract.exe (in cnf.ini file)
* Configure language (supported languages: en, pl) in cnf.ini file. To use Polish (pl) language, you have to download pl.traineddata and copy this file to your tesseract path/tessdata. https://github.com/tesseractocr/tessdata/blob/master/pol.traineddata
* run cmd pip install  git+https://github.com/rpiotrow96/LOTR-Lector.git
* Play your game (1920x1080 reccomended - If you run on another resolution and have problems, let me know), then run this script  python main.py
It works!
