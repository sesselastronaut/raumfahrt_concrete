#/bin/bash
echo "_____login"
wget -d --cookies=on --keep-session-cookies --save-cookies cookies.txt     --post-data 'username=olsen&password=Trafalmador3&_submit=Submit&_submitted=1' https://www.space-track.org/perl/login.pl
rm login.pl
sleep 3
echo "_____get catalag data"
wget --load-cookies=cookies.txt  --restrict-file-names=unix 'https://www.space-track.org/perl/dl.pl?ID=2'
echo "_____downloaded"
UNCOMPRESS_CHECK=$(file dl.pl\?ID\=2 | grep compressed)
if [ -z $UNCOMPRESS_CHECK];
	then
		echo "__File is empty"
	else
		echo "__got calatog - unzipping it"
		mv dl.pl?ID=2 catalog.txt.gz
		gunzip -f catalog.txt.gz

	fi
#rm catalog.txt
#gunzip -f catalog.txt.gz
