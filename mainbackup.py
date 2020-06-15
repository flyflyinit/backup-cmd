import subprocess
import datetime
import os
from random import randint

def mainbackups():
    while True:
        try:
            ask = str(input("\n1- Create Full Backup\n2- Create Incremental Backup\n3- Restore Full Backups\n4- Restore Incremental Backups\n5- List recent backups\n6- Schedule Backups\n7- List Scheduled Backups\n8- Exit Backup Mode\nChoose : "))
        except TypeError:
            print("\n[DATATYPE ERROR] try again! ")
            continue
        except ValueError:
            print("\n[VALUE ERROR] try again! ")
            continue
        except:
            print("\n[ERROR] try again! ")
            continue
        else:
            if str(ask) == '1':
                fullbackup()
                continue
            elif str(ask) == '2':
                incrementalbackup()
                continue
            elif str(ask) == '3':
                restorefullbackup()
                continue
            elif str(ask) == '4':
                restoreincrementalbackup()
                continue
            elif str(ask) == '5':
                listbackups()
                continue
            elif str(ask) == '6':
                scheduleBackups()
                continue
            elif str(ask) == '7':
                listScheduledBackups()
                continue
            elif str(ask) == '8':
                break
            else:
                print("\n[WRONG VALUE] try again! ")
                continue

def listScheduledBackups():
    while True:
        print("\nAll cron Backups jobs that exist in this user : ")
        try:
            cron = subprocess.Popen("crontab -l | awk '/[.]sh$/ {print}'", shell=True, stdout=subprocess.PIPE)
            out = cron.communicate()[0].decode('utf-8')
        except TypeError:
            print("\n[DATATYPE ERROR] try again! ")
            continue
        except ValueError:
            print("\n[VALUE ERROR] try again! ")
            continue
        except:
            print("\n[ERROR] try again! ")
            continue
        else:
            print(out)
            break

def scheduleBackups():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    while True:
        listScheduledBackups()
        try:
            print("\n\nCreate a cron job (make sure to respect the cron job structure, and to put spaces between columns),  Some examples :\n@yearly                      (execute yearly) ..\n0 2 * * *                    (execute at 2am daily)\n* * * jan,may,aug *          (execute on january,may,august)\n0 17 * * sun,fri             (each sunday and friday at 5pm)")
            job = str(input("\nMinutes   Hours  Day-of-Month   Month   Day-of-Week\n"))
        except TypeError:
            print("\n[DATATYPE ERROR] try again! ")
            continue
        except ValueError:
            print("\n[VALUE ERROR] try again! ")
            continue
        except:
            print("\n[ERROR] try again! ")
            continue
        else:
            fullbackups = getmyfullbackupslist()
            incrementalbackups = getmyincrementalbackupslist()

            while True:
                try:
                    backupid = int(input("\nSelect a backup ID : "))
                except TypeError:
                    print("\n[DATATYPE ERROR] try again! ")
                    continue
                except ValueError:
                    print("\n[VALUE ERROR] try again! ")
                    continue
                except:
                    print("\n[ERROR] try again! ")
                    continue
                else:
                    if (0 <= backupid <= 500):
                        for i in fullbackups:
                            if (backupid == int(i[0])):
                                CMD =f"tar -cvvpzf {i[4]}/{i[2]}_$( date '+%Y-%m-%d_%H-%M-%S' ).tar.gz  {i[5]}  {i[3]}\n"

                                with open(f'{dir_path}/command_{i[2]}.sh', mode='w') as f:
                                    f.write(f'#!/bin/bash\n#Description : this is a shell script contains the command of creating a backup (id:{i[0]}, name:{i[2]}), and it will be used by a cron job\n\n\n{CMD}')
                                subprocess.call(f"chmod u+x {dir_path}/command_{i[2]}.sh",shell=True)

                                line = f"{job}      cd {dir_path} ; ./command_{i[2]}.sh"
                                print(f"\nappending a new line to the cron jobs list..\n{line}")
                                with open(f'/var/spool/cron/root', mode='a') as f:
                                    f.write(f'{line}\n')
                                subprocess.call("crontab -e",shell=True)

                            else:
                                continue
                        break
                    elif (501 <= backupid <= 1000):
                        for i in incrementalbackups:
                            if (backupid == int(i[2])):

                                CMD =f"tar -cvvpzg  {i[6]}/{i[1]}.snar  -f {i[6]}/{i[4]}_$( date '+%Y-%m-%d_%H-%M-%S' ).tar.gz  {i[7]}  {i[5]}\n"
                                with open(f'{dir_path}/command_{i[1]}_{i[4]}.sh', mode='w') as f:
                                    f.write(f'#!/bin/bash\n#Description : this is a shell script contains the command of creating a backup (metaname:{i[1]}, id:{i[2]}, name:{i[4]}), and it will be used by a cron job\n\n\n{CMD}')
                                subprocess.call(f"chmod u+x {dir_path}/command_{i[1]}_{i[4]}.sh",shell=True)

                                line = f"{job}      cd {dir_path}  ; ./command_{i[1]}_{i[4]}.sh"
                                print(f"\nappending a new line to the cron jobs list..\n{line}")
                                with open(f'/var/spool/cron/root', mode='a') as f:
                                    f.write(f'{line}\n')
                                subprocess.call("crontab -e", shell=True)

                            else:
                                continue
                        break
                    else:
                        print("\nWRONG VALUE! BACKUP ID OUT OF RANGE\n[0-500] full backups\n[501-1000] incremenal backups")
                        continue
            break


def restorefullbackup():
    fullbackups = getmyfullbackupslist()
    printmyfullbackupslist(fullbackups)
    while True:
        try:
            backupid = int(input(f"\nEnter a backup ID : "))
        except TypeError:
            print("\n[DATATYPE ERROR] try again! ")
            continue
        except ValueError:
            print("\n[VALUE ERROR] try again! ")
            continue
        except:
            print("\n[ERROR] try again! ")
            continue
        else:
            if (0 <= backupid <= 500):
                for i in fullbackups:
                    if (backupid == int(i[0])):
                        restoreDestination = str(input("\nEnter The Restore destination (ex: /home/DIR1/) : "))
                        print(f"\nRestoring the backup {i[2]} in the destination {restoreDestination}..")
                        subprocess.call(f"tar -xvvpzf  {i[4]}/{i[2]}.tar.gz  -C {restoreDestination}", shell=True)
                    else:
                        continue
                break
            else:
                print("\nWRONG VALUE! BACKUP ID OUT OF RANGE\n[0-500] full backups\n[501-1000] incremenal backups")
                continue


def fullbackup():
    print("\nRoot tree : ")
    subprocess.call(f'tree / -L 1', shell=True)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    backuppath = str(input("\n\nMAKE SURE TO PROVIDE FULL PATHS (ex:/DIR1/DIR2/DIR3) (ex:/DIR1/file1)\nSpecify what you are going to backup (ex:/var/www) (ex:/) : "))
    dstbackup =  str(input(f"Specify the directory destination backup (where the backup file going to be stored, it can be locally or remotely) (ex:/home) (ex:remotehost:/home) : "))

    IsDIR = os.path.isdir(backuppath)

    if IsDIR:
        subprocess.call(f'tree {backuppath} -L 2', shell=True)

    excluded=""
    while IsDIR:
        backupexclude = str(input(f"Do you want to exclude any directories/files (leave it empty if you don't want to exclude) (ex:{backuppath}/DIR2) (ex:{backuppath}/file1) : "))
        if (backupexclude == ""):
            break
        excluded=excluded+" --exclude="+backupexclude
        continue

    backupname = str(input("Give your backup a name (ex:myfirstbackup) : "))
    print(f"\nCreating a backup  {backupname}  of  {backuppath} by excluding {excluded} ..")
    CMD = "tar -cvvpzf "+dstbackup+"/"+backupname+".tar.gz "+excluded+" "+backuppath
    subprocess.call(f'{CMD}', shell=True)
    today = datetime.datetime.today()
    line = str(randint(0,500))+"::"+str(today)+"::"+backupname+"::"+backuppath+"::"+dstbackup+"::"+excluded
    with open(f'{dir_path}/fullbackuphistory', mode='a') as f:
        f.write(f'\n{line}')



def restoreincrementalbackup():
    while True:
        incrementalbackups = getmyincrementalbackupslist()
        printmyincrementalbackupslist(incrementalbackups)
        try:
            metafilename = str(input(f"\nEnter a meta file name (ex:mydata) : "))
            incrementalbackupsundermetaname, metanameexist = listmetafiles(incrementalbackups,metafilename)
            print(incrementalbackupsundermetaname)
            if metanameexist == False:
                print("ERROR : meta name not found")
                continue
            restoreDestination = str(input("\nEnter The Restore destination (ex: /home/DIR1/) : "))
            restorelevel = str(input("Do You Want to Restore all the backups under the meta name [YES/NO] : "))
        except TypeError:
            print("\n[DATATYPE ERROR] try again! ")
            continue
        except ValueError:
            print("\n[VALUE ERROR] try again! ")
            continue
        except:
            print("\n[ERROR] try again! ")
            continue
        else:
            if restorelevel.lower() == 'yes':
                for backup in incrementalbackupsundermetaname:
                    print(f"\nRestoring the backup {backup[4]} , level {backup[0]}, in the destination {restoreDestination}..")
                    subprocess.call(f"tar --extract --verbose --verbose --preserve-permissions --listed-incremental=/dev/null --file={backup[6]}/{backup[4]}.tar.gz  --directory={restoreDestination}", shell=True)

                break
            elif restorelevel.lower() == 'no':
                while True:
                    try:
                        beginLevel = int(input("Specify The beginning Level : "))
                        endLevel = int(input("Specify The End Level : "))
                    except TypeError:
                        print("\n[DATATYPE ERROR] try again! ")
                        continue
                    except ValueError:
                        print("\n[VALUE ERROR] try again! ")
                        continue
                    except:
                        print("\n[ERROR] try again! ")
                        continue
                    else:
                        for backup in incrementalbackupsundermetaname[beginLevel:endLevel+1]:
                            print(f"\nRestoring the backup {backup[4]} , level {backup[0]}, in the destination {restoreDestination}..")
                            subprocess.call(f"tar --extract --verbose --verbose --preserve-permissions --listed-incremental=/dev/null --file={backup[6]}/{backup[4]}.tar.gz  --directory={restoreDestination}", shell=True)
                        break
                break
            else:
                print("\n[WRONG VALUE] try again! ")
                continue


def incrementalbackup():

    IsDIR = True
    print("\nRoot tree : ")
    subprocess.call(f'tree / -L 1', shell=True)
    dir_path = os.path.dirname(os.path.realpath(__file__))


    while True:
        try:
            metafilename = str(input(f"Have you created already an initial first backup (level 0), Enter the meta file name, if you didn't leave it empty : "))
        except TypeError:
            print("\n[DATATYPE ERROR] try again! ")
            continue
        except ValueError:
            print("\n[VALUE ERROR] try again! ")
            continue
        except:
            print("\n[ERROR] try again! ")
            continue
        else:

            if metafilename=="":
                metafilename = str(input(f"Enter a new meta file name (ex:mydata) : "))
                backuppath = str(input("MAKE SURE TO PROVIDE FULL PATHS (ex:/DIR1/DIR2/DIR3) (ex:/DIR1/file1)\nSpecify what you are going to backup (ex:/var/www) (ex:/) : "))
                dstbackup =  str(input(f"Specify the directory destination backup (where the backup file going to be stored, it can be locally or remotely) (ex:/home) (ex:remotehost:/home) : "))

                IsDIR = os.path.isdir(backuppath)

                if IsDIR:
                    subprocess.call(f'tree {backuppath} -L 2', shell=True)

                excluded=""
                while IsDIR:
                    backupexclude = str(input(f"Do you want to exclude any directories/files (leave it empty if you don't want to exclude) (ex:{backuppath}/DIR2) (ex:{backuppath}/file1) : "))
                    if (backupexclude == ""):
                        break
                    excluded=excluded+" --exclude="+backupexclude
                    continue


                backupname = str(input("Give your backup a name (ex:myfirstbackup) : "))

                subprocess.call(f'mkdir {dstbackup}/{metafilename}',shell=True)

                print(f"\nCreating a backup  {backupname} under the meta file name  {metafilename}  of  {backuppath}  by excluding {excluded} ..")
                CMD = "tar -cvvpzg  "+dstbackup+"/"+metafilename+"/"+metafilename+".snar "+"  -f  "+dstbackup+"/"+metafilename+"/"+backupname+".tar.gz "+excluded+" "+backuppath
                subprocess.call(f'{CMD}', shell=True)

                today = datetime.datetime.today()
                dstbackup=dstbackup+"/"+metafilename
                line = "0::"+metafilename+"::"+str(randint(501, 1000)) + "::" + str(today) + "::" + backupname + "::" + backuppath + "::" + dstbackup+"::"+excluded
                with open(f'{dir_path}/incrementalbackuphistory', mode='a') as f:
                    f.write(f'\n{line}')
                break

            else:
                incrementalbackups = getmyincrementalbackupslist()
                incrementalbackupsundermetaname,metanameexist = listmetafiles(incrementalbackups,metafilename)
                if metanameexist==False:
                    break

                backupname = str(input("\nGive your backup a name (ex:mythirdbackup) : "))
                print(f"\nCreating a backup  {backupname} under the meta file name  {metafilename}  of  {incrementalbackupsundermetaname[0][5]}  in {incrementalbackupsundermetaname[0][6]} ..")
                CMD = "tar -cvvpzg  "+incrementalbackupsundermetaname[0][6]+"/"+metafilename+".snar "+"  -f  "+incrementalbackupsundermetaname[0][6]+"/"+backupname+".tar.gz "+incrementalbackupsundermetaname[0][7]+" "+incrementalbackupsundermetaname[0][5]
                subprocess.call(f'{CMD}', shell=True)
                today = datetime.datetime.today()

                lastlevel= getlastlevel(incrementalbackups,metafilename)
                lastlevel=lastlevel+1

                line = str(lastlevel)+"::"+metafilename+"::"+str(randint(501, 1000)) + "::" + str(today) + "::" + backupname + "::" + incrementalbackupsundermetaname[0][5] + "::" + incrementalbackupsundermetaname[0][6] +"::"+ incrementalbackupsundermetaname[0][7]
                with open(f'{dir_path}/incrementalbackuphistory', mode='a') as f:
                    f.write(f'\n{line}')
                break


def getlastlevel(incrementalbackups,metafilename):
    levels = []
    for i in incrementalbackups:
        if (metafilename==i[1]):
            levels.append(i[0])
        else:
            continue
    levels.sort()
    return int(levels[-1])

def listmetafiles(incrementalbackups,metaname):
    incrementalbackupsundermetaname = []
    metanameexist = False

    print(f"\nbackups under {metaname} meta file : ")
    for i in incrementalbackups:
        if (metaname==i[1]):
            incrementalbackupsundermetaname.append(i)
            print(f"backup level:{i[0]} ,backup meta name:{i[1]} ,backupID:{i[2]} ,backup date:{i[3]} ,backup name:{i[4]}  ,source backup path:{i[5]} ,destination backup path:{i[6]}  ,excluded:{i[7]}")
            metanameexist = True
        else:
            continue
    if metanameexist==False:
        print(f"No Backup Found\n")

    return incrementalbackupsundermetaname,metanameexist


def listbackups():
    fullbackups = getmyfullbackupslist()
    incrementalbackups = getmyincrementalbackupslist()
    printmyfullbackupslist(fullbackups)
    printmyincrementalbackupslist(incrementalbackups)

    while True:
        try:
            backupid = int(input(f"\nEnter a backup ID : "))
        except TypeError:
            print("\n[DATATYPE ERROR] try again! ")
            continue
        except ValueError:
            print("\n[VALUE ERROR] try again! ")
            continue
        except:
            print("\n[ERROR] try again! ")
            continue
        else:
            if (0 <= backupid <= 500):
                for i in fullbackups:
                    if (backupid == int(i[0])):
                        print(
                            f"\nbackupID:{i[0]} ,backup date:{i[1]} ,backup name:{i[2]}  ,source backup path:{i[3]} ,destination backup path:{i[4]}  ,excluded:{i[5]}")
                        print("\nbackup contents : ")
                        subprocess.call(f"tar --list --verbose --verbose --file={i[4]}/{i[2]}.tar.gz", shell=True)
                    else:
                        continue
                break
            elif (501 <= backupid <= 1000):
                for i in incrementalbackups:
                    if (backupid == int(i[2])):
                        print(
                            f"\nbackup level:{i[0]} ,backup meta name:{i[1]} ,backupID:{i[2]} ,backup date:{i[3]} ,backup name:{i[4]}  ,source backup path:{i[5]} ,destination backup path:{i[6]} ,excluded:{i[7]}")
                        print("\nbackup contents : ")
                        subprocess.call(f"tar --list --verbose --verbose --listed-incremental={i[6]}/{i[1]}.snar --file={i[6]}/{i[4]}.tar.gz",
                            shell=True)
                    else:
                        continue
                break
            else:
                print("\nWRONG VALUE! BACKUP ID OUT OF RANGE\n[0-500] full backups\n[501-1000] incremenal backups")
                continue




def getmyfullbackupslist():
    list_of_full_backups = []
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(f"{dir_path}/fullbackuphistory", mode='r') as fullbackup_content:
        each_line = fullbackup_content.readlines()
        fullbackup_content.close()


    for each_backup in each_line:
        each_backup = each_backup.rstrip()
        each_backup2 = each_backup.split("::")
        list_of_full_backups.append(each_backup2)

    list_of_full_backups = list_of_full_backups[1:]
    return list_of_full_backups


def printmyfullbackupslist(list_of_full_backups):
    print("\n\nList Of Full Backups :")
    for i in list_of_full_backups:
        print(f"backupID:{i[0]} ,backup date:{i[1]} ,backup name:{i[2]}  ,source backup path:{i[3]} ,destination backup path:{i[4]} ,excluded:{i[5]}")



def getmyincrementalbackupslist():
    list_of_incremental_backups = []
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(f"{dir_path}/incrementalbackuphistory", mode='r') as incrementalbackup_content:
        each_line = incrementalbackup_content.readlines()
        incrementalbackup_content.close()

    for each_backup in each_line:
        each_backup = each_backup.rstrip()
        each_backup2 = each_backup.split("::")
        list_of_incremental_backups.append(each_backup2)

    list_of_incremental_backups = list_of_incremental_backups[1:]
    return list_of_incremental_backups


def printmyincrementalbackupslist(list_of_incremental_backups):
    print("\n\nList Of Incremental Backups :")
    for i in list_of_incremental_backups:
        print(f"backup level:{i[0]} ,backup meta name:{i[1]} ,backupID:{i[2]} ,backup date:{i[3]} ,backup name:{i[4]}  ,source backup path:{i[5]} ,destination backup path:{i[6]} ,excluded:{i[7]}")





if __name__ == "__main__":
	mainbackups()