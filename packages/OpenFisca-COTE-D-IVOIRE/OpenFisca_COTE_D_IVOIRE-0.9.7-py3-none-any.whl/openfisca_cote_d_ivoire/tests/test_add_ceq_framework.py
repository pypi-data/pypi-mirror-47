# -*- coding: utf-8 -*-


import logging
import sys


from openfisca_ceq.tools import add_ceq_framework
from openfisca_cote_d_ivoire import CountryTaxBenefitSystem as CoteDIvoireTaxBenefitSystem
from openfisca_cote_d_ivoire.survey_scenarios import CoteDIvoireSurveyScenario
from openfisca_cote_d_ivoire.tests.test_survey_scenario_from_stata_data import (
    data_is_available,
    create_data_from_stata,
    )


log = logging.getLogger(__name__)


def test_add_ceq_framework_to_cote_d_ivoire():
    tax_benefit_system = CoteDIvoireTaxBenefitSystem()
    ceq_enhanced_tax_benefit_system = add_ceq_framework(tax_benefit_system)
    if not data_is_available:
        return
    data = create_data_from_stata()
    survey_scenario = CoteDIvoireSurveyScenario(
        tax_benefit_system = ceq_enhanced_tax_benefit_system,
        data = data,
        year = 2017,
        )
    log.info(survey_scenario.calculate_variable('impots_directs', period = 2017)[0:10])
    log.info(survey_scenario.calculate_variable('impot_general_revenu', period = 2017)[0:10])
    log.info(survey_scenario.calculate_variable('personal_income_tax', period = 2017).sum())
    log.info(survey_scenario.compute_aggregate('personal_income_tax', period = 2017))
    return survey_scenario


if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    test_add_ceq_framework_to_cote_d_ivoire()
