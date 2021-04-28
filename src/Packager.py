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
    def export_to_zip(self, vm_list, file_list, output_file):
        parent_directory = os.path.dirname(output_file)
        temp_directory = output_file
        os.mkdir(temp_directory)

        for vm in vm_list:
            print(vm)
            #Use Virtualbox export to ovf functions to the output folder

        #Copy files to temp directory
        for file_path in file_list:
            file_name = os.path.basename(file_path)
            output_path = os.path.join(temp_directory,file_name)
            shutil.copyfile(file_path,output_path)
        #Create a zip from temp directory
        final_directory = os.path.join(parent_directory,output_file)
        shutil.make_archive(final_directory, 'zip', temp_directory)

        #Delete temp directory
        try:
            shutil.rmtree(temp_directory)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
            

if __name__ == "__main__":

    Packager = Packager()
    vmlist = ["VM1","VM2"]
    filelist = []
    outputdirectory = []
    Packager.export_to_zip(vm_list=vmlist, file_list=filelist, output_directory=outputdirectory)