import subprocess
import shutil
import os
import re
from zipfile import ZipFile

class Packager:
    def __init__(self):
        
        self.vm_list = ''

    def get_vm_list(self):
        vms_string = subprocess.check_output(["C:\Program Files\Oracle\VirtualBox\VBoxManage.exe","list","vms"], stderr=subprocess.PIPE, stdin=subprocess.PIPE).decode()

        self.vm_list = re.findall(r'"(.*?)"', vms_string)
        return self.vm_list

    def export_to_zip(self, vm_list, file_list, output_file):
        parent_directory = os.path.dirname(output_file)
        base_name = os.path.basename(output_file)
        f_name,f_ext = os.path.splitext(base_name)
        temp_directory = os.path.join(parent_directory,f_name)
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
        final_zip = os.path.join(parent_directory,f_name)
        shutil.make_archive(final_zip, 'zip', temp_directory)

        #Delete temp directory
        try:
            shutil.rmtree(temp_directory)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))


    def import_from_zip(self, zip_file):
        parent_directory = os.path.dirname(zip_file)
        temp_dir = os.path.join(parent_directory,'zip_temp')
        base=os.path.basename(zip_file)
        print(base)
        f_name,f_ext = os.path.splitext(base)
        file_dir = f_name+"_files"
        file_output_dir = os.path.join(parent_directory,file_dir)

        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(file_output_dir, exist_ok=True)

        with ZipFile(zip_file, 'r') as zipObj:
            zipObj.extractall(temp_dir)

        filelist = []

        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                filelist.append(os.path.join(root,file))
                print(file)

        for file in filelist:
            #If OVA, import to VirtualBox
            if(file.endswith(".ova")):
                subprocess.run(["C:\Program Files\Oracle\VirtualBox\VBoxManage.exe","import", file])
            #Any other file, copy to temp directory
            else:
                file_name = os.path.basename(file)
                output_path = os.path.join(file_output_dir,file_name)
                shutil.copyfile(file,output_path)

         #Delete temp directory
        try:
            shutil.rmtree(temp_dir)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == "__main__":

    Packager = Packager()
    vmlist = ["VM1","VM2"]
    filelist = []
    outputdirectory = []
    Packager.export_to_zip(vm_list=vmlist, file_list=filelist, output_directory=outputdirectory)