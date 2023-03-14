#!/bin/bash

rm -rf bufr_encode_L2B.exe
ifort $FCFLAGS -c bufr_encode_L2B.f90
ifort -o bufr_encode_L2B.exe bufr_encode_L2B.o /uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/GSI/GSILIBS/build/lib/libbufr_v.a
./bufr_encode_L2B.exe
