import argparse
import platform

from osnap import default_python_version, get_logger, init_logger_from_args, __application_name__
import osnap.util
import osnap.installer_mac
import osnap.installer_win

LOGGER = get_logger(__application_name__)


def make_installer(
        python_version,
        application_name,
        application_version,
        author              = '',
        description         = '',
        url                 = '',
        compile_code        = True,
        use_pyrun           = False,
        create_installer    = True,
        architecture        = '64bit',
        variant             = 'window',
        ):

    if osnap.util.is_mac():
        class_ = osnap.installer_mac.OsnapInstallerMac
    elif osnap.util.is_windows():
        class_ = osnap.installer_win.OsnapInstallerWin
    else:
        raise NotImplementedError("Your platform - {} - is not supported".format(platform.system()))

    installer = class_(
        python_version,
        application_name,
        application_version,
        author,
        description,
        url,
        compile_code,
        use_pyrun,
        create_installer,
        architecture,
        variant,
    )

    installer.make_installer()


def main():

    parser = argparse.ArgumentParser(description='create the osnap installer',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--application', default=None, help='application name (required for OSX/MacOS)')
    parser.add_argument('-A', '--architecture', default='64bit', choices=['64bit', '32bit'], help="The architecture to use for the launcher")
    parser.add_argument('-b', '--binary-only', action='store_true', default=False, help=(
        "Only produce the binary of the script as an executable without creating an installer. This avoids the NSIS requirement on windows"
    ))
    parser.add_argument('-c', '--console', action='store_true', default=False, help="Use a console for the application")
    parser.add_argument('-p', '--python_version', default=default_python_version, help='python version')
    parser.add_argument('-e', '--egenix_pyrun', action='store_true', default=False, help='use eGenix™ PyRun™')
    parser.add_argument('-n', '--name_of_author', default='', help='author name')
    parser.add_argument('-d', '--description', default='', help='application description')
    parser.add_argument('-u', '--url', default='', help='application URL')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print more verbose messages')
    args = parser.parse_args()

    init_logger_from_args(args)

    try:
        make_installer(
            args.python_version,
            args.application,
            args.name_of_author,
            args.description,
            args.url,
            True,
            args.egenix_pyrun,
            create_installer    = not args.binary_only,
            architecture        = args.architecture,
            variant             = 'console' if args.console else 'window',
        )
    except Exception as e:
        LOGGER.exception("Fatal error: %s", e)


if __name__ == '__main__':
    main()
