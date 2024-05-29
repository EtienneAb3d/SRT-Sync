import argparse
from pathlib import Path
import whisper
from whisper.utils import WriteSRT

modelSize = "large"

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Synchronize SRT timestamps over an existing accurate transcription.")
        parser.add_argument('pathMp3', type=str, help="Path to the SRT file with good timestamps")
        parser.add_argument('modelSize', type=str, help="Path to the TXT file with good text", nargs='?')
        args = parser.parse_args()
        
        if args.modelSize != None:
            modelSize = args.modelSize
            
        print("Loading Whisper model: "+modelSize+" ...")
        model = whisper.load_model(modelSize)
        
        print("Transcribing: "+args.pathMp3+" ...")
        result = model.transcribe(args.pathMp3)
        
        print(result["text"])
        
        print("Saving: "+args.pathMp3+".srt ...")
        p = Path(args.pathMp3)
        writer = WriteSRT(p.parent)
        writer(result, args.pathMp3)
    except BaseException:
        print("")
    
    

