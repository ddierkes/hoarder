"""The cleanup script is independent from the project and meant to be run as a cron.  It probably has deep flaws at scale"""


import glob, os, time
import sys
from operator import itemgetter

import config


def directory_cleanse(directory):
    """
    walks through the directories to remove those without contents.
    IIIF file paths are identifier/region/size/rotation/quality.informat
    so this has to loop three times to remove rotation, then size, then region.
    """
    print('\n\nEmpty Directories Removed:')
    for num in range(3):
        y = [x[0] for x in os.walk(directory)]
        for dir in y:
            if not os.listdir(dir):
                print(f"\t {dir}")
                os.rmdir(dir)


def chop_to_date(filelist, days):
    """
    Given a list of files with datestamps and a number of days, chop_to_date
    will return a new list with only those files younger than the number of days specified
    """
    diff = days * 86400
    timestamp = time.time()
    expiration = int(timestamp) - int(diff)
    print(expiration)
    new_filelist = []
    for file in filelist:
        if int(file["date"]) < expiration:
            print(f"{file['path']} is older than {days} days")
            os.remove(f["path"])
        else:
            new_filelist.append(file)
    return new_filelist


def chop_to_size(filelist, sizelimit, mode):
    """
    Given a size limit and a list of files with sizes and timestamps, chop_to_size
    sorts them by date and cuts off that part of the list that is oldest in order
    to fit within the size limit.  If the mode is equal to 'run', those files will
    be deleted.
    """
    sortedlist = sorted(filelist, key=itemgetter("date"))
    sortedlist = sortedlist[::-1]
    size = 0
    lastfileindex = -1
    print("\n\nKeep These:")
    for index, f in enumerate(sortedlist):
        size = size + f["size"]
        if size > int(sizelimit):
            lastfileindex = index
            size = size - f["size"]
            break
        else:
            print('\t' + str(f))
    print(f'\n\tTotal Storage is: {size}')

    bloat = 0
    if lastfileindex > -1:
        print("\n\nDiscard These:")
        for f in sortedlist[lastfileindex:]:
            print('\t'+str(f))
            bloat = bloat + f["size"]
            if mode == "run":
                os.remove(f["path"])
        print(f'\n\tTotal Weight Loss is: {bloat}')
    else:
        print("\n\nNothing to Discard.")
        return False
    return True


def main(mypath, sizelimit, mode="test", days=30):
    """
    To keep the hoarder system from overloading one's file system, this script
    is run to (1) remove anything older than a number of specified days, (2) remove
    the oldest files left until the cache is under a specified size limit, (3) remove
    empty directories to not waste inodes.
    """
    files = glob.glob(mypath + "/*/*/*/*/*")
    filelist = []
    for f in files:
        filedict = {}
        filedict["path"] = f
        filedict["size"] = os.stat(f).st_size
        filedict["date"] = os.stat(f).st_atime
        filelist.append(filedict)
    filelist = chop_to_date(filelist, days)
    deletion = chop_to_size(filelist, sizelimit, mode)

    if not deletion:
        print("\nWith nothing to delete, there are no directories to remove.")
    elif mode == "run":
        directory_cleanse(mypath)
    else:
        print("\nThis is only a test.  To remove files use the 'run' mode")


if __name__ == "__main__":
    # main("files", 2000000, "test", 1)
    if len(sys.argv) > 1:
        try:
            print(sys.argv)
            main(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
        except:
            print(
                "cleanup.py should be run with four arguments\n"
                "these being the file directory\n"
                "the size limit\n"
                "the 'test' or 'run'\n"
                "and how many days to purge\n"
                "an example command would be:\n"
                "\tpython3 cleanup.py 'files' 2000000 'test' 20"
            )
    else:
        try:
            print("running default cleanup parameters")
            main(config.file_directory, config.size_limit, config.mode, config.days)
        except:
            print("didn't work")
