from datetime import datetime, timedelta
from random import randint
import math
import string


capacity_drivers = {'pct_pts_narratives': 0.0, 'phase': 'Phase IV', 'MW-sourcing': 'Outsourced Function Paid', 'DM-sourcing': 'Outsourced', 'BIOS-sourcing': 'Outsourced', 'SP-sourcing': 'Outsourced', 'TM-sourcing': 'Supported', 'ClinDev-sourcing': 'Inhouse', 'GMO-sourcing': 'In House', 'MW-complexity': '1 Very Low', 'DM-complexity': '1 Very Low', 'LDM-complexity': '1 Very Low', 'DBP-complexity': '1 Very Low', 'BIOS-complexity': '1 Very Low', 'TS-complexity': '1 Very Low', 'SP-complexity': '2 Low', 'TM-complexity': '1 Very Low', 'GTD-complexity': '1 Very Low', 'GTM-complexity': '1 Very Low', 'ClinDev-complexity': '2 Low', 'CDMD-complexity': '2 Low', 'CDD-complexity': '2 Low', 'CSE-complexity': '2 Low', 'GMO-complexity': '2 Low', 'CRA-complexity': '2 Low', 'CSM-complexity': '2 Low', 'SUP-complexity': '2 Low', 'MGMT-complexity': '2 Low', 'GCS-complexity': ' ', 'data-standards': 'NCDS_2', 'healthy_patients_volunteers': 'Patients', 'clinical_comparator_study': 'No', 'clinical_combination_study': 'No', 'collab_coop_group_trial': ' ', 'new_indication': ' ', 'no_of_patients': 50, 'no_of_countries': 1, 'no_of_sites': 1, 'no_of_ias': 0, 'no_of_dmcs': 3, 'no_of_crfs': 10000, 'no_of_third_party_vendors': 0}
country_capacity_drivers = {'mon_region_code': 'JPN', 'country_mmu': 'Oncology GMO Japan', 'trial_country_sites_planned_number': 1, 'trial_country_sites_setup_number': 1}
milestone_dates = {'2500': '2016-01-13','3200': '2016-05-03','3500': '2017-06-09','3700': '2017-07-20','4000': '2018-01-15','4650': '2018-05-01','4950': '2019-01-29'}
country_milestone_dates = {'FPFV': '2014-06-26'}

DATE_FORMAT = "%Y-%m-%d"
#DATE_FORMAT = "%Y-%m-%d hh:mm"
FINAL_DATE_FORMAT = "%Y-%m-%d"
ia_demand_dictionary = {}
derived_values={}
#derived_values = {'D_cty_planned_fpfv': '2016-05-03'}

# These are the actual methods in the programme, with the error logging simplified to just print the error out. DO NOT amend these.

def DATEADD(milestone_name, no_of_days):
    """
    CUSTOM FUNCTION - looks up the milestone date from the milestone_dates dictionary,
    adds the no_of_days to it and returns the new date
    """

    try:
        milestone_full_date = milestone_dates.get(str(milestone_name))
        if milestone_full_date is None:
            return None
        else:
            milestone_stripped_date = datetime.strptime(milestone_full_date,
                                                        DATE_FORMAT).date()
            return milestone_stripped_date + timedelta(days=no_of_days)
    except Exception as err:
        print(err)


def COUNTRYDATEADD(milestone_name, no_of_days):
    """
    CUSTOM FUNCTION - looks up the milestone date from the country_milestone_dates
    dictionary, adds the no_of_days to it and returns the new date
    """
    try:
        milestone_full_date = country_milestone_dates.get(str(milestone_name))
        if milestone_full_date is None:
            return None
        else:
            milestone_stripped_date = datetime.strptime(milestone_full_date,
                                                        DATE_FORMAT).date()
            return milestone_stripped_date + timedelta(days=no_of_days)
    except Exception as err:
        print(err)


def DERIVEDDATEADD(derived_date_name, no_of_days):
    """
    CUSTOM FUNCTION - looks up the derived date from the derived_values
    dictionary, adds the no_of_days to it and returns the new date
    """
    try:
        milestone_full_date = derived_values.get(str(derived_date_name))
        if milestone_full_date is None:
            return None
        else:
            milestone_stripped_date = datetime.strptime(milestone_full_date,
                                                        DATE_FORMAT).date()
            return milestone_stripped_date + timedelta(days=no_of_days)
    except Exception as err:
        print("unable to return a valid date :" + err)


def DATEMAX(date_1, date_2):
    """
    CUSTOM FUNCTION - returns the max from the two dates passed in
    """

    try:
        return max(date_1, date_2)
    except Exception as err:
        print(err)


def CALC_IA_CON(first_milestone_name,
                last_milestone_name,
                no_ia, ia_start_days,
                ia_end_days,
                load,
                range_min,
                range_max):
    """
    CUSTOM FUNCTION - calculates the start date, end date and demand effort
    for IAs specified between range_min and range_min
    """

    try:
        first_milestone_date = datetime.strptime(
            milestone_dates.get(str(first_milestone_name)), DATE_FORMAT).date()

        last_milestone_date = datetime.strptime(
            milestone_dates.get(str(last_milestone_name)), DATE_FORMAT).date()

        # Days of IAs
        diff = (last_milestone_date - first_milestone_date).days / (no_ia + 1)

        for interim_analysis in range(range_min, range_max + 1):
            ia_date = first_milestone_date + timedelta(days=diff * (interim_analysis))
            start_work = ia_date + timedelta(days=ia_start_days)
            end_work = ia_date + timedelta(days=ia_end_days)

            # Start of work should never be before the period start date
            final_start_work = max(start_work, first_milestone_date)
            # End of work should never be later than the period end date
            final_end_work = min(end_work, last_milestone_date)

            random_number = randint(1, 1000000)
            ia_id = '{}{}{}{}{}'.format("IA",
                                        str(interim_analysis),
                                        random_number,
                                        range_min,
                                        no_ia)

            if interim_analysis in range(range_min, range_max + 1):
                global ia_demand_dictionary
                ia_demand_dictionary[ia_id] = {'start_date': final_start_work.strftime(
                    FINAL_DATE_FORMAT),
                    'end_date': final_end_work.strftime(
                        FINAL_DATE_FORMAT),
                    'demand_effort': load}
    except Exception as err:
        print(err)


def if_in(search_term, array_to_search, value_to_assign, default_value):
    """CUSTOM FUNCTION - searches for a value (search_term) in array (array_to_search) and
    returns the value_to_assign if it exists, otherwise returns default_value"""
    try:
        if search_term in array_to_search:
            return value_to_assign
        else:
            return default_value
    except Exception as err:
        print(err)





def get_capacity_driver(capacity_driver_name):
    """
    Looks in the capacity_drivers dictionary and retrieves the
    capacity driver value based on the variable name passed in
    """

    try:
        result = capacity_drivers.get(capacity_driver_name)
        if result is None:
            result = country_capacity_drivers.get(capacity_driver_name)
        return result
    except KeyError as key_err:
        print(key_err)
    except Exception as err:
        print(err)


def get_derived_value(derived_variable_name):
    """
    Looks in the derived_values dictionary and retrieves the
    derived value based on the variable name passed in
    """

    try:
        derived_value = derived_values.get(derived_variable_name)
        if derived_value is None:
            print("derived value is none ", derived_variable_name)
        return derived_value
    except KeyError as key_err:
        print(key_err)
    except Exception as err:
        print(err)

#print(DERIVEDDATEADD('D_cty_planned_fpfv', 400))