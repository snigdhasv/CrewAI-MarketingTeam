#!/usr/bin/env python
import sys
import warnings

import datetime

from .crew import ProjectCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'current_date': datetime.datetime.now().strftime("%Y-%m-%d"),
        'instagram_description': input('Enter the page description here: '),
        'topic_of_the_week': input('Enter the topic of the week here: '),
        'brand_tone': input('Enter brand tone: '),
        'target_demographics': input('Enter target demographics: '),
        'brand_goals': input('Enter brand goals: '),
    }

    try:
        ProjectCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
