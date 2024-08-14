import glob
import shutil
import os
import os.path
import re
import sys
import getopt
import subprocess

scripts_path = os.path.dirname(os.path.realpath(__file__))
lib_path = scripts_path + '/../libs'
sys.path = sys.path + [lib_path]
import petalinuxcorelibs

def read_file(path):
  read_lines = []
  with open(path,'r') as fp:
    for line in fp:
      line = line.splitlines()
      read_lines += line
  fp.closed
  return read_lines

def get_image_appends(override_conf):
  image_append = []
  serch_str = re.escape("EXTRA_IMAGEDEPENDS_remove =")
  for e in override_conf:
    e_str = str(e)
    if re.search(serch_str,e_str):
      packg = e_str.split('=')[1]
      packg = str(packg)
      packg = re.sub("\"",'',packg)
      image_append += [str(x) for x in packg.split(' ')]
  return image_append

def read_plnx_hwdata(proot,string):
  data_file=proot + "/build/misc/config/plnx_syshw_data"
  with open(data_file, 'r') as file:
    for line in file:
      if string in line:
        data = line.split(' ')
        return data[1].strip()

def copy_file_path(proot,machine_name,src_dir,dest_dir):
  src_file = ''
  for f in os.listdir(src_dir):
    if re.search('.bit', f):
      src_file = f
  if src_file and not src_file.isspace():
    orig_src_file = os.path.join(src_dir,src_file)
    dt_overlay_enabled=petalinuxcorelibs.get_value_from_key(sysconf, "CONFIG_SUBSYSTEM_DTB_OVERLAY")
    bitfile_name=read_plnx_hwdata(proot,"hw_design_name: ") + ".bit"
    # Removing previously existing bit file in images folder
    if os.path.exists(os.path.join(dest_dir,"system.bit")): os.remove(os.path.join(dest_dir,"system.bit"))
    if os.path.exists(os.path.join(dest_dir,bitfile_name)): os.remove(os.path.join(dest_dir,bitfile_name))

    if dt_overlay_enabled == "y":
      dest_dir = dest_dir + bitfile_name
    else:
      dest_dir = dest_dir + "system.bit"
    shutil.copy2(orig_src_file, dest_dir)
    os.chmod(dest_dir, 0o644)
  return

def copy_file(proot,machine_name,file_name,dest_name):
  images_dir = proot + "/images/linux"
  deploy_dir = tmp_dir + "/deploy/images/" + machine_name
  file_name = deploy_dir + "/" + file_name
  dest_name = images_dir + "/" + dest_name
  petalinuxcorelibs.mkdir(images_dir,silent_discard = False)
  isfile = os.path.isfile(file_name)
  if isfile==False:
   # print "WARNINIG: File:" + file_name + " doesn't exit, Skipping .."
    return
  islink = os.path.islink(file_name)
  if islink==True:
    orig_file = os.readlink(file_name)
    orig_full_file = os.path.join(deploy_dir,orig_file)
  else:
    orig_full_file = file_name
  if os.path.exists(dest_name):
    os.remove(dest_name)
  shutil.copy2(orig_full_file, dest_name)

def copy_dir(proot,machine_name,dir_name,dest_name):
  images_dir = proot + "/images/linux"
  deploy_dir = tmp_dir + "/deploy/images/" + machine_name
  src_dir = deploy_dir + "/" + dir_name
  petalinuxcorelibs.mkdir(images_dir,silent_discard = False)
  if dest_name:
    petalinuxcorelibs.mkdir(images_dir + "/" + dest_name)
  if os.path.exists(src_dir):
    dirlist = os.listdir(src_dir)
    for name in dirlist:
      src_name = src_dir + '/' + name
      dst_name = images_dir + "/" + dest_name + "/" + name
      if os.path.isdir(src_name):
        if os.path.exists(dst_name):
          shutil.rmtree(dst_name)
        shutil.copytree(src_name, dst_name)
      else:
        copy_file(proot,machine_name,dir_name + '/' + name,dest_name + '/' + name)

def copy_embedded_sw_apps(proot,machine_name,override_conf):
  image_append=get_image_appends(override_conf)

#Copy device tree
  file_name = machine_name + "-system.dtb"
  dest_name = petalinuxcorelibs.get_value_from_key(sysconf, "CONFIG_SUBSYSTEM_IMAGES_ADVANCED_AUTOCONFIG_DTB_IMAGE_NAME")
  if not dest_name:
    dest_name = "system.dtb"
  copy_file(proot,machine_name,file_name,dest_name)

#Copy ATF
  file_name = "arm-trusted-firmware.elf"
  dest_name = "bl31.elf"
  copy_file(proot,machine_name,file_name,dest_name)
  file_name = "arm-trusted-firmware.bin"
  dest_name = "bl31.bin"
  copy_file(proot,machine_name,file_name,dest_name)

  if "virtual/fsbl" not in image_append :
    file_name = "fsbl-" + machine_name + ".elf"
    dest_name = xilinx_arch + "_fsbl.elf"
    copy_file(proot,machine_name,file_name,dest_name)

  if "virtual/pmu-firmware" not in image_append :
    file_name = "pmu-firmware-" + machine_name + ".elf"
    dest_name = "pmufw.elf"
    copy_file(proot,machine_name,file_name,dest_name)

  if "virtual/plm" not in image_append :
    file_name = "plm-" + machine_name + ".elf"
    dest_name = "plm.elf"
    copy_file(proot,machine_name,file_name,dest_name)

  if "virtual/psm-firmware" not in image_append :
    file_name = "psm-firmware-" + machine_name + ".elf"
    dest_name = "psmfw.elf"
    copy_file(proot,machine_name,file_name,dest_name)

  if "virtual/fsboot" not in image_append  :
    file_name = "fsboot-" + machine_name + ".elf"
    dest_name = "fs-boot.elf"
    copy_file(proot,machine_name,file_name,dest_name)
    copy_file(proot,machine_name,"u-boot-s.bin","u-boot-s.bin")

  if "u-boot-zynq-scr" not in image_append :
    copy_file(proot,machine_name,"boot.scr","boot.scr")
    copy_dir(proot,machine_name,"pxelinux.cfg","pxelinux.cfg")

def copy_cdo(proot,machine_name):
  copy_file(proot,machine_name,"CDO/pmc_cdo.bin","pmc_cdo.bin")

def copy_uboot(proot,machine_name):
  #FIXME: For MB there is one more file
  copy_file(proot,machine_name,"u-boot.elf","u-boot.elf")
  copy_file(proot,machine_name,"u-boot.bin","u-boot.bin")

def copy_kernel(proot,machine_name,override_conf):
  b = r'(\s|^|$)'
  vmlinux_image="vmlinux"
  if re.search("arm",machine_arch):
    kernel_image="zImage"
    dest_name = kernel_image
    kernel_uimage="uImage"
    dest_uimage= kernel_uimage
  elif re.search("aarch64",machine_arch):
    kernel_image="Image"
    dest_name = kernel_image
  elif re.search("microblaze",machine_arch):
    kernel_image="simpleImage.mb" + '-' + machine_name + ".strip"
    dest_name = "image.elf"
    kernel_uimage = "linux.bin.ub"
    dest_uimage= kernel_uimage
  for e in override_conf:
    e_str=str(e)
    if re.search('INITRAMFS_IMAGE_BUNDLE = "1"',e_str ):
      if not re.search("microblaze",machine_arch):
        kernel_image = kernel_image + "-initramfs-" + machine_name + ".bin"
      vmlinux_image = vmlinux_image + "-initramfs-" + machine_name + ".bin"
      if not re.search("aarch64",machine_arch):
        kernel_uimage = kernel_uimage + "-initramfs-" + machine_name + ".bin"
  if not re.search("aarch64",machine_arch):
    copy_file(proot,machine_name,kernel_uimage,dest_uimage)
  copy_file(proot,machine_name,kernel_image,dest_name)
  copy_file(proot,machine_name,"System.map.linux","System.map.linux")  
  copy_file(proot,machine_name,vmlinux_image,"vmlinux")
  copy_file(proot,machine_name,"xen.ub","xen.ub")
  
def copy_rootfs(proot,machine_name,override_conf):
  source_folder = tmp_dir + "/deploy/images/" + machine_name
  search_str="petalinux-user-image-" + machine_name + '.'
  search_str=re.escape(search_str)
  dest_name=''
  if os.path.exists(source_folder):
    for _file in os.listdir(source_folder):
      if re.search(search_str, _file):
        source_name=str(_file)
        dest_name=source_name.split(machine_name)[1]
        dest_name= 'rootfs' + dest_name
        copy_file(proot,machine_name,source_name,dest_name)

def copy_fit_image(proot,machine_name,override_conf):
  fit_image=petalinuxcorelibs.get_value_from_key(sysconf, "CONFIG_SUBSYSTEM_UIMAGE_NAME")
  for e in override_conf:
    e_str=str(e)
    if re.search('INITRAMFS_IMAGE = "petalinux-user-image"',e_str ):
        fit_src= 'fitImage-petalinux-user-image-' + machine_name + '-' + machine_name
        break
    else:
        fit_src= 'fitImage-' + machine_name + '.bin'

  copy_file(proot,machine_name,fit_src,fit_image)

def copy_bit_stream(proot,machine_name):
  dest_dir = proot +"/images/linux/"
  src_dir = proot + "/project-spec/hw-description"
  copy_file_path(proot,machine_name,src_dir,dest_dir)
  dt_overlay_enabled=petalinuxcorelibs.get_value_from_key(sysconf, "CONFIG_SUBSYSTEM_DTB_OVERLAY")
  dest_name = "pl.dtbo"
  source_name = machine_name + "-system.dtbo"
  if os.path.exists(os.path.join(dest_dir, dest_name)):
    os.remove(os.path.join(dest_dir, dest_name))
  if dt_overlay_enabled == "y":
    copy_file(proot,machine_name,source_name,dest_name)

def copy_qemu_hwdtb(proot,machine_name):
  qemuhw_dir = "qemu-hw-devicetrees/"
  multi_qemuhw_dir = qemuhw_dir + "multiarch/"
  dtbfiles = {
    'zynqmp':{'zc1751':'zc1751-dc2-arm.dtb','ultra96':'zcu100-arm.dtb'},
    'versal':{'vc-p-a2197-00':['board-versal-ps-vc-p-a2197-00.dtb',
                               'board-versal-pmc-vc-p-a2197-00.dtb']
             }
  }
  default_dtbs = {
    'zynqmp':{'src':['zcu102-arm.dtb','zynqmp-pmu.dtb'],
              'dst':['zynqmp-qemu-arm.dtb','zynqmp-qemu-multiarch-arm.dtb',
                                           'zynqmp-qemu-multiarch-pmu.dtb']
             },
    'versal':{'src':['board-versal-ps-virt.dtb','board-versal-pmc-virt.dtb'],
              'dst':['versal-qemu-ps.dtb','versal-qemu-multiarch-ps.dtb',
                                            'versal-qemu-multiarch-pmc.dtb']
             }
  }

  if xilinx_arch in list(dtbfiles.keys()):
    for key in list(dtbfiles[xilinx_arch].keys()):
      if re.search(key,machine_name):
        if xilinx_arch == "zynqmp":
          default_dtbs[xilinx_arch]['src'][0]=dtbfiles[xilinx_arch][key]
      if xilinx_arch == "versal":
        default_dtbs[xilinx_arch]['src'][0]=dtbfiles[xilinx_arch][key][0]
        default_dtbs[xilinx_arch]['src'][1]=dtbfiles[xilinx_arch][key][1]

  if xilinx_arch in list(dtbfiles.keys()):
    copy_file(proot,machine_name,qemuhw_dir + default_dtbs[xilinx_arch]['src'][0],\
                        default_dtbs[xilinx_arch]['dst'][0])
    copy_file(proot,machine_name,multi_qemuhw_dir + default_dtbs[xilinx_arch]['src'][0],\
                        default_dtbs[xilinx_arch]['dst'][1])
    copy_file(proot,machine_name,multi_qemuhw_dir + default_dtbs[xilinx_arch]['src'][1],\
                        default_dtbs[xilinx_arch]['dst'][2])

def copy_to_tftpfolder(proot):
   tftp_boot_enabled=petalinuxcorelibs.get_value_from_key(sysconf, "CONFIG_SUBSYSTEM_COPY_TO_TFTPBOOT")
   if tftp_boot_enabled == "y":
     tftpboot_dir = petalinuxcorelibs.get_value_from_key(sysconf, "CONFIG_SUBSYSTEM_TFTPBOOT_DIR")
     src_dir = proot + "/images/linux"
     if not os.path.exists(tftpboot_dir):
         sys.stdout = open(os.devnull, 'w')
         try:
             os.makedirs(tftpboot_dir)
         except Exception as e:
             print(e)
         sys.stdout = sys.__stdout__
     if not os.path.isdir(tftpboot_dir):
         print('NOTE: Failed to copy built images to tftp dir: %s ' % str(tftpboot_dir))
         sys.exit()
     if os.access(tftpboot_dir, os.W_OK):
       files = os.listdir(src_dir)
       try:
         for l in files:
             source = os.path.join(src_dir, l)
             if os.path.isdir(source):
               dstdir=os.path.join(tftpboot_dir,l)
               if os.path.exists(dstdir): shutil.rmtree(dstdir)
               shutil.copytree(source,dstdir)
             else:
              shutil.copy2(source,tftpboot_dir)
       except Exception as e:
         print(e)
       print('NOTE: Successfully copied built images to tftp dir: %s' % str(tftpboot_dir))
     else:
         print('NOTE: Failed to copy built images to tftp dir: %s' % str(tftpboot_dir))
         sys.exit()
   else:
     print('NOTE: copy to TFTP-boot directory is not enabled !!')
     sys.exit()

def main_func(proot,machine_name):
  override_conf_path=proot + "/build/conf/plnxtool.conf"
  override_conf=read_file(override_conf_path)
  copy_embedded_sw_apps(proot,machine_name,override_conf)
  copy_cdo(proot,machine_name)
  copy_uboot(proot,machine_name)
  copy_kernel(proot,machine_name,override_conf)
  copy_rootfs(proot,machine_name,override_conf)
  copy_fit_image(proot,machine_name,override_conf)
  copy_bit_stream(proot,machine_name)
  copy_qemu_hwdtb(proot,machine_name)
  copy_to_tftpfolder(proot)

def parse_args(argv):
  global tmp_dir
  global sysconf
  global machine_arch
  global xilinx_arch
  try:
    opts, args = getopt.getopt(argv,"hd:",["deploy="])
  except getopt.GetoptError:
    print('ERROR: valid options --deploy')
    print('run code with: python3 deploy.py -h  for help')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('HELP: ')
      print("Usage: python3 rootfs_config.py --deploy <proot> <machine name>")
      sys.exit()
    elif opt in ("-d","--deploy"):
      print('INFO: Copying Images from deploy to images')
      proot = argv[1]
      machine_name = argv[2]
      tmp_dir = argv[3]
      sysconf = argv[4]
      machine_arch = argv[5]
      xilinx_arch = argv[6]
      main_func(proot,machine_name)
    else:
      print("Error:")
      print("Usage: python3 rootfs_config.py --deploy <proot> <machine name>")

parse_args(sys.argv[1:])

