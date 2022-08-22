from api import api
from database.model.Activity import Activity
from database.model.Category import Category
from database import db
from flask_restx import Resource

backup_ns = api.namespace("backup", validate=True)


@backup_ns.route("/")
class BackupAPI(Resource):
    def post(self, *args, **kwargs):
        """
        Backup categories and activities into database
        """
        # Add categories
        db.session.add(Category(name="motor", path="/img/Category/mechanic.jpg"))
        db.session.add(Category(name="water", path="/img/Category/water.jpg"))
        db.session.add(Category(name="air", path="/img/Category/air.jpg"))
        db.session.add(Category(name="wheel", path="/img/Category/wheel.jpg"))
        db.session.add(Category(name="shooting", path="/img/Category/shooting.jpg"))
        db.session.add(Category(name="animal", path="/img/Category/animal.jpg"))
        db.session.add(Category(name="mountain", path="/img/Category/mountain.jpg"))
        db.session.add(Category(name="indoor", path="/img/Category/indoor.jpg"))
        db.session.add(Category(name="outdoor", path="/img/Category/outdoor.jpg"))
        db.session.add(Category(name="ticket", path="/img/Category/ticket.jpg"))
        db.session.add(Category(name="vip", path="/img/Category/vip.jpg"))

        # Add vip acitivies
        db.session.add(
            Activity(
                cat="vip", name="bodyguard", path="/img/Activity/vip/bodyguard.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="vip", name="chauffeur", path="/img/Activity/vip/chauffeur.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="vip", name="concierge", path="/img/Activity/vip/concierge.jpg"
            )
        )
        db.session.add(
            Activity(cat="vip", name="event", path="/img/Activity/vip/event.jpg")
        )
        db.session.add(
            Activity(
                cat="vip", name="luxury car", path="/img/Activity/vip/luxurycar.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="vip", name="luxury house", path="/img/Activity/vip/luxuryhouse.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="vip",
                name="private helicopter",
                path="/img/Activity/vip/privatehelicopter.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="vip", name="private jet", path="/img/Activity/vip/privatejet.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="vip", name="V.I.P Table", path="/img/Activity/vip/viptable.jpg"
            )
        )
        db.session.add(
            Activity(cat="vip", name="yacht", path="/img/Activity/vip/yacht.jpg")
        )

        # Add ticket activites
        db.session.add(
            Activity(
                cat="ticket",
                name="circus tickets",
                path="/img/Activity/ticket/circus.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="ticket",
                name="concert tickets",
                path="/img/Activity/ticket/concert.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="ticket",
                name="opera tickets",
                path="/img/Activity/ticket/opera.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="ticket",
                name="sports tickets",
                path="/img/Activity/ticket/sports.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="ticket",
                name="theater tickets",
                path="/img/Activity/ticket/theater.jpg",
            )
        )

        # Add outdoor activities
        db.session.add(
            Activity(
                cat="outdoor",
                name="american football",
                path="/img/Activity/outdoor/americanfootball.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="outdoor",
                name="baseball",
                path="/img/Activity/outdoor/baseball.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="outdoor",
                name="beach volleyball",
                path="/img/Activity/outdoor/beachvolleyball.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="outdoor", name="bus tour", path="/img/Activity/outdoor/bustour.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="outdoor",
                name="cheerleading",
                path="/img/Activity/outdoor/cheerleading.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="outdoor", name="cricket", path="/img/Activity/outdoor/cricket.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="outdoor", name="croquet", path="/img/Activity/outdoor/croquet.jpg"
            )
        )
        db.session.add(
            Activity(cat="outdoor", name="golf", path="/img/Activity/outdoor/golf.jpg")
        )
        db.session.add(
            Activity(
                cat="outdoor", name="guide", path="/img/Activity/outdoor/guide.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="outdoor",
                name="land sailing",
                path="/img/Activity/outdoor/landsailing.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="outdoor", name="soccer", path="/img/Activity/outdoor/soccer.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="outdoor",
                name="softball",
                path="/img/Activity/outdoor/softball.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="outdoor",
                name="street hockey",
                path="/img/Activity/outdoor/streethockey.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="outdoor", name="tennis", path="/img/Activity/outdoor/tennis.jpg"
            )
        )
        db.session.add(
            Activity(cat="outdoor", name="yoga", path="/img/Activity/outdoor/yoga.jpg")
        )
        db.session.add(
            Activity(
                cat="outdoor",
                name="ziplining",
                path="/img/Activity/outdoor/ziplining.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="outdoor", name="zorbing", path="/img/Activity/outdoor/zorbing.jpg"
            )
        )

        # Add indoor activites
        db.session.add(
            Activity(
                cat="indoor", name="aerobics", path="/img/Activity/indoor/aerobics.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="aikido", path="/img/Activity/indoor/aikido.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="badminton",
                path="/img/Activity/indoor/badminton.jpg",
            )
        )
        db.session.add(
            Activity(cat="indoor", name="bandy", path="/img/Activity/indoor/bandy.jpg")
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="basketball",
                path="/img/Activity/indoor/basketball.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="bowling", path="/img/Activity/indoor/bowling.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="boxing", path="/img/Activity/indoor/boxing.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="coaching", path="/img/Activity/indoor/coaching.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="cooking classes",
                path="/img/Activity/indoor/cooking.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="crossfit", path="/img/Activity/indoor/crossfit.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="curling", path="/img/Activity/indoor/curling.jpg"
            )
        )
        db.session.add(
            Activity(cat="indoor", name="dj", path="/img/Activity/indoor/dj.jpg")
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="dodgeball",
                path="/img/Activity/indoor/dodgeball.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="fencing", path="/img/Activity/indoor/fencing.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="fight cage",
                path="/img/Activity/indoor/fightcage.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="fitness", path="/img/Activity/indoor/fitness.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="foam pit", path="/img/Activity/indoor/foampit.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="handball", path="/img/Activity/indoor/handball.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="ice hockey",
                path="/img/Activity/indoor/icehockey.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="ice skating",
                path="/img/Activity/indoor/iceskating.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="indoor climbing",
                path="/img/Activity/indoor/indoorclimbing.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="jorkyball",
                path="/img/Activity/indoor/jorkyball.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="karaoke", path="/img/Activity/indoor/karaoke.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="kickboxing",
                path="/img/Activity/indoor/kickboxing.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="massage", path="/img/Activity/indoor/massage.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="mechanic bull",
                path="/img/Activity/indoor/mechanicbull.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="music lessons",
                path="/img/Activity/indoor/music.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="photo shooting",
                path="/img/Activity/indoor/photoshooting.jpg",
            )
        )
        db.session.add(
            Activity(cat="indoor", name="poker", path="/img/Activity/indoor/poker.jpg")
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="pole dance",
                path="/img/Activity/indoor/poledance.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="pool table",
                path="/img/Activity/indoor/pooltable.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="roller derby",
                path="/img/Activity/indoor/rollerderby.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="simulator",
                path="/img/Activity/indoor/simulator.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="squash", path="/img/Activity/indoor/squash.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="striptease",
                path="/img/Activity/indoor/striptease.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor", name="tennis", path="/img/Activity/indoor/tennis.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="trampoline",
                path="/img/Activity/indoor/trampoline.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="volleyball",
                path="/img/Activity/indoor/volleyball.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="indoor",
                name="wind tunnel",
                path="/img/Activity/indoor/windtunnel.jpg",
            )
        )

        # Add mountain activities
        db.session.add(
            Activity(
                cat="mountain",
                name="bobsled",
                path="/img/Activity/mountain/bobsled.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="cross-country skiing",
                path="/img/Activity/mountain/crosscountryskiing.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="dogsled",
                path="/img/Activity/mountain/dogsled.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="horsesled",
                path="/img/Activity/mountain/horsesled.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain", name="igloo", path="/img/Activity/mountain/igloo.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="mountain bike",
                path="/img/Activity/mountain/mountainbike.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="rock climbing",
                path="/img/Activity/mountain/rockclimbing.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="scooter bike",
                path="/img/Activity/mountain/scooterbike.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain", name="ski", path="/img/Activity/mountain/skiing.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="skijoring",
                path="/img/Activity/mountain/skijore.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="snowbike",
                path="/img/Activity/mountain/snowbike.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="snowboard",
                path="/img/Activity/mountain/snowboard.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="snowkite",
                path="/img/Activity/mountain/snowkite.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="snowmobile",
                path="/img/Activity/mountain/snowmobile.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="snowshoes",
                path="/img/Activity/mountain/snowshoes.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="mountain",
                name="speedskiing",
                path="/img/Activity/mountain/speedskiing.jpg",
            )
        )

        # Add shooting activities
        db.session.add(
            Activity(
                cat="shooting",
                name="airsoft",
                path="/img/Activity/shooting/airsoft.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="shooting",
                name="archery",
                path="/img/Activity/shooting/archery.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="shooting",
                name="clay target",
                path="/img/Activity/shooting/claytarget.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="shooting",
                name="foxhunting",
                path="/img/Activity/shooting/foxhunting.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="shooting",
                name="gunshoot",
                path="/img/Activity/shooting/gunshoot.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="shooting",
                name="hunting",
                path="/img/Activity/shooting/hunting.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="shooting",
                name="laser games",
                path="/img/Activity/shooting/lasergames.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="shooting",
                name="paintball",
                path="/img/Activity/shooting/paintball.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="shooting", name="rifle", path="/img/Activity/shooting/rifle.jpg"
            )
        )

        # Add wheel activities
        db.session.add(
            Activity(
                cat="wheel", name="bicycle", path="/img/Activity/wheel/bicycle.jpg"
            )
        )
        db.session.add(
            Activity(cat="wheel", name="BMX", path="/img/Activity/wheel/bmx.jpg")
        )
        db.session.add(
            Activity(
                cat="wheel",
                name="electric skateboard",
                path="/img/Activity/wheel/electricskateboard.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="wheel", name="golf car", path="/img/Activity/wheel/golfcar.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="wheel", name="minicar", path="/img/Activity/wheel/minicar.jpg"
            )
        )
        db.session.add(
            Activity(cat="wheel", name="roller", path="/img/Activity/wheel/roller.jpg")
        )
        db.session.add(
            Activity(cat="wheel", name="segway", path="/img/Activity/wheel/segway.jpg")
        )

        # Add water activities
        db.session.add(
            Activity(cat="water", name="boat", path="/img/Activity/water/boat.jpg")
        )
        db.session.add(
            Activity(
                cat="water",
                name="exotic boat",
                path="/img/Activity/water/exoticboat.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water", name="gondolas", path="/img/Activity/water/gondolas.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="water", name="jet ski", path="/img/Activity/water/jetskiing.jpg"
            )
        )
        db.session.add(
            Activity(cat="water", name="kayak", path="/img/Activity/water/kayak.jpg")
        )
        db.session.add(
            Activity(
                cat="water",
                name="kite surf",
                path="/img/Activity/water/kitesurfing.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="outrigger canoes",
                path="/img/Activity/water/outriggercanoes.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="paddle board",
                path="/img/Activity/water/paddleboarding.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="parasailing",
                path="/img/Activity/water/parasailing.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water", name="pirogue", path="/img/Activity/water/pirogue.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="water", name="rafting", path="/img/Activity/water/rafting.jpg"
            )
        )
        db.session.add(
            Activity(cat="water", name="rowing", path="/img/Activity/water/rowing.jpg")
        )
        db.session.add(
            Activity(
                cat="water", name="sailing", path="/img/Activity/water/sailing.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="scubadiving",
                path="/img/Activity/water/scubadiving.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="sea breacher",
                path="/img/Activity/water/seabreacher.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water", name="shark cage", path="/img/Activity/water/sharkcage.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="snorkeling",
                path="/img/Activity/water/snorkeling.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="spear fishing",
                path="/img/Activity/water/spearfishing.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water", name="submarine", path="/img/Activity/water/submarine.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="water", name="surfing", path="/img/Activity/water/surfing.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="swim dolphins",
                path="/img/Activity/water/swimdolphins.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water", name="thai boat", path="/img/Activity/water/thaiboat.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="trampoline water",
                path="/img/Activity/water/trampolinewater.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="underwater photo",
                path="/img/Activity/water/underwaterphoto.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="underwater scooter",
                path="/img/Activity/water/underwaterscooter.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="wakeboarding",
                path="/img/Activity/water/wakeboarding.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="water aerobic",
                path="/img/Activity/water/wateraerobic.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="water basketball",
                path="/img/Activity/water/waterbasketball.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="water jetpack",
                path="/img/Activity/water/waterjetpack.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water", name="water jump", path="/img/Activity/water/waterjump.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="water", name="water polo", path="/img/Activity/water/waterpolo.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="water",
                name="water ski",
                path="/img/Activity/water/waterskiing.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="water", name="windsurf", path="/img/Activity/water/windsurfing.jpg"
            )
        )

        # Add air activities
        db.session.add(
            Activity(
                cat="air",
                name="acrobatic airplane",
                path="/img/Activity/air/acrobaticairplane.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="air",
                name="aeromodelisme",
                path="/img/Activity/air/aeromodelisme.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="air", name="aeroplane", path="/img/Activity/air/aeroplane.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="air",
                name="aeroplane banner",
                path="/img/Activity/air/aeroplanebanner.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="air", name="ballooning.jpg", path="/img/Activity/air/ballooning"
            )
        )
        db.session.add(
            Activity(
                cat="air", name="base jumping", path="/img/Activity/air/basejumping.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="air",
                name="bungee jumping",
                path="/img/Activity/air/bungeejumping.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="air",
                name="fighter plane",
                path="/img/Activity/air/fighterplnae.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="air", name="hang gliding", path="/img/Activity/air/hanggliding.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="air", name="helicopter", path="/img/Activity/air/helicopter.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="air", name="paragliding", path="/img/Activity/air/paragliding.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="air", name="paramotor", path="/img/Activity/air/paramotor.jpg"
            )
        )
        db.session.add(
            Activity(cat="air", name="plane", path="/img/Activity/air/plane.jpg")
        )
        db.session.add(
            Activity(
                cat="air", name="skydiving", path="/img/Activity/air/skydiving.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="air",
                name="space shuttle",
                path="/img/Activity/air/spaceshuttle.jpg",
            )
        )
        db.session.add(
            Activity(cat="air", name="wing suit", path="/img/Activity/air/wingsuit.jpg")
        )

        # Add animal acitivies
        db.session.add(
            Activity(
                cat="animal",
                name="dog racing",
                path="/img/Activity/animal/dogracing.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="animal", name="dogsled", path="/img/Activity/animal/dogsled.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="animal",
                name="elephant polo",
                path="/img/Activity/animal/elephantpolo.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="animal",
                name="horse polo",
                path="/img/Activity/animal/horsepolo.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="animal", name="horse ski", path="/img/Activity/animal/horseski.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="animal",
                name="horsesled",
                path="/img/Activity/animal/horsesled.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="animal",
                name="riding camel",
                path="/img/Activity/animal/ridingcamel.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="animal",
                name="riding elephant",
                path="/img/Activity/animal/ridingelephant.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="animal",
                name="riding horse",
                path="/img/Activity/animal/ridinghorse.jpg",
            )
        )
        db.session.add(
            Activity(cat="animal", name="rodeo", path="/img/Activity/animal/rodeo.jpg")
        )
        db.session.add(
            Activity(
                cat="animal",
                name="shark cage",
                path="/img/Activity/animal/sharkcage.jpg",
            )
        )
        db.session.add(
            Activity(
                cat="animal",
                name="swim dolphins",
                path="/img/Activity/animal/swimdolphins.jpg",
            )
        )

        # Add motor activities
        db.session.add(
            Activity(cat="motor", name="4x4", path="/img/Activity/motor/4x4.jpg")
        )
        db.session.add(
            Activity(cat="motor", name="A.T.V", path="/img/Activity/motor/atv.jpg")
        )
        db.session.add(
            Activity(cat="motor", name="buggy", path="/img/Activity/motor/buggy.jpg")
        )
        db.session.add(
            Activity(cat="motor", name="desert", path="/img/Activity/motor/desert.jpg")
        )
        db.session.add(
            Activity(cat="motor", name="drift", path="/img/Activity/motor/drift.jpg")
        )
        db.session.add(
            Activity(
                cat="motor", name="formula 1", path="/img/Activity/motor/formula1.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="motor", name="ice-racing", path="/img/Activity/motor/iceracing.jpg"
            )
        )
        db.session.add(
            Activity(cat="motor", name="kart", path="/img/Activity/motor/kart.jpg")
        )
        db.session.add(
            Activity(
                cat="motor",
                name="locomotive",
                path="/img/Activity/motor/locomotive.jpg",
            )
        )
        db.session.add(
            Activity(cat="motor", name="moto", path="/img/Activity/motor/moto.jpg")
        )
        db.session.add(
            Activity(
                cat="motor", name="motocross", path="/img/Activity/motor/motocross.jpg"
            )
        )
        db.session.add(
            Activity(cat="motor", name="rallye", path="/img/Activity/motor/rallye.jpg")
        )
        db.session.add(
            Activity(
                cat="motor", name="scooter", path="/img/Activity/motor/scooter.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="motor", name="sidecar", path="/img/Activity/motor/sidecar.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="motor", name="sportive", path="/img/Activity/motor/sportive.jpg"
            )
        )
        db.session.add(
            Activity(
                cat="motor",
                name="sportive-car",
                path="/img/Activity/motor/sportivecar.jpg",
            )
        )
        db.session.add(
            Activity(cat="motor", name="tuk-tuk", path="/img/Activity/motor/tuktuk.jpg")
        )

        db.session.commit()
        return "Successfully Added", 200
