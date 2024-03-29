from app import db


# database table class for plant_information
class PlantDatabase(db.Model):
    __tablename__ = 'plant_information'
    plant_id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String)
    image_link = db.Column(db.String)
    variety_names = db.Column(db.String)
    alt_names = db.Column(db.String)
    family_name = db.Column(db.String)
    plant_type = db.Column(db.String)
    pref_season = db.Column(db.String)
    pref_season_num1 = db.Column(db.Integer)
    pref_season_num2 = db.Column(db.Integer)
    life_cycle = db.Column(db.String)
    hardiness_zone = db.Column(db.String)
    sun_exposure = db.Column(db.String)
    water_needs = db.Column(db.String)
    maint_needs = db.Column(db.String)
    soil_type = db.Column(db.String)
    soil_ph = db.Column(db.String)
    soil_drain = db.Column(db.String)
    start_type = db.Column(db.String)
    spacing_needs = db.Column(db.String)
    grow_time_maturity = db.Column(db.String)
    harvest_recommendations = db.Column(db.String)
    pref_nutrients = db.Column(db.String)
    companion_plants = db.Column(db.String)
    avoid_with = db.Column(db.String)
    crop_rotate = db.Column(db.String)
    instructions = db.Column(db.String)
    uses = db.Column(db.String)
    general_info = db.Column(db.String)
    preservation_ideas = db.Column(db.String)

    def __init__(self, plant_id, plant_name, image_link, variety_names, alt_names, family_name, plant_type,
                 pref_season, pref_season_num1, pref_season_num2, life_cycle, hardiness_zone,
                 sun_exposure, water_needs, maint_needs,
                 soil_ph, soil_drain, start_type, spacing_needs, grow_time_maturity,
                 harvest_recommendations, pref_nutrients, companion_plants,
                 avoid_with, crop_rotate, instructions, uses, general_info, preservation_ideas):

        self.plant_id = plant_id
        self.plant_type = plant_name
        self.image_link = image_link
        self.variety_names = variety_names
        self.alt_names = alt_names
        self.family_name = family_name
        self.plant_type = plant_type
        self.pref_season = pref_season
        self.pref_season_num1 = pref_season_num1
        self.pref_season_num2 = pref_season_num2
        self.life_cycle = life_cycle
        self.hardiness_zone = hardiness_zone
        self.sun_exposure = sun_exposure
        self.water_needs = water_needs
        self.maint_needs = maint_needs
        self.soil_ph = soil_ph
        self.soil_drain = soil_drain
        self.start_type = start_type
        self.spacing_needs = spacing_needs
        self.grow_time_maturity = grow_time_maturity
        self.harvest_recommendations = harvest_recommendations
        self.pref_nutrients = pref_nutrients
        self.companion_plants = companion_plants
        self.avoid_with = avoid_with
        self.crop_rotate = crop_rotate
        self.instructions = instructions
        self.uses = uses
        self.general_info = general_info
        self.preservation_ideas = preservation_ideas


