import glob, os, time
import sys
from operator import itemgetter


def directory_cleanse(directory):
    """
    walks through the directories to remove those without contents.
    IIIF file paths are identifier/region/size/rotation/quality.informat
    so this has to loop three times to remove rotation, then size, then region.
    """
    for num in range(3):
        y = [x[0] for x in os.walk(directory)]
        for dir in y:
            if not os.listdir(dir):
                print(f"removing {dir}")
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
    lastfileindex = 0
    print("\nKeep These:")
    for index, f in enumerate(sortedlist):
        print(f)
        size = size + f["size"]
        if size > sizelimit:
            lastfileindex = index
            break
    if lastfileindex > 0:
        print("\nDiscard These:")
        for f in sortedlist[lastfileindex:]:
            print(f)
            if mode == "run":
                os.remove(f["path"])
    else:
        print("\nNothing to Discard.")
    print("Total Memory Used Equals " + str(size))


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
    chop_to_size(filelist, sizelimit, mode)

    directory_cleanse(mypath)


if __name__ == "__main__":
    # main("files", 2000000, "test", 1)
    try:
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
