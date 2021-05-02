import subprocess
import shutil
import os
import re

class Packager:
    def __init__(self):
        
        vms_string = subprocess.check_output(["C:\Program Files\Oracle\VirtualBox\VBoxManage.exe","list","vms"], stderr=subprocess.PIPE, stdin=subprocess.PIPE).decode()

        self.vm_list = re.findall(r'"(.*?)"', vms_string)

    def get_vm_list(self):
        return self.vm_list

    def export_to_zip(self, vm_list, file_list, output_file):
        parent_directory = os.path.dirname(output_file)
        temp_directory = output_file
        os.mkdir(temp_directory)

        for vm in vm_list:
            vm_filename = vm+".ova"
            export_vm_path = os.path.join(temp_directory,vm_filename)
            subprocess.run(["C:\Program Files\Oracle\VirtualBox\VBoxManage.exe","export", vm, "-o", export_vm_path])

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