from coroutineworld.entity import EntityDefinition, Animate

definitions = [

    # HUMAN

    EntityDefinition(
        name='Mary',
        categories=['HUMAN'],
        cls=Animate,
    ),

    EntityDefinition(
        name='John',
        categories=['HUMAN'],
        cls=Animate,
    ),


    # HERBIVORE

    EntityDefinition(
        name='squirrel',
        categories=['HERBIVORE'],
        cls=Animate,
    ),
]
