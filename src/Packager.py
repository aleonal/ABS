#import virtualbox
import shutil
import os

class Packager:
    def __init__(self):
        print("packager")
        #self.vbox = virtualbox.VirtualBox()
        #self.vm_list = [m.name for m in self.vbox.machines]

        #for item in self.vm_list:
        #    print(item)

    #def get_vm_list(self):
        #return self.vm_list
    def export_to_zip(self, vm_list, file_list, output_directory):
        for vm in vm_list:
            print(vm)
            #Use Virtualbox export to ovf functions
        for file_path in file_list:
            file_name = os.path.basename(file_path)
            output_path = os.path.join(output_directory,file_name)
            shutil.copyfile(file_path,output_path)
        

        
        # src = r'C:\Users\Administrator.SHAREPOINTSKY\Desktop\Work\file2.txt'
        # dst = r'C:\Users\Administrator.SHAREPOINTSKY\Desktop\Newfolder\file2.txt'
        # shutil.copyfile(src, dst)

            

if __name__ == "__main__":

    Packager = Packager()
    vmlist = ["VM1","VM2"]
    filelist = []
    outputdirectory = []
    Packager.export_to_zip(vm_list=vmlist, file_list=filelist, output_directory=outputdirectory)