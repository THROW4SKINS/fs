#here is the bianry fs object
import os,pickle
class Fsfile:
    def __init__(self,filename,numberbyte):
        self.filename = filename
        self.numberbytes = numberbyte
        self.value = []
        self.position = 0
        self.w_or_r = ' '
        self.isOpen = 0
class Dir:
     def __init__(self,dirname):
         self.dirnames = dirname
         self.dirlist = []
         self.filelist = []


class Fs:

    def __init__(self):
        self.totalbyte = 0
        self.root = Dir('')
        self.position = self.root
        self.lastposition = Dir('')
    def init(self,fsname):
        self.name = fsname
        self.nativefilesize = os.path.getsize(fsname)
        self.content = open(fsname, 'w')

    def mkdir(self,dirname):
        targe = dirname.split('/')
        if len(targe) >= 3:
            print('typo '+dirname+' is not supported')
            return
        #print (str(targe[1]))
        dirob = Dir(str(targe[1]))
        for i in range(len(self.position.dirlist)):
            if targe[1] in self.position.dirlist[i].dirnames:
                fname=self.position.dirlist[i].dirnames
                print('/'+fname+" already exist")
                return
        if self.position.dirlist == None:
            self.position.dirlist[0] = dirob
        else:
            self.position.dirlist.append(dirob)
            print("the dir you create is:",self.position.dirlist)


    def deldir(self,dirname):
        for i in range(len(self.position.dirlist)):
            if dirname in self.position.dirlist[i].dirnames:
                self.position.dirlist.remove( self.position.dirlist[i])
            else:
                print("no such directory")
        print("after del dir the dirlist is:",self.position.dirlist)

    def isdir(self,dirname):
        for i in range(len(self.position.dirlist)):
            if dirname in self.position.dirlist[i].dirnames:
                print("yes")
            else:
                print("no")


    def chdir(self,dirname):
        targe = dirname.split('/')
        for i in range(len(targe)):
            if targe[i] == '.':
                continue
            elif targe[i] == '..':
                self.position = self.lastposition
            else:
                for j in range(len(self.position.dirlist)):
                    if(self.position.dirlist[j].dirnames == targe[i]):
                        self.lastposition = self.position
                        self.position = self.position.dirlist[j]
                        break
                    if j == len(self.position.dirlist):
                        print ('/'+dirname+" is not found")
                        self.position = self.lastposition
        if self.position.dirnames == '':
            print('current location is:', '/root'+self.position.dirnames)
        else:
            print('current location is:', '/' + self.position.dirnames)

    def listdir(self,dirname):
        self.chdir(dirname)
        for i in range(len(self.position.dirlist)):
            print (' /'+self.position.dirlist[i])


    def create(self,filename,nbytes):
        self.fsFile = Fsfile(filename,nbytes)
        try:
            self.position.filelist.append(self.fsFile)
            h = len(self.position.filelist)
            self.totalbyte += nbytes
        except nbytes + self.totalbyte >= self.nativefilesize:
            print('oversize input')
        else:
            print("the file you create name is:",self.position.filelist[h - 1].filename)
            print("the filelist is:",self.position.filelist)

    def open(self,filename,mode):
         self.w_or_r = mode
         for i in range(len(self.position.filelist)):
             if filename == str(self.position.filelist[i].filename):
                 self.position.filelist[i].isOpen = 1
                 return self.position.filelist[i]
         print("error")

#after close need to seperate the different space for different files, also write and read at the fixed location
    def close(self,fd):
        for i in range(len(fd.value)):
            st = fd.value[i]
            self.content.write(st)
        fd.isOpen = 0
        print("closed")

    def length(self,fd):
        ssize = 0
        for i in range(len(fd.value)):
            ssize = ssize + len(fd.value[i])
        return ssize

    def pos(self,fd):
        return fd.position

    def seek(self,fd,pos):
            str = ' '
            for i in range(len(fd.value)):
                str += (fd.value[i])
                try:
                    fd.position = pos-1
                except(pos < 0 or pos > len(str)):
                    print("error inpout")

#the question here is if i need to take care of the position to read method so ,read2 is don't care it
    def read(self,fd,nbytes):
        if self.w_or_r == 'r':
             str = ' '
             a = self.pos(fd)
             for i in range(len(fd.value)):
                 str += (fd.value[i])
                 try:
                     result = str[(a + nbytes)]
                     return result
                 except:
                     print("your input number of bytes is too big")
        else:
            print("mode error")
    def read2(self,fd,nbytes):
        if self.w_or_r == 'r':
             str = ' '
             for i in range(len(fd.value)):
                 str += (fd.value[i])
                 if nbytes <= len(str):
                     result = str[nbytes]
                     fd.position = nbytes-1
                     return result
             else:
                 print("your input number of bytes is too big")
        else:
            print("mode error")

    def write(self,fd,writebuf):
        bfsize= len(writebuf)
        if self.w_or_r == 'w':
            if fd.value == []:
                fd.value.append(writebuf)
                fd.position = len(writebuf) - 1
            else:
                fd.value.append(writebuf)
                fd.position = self.length(fd)-1
            print("the value now in the file is:",fd.value)
        else:
            print("mode error")
        for i in range(len(self.position.filelist)):
            if fd.filename == str(self.position.filelist[i].filename):
                if self.position.filelist[i].numberbytes - bfsize >= 0:
                    self.totalbyte += self.position.filelist[i].numberbytes - bfsize



    def readlines(self,fd):
        result = []
        for i in range(len(fd.value)):
            result.append(fd.value[i])
        return result

    def delfile(self,filename):
        for i in range(len(self.position.filelist)):
            if filename == str(self.position.filelist[i].filename):
                self.position.filelist.pop(i)
        print("the file is delete")
        print("after delete, the filelist is :",self.position.filelist)

    def suspend(self,fd):
        print(fd.isOpen)
        if fd.isOpen == 1:
            print ('file is not closed')
        else:
            pickle.dump(self, open('f.fssave', 'wb'))
            print ('suspension is complete')

    def resume(self):
        self = pickle.load(open('f.fssave', 'rb'))



fs = Fs()
fs.mkdir('/x')
fs.mkdir('/x')
fs.mkdir('/x/y')








# length = tr.length(fi)
# print("the length of this file is",length)
# fi = tr.open('ab','r')
# strs = tr.read2(fi,9)
# print("the bytes you read is",strs)
# x = tr.pos(fi)
# print("after read the position is:",x)
# tr.seek(fi,5)
# z = tr.pos(fi)
# print("after seek the position:",z)
# lines = tr.readlines(fi)
# print("the lines information is:",lines)
# print()
# tr.create('test',20)
# tr.delfile('test')
# tr.close(fi)