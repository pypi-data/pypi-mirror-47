
import os
import shutil
import collections
import subprocess
import distutils.dir_util

from osnap import dist_dir, windows_app_dir, python_folder, main_program_py, get_logger, __application_name__
import osnap.util
import osnap.make_nsis
import osnap.installer_base


LOGGER = get_logger(__application_name__)


class OsnapInstallerWin(osnap.installer_base.OsnapInstaller):

    def make_installer(self):

        osnap.util.rm_mk_tree(dist_dir)
        osnap.util.rm_mk_tree('installers')
        self.unzip_launcher(dist_dir)

        distutils.dir_util.copy_tree(self.application_name, os.path.join(dist_dir,
                                                                         windows_app_dir,
                                                                         self.application_name))
        distutils.dir_util.copy_tree(python_folder,
                                     os.path.join(dist_dir, windows_app_dir,
                                                  python_folder))
        win_app_dir_path = os.path.join(dist_dir, windows_app_dir)
        for f in [main_program_py]:
            LOGGER.debug('copying %s to %s', f, win_app_dir_path)
            if os.path.exists(f):
                shutil.copy2(f, win_app_dir_path)
            else:
                raise Exception('expected {} ({}) to exist but it does not'.format(f, os.path.abspath(f)))

        # copy over any MSVC files (e.g. .dlls) needed
        msvc_dir = 'msvc'
        if os.path.exists(msvc_dir):
            for file_name in os.listdir(msvc_dir):
                src = os.path.join(msvc_dir, file_name)
                for dest_folder in [dist_dir, os.path.join(dist_dir, windows_app_dir)]:
                    dest = os.path.join(dest_folder, file_name)
                    LOGGER.info('copying %s to %s' % (src, dest))
                    shutil.copy2(src, dest)
        else:
            LOGGER.warning(
                'nothing in folder %s (%s) to copy over (no DLLs needed?)' % (msvc_dir, os.path.abspath(msvc_dir)))

        # application .exe
        exe_name = self.application_name + '.exe'
        orig_launch_exe_path = os.path.join(dist_dir, 'launch.exe')
        dist_exe_path = os.path.join(dist_dir, exe_name)
        LOGGER.debug('moving %s to %s', orig_launch_exe_path, dist_exe_path)
        os.rename(orig_launch_exe_path, dist_exe_path)

        # support files
        for f in [self.application_name + '.ico', 'LICENSE']:
            shutil.copy2(f, dist_dir)

        # write NSIS script
        if not self.create_installer:
            LOGGER.debug("Not creating NSIS installer - it was not requested")
            return

        nsis_file_name = self.application_name + '.nsis'

        nsis_defines = collections.OrderedDict()
        nsis_defines['COMPANYNAME'] = self.author
        nsis_defines['APPNAME'] = self.application_name
        nsis_defines['EXENAME'] = exe_name
        nsis_defines['DESCRIPTION'] = '"' + self.description + '"'  # the description must be in quotes

        v = self.application_version.split('.')
        if len(v) != 3:
            LOGGER.error('version string "%s" does not adhere to the x.y.z format' % self.application_version)
            nsis_defines['VERSIONMAJOR'] = '0'
            nsis_defines['VERSIONMINOR'] = '0'
            nsis_defines['VERSIONBUILD'] = '0'
        else:
            nsis_defines['VERSIONMAJOR'] = v[0]
            nsis_defines['VERSIONMINOR'] = v[1]
            nsis_defines['VERSIONBUILD'] = v[2]

        # These will be displayed by the "Click here for support information" link in "Add/Remove Programs"
        # It is possible to use "mailto:" links in here to open the email client
        nsis_defines['HELPURL'] = self.url  # "Support Information" link
        nsis_defines['UPDATEURL'] = self.url  # "Product Updates" link
        nsis_defines['ABOUTURL'] = self.url  # "Publisher" link

        LOGGER.debug('writing %s', nsis_file_name)
        nsis = osnap.make_nsis.MakeNSIS(nsis_defines, nsis_file_name)
        nsis.write_all()

        shutil.copy(nsis_file_name, dist_dir)

        os.chdir(dist_dir)

        nsis_path = os.path.join('c:', os.sep, 'Program Files (x86)', 'NSIS', 'makensis.exe')
        if os.path.exists(nsis_path):
            pkgproj_command = [nsis_path, nsis_file_name]
            LOGGER.debug('Executing %s', pkgproj_command)
            subprocess.check_call(pkgproj_command)
        else:
            raise Exception(('NSIS tool could not be found (expected at {})'
                'See http://nsis.sourceforge.net for information on how to obtain the NSIS '
                '(Nullsoft Scriptable Install System) tool.').format(nsis_path))
