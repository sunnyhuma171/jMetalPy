import logging
from queue import Queue
from typing import TypeVar

from jmetalpy.core.population import Population
from jmetalpy.core.evaluator import Evaluator

S = TypeVar('S')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Sequential(Evaluator):

    def __init__(self):
        super(Sequential, self).__init__()
        self.buffer = Queue()

    def update(self, *args, **kwargs):
        logger.info("SEQUENTIAL_EVALUATION update invoked")
        population = kwargs["POPULATION"]

        try:
            self.buffer.put(population)
        except Exception as ex:
            print("SEQUENTIAL EVALUATION buffer ex: " + str(ex))

    def apply(self, population: Population):
        problem = population.problem
        if not population.is_terminated:

            logger.info("SEQUENTIAL_EVALUATION: APPLY invoked")

            if population.mating_pool is None:
                for solution in population:
                    Evaluator.evaluate_solution(solution, problem)
                logger.info("SequentialEvaluation: POPULATION EVALUATED")
            else:
                for solution in population.mating_pool:
                    Evaluator.evaluate_solution(solution, problem)
                logger.info("SequentialEvaluation: OFFSPRING POPULATION EVALUATED")

            population.evaluations = population.evaluations + len(population)
            logger.info("SEQUENTIAL EVALUATION: " + str(population.evaluations))

        observable_data = {'POPULATION': population}
        self.notify_all(**observable_data)

    def run(self):
        logger.info("SEQUENTIAL EVALUATION OBSERVER: RUN")

        try:
            while True:
                population = self.buffer.get()
                logger.info("SEQUENTIAL EVALUATION OBSERVER: GET READY")
                self.apply(population)

                if population.is_terminated:
                    break
        except Exception as ex:
            print("SEQUENTIAL EVALUATION ex: " + str(ex))

        logger.info("SEQUENTIAL EVALUATION OBSERVER: END RUN")
