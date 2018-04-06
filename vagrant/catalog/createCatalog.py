#!/usr/bin/python
from __future__ import print_function
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Category, CatalogItem

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(username="RoboUser", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
User1.hash_password("Udacity1")
session.add(User1)
session.commit()

Category1 = Category(user_id=1, name="Funk")
session.add(Category1)
session.commit()

item1_desc = "Parliament is a funk band formed in the late 1960s by George \
Clinton as part of his Parliament-Funkadelic collective. Less rock-oriented \
than its sister act Funkadelic, Parliament drew on science-fiction, outlandish\
 performances, and psychedelia in their work. The band scored a number of \
 Top 10 hits, including the million-selling 1975 single 'Give Up \
 the Funk(Tear the Roof off the Sucker)'."
catalogItem1 = CatalogItem(user_id=1,
                           name="Parliament",
                           description=item1_desc,
                           user=User1,
                           category=Category1)
session.add(catalogItem1)
session.commit()

item2_desc = "Funkadelic is an American band that was most prominent during \
the 1970s. The band and its sister act Parliament, both led by \
George Clinton, pioneered the funk music culture of that decade. \
Relative to its sister act, Funkadelic pursued a heavier, \
psychedelic rock-oriented sound."
catalogItem2 = CatalogItem(user_id=1,
                           name="Funkadelic",
                           description=item2_desc,
                           user=User1,
                           category=Category1)
session.add(catalogItem2)
session.commit()

item3_desc = "The Meters are an American funk band formed in 1965 by Zigaboo \
Modeliste (drums), George Porter Jr. (bass), Leo Nocentelli (guitar), and \
Art Neville (keyboards) in New Orleans, Louisiana. The band performed and \
recorded their own music from the late 1960s until 1977 and played an \
influential role as backing musicians for other artists, including Lee \
Dorsey, Robert Palmer, Dr. John, and Allen Toussaint. Their original songs \
'Cissy Strut' and 'Look-Ka Py Py' are considered funk classics."
catalogItem3 = CatalogItem(user_id=1,
                           name="The Meters",
                           description=item3_desc,
                           user=User1,
                           category=Category1)
session.add(catalogItem3)
session.commit()

item4_desc = "The Brothers Johnson were an American funk, Motown and R&B band \
consisting of American musicians and brothers George (Lightnin' Licks) and \
Louis E. Johnson (Thunder Thumbs). They achieved their greatest success from \
the mid-1970s to early 1980s, with three singles topping the R&B charts \
(I\'ll Be Good to You, Strawberry Letter 23, and Stomp!)."
catalogItem4 = CatalogItem(user_id=1,
                           name="The Brothers Johnson",
                           description=item4_desc,
                           user=User1,
                           category=Category1)
session.add(catalogItem4)
session.commit()

Category2 = Category(user_id=1, name="Rock")
session.add(Category2)
session.commit()

item5_desc = "Aerosmith is an American rock band, sometimes referred to as \
'the Bad Boys from Boston' and 'America\'s Greatest Rock and Roll Band'. \
Their style, which is rooted in blues-based hard rock, has come to also \
incorporate elements of pop, heavy metal, and rhythm and blues, and has \
inspired many subsequent rock artists. They were formed in \
Boston, Massachusetts, in 1970."
catalogItem5 = CatalogItem(user_id=1,
                           name="Aerosmith",
                           description=item5_desc,
                           user=User1,
                           category=Category2)
session.add(catalogItem5)
session.commit()

item6_desc = "Kiss (often stylized as KISS) is an American rock band formed \
in New York City in January 1973 by Paul Stanley, Gene Simmons, Peter Criss, \
and Ace Frehley. Well known for its members' face paint and stage outfits, \
the group rose to prominence in the mid-to-late 1970s with their elaborate \
live performances, which featured fire breathing, blood-spitting, \
smoking guitars, shooting rockets, levitating drum kits, and pyrotechnics."
catalogItem6 = CatalogItem(user_id=1,
                           name="KISS",
                           description=item6_desc,
                           user=User1,
                           category=Category2)
session.add(catalogItem6)
session.commit()

item7_desc = "Van Halen is an American hard rock band formed in Pasadena, \
California, in 1972. From 1974 until 1985, the band consisted of guitarist \
Eddie Van Halen, vocalist David Lee Roth, drummer Alex Van Halen, \
and bassist Michael Anthony."
catalogItem7 = CatalogItem(user_id=1,
                           name="Van Halen",
                           description=item7_desc,
                           user=User1,
                           category=Category2)
session.add(catalogItem7)
session.commit()

Category3 = Category(user_id=1, name="Punk")
session.add(Category3)
session.commit()

item8_desc = "The Sex Pistols were an English punk rock band that formed in \
London in 1975. They were responsible for initiating the punk movement in the \
United Kingdom and inspiring many later punk and alternative rock musicians. \
Although their initial career lasted just two and a half years and produced \
only four singles and one studio album, Never Mind the Bollocks, Here's the \
Sex Pistols, they are regarded as one of the most influential acts in the \
history of popular music."
catalogItem8 = CatalogItem(user_id=1,
                           name="Sex Pistols",
                           description=item8_desc,
                           user=User1,
                           category=Category3)
session.add(catalogItem8)
session.commit()

item9_desc = "The Clash were an English rock band formed in London in 1976 as \
a key player in the original wave of British punk rock. They have also \
contributed to the post-punk and new wave movements that emerged in the wake \
of punk and employed elements of a variety of genres including reggae, dub, \
funk, ska and rockabilly. For most of their recording career, the Clash \
consisted of lead vocalist and rhythm guitarist Joe Strummer, lead guitarist \
and lead vocalist Mick Jones, bassist Paul Simonon, and drummer Nicky \
'Topper' Headon. Headon left the group in 1982, and internal friction led to \
Jones' departure the following year. The group continued with new members, \
but finally disbanded in early 1986."
catalogItem9 = CatalogItem(user_id=1,
                           name="The Clash",
                           description=item9_desc,
                           user=User1,
                           category=Category3)
session.add(catalogItem9)
session.commit()

Category4 = Category(user_id=1, name="Funk Rock")
session.add(Category4)
session.commit()

item10_desc = "Red Hot Chili Peppers are an American funk rock band formed in \
Los Angeles in 1983. The group's musical style primarily consists of rock \
with an emphasis on funk, as well as elements from other genres such as punk \
rock and psychedelic rock. When played live, their music incorporates \
elements of jam band due to the improvised nature of many of their \
performances. Currently, the band consists of founding members \
vocalist/rhythm guitarist Anthony Kiedis and bassist Flea, longtime drummer \
Chad Smith, and former touring guitarist Josh Klinghoffer. Red Hot Chili \
Peppers are one of the best-selling bands of all time with over 80 million \
records sold worldwide, have been nominated for sixteen Grammy Awards, of \
which they have won six, and are the most successful band in alternative \
rock radio history, currently holding the records for most number-one \
singles (13), most cumulative weeks at number one (85) and most top-ten \
songs (25) on the Billboard Alternative Songs \
chart. In 2012, they were inducted into the Rock and Roll Hall of Fame."
catalogItem10 = CatalogItem(user_id=1,
                            name="Red Hot Chili Peppers",
                            description=item10_desc,
                            user=User1,
                            category=Category4)
session.add(catalogItem10)
session.commit()

item11_desc = "Rage Against the Machine is an American rock band from \
Los Angeles, California. Formed in 1991, the group consists of vocalist \
Zack de la Rocha, bassist and backing vocalist Tim Commerford, guitarist \
Tom Morello, and drummer Brad Wilk. Rage Against the Machine is well known \
for the members' revolutionary political views, which are expressed in many \
of the band's songs. As of 2010, they had sold over 16 million records \
worldwide."
catalogItem11 = CatalogItem(user_id=1,
                            name="Rage Against the Machine",
                            description=item11_desc,
                            user=User1,
                            category=Category4)
session.add(catalogItem11)
session.commit()

item12_desc = "Primus is an American rock band based in San Francisco, \
California, currently composed of bassist/vocalist Les Claypool, guitarist \
Larry 'Ler' LaLonde and drummer Tim 'Herb' Alexander. Primus originally \
formed in 1984 with Claypool and guitarist Todd Huth, later joined by drummer \
Jay Lane, though the latter two departed the band at the end of 1988. \
Featuring LaLonde and Alexander, Primus recorded their debut Suck on This \
in 1989, followed by four studio albums: Frizzle Fry, Sailing the Seas of \
Cheese, Pork Soda, and Tales from the Punchbowl. Alexander left the band in \
1996, replaced by Bryan 'Brain' Mantia, and Primus went on to record the \
original theme song for the TV show South Park and two more albums, Brown \
Album and Antipop, before declaring a hiatus in 2000."
catalogItem12 = CatalogItem(user_id=1,
                            name="Primus",
                            description=item12_desc,
                            user=User1,
                            category=Category4)
session.add(catalogItem12)
session.commit()

Category5 = Category(user_id=1, name="Jazz")
session.add(Category5)
session.commit()

item13_desc = "Miles Dewey Davis III (May 26, 1926 - September 28, 1991) was \
an American jazz trumpeter, bandleader, and composer. He is among the most \
influential and acclaimed figures in the history of jazz and 20th century \
music. Davis adopted a variety of musical directions in his five-decade \
career which kept him at the forefront of a number of major stylistic \
developments in jazz."
catalogItem13 = CatalogItem(user_id=1,
                            name="Miles Davis",
                            description=item13_desc,
                            user=User1,
                            category=Category5)
session.add(catalogItem13)
session.commit()

item14_desc = "John William Coltrane, also known as 'Trane' (September 23, \
1926 - July 17, 1967), was an American jazz saxophonist and composer. Working \
in the bebop and hard bop idioms early in his career, Coltrane helped pioneer \
the use of modes in jazz and was later at the forefront of free jazz. He led \
at least fifty recording sessions during his career, and appeared as a \
sideman on many albums by other musicians, including trumpeter Miles Davis \
and pianist Thelonious Monk."
catalogItem14 = CatalogItem(user_id=1,
                            name="John Coltrane",
                            description=item14_desc,
                            user=User1,
                            category=Category5)
session.add(catalogItem14)
session.commit()

item15_desc = "Thelonious Sphere Monk (October 10, 1917 - February 17, 1982) \
was an American jazz pianist and composer."
catalogItem15 = CatalogItem(user_id=1,
                            name="Thelonious Monk",
                            description=item15_desc,
                            user=User1,
                            category=Category5)
session.add(catalogItem15)
session.commit()

print("Added all items to catalog!")
