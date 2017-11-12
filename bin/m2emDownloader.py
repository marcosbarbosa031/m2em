import ssl
from bs4 import BeautifulSoup
import requests
import os
import logging
import bin.m2emHelper as helper
import bin.sourceparser.m2emMangastream as msparser


def ChapterDownloader(config):
    
    # Load configs required here
    database = config["Database"]
    saveloc  = config["SaveLocation"]

    # Load Chapters from Database
    chapters = helper.getChapters(database)
    logging.debug("Loaded Chapers:")
    for i in chapters:
        logging.debug(i)
    pass


    # Start Download loop!
    for chapter in chapters:

        # get relevant data of this Manga
        mangaid         = chapter[0]
        mangastarturl   = chapter[4]
        ispulled        = chapter[6]
        mangapages      = chapter[9]
        mangatitle      = chapter[2]
        downloadfolder  = str(saveloc + mangatitle + "/images")

        if os.path.isdir(downloadfolder):
            logging.debug("Manga %s downloaded already!" % mangatitle)
        else:
            logging.info("Starting download of %s..." % mangatitle)


            # get Origin of manga
            origin = helper.getSourceURL(mangastarturl)


            # Get image urls!
            if origin == "mangastream.com":
                urllist = msparser.getPagesUrl(mangastarturl,mangapages)


                # Turn Manga pages into Image links!
                imageurls=[]
                for i in urllist:
                    imageurls.append(msparser.getImageUrl(i))
                logging.debug("List of all Images for %s" % mangatitle)
                logging.debug(imageurls)
                

            # Mangafox Parser
            elif origin == "mangafox.com":
                #logging.info("Getting Mangadata from Mangafox.me")
                pass

            else:
                pass


            # Download & save images!
            # check if we have images to download
            if not len(imageurls) == 0:
                helper.createFolder(downloadfolder)
                counter = 0
                for image in imageurls:
                    counter = counter + 1
                    f = open(downloadfolder + "/" + str("{0:0=3d}".format(counter)) + ".png", 'wb')
                    f.write(requests.get(image).content)
                    f.close

                logging.info("Finished download!")