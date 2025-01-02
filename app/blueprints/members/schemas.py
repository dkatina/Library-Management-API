from app.models import Member
from app.extensions import ma

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
login_schema = MemberSchema(exclude=['name', 'DOB'])