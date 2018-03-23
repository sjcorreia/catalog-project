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
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

Category1 = Category(user_id=1, name="Hockey")
session.add(Category1)
session.commit()

catalogItem1 = CatalogItem(user_id=1,
                           name="CCM Helmet",
                           description="Something to protect your head!",
                           user=User1,
                           category=Category1)
session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1,
                           name="Shoulder Pads",
                           description="Padding to protect your shoulders.",
                           user=User1,
                           category=Category1)
session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1,
                           name="Shin Guards",
                           description="Padding to protect your shins.",
                           user=User1,
                           category=Category1)
session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1,
                           name="Hockey Stick",
                           description="The stick used to play the game.",
                           user=User1,
                           category=Category1)
session.add(catalogItem4)
session.commit()

Category2 = Category(user_id=1, name="Soccer")
session.add(Category2)
session.commit()

catalogItem5 = CatalogItem(user_id=1,
                           name="Soccer Cleats",
                           description="The shoes worn while playing soccer.",
                           user=User1,
                           category=Category2)
session.add(catalogItem5)
session.commit()

catalogItem5 = CatalogItem(user_id=1,
                           name="Soccer Gloves",
                           description="The gloves worn by a soccer goaltender.",
                           user=User1,
                           category=Category2)
session.add(catalogItem5)
session.commit()

print("Added all items to catalog!")
