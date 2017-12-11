from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

engine = create_engine("postgresql://catalog:topsecret@localhost/catalogdb")
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
User1 = User(name="Yashwanth Manchikatla", email="yashwanth.manchikatla@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

#Item for Snowboarding
category0 = Category(user_id=1,name = "Snowboarding")

session.add(category0)
session.commit()

categoryItem1 = CategoryItem(user_id=1,name = "Snowboard", description = "Description: Best for any terrian and conditions. All-mountain snowboards perform anywhere on a mountain -- groomed runs, backcountry, even park and pipe.", category = category0)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1,name = "Goggles", description = "The Snow Goggles combine fit, function and affordability in a classic, stylish package. The Super Fit frame and plush, tailored face foam ensure a comfortable and secure fit that will keep you going for hours on the mountain. The Verse is designed to play nicely with your favorite helmet for seamless integration, while the AR40 lens takes on a variety of light conditions with ease.", category = category0)
session.add(categoryItem2)
session.commit()

#Item for Baseball
category1 = Category(user_id=1,name = "Baseball")

session.add(category1)
session.commit()

categoryItem1 = CategoryItem(user_id=1,name = "Bats", description = "Description: For players still learning the basics of the game, the RX4 USA Youth Bat features a stiff, traditional feel and lighter swing weight that helps players ease into the game with a durable, balanced bat.", category = category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1,name = "Batting Gloves", description = "Description: Dynamic performance for the superstar athlete, the Pro Series Batting Gloves are back and better than ever. Digitally-etched sheepskin leather is ultra-soft and provides a comfortable, secure grip on the bat in any playing conditions. Tectonic inserts allow for more hand movement without feeling bulky on your hand, while quad-flex creasing prevents these gloves from bunching up when your grip tightens.", category = category1)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1,name = "Baseballs", description = "Description: Get into the game with the Diamond Little League Baseball. The DLL-1 tournament grade baseball is built for the most demanding youth athletes. The DLL-1 Baseball features a premium leather cover, a cork/rubber pill core and select grey wool blend windings for excellent durability. The Diamond Little League Baseball is ideal for regular season play.", category = category1)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1,name = "Batting Helmets", description = "Description: Featuring a fabric-wrapped Charged Foam liner that absorbs impact, the Under Armour Junior Heater Digi Camo Batting Helmet offers critical protection when you need it most.", category = category1)
session.add(categoryItem4)
session.commit()

#Item for Basketball
category2 = Category(user_id=1,name = "Basketball")

session.add(category2)
session.commit()

categoryItem1 = CategoryItem(user_id=1,name = "Basketballs", description = "Description: The preferred ball of many high school and college athletes, the Wilson Evolution Game Basketball is among the top performers in it's class. Cushion Core Technology combines low-density sponge rubber and ultra-durable butyl rubber, producing a basketball with exceptional feel and unmatched durability. Constructed with a microfiber cover that is exclusively designed for the indoor court, the Wilson Official Evolution Game Basketball is a true champion.", category = category2)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1,name = "Hoops", description = "Description: Enhance your game with the Lifetime Steel-Framed Shatterproof Portable Basketball Hoop. This basketball system features a steel-framed, shatter-proof backboard with a blow-molded frame pad for maximum durability. Power Lift construction allows for effortless height adjustments, while the heavy-duty portable base and straight round extension arms provide extra stability.", category = category2)
session.add(categoryItem2)
session.commit()

#Item for Bowling
category3 = Category(user_id=1,name = "Bowling")

session.add(category3)
session.commit()

categoryItem1 = CategoryItem(user_id=1,name = "Balls", description = "Description: The Ebonite Reactive Crush/R Bowling Ball is designed for experienced and serious bowlers. A reactive resin cover provides an extreme hook for players with excellent control over the ball. High hook potential is provided by the highly polished finish that performs best on medium to heavy oiled lanes.", category = category3)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1,name = "Bowling Shoes", description = "Description: Bowl your best in the sleek looking Dexter Ricky IV Bowling Shoes. The Ricky IV is fully fabric-lined with a padded tongue and collar to maximize comfort and support. Its outsole is super lightweight for the best comfort and performance. The non-marking EVA midsole with defined rubber horseshoe heel delivers slide control.", category = category3)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1,name = "Ball Bags", description = "Description: Transport your bowling gear easily with the KR Strikeforce Rook Single Bowling Bag. The Rook Bowling Bag holds 1 bowling and has a foam ball holder protecting your bowling ball from scratches. Its side shoe compartment holds up to a size 11. Designed with 600D fabric, this bowling bag is strong and durable. Adjustable shoulder strap makes for easy carrying. Hit the lanes and roll strikes with the Rook Bowling Bag.", category = category3)
session.add(categoryItem3)
session.commit()


#Item for Fishing
category4 = Category(user_id=1,name = "Fishing")

session.add(category4)
session.commit()

categoryItem1 = CategoryItem(user_id=1,name = "Rods", description = "Description: The GX2 Casting Rod offers balance and durability. The GX2 rod is built with graphite and fiberglass to create a sensitive rod that is easy to balance. Ugly Tuff guides offer improved strength. Armed with the Clear Tip, the Shakespeare Ugly Stik GX2 Casting Rod stays strong without losing sensitivity, allowing you to detect even the lightest strike without losing one bit of the strength and durability.", category = category4)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1,name = "Reels", description = "Description: If you are looking for a well-crafted reel without breaking the bank, turn to the Daiwa Strikeforce-B Spinning Reel. Don't be fooled by the affordable price, this freshwater reel features Digigear digital gear design for optimized speed, power and durability as well as an ABS aluminum spool for longer and easier casting. With Twist Buster line twist reduction and a smooth, ball bearing drive, the Strikeforce-B is a winner.", category = category4)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1,name = "Fishing Line", description = "Description: New and improved, Berkley Trilene XL Monofilament Fishing Line utilizes the most versatile XL formula yet. Its low memory design keeps the line from twisting and prevents kinks, ensuring consistent performance every time it's cast. The Trilene XL line is made with flexible material that enhances sensitivity to help anglers feel strikes and obstacles better.", category = category4)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1,name = "Fishing Boats", description = "Description: The lightweight Sun Dolphin 12' Jon Boat has everything you need to stay on the water all day long. Stash your gear in the extra space on the bow and stern and still have room for a cooler filled with bait or snacks. Set your rods in the built in rod-holders and sit back as you wait for the fish to bite.", category = category4)
session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(user_id=1,name = "Fishing Kayaks", description = "Description: The Pelican Tracker Angler Kayak keeps you casting out and reeling in all season long! With two flush mount rod holders, plus convenient bungee storage system, this boat provides plenty of awesome features without sacrificing high performance. A twin-arched, multi chine hull helps keep you on track, while a paddle tie-down and carry handles simplify your next trip.", category = category4)
session.add(categoryItem5)
session.commit()

categoryItem6 = CategoryItem(user_id=1,name = "Waders", description = "Description: Step into a pair of PVC Hip Waders and step out into the water with confidence. These waders are constructed with a 20 denier nylon upper with a PVC backing, making them durable and completely waterproof. In addition, they are equipped with a lug sole PVC boot. Adjustable side straps ensure that you obtain a proper fit while wearing Pro Line PVC Hip Waders.", category = category4)
session.add(categoryItem6)
session.commit()

#Item for Golf
category5 = Category(user_id=1,name = "Golf")

session.add(category5)
session.commit()

categoryItem1 = CategoryItem(user_id=1,name = "Gloves", description = "Description: Experience the next level of fit, flex and feel with the EXO4 Golf Glove. The bonded FJ Exoskeleton features specially-designed FLX Zones for lightweight feel and enhanced range of motion. FiberSof MicroTAC palm material pairs with advanced Taction grip to deliver soft feel and a remarkable grip throughout the stroke. A hook-and-loop closure pairs with wrist elastic to maximize comfort with FootJoy EXO4 Golf Gloves.", category = category5)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1,name = "Drivers", description = "Description: Combine distance and forgiveness with a Driver. Cobra's longest, most forgiving adjustable driver features 10g of moveable weight, allowing golfers to choose penetrating (front) or towering (back) shot trajectory. MyFly 8 with SmartPad equips Cobra KING F6 Drivers for fine-tuned performance.", category = category5)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1,name = "Balls", description = "Description: Gain control of your short game with Revolution Control Golf Balls. A soft Shore 62D cover outfitted with dual radius dimple design allows the ball to stay on the face longer for more spin on scoring shots. The large, high C.O.R. core maximizes ball speed to generate fast, high and long trajectory for optimized launch. A 2-piece construction maximizes distance and control to equip Maxfli Revolution Control Golf Balls with added performance.", category = category5)
session.add(categoryItem3)
session.commit()

#Item for Football
category6 = Category(user_id=1,name = "Football")

session.add(category6)
session.commit()

categoryItem1 = CategoryItem(user_id=1,name = "Footballs", description = "Description: Train your young player on proper form when delivering a perfect spiral or bringing in catches with the Nike Vapor Strike Pee Wee Football. Built with a tacky synthetic leather and extruded lacing system, they'll quickly learn finger and hand placement to achieve success through the air. Whether using for official youth games or recreational play, the ball's TPU bladder ensures consistent air and shape retention for quality performances.", category = category6)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1,name = "Gloves", description = "Description: Designed for receivers looking to make all the tough catches in traffic, the Under Armour Youth F5 Receiver gloves provide the seamless, comfortable feel with maximum grip strength for elite athletes that make big plays in big moments.", category = category6)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1,name = "Football Cleats", description = "Description: Perform at your highest level in the Vapor Untouchable II. A woven upper with one-piece collar wraps your foot for a comfortable glove like fit from the first wear while Flywire cables lock your foot in for a durable supportive fit during lateral movements. The Nike Vapor Untouchable 2 football cleat has a carbon fiber plate that provide enhanced traction, speed and performance to put you head and shoulders above your opponents.", category = category6)
session.add(categoryItem3)
session.commit()

print "added menu items!"
