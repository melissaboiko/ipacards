gendir=generated
$(gendir)/deck_description.anki.html: deck_description.md Makefile
	rm -f $@
	markdown deck_description.md > $@
	sed -e 's,</\?p>,,g' -e 's,h1>,b>,g' -e 's,em>,i>,g' -e 's,strong>,b>,g' -i $@
	chmod a-w $@
