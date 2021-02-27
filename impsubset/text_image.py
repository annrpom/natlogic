
# Represents a block of text that can be treated like an "Image"
# i.e., you can then combine two text images to get another (possibly bigger)
# TextImage (like 2htdp's images)
# (U String [String]) -> TextImage 
class TextImage:
    def __init__(self, text):
        self.strs   = text.split("\n") if isinstance(text,str) else text.copy()  # TextImage basically is a wrapper around lines of text
        self.height = len(self.strs)                                    # height is number of lines
        self.width  = len(max(self.strs,key=len)) if self.height else 0 # width is the longest line 
        self.strs = [s + (" " * (self.width - len(s))) for s in self.strs]

    # TextImage (Int) -> TextImage
    # creates a TextImage where `self`s text is on the left,
    # and `image`s on the right. Texts in both objects keep
    # their indentation as it was before
    # By default, TextImages are aligned at the bottom since that's
    # useful in this project's case
    def beside(self,image,gapBw=0):
        userGap = gapBw * " "
        leftGap  = (" " * self.width) + userGap
        rightGap  = userGap + (" " * image.width)
        if(len(self.strs) == 0):
            return TextImage(image.strs)
        if(len(image.strs) == 0):
            return TextImage(self.strs)
        newArr  = [""] * max(self.height, image.height)
        smaller,bigger,fix = None,None,None
        if self.height < image.height: 
            fix     = lambda x: leftGap + x
            bigger  = image.strs
            smaller = self.strs
        else:
            fix     = lambda x: x + rightGap
            bigger  = self.strs
            smaller = image.strs
        i  = len(newArr)  - 1
        lx = self.height  - 1
        rx = image.height - 1
        for _ in range(len(smaller)):
            leftStr   = self.strs[lx] 
            rightStr  = image.strs[rx] 
            newArr[i] = leftStr + userGap + rightStr
            i-=1
            lx-=1
            rx-=1
        for j in range(len(bigger) - len(smaller)-1,-1,-1):
            newArr[i] = fix(bigger[j])
            i-=1
        return TextImage(newArr)
    
    # TextImage -> TextImage
    # similar to beside but places the text on top
    # By default, the smaller TextImage is mid-aligned with the larger
    # image
    def above(self,image):
        ab = TextImage(self.strs)
        be = TextImage(image.strs)
        if(ab.height == 0):
            return be
        if(be.height == 0):
            return ab
        w,smaller,bigger = None,None,None
        if ab.width > be.width:
            w       = ab.width
            bigger  = ab.strs
            smaller = be.strs
        else:
            w       = be.width
            bigger  = be.strs
            smaller = ab.strs
        for i in range(len(smaller)):
            strW = w - len(smaller[i])
            smaller[i] = (" " * (strW//2)) + smaller[i] + (" " * (strW - strW//2))
        return TextImage(ab.strs + be.strs)


    # String -> TextImage
    # Like `above` but for strings
    def aboveStr(self,text):
        return self.above(TextImage(text))
    
    def __str__(self):
        return "\n".join(self.strs)

    def __add__(self,image):
        return self.beside(image)