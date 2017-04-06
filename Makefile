gendir=generated
$(gendir)/README.anki.html: README.md Makefile
	rm -f $@
	markdown README.md > $@
	sed -e 's,</\?p>,,g' -e 's,h1>,b>,g' -e 's,em>,i>,g' -e 's,strong>,b>,g' -i $@
	chmod a-w $@
