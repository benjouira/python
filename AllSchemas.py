from flask_marshmallow import Marshmallow

ma= Marshmallow()
class JobSchema(ma.Schema):
    class Meta:
        fields = ("_class", "description", "displayName","name","url","builds")
        
        
        
        
        
        
