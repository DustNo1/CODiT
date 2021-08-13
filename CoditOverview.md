#  Covid Opensource Digital Twin project (CODiT)

#### Creating provisional code to model a community's response to the Covid-19 epidemic



## Overview

An outbreak is simulated by defining a disease, a type of society, and a population of individuals. We will examine these respective models of disease, society, population, and outbreak in turn.


## Disease Model

There is a generic `Disease` model that is defined by only two variables: the duration of time (measured in days) that it is infectious, and the probability of its transmission upon contact between an infected and an uninfected individual.

The `Covid` model is a subclass of the `Disease` model, which includes four other variables: The duration of the incubation period before it becomes infectious, the duration between infection and the appearance of symptoms, the duration between symptoms appearing and the end of infection, and the probability that a given infected individual develops actionable symptoms.

Here is a summary of these values as they are currently defined. These can all be easily adjusted as findings are updated or new strains become prevalent.


* Duration from transmission to onset of infectious period: 4 days
* Duration from onset of infectious period to onset of symptomatic stage: 2 days
* Duration from onset of symptomatic stage to end of infectious period: 5 days
* Duration of infectious period (sum of the two above): 7 days
* Probability of infected person developing actionable symptoms: 60%
* Probability of transmission from infected to non-infected person during contact:
  * SARS-CoV-2: 2.5%
  * B.1.1.7: 3.9%
  * B.1.617.2: 5.46%


By default, it is assumed that the symptomatic stage and the infectious stage end at the same time; that is, when you stop showing symptoms, you stop being infectious. However, there is an option to specify a different duration for the symptomatic stage if this is not the case.




## Society Model

A `Society` object is essentially a set of rules that govern the methods by which individuals are isolated and/or tested during an outbreak. A `Society` is distinct from the actual set of interactive individuals who participate in the society; see the next section on Population.

A simple example of a `Society` is the subclass `DraconianSociety`. This type of society performs no testing, and simply forces all symptomatic individuals to isolate.

A defining factor of most `Society` subclasses is the manner of testing for infection of a disease. A `Test` is an object that models a test taken by an individual to see whether they are infectious. It takes a certain number of days to obtain a result. Each `Test` keeps track of its own set of properties, including the time since the test was submitted, the result of a completed test, and which individual the test was for. By default, a `Test` provides perfect results, giving no false positives or false negatives. There is also a `LateralFlowTest` object, a subclass of `Test`, which can produce such false responses. It is currently defined as having 76.8% sensitivity and 99.68% specificity.

A `TestQueue` is an object that essentially contains a list of Covid tests that have been submitted for analysis. The `TestQueue` has various methods that allow for adding and removing tests, checking whether an individual already has a test submitted in the queue, and updating the status of the tests it contains. There are options for allowing certain tests to move to the front of the queue, and for specifying a maximum number of tests that can be processed per day.

For our current modelling, we focus on a `TwoTrackTester` type of society. As a subclass of `TestingSociety`, it has the ability to add, remove, and process tests for infection. As a subclass of `TestingTracingSociety`, it can test and/or isolate contacts of infected individuals. As a subclass of the `UKSociety` model, it has a finite capacity for processing daily tests. Finally, the `TwoTrackTester` class gets its name by having two separate `TestQueue` objects, one higher priority than the other.

`LateralFlowUK`

## Population Model

In order to run a simulation of an outbreak, we need a model for the population that is exposed to an outbreak of a disease. (Again, this population model is the actual set of individuals that will be interacting within a simulation, and is technically distinct from a `Society` as discussed above, which is the set of testing rules that govern a population.)

A `Person` is a model of an individual within a population. This model includes properties like the home they are associated with, as well as disease-related characteristics including whether they are isolating, whether they are infectious, and which vaccinations they have. It has the ability to change the status for isolation, infectiousness, and vaccination, and can potentially infect another `Person` it contacts.

A subclass `PersonCovid` has additional methods that handle the progression of a disease when infected, and the reaction to test results. The disease progression can move from non-infectious, to infectious, to infectious and symptomatic, and finally to recovered. This `PersonCovid` model also has a probability of isolating and/or getting tested when they become symptomatic, and a probability of isolating when receiving a positive test.

A `Population` object is a set of individuals (i.e., `Person` objects or a subclass like `PersonCovid`). The `Population` has a `census` variable that is a list of all members of that population in a format that’s easy for other methods to process. A `Population` has the ability to form groupings of its individuals (random groupings by default), and simulate a disease potentially spreading from an infected member of the group. The `Population` has the ability to keep track of which members have been infected, the number of infected, and the initial seeding of infected members of the population.

A `FixedNetworkPopulation` is a more advanced subclass of `Population`. It defines a fixed set of cliques among individuals at the outset, and then derives the fixed set of contacts for each individual in the population. These cliques are thereafter used as the groupings in which an infection may spread.

There are more advanced population models that are also very useful for more complex simulations. In particular, the `City` model includes the creation of multiple types of buildings in which individuals interact for various reasons. These include households, workplaces, classrooms, and care homes. Members of the population can be assigned to interact within these buildings based on age range, for example. These contacts are in addition to random ephemeral contact between individuals unrelated to these locations.


## Outbreak Model

An `Outbreak` is primarily defined by a type of society and a type of disease, as it will model how they interact. A given instance of an `Outbreak` also depends on the population of individuals it can spread through, which is defined by a few additional parameters. These parameters are customisable, but their defaults are as follows:

* Size of population: 5000
* Number of individuals initially infected: 50
* Duration of simulation: 150 days

When an `Outbreak` is initiated, a population is created with the properties specified by the above parameters. After this, the `Outbreak` simulation is begun. A series of time-steps is undergone, based on the specified number of days and events per day. At each time-step, the society “manages” the outbreak, the infection has a chance to spread among groups of individuals, and the current state of the outbreak is recorded.


