This project will find the fairest FIFA World Cup draw.

##Primer.
The world cup has 32 teams.  They are grouped in 4.
So 8 groups of 4.

At the start, in group play, each team plays the other in the group.
The top 2 teams move on.

World Cups always tend to have a Group of Death - One
group will several very good teams.

They will often have a Group of Life - A group of weak teams.

FIFA keeps a rankings of national teams.
http://www.fifa.com/worldranking/rankingtable/

We will assume the groups are "fair" if each groups' teams' sum are
'close' to the other groups sum.

In other words, determine every single possible "8 groups of 4" and
find the one (the field) that has the smallest standard deviation amongst
the groups.


##Math.
Every single possible "8 groups of 4" is a big number.
(32 | 4) * (28 | 4) * (24 | 4) ... (4 | 4) = 2390,461,829,733,887,910,000,000
https://www.google.com/search?q=32+choose+4&oq=32+choose+4&aqs=chrome..69i57j0j69i59l2j69i61.3021j0j4&sourceid=chrome&espv=210&es_sm=91&ie=UTF-8#es_sm=91&espv=210&q=32%20choose%204%20times%2028%20choose%204%20times%2024%20choose%204%20times%2020%20choose%204%20times%2016%20choose%204%20times%2012%20choose%204%20times%208%20choose%204%20times%204%20choose%204


##Errata
The official FIFA ranking are notoriously inaccurate.
But they are official.

There are others.
* ELO: http://www.eloratings.net
* Nate Silver: http://espnfc.com/spi/rankings?cc=5901

Their data files are also included


     
The fifa draw does not allow more than 2 euro teams per group 
and no more that 1 from the others.


To run:
~/bin/wc$ python wc.py
