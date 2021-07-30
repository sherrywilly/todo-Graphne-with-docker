
from graphene.types.mutation import Mutation
from .models import Todo
from graphene_django import DjangoObjectType,DjangoListField
import graphene

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = ('id','name',)


class Query(graphene.ObjectType):
    all_todos = DjangoListField(TodoType)
    get_todo_by_id = graphene.Field(TodoType,id = graphene.Int())

    def resolve_all_todos(root,info):
        return Todo.objects.all()

    def resolve_get_todo_by_id (root,info,id):
        return Todo.objects.get(id=id)

class TodoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name= graphene.String(required=True)

    todo = graphene.Field(TodoType)

    @classmethod
    def mutate(cls,root,info,name,id=None):
        if id is not None:
            todo =Todo.objects.get(pk=id)
        else:
            todo = Todo()
        todo.name=name
        todo.save()
        return TodoMutation(todo=todo)
class Mutation(graphene.ObjectType):
    create_or_update_todo = TodoMutation.Field()
schema = graphene.Schema(query=Query,mutation=Mutation)