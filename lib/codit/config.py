import os

from codit import share_dir

DATA_PATH = os.path.join(share_dir(), 'codit', 'data')
POPULATION_LSOA_CSV = os.path.join(DATA_PATH, 'city', 'population', 'sample_lsoa_population.csv.gz')


class CFG:

    # Disease:
    DEFAULT_COVID = "SARS-CoV-2"
    _TARGET_R0 = 1.4  # before Test and Trace and Isolation

    DAYS_BEFORE_INFECTIOUS = 4   # t0
    DAYS_INFECTIOUS_TO_SYMPTOMS = 2         # t1
    DAYS_OF_SYMPTOMS = 5         # t2
    PROB_SYMPTOMATIC = 0.6       # pS  probability that an infected person develops actionable symptoms

    # Person:
    PROB_ISOLATE_IF_SYMPTOMS = 0.75   # pIsolSimpt
    PROB_ISOLATE_IF_TRACED = 0.3      #
    PROB_ISOLATE_IF_TESTPOS = 0.3      #
    PROB_GET_TEST_IF_TRACED = 0.75     #
    PROB_APPLY_FOR_TEST_IF_SYMPTOMS = 0.75   # pA
    DURATION_OF_ISOLATION = 10   #tIsol

    # Society:
    PROB_INFECT_IF_TOGETHER_ON_A_DAY = {'SARS-CoV-2': 0.025, 'B.1.1.7': 0.039, 'B.1.617.2': 0.039 * 1.4}
    #  Tom Wenseleers: could be 60% more transmissible

    X_IMMUNITY = 1.   # more realistic to put this down to 0.8



    # this is a moving target - because depends on hand-washing, masks ...
    # 'B.1.1.7' 56% more infectious than initial strain
    PROB_NON_C19_SYMPTOMS_PER_DAY = 0.01  # like b - probability someone unnecessarily requests a test on a given day
    PROB_TEST_IF_REQUESTED = 1            # pG   # set to 1 ... however, see the next parameter ... with capacity idea
    DAILY_TEST_CAPACITY_PER_HEAD = 0.0075  # being very generous here ... this is probably more like 0.005
    TEST_DAYS_ELAPSED = 1                 # like pR  # time to get result to the index in an ideal world with no backlog
    # DAYS_GETTING_TO_CONTACTS = 1       # tricky to implement, leaving for now
    PROB_TRACING_GIVEN_CONTACT = 0.8 * 0.75       # pT

    # Simulator
    SIMULATOR_PERIODS_PER_DAY = 1

    MEAN_NETWORK_SIZE = 1 +_TARGET_R0 / (DAYS_INFECTIOUS_TO_SYMPTOMS + DAYS_OF_SYMPTOMS) / \
                        PROB_INFECT_IF_TOGETHER_ON_A_DAY['SARS-CoV-2']
    # the above formula, and the _TARGET_R0 concept, assumes that all people have identical network size

    _PROPORTION_OF_INFECTED_WHO_GET_TESTED = PROB_SYMPTOMATIC * \
                                             PROB_APPLY_FOR_TEST_IF_SYMPTOMS * \
                                             PROB_TEST_IF_REQUESTED   # should be 0.205
    
    @property
    def __X_IMMUNITIES(self):
        return {'SARS-CoV-2': self.X_IMMUNITY,
                    'B.1.1.7': self.X_IMMUNITY,
                    'B.1.617.2': self.X_IMMUNITY ** 2}

    @property
    def CROSS_IMMUNITY(self): 
        return {'other': {'other': 1.},
                      'SARS-CoV-2': self.__X_IMMUNITIES,
                      'B.1.1.7': self.__X_IMMUNITIES,
                      'B.1.617.2': {'SARS-CoV-2': self.X_IMMUNITY ** 2,
                                    'B.1.1.7': self.X_IMMUNITY ** 2,
                                    'B.1.617.2': self.X_IMMUNITY}}
    # https://www.gov.uk/government/news/past-covid-19-infection-provides-some-immunity-but-people-may-still-carry-and-transmit-virus
    
    @property
    def VACCINATION_IMMUNITY(self):
        return {'AstraZeneca': self.__X_IMMUNITIES,
                            'Pfizer': self.__X_IMMUNITIES,
                            'Moderna': self.__X_IMMUNITIES}
    # https://www.who.int/emergencies/diseases/novel-coronavirus-2019/covid-19-vaccines
    # https://www.gov.uk/government/news/one-dose-of-covid-19-vaccine-can-cut-household-transmission-by-up-to-half
    # https://twitter.com/JamesWard73/status/1388524356490440708

    @property
    def MULTI_VACCINATION_IMMUNITY(self):
        # Placeholder numbers until more reliable numbers can be found
        return {'AstraZeneca': [.8, .9, .95],
                'Pfizer': [.8, .9, .95],
                'Moderna': [.8, .9, .95]}




def set_config(obj, conf):
    obj.cfg = CFG()
    if conf is not None:
        extra_params = (conf.keys() - set(dir(obj.cfg)))
        if len(extra_params) > 0:
            raise AttributeError(f"unrecognised parameter overrides: {extra_params}")
    obj.cfg.__dict__.update(conf or {})


def print_baseline_config():
    cfg = CFG()
    for param in dir(cfg):
        if not param.startswith("__"):
            print(param, getattr(cfg, param))
