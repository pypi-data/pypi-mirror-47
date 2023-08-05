from abc import ABC, abstractmethod

class IFileInfo(ABC):
    """
        Interface which must be implemented if you want to support your own filetype; Used by the Writer, Util and Merger
    """
    def __init__(self,file):
        self.file = file
        pass

    @abstractmethod
    def __enter__(self):
        pass
    @abstractmethod
    def __exit__(self,type,value,traceback):
        pass

    @abstractmethod
    def getFilepath(self):
        pass

    @abstractmethod
    def getNumberOfFrames(self):
        pass

    @abstractmethod
    def getSamplerate(self):
        pass

    @abstractmethod
    def getNumberOfChannels(self):
        pass    

    @abstractmethod        
    def getSamples(self):
        pass

    # writing methods
    @abstractmethod
    def setSamples(self, samples):
        pass
    
    @abstractmethod
    def truncate(self, num_frames):
        pass

    @abstractmethod
    def addSamples(self, samples):
        pass
    
    @abstractmethod
    def close(self):
        pass
    