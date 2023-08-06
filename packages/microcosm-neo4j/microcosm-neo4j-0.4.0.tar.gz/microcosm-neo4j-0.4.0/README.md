# microcosm-neo4j

Opinionated persistence with Neo4J.


## Testing

Unit-tests require a running Neo4j instance. To run locally, can use the included Docker compose files:

    $ docker-compose up
    $ nosetests

As of the time of this writing, we test against Neo4J 3.5.5, which is the same version we use on our live environments via GrapheneDB. Always check the Dockerfile for the version of neo4j server we're using if you suspect version incompatability issues when running unit-tests.
