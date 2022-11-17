#!/bin/sh
echo "Start installation of SecurePassworld"
echo ""
sh ./buildimage.sh
echo ""
sh ./inithelm.sh
echo ""
sh ./loadimage.sh
echo ""
sh ./kubectlapply.sh