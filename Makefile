#//////////////////////////////////////////////////////////////
#//                                                          //
#//  docker-multimedia, 2024                                 //
#//  Created: 30, May, 2021                                  //
#//  Modified: 14 November, 2024                             //
#//  file: -                                                 //
#//  -                                                       //
#//  Source:                                                 //
#//  OS: ALL                                                 //
#//  CPU: ALL                                                //
#//                                                          //
#//////////////////////////////////////////////////////////////

SERVER_DIRECTORY ?= website

WEB_SERVICES ?= zola

PROFILES ?= $(WEB_SERVICES)

.PHONY: rmmetadata
rmmetadata:
	time find . -type f \( -iname "*.jpeg" -o -iname "*.jpg" -o -iname "*.png" \) -print0 | parallel -0 exiftool -all= -overwrite_original "{}"

include DockerCompose.mk
