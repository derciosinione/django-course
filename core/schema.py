from django.db.models.fields import Field
import graphene
from graphene_django import DjangoObjectType

from app.models import Friends, User


class FriendsType(DjangoObjectType):
  class Meta:
    model = Friends
    fields = '__all__'


class UserType(DjangoObjectType):
  class Meta:
    model = User
    exclude = ('password',)


class Query(graphene.ObjectType):
  hello = graphene.String(default_value='Hi!')
  all_friends = graphene.List(FriendsType)

  user = graphene.Field(UserType, id=graphene.ID(required=False), username=graphene.String(required=False))
  all_users = graphene.List(UserType)

  def resolve_all_friends(self, info):
    return Friends.objects.all()

  def resolve_user(self, info, id=None, username=None):
    if id:
      return User.objects.get(pk=id)
    elif username:
      return User.objects.get(username=username)


  def resolve_all_users(self, info):
    return User.objects.all()


class AddFriendMutation(graphene.Mutation):
  data = graphene.Field(FriendsType)

  class Arguments:
    name = graphene.String()
    age = graphene.ID()
    email = graphene.String()
    userid = graphene.ID()

  def mutate(self, info, name, age, email, userid):
    user = User.objects.get(id=userid)
    friend = Friends(name=name, age=age, email=email, userid=user)
    friend.save()
    return AddFriendMutation(data=friend)



class Mutation(graphene.ObjectType):
  add_friend = AddFriendMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)