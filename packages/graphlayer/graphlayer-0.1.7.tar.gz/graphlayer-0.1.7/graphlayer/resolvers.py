from . import core, iterables


def create_object_builder(object_query):
    field_resolvers = {}

    def create_object(value):
        return object_query.create_object(iterables.to_dict(
            (field_query.key, field_resolvers[field_query.key](value))
            for field_query in object_query.field_queries
        ))

    def field_resolver(field):
        def add_field_resolver(build_field_resolver):
            for field_query in object_query.field_queries:
                if field_query.field == field or field_query.field.name == field:
                    field_resolvers[field_query.key] = build_field_resolver(field_query)

            return build_field_resolver

        return add_field_resolver

    create_object.field = field_resolver

    def getter(field):
        def add_field_resolver(resolve_field):
            return field_resolver(field)(lambda field_query: resolve_field)

        return add_field_resolver

    create_object.getter = getter

    return create_object


def constant_object_resolver(type, values):
    @core.resolver(type)
    def resolve(graph, query):
        return query.create_object(iterables.to_dict(
            (field_query.key, values[field_query.field.name])
            for field_query in query.field_queries
        ))

    return resolve


def root_object_resolver(type):
    field_handlers = {}

    @core.resolver(type)
    @core.dependencies(injector=core.Injector)
    def resolve_root(graph, query, *, injector):
        def resolve_field(field_query):
            field_resolver = field_handlers[field_query.field]
            return injector.call_with_dependencies(field_resolver, graph, field_query.type_query, field_query.args)

        return query.create_object(iterables.to_dict(
            (field_query.key, resolve_field(field_query))
            for field_query in query.field_queries
        ))

    def field(field):
        def add_handler(handle):
            field_handlers[field] = handle
            return handle

        return add_handler

    resolve_root.field = field

    return resolve_root
