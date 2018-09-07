import os, sys, shutil, re

mal_codes = ['UPS', 'UPG']

ad_groups_to_add_dict = { 
   'UPS': ['aaa-cloud-ops', 'aaa-eng-cloud-servicedelivery-s3', 'aaa-eito-mw-support', 'ABC_PRODUCTION_SUPPORT' ],
   'UPG': ['aaa-cloud-ops', 'aaa-eng-cloud-servicedelivery-s3', 'aaa-eito-mw-support' ]
}

ad_groups_to_remove = ['aaa-cloud-prod', 'aaa-support-grp']

access_file = 'access.conf'

# replace this line with the exact change order number
rollback_dir='/var/tmp/CO123456'

def backup_access_file(access_file, rollback_dir):
    # make a copy of access_file to the rollback directory for rolling back the change
    if (not os.path.exists(rollback_dir)): 
        os.mkdir(rollback_dir)
    shutil.copy2(access_file, rollback_dir)

def restore_access_file(access_file, rollback_dir):
    if (os.path.exists(rollback_dir)): 
        shutil.copy2(access_file, rollback_dir+os.path.basename(access_file)+'.orig')
        if (os.ppth.isfile()):
            shutil.copy2(rollback_dir + os.path.basename(access_file), access_file)
        else:
            print("roll back file %s doesn't exist" % rollback_dir + os.path.basename(access_file))
    else:
        print("roll back directory %s doesn't exist" % rollback_dir )

def update_access_file(access_file, ad_groups_to_add, ad_groups_to_remove):
    # open access_file 
    try:
        fd = open(access_file, "r+")
        file_content = fd.read()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    # construct lines for ad groups to be added to access.conf file
    lines_to_add = "# BEGIN of ITS and TS support groups BLOCK\n"
    for group in ad_groups_to_add:
        lines_to_add = lines_to_add + "+:%s:ALL\n" % group
    lines_to_add = lines_to_add + "# END of ITS and TS support groups BLOCK\n"

    # remember the position to insert later, it's right at the position of first AD groups to remove
    regex_string = r"^\+.*:.*\b" + re.escape(ad_groups_to_remove[0]) + r"\b"
    file_position = re.search(regex_string, file_content, flags=re.IGNORECASE | re.MULTILINE).start()

    # revoke ad groups to remove
    for group in ad_groups_to_remove:
            regex_string = r"^\+.*:.*\b" + re.escape(group) + r"\b.*:ALL\n"
            file_content = re.sub(regex_string,'',file_content,flags=re.IGNORECASE | re.MULTILINE)

    # insert the lines for new ad groups
    file_content = file_content[:file_position] + lines_to_add + file_content[file_position:]

    try:
       fd.seek(0)
       fd.write(file_content)
       fd.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def get_mal_code():
     return 'UPS'


def main(argv):

    mal_code = get_mal_code()
    if mal_code not in mal_codes:
        print("Sorry This change doesn't support application mal code not in list %s." % mal_codes )
        exit(1)

    backup_access_file(access_file, rollback_dir)
    update_access_file(access_file, ad_groups_to_add_dict[mal_code], ad_groups_to_remove)


if __name__ == "__main__":
    main(sys.argv)
